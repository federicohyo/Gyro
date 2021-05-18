import numpy as np
from time import sleep

# Registers
reg_id        = 0x00
reg_timestamp = 0x04
reg_pkt_len   = 0x08
reg_decay     = 0x0C
reg_wr_en     = 0x10
reg_rst       = 0x14
reg_n_in      = 0x18
reg_n_out     = 0x1C
# First mean in register
reg_mean_in   = 0x20
# First mean out register
reg_mean_out  = 0xC60

# Generic functions

def check_register(ip, register, expected_value):
    value = ip.read(register)
    if (value == expected_value):
        print("Read register succesful, got %d" % value)
    else:
        print("Read register failed, expected %d, got %d" % (expected_value, value))

def set_mean_equal(srbm, n_in, value):
    print("Set {} input means to {}".format(n_in, value))
    for i in range(n_in):
        srbm.write(reg_mean_in+i*0x4, value)

def set_mean(srbm, mean_in):
    print("Set input means")
    for i in range(len(mean_in)):
        srbm.write(reg_mean_in+i*0x4, int(mean_in[i]))

def print_mean(srbm, n_out):
    # Print output mean of all n_out neurons
    print("Neuron output means:")
    for i in range(n_out):
        print("{:<3} ".format(srbm.read(reg_mean_out+i*0x4)), end='')
    print("")

def get_mean(srbm, n_out, filename):
    mean_out = []
    for i in range(n_out):
        mean = srbm.read(reg_mean_out+i*0x4)
        mean_out.append(mean)
        print('%3d ' % mean, end='')
    print('')

    mean_out_array = np.array(mean_out)
    mean_out_array = np.reshape(mean_out_array, [num_meas, -1])
    np.savetxt(filename, mean_out_array, fmt="%3d")

def print_input(x, width, length):
    for i in range(length):
        for j in range(width):
            print('{:<3} '.format(x[i*length+j]), end='')
        print('')

def run_once(srbm, n_out, mean_in, sleep_time):
    srbm.write(reg_rst, 1)
    srbm.write(reg_rst, 0)
    set_mean(srbm, mean_in)
    sleep(sleep_time)
    print_mean(srbm, n_out)

def get_mean_int(srbm, n_out):
    mean_out = np.zeros([n_out])
    for i in range(n_out):
        mean_out[i] = srbm.read(reg_mean_out+i*0x4)
    return mean_out

def run_int(srbm, n_out, mean_in, num_samples=100, sleep_time=0.005):
    srbm.write(reg_rst, 1)
    srbm.write(reg_rst, 0)
    set_mean(srbm, mean_in)
    mean_values_ = np.zeros([n_out, num_samples]) 
    for i in range(num_samples):
        mean_values_[:,i] = get_mean_int(srbm, n_out)
        sleep(sleep_time)
    mean_values_ = np.mean(mean_values_,axis=1)
    return mean_values_

def run_test(srbm, n_out, mean_in, ref, num_samples=100, sleep_time=0.005):
    output = np.zeros([np.shape(mean_in)[0]])
    for this_image in range(np.shape(mean_in)[0]):
        print('Testing image %3d' % this_image)
        mean_values =  run_int(srbm, n_out, mean_in[this_image], num_samples=num_samples, sleep_time=sleep_time)
        result = np.where(np.max(mean_values) == mean_values)[0][0]
        print(' res %d' % result)
        output[this_image] = result

    test_accuracy = np.sum(np.array(ref).astype('int') == output) / len(output)
    print(' TEST ACCURACY %f' % test_accuracy)
    return output, test_accuracy

def make_dset(srbm, n_out, mean_in, ref, num_samples=100, sleep_time=0.005):
    output = []
    for this_image in range(np.shape(mean_in)[0]):
        print('Testing image %3d' % this_image)
        mean_values = run_int(srbm, n_out, mean_in[this_image], num_samples=num_samples, sleep_time=sleep_time)
        output.append(mean_values)

    return np.array(output)
