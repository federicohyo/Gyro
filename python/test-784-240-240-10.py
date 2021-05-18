import argparse
import time
import math
import srbm as ext
import numpy as np

from pynq import Xlnk
from pynq import Overlay

from time import sleep

#
# This tests an SRBM that has 784 input means and 20 output means
#

# Registers
reg_id        = 0x00
reg_timestamp = 0x04
reg_pkt_len   = 0x08
reg_decay     = 0x0C
reg_wr_en     = 0x10
reg_rst       = 0x14
reg_n_in      = 0x18
reg_n_out     = 0x1C
# 784 mean in
reg_mean_in   = 0x20
# voltages
reg_voltage   = 0xC60
# mean out
reg_mean_out  = 0xCB0

# Parse argument
parser = argparse.ArgumentParser()
parser.add_argument("bit", help="FPGA bit file")
args = parser.parse_args()

# Set variables
overlay = Overlay(args.bit)
srbm = overlay.srbm
xlnk = Xlnk()

# Check register values
ext.check_register(srbm, reg_id, 0x5352424d)
ext.check_register(srbm, reg_n_in, 784)
ext.check_register(srbm, reg_n_out, 20)

print("Timestamp " + str(srbm.read(reg_timestamp)))

# Read y from file into ref
f = open('data/y_small', 'r')
# Read file and remove \t\n characters
ref = [i.replace('\t\n', '') for i in f.readlines()]
f.close()
# Read x from file
f = open('data/x_small', 'r')
x = f.readlines()
f.close()

#mean_list0 = [int(i) for i in x[0].split('\t')[:-1]] # -1 to remove last empty entry

x_list = np.zeros([np.shape(x)[0], 784]) 
for j in range(np.shape(x)[0]):
    # Select one line from x and create list using split
    x_ = np.array([int(i) for i in x[j].split("\t")])
    # Scaling factor to limit the total spike rate at the input
    factor = np.sum(x_) / np.max(x_) / 1 
    # Scale each value of the line with the factor and append whole line to x_list
    x_list[j,:] = np.array([int(i/factor) for i in x_])

mean_in = np.array(x_list)
#ext.run_once(srbm, reg_rst, reg_mean_in, reg_mean_out, 20, mean_in, 0.01)
#ext.run_test(srbm, reg_rst, reg_mean_in, reg_mean_out, 20, mean_in, 20, 0.005)

print("")
print("")
print("Write: srbm.write(reg_mean_in, 0xFF)")
print("Read: srbm.read(reg_timestamp)")
print("ext.run_once(srbm, reg_rst, reg_mean_in, reg_mean_out, 64, mean_in, 0.01)")
print("ext.run_test(srbm, reg_rst, reg_mean_in, reg_mean_out, 64, mean_in, 10, 0.005)")
print("")

xlnk.xlnk_reset()

from sklearn import svm
dset = ext.make_dset(srbm, reg_rst, reg_mean_in, reg_mean_out, 20, mean_in, ref, 3, 0.01)

ref_int = [int(i) for i in ref]

#make an svm
clf = svm.SVC()
clf.fit(dset[0:800], ref_int[0:800])
preds_ = clf.predict(dset[800:1000])
accuracy = np.sum(preds_ == np.array(ref_int[800:1000]))/len(preds_)

print("TEST ACCURACY %f" % accuracy)


#if __name__ == "__main__":
    #main()
