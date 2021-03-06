import math
import numpy as np
from IPython import embed
from contextlib import contextmanager
import time

import matplotlib
import matplotlib.pyplot as plt
plt.ion()

def Plot(y_list, title,num_fig=1,path=None):
    plt.figure(num_fig, clear=True, figsize=(5.5, 4))
    plt.title(title)

    i = 0
    for y in y_list:
        plt.plot(y[0], label=y[1])
        i+= 1

    plt.legend(loc=2)
    plt.show()
    plt.pause(0.001)
    if path is not None:
        plt.savefig(path, format="png")


class TimeChecker():
    def __init__(self):
        self._timeList = {}

    @contextmanager
    def check(self, key):
        if key not in self._timeList:
            self._timeList[key] = 0
        _st = time.time()
        yield
        self._timeList[key] += time.time() - _st


    def printAll(self):
        for k, v in self._timeList.items():
            print("{} : {}s".format(k, v))

    def clear(self):
        self._timeList = {}

def v_sub(a, b):
    result = []
    for i in range(len(a)):
        result.append(a[i] - b[i])
    return result

def v_len(a):
    s = 0;
    for i in range(len(a)):
        s += a[i]*a[i]
    return math.sqrt(s)

def v_cross(v1, v2):
    x = v1[1]*v2[2] - v1[2]*v2[1];
    y = v2[0]*v1[2] - v2[2]*v1[0];
    c = [0]*3
    c[2] = v1[0]*v2[1] - v1[1]*v2[0];
    c[0] = x;
    c[1] = y;
    return c

def v_dot(v0, v1):
    return (v0[0]*v1[0] + v0[1]*v1[1] + v0[2]*v1[2]);


def v_angle(v0, v1):
    vDot = v_dot(v0, v1) / (v_len(v0)*v_len(v1));
    if( vDot < -1.0): vDot = -1.0;
    if( vDot >  1.0): vDot =  1.0;
    return((math.acos( vDot )));

class Normalize(object):
    def __init__(self, mean, std):
#         self.mean = mean
#         self.std = std
        nzMean = []
        nzStd = []
        self.zero_indices = []
        for i in range(len(mean)):
            if (std[i] <= 0.00011):
                # print("{} : {}, {}".format(i, mean[i], std[i]))
                self.zero_indices.append(i)
                continue
            nzMean.append(mean[i])
            nzStd.append(std[i])

        self.mean = nzMean
        self.std = nzStd

        self.total_mean = mean
        self.total_std = std
        
    def normalize(self, data):
        return (data - self.mean)/self.std
    
    def de_normalize(self, data):
        return data*self.std + self.mean
    
    def de_normalize_idx(self, data, index):
        return data*self.std[index] + self.mean[index]
    
    def normalize_l(self, data):
        result = []
        for i in range(len(data)):
            if i >= len(self.mean):
                result.append(data[i])
            else:
                result.append((data[i] - self.mean[i])/self.std[i])
        return result
    
    def de_normalize_l(self, data):
        result = []
        for i in range(len(data)):
            if i >= len(self.mean):
                result.append(data[i])
            else:
                result.append(data[i]*self.std[i] + self.mean[i])
        return result
    
    def size(self):
        return len(self.mean)

    def get_data_with_zeros(self, data):
        new_data = np.asarray(data)
        for i in self.zero_indices:
            new_data = np.insert(new_data, i, self.total_mean[i])
        return new_data

    def normalize_and_remove_zero(self,data):
        result = []
        zero_pass_cnt= 0
        for i in range(len(data)):
            if i in self.zero_indices:
                zero_pass_cnt= zero_pass_cnt+1
                continue
            else:
                result.append((data[i] - self.mean[i-zero_pass_cnt])/self.std[i-zero_pass_cnt])
        return result

    def denormalize_and_fill_zero(self,data):
        result = []
        zero_pass_cnt= 0
        for i in range(len(data)+len(self.zero_indices)):
            if i in self.zero_indices:
                zero_pass_cnt= zero_pass_cnt+1
                result.append(self.total_mean[i])
                continue
            else:
                result.append(data[i-zero_pass_cnt]* self.std[i-zero_pass_cnt] + self.mean[i-zero_pass_cnt])
        return result

    def get_zero_not_removed_index(self, index):
        removed_index_counter= 0
        zero_index_counter= 0
        for i in range(len(self.mean)+ len(self.zero_indices)):
            if removed_index_counter== index:
                return (removed_index_counter+ zero_index_counter)
            if i in self.zero_indices:
                zero_index_counter = zero_index_counter+1
            else:
                removed_index_counter= removed_index_counter+1

    def get_zero_removed_index(self, index):
        if index in self.zero_indices:
            return -1
        removed_index_counter= 0
        zero_index_counter= 0
        for i in range(len(self.mean)+ len(self.zero_indices)):
            if (removed_index_counter+ zero_index_counter)== index:
                # print("get_zero_removed_index of ", index, " = ", removed_index_counter)
                return removed_index_counter
            if i in self.zero_indices:
                zero_index_counter = zero_index_counter+1
            else:
                removed_index_counter= removed_index_counter+1

    def get_mean(self, index):
        return self.total_mean[index]