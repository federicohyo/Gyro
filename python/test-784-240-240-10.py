import argparse
import time
import math
import gyro as sr
import numpy as np

from pynq import Xlnk
from pynq import Overlay

from time import sleep

#
# This tests an SRBM that has 784 input means and 10 output means
#

# Parse argument
parser = argparse.ArgumentParser()
parser.add_argument("bit", help="FPGA bit file")
args = parser.parse_args()

# Set variables
overlay = Overlay(args.bit)
srbm = overlay.srbm
xlnk = Xlnk()

# Check register values
sr.check_register(srbm, sr.reg_id, 0x5352424d)
sr.check_register(srbm, sr.reg_n_in, 784)
sr.check_register(srbm, sr.reg_n_out, 10)

print("Timestamp " + str(srbm.read(sr.reg_timestamp)))

# Read y from file into ref
f = open('data/y', 'r')
# Read file and remove \t\n characters
ref = [i.replace('\t\n', '') for i in f.readlines()]
f.close()
# Read x from file
f = open('data/x', 'r')
x = f.readlines()
f.close()

#factor = np.sum(x_) / np.max(x_) / 10 
# Scaling factor to limit the total spike rate at the input
factor = 50

x_list = []
for j in range(np.shape(x)[0]):
    # Select one line from x and create list using split
    x_ = np.array([int(i) for i in x[j].split("\t")[:-1]])
    # Scale each value of the line with the factor and append whole line to x_list
    x_list.append(np.array([int(i/factor) for i in x_]))
    #x_list.append(np.array([int(i) for i in x_]))

mean_in = np.array(x_list)
#sr.run_once(srbm, 10, mean_in[0], 0.01)
sr.run_test(srbm, 10, mean_in, ref, 10, 0.005)

print("")
print("")
print("Write: srbm.write(sr.reg_mean_in0, 0xFF)")
print("Read: srbm.read(sr.reg_timestamp)")
print("sr.run_once(srbm, 10, mean_in[0], 0.01)")
print("sr.run_test(srbm, 10, mean_in, ref, 10, 0.005)")
print("")

xlnk.xlnk_reset()

#if __name__ == "__main__":
    #main()
