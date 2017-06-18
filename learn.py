import numpy as np
from scipy import signal
from pylab import *
import os

import config

class Arrange:
    past_c = "xx"
    bwn_a = False
    ax = None
    plots_numbers = []
    count = 0
    pattern = {"train": 100, "test":30, "raw": 1000}

    count_calibration = 0
    FRAMES_CALIBRATION = 5
    array_calibration = []
    array = [0 for n in range(132)]
    calibration_numbers = np.array(array).astype(np.int64)

    def __init__(self):
        self.MODE = config.mode
        self.is_new = config.is_new
        print("class made")

    def make_dir_train_or_test(self):
        if self.MODE == "test" or self.MODE == "train":
            fn = os.path.join(os.getcwd(), self.MODE)
            if not os.path.exists(fn):
                os.makedirs(fn)
            elif config.is_new == "n":
                nums = []
                list_dirs = os.listdir(os.getcwd())
                for d in list_dirs:
                    if d[0:len(self.MODE)] == self.MODE:
                        exist_str = d[len(self.MODE) + 1:]
                        if exist_str == "":
                            nums.append(0)
                        else:
                            nums.append(int(exist_str))
                if nums == []:
                    maxnum = 0
                else:
                    maxnum = np.max(nums)

                if maxnum < 9:
                    str_num = "0" + str(maxnum + 1)
                else:
                    str_num = str(maxnum + 1)
                os.rename(os.path.join(os.getcwd(), self.MODE), os.path.join(os.getcwd(), self.MODE + str_num))
                os.makedirs(os.path.join(os.getcwd(), self.MODE))
            else:
                pass

    def write_ceps(self, ceps, filename):
        if self.MODE == "test" or self.MODE == "train":
            fn = os.path.join(os.getcwd(), self.MODE, filename)
            if not os.path.exists(fn):
                os.makedirs(fn)
            #base_fn,ext = os.path.splitext(fn)
            count_str = "00"
            if self.count < 10:
                count_str = "0" + str(self.count)
            else:
                count_str = str(self.count)
            data_fn = os.path.join(self.MODE, filename, count_str + ".ceps")
            np.save(data_fn,ceps)
            self.count += 1

    def fetch_numbers(self, unused_addr, *raws):
        face_array = []
        is_calibration = config.is_calibration
        c = config.c
        #print(raws[0], type(raws[0]))
        raw_list = [float(r)*10.0 for r in raws]
        if self.past_c != c:
            self.past_c = c
            self.count = 0
        if is_calibration == True:
            is_calibration = self.start_calibration(is_calibration, np.array(raw_list).astype(np.int64))
        if self.count < self.pattern[self.MODE]:
            input_array = np.array(raw_list).astype(np.int64) - self.calibration_numbers
            if config.c != "1025":
                self.write_ceps(raw_list)
                print("Calibration Mode is ", is_calibration, ":input array = ", input_array, ":MODE = ", self.MODE)
            else:
                print(input_array)
        config.is_calibration = is_calibration

    def start_calibration(self, is_calibration, input_array):
        if self.count_calibration < self.FRAMES_CALIBRATION:
            if is_calibration:
                self.count_calibration += 1
                self.array_calibration.append(input_array)
        else:
            self.calibration_numbers = np.mean(np.array(self.array_calibration), axis=0)
            is_calibration = False
            self.count_calibration = 0
            self.array_calibration = []
            print("Calibration Finished")
        return is_calibration
