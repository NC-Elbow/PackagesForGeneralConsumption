#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:26:50 2020

@author: clark
"""

import numpy as np
import pandas as pd
from math import nan
from numpy import matmul as mm

class blockmm:
    def __init__(self, A, B, partition_shape = 10):
        # A and B are large matrices to be multiplied whose dimensions line up
        # ie A is nxm, B is mxp so C = AB is nxp. 
        self.A = A
        self.B = B
        self.partition_shape = partition_shape
        
    def partition(self):
            a1,a2 = self.A.shape
            b1,b2 = self.B.shape
            if (a2 != b1):
                print("We cannot multiply these matrices as presented.")
                self.C = nan
            else:
                if a1 > self.partition_shape:
                    self.rows_a = [k*self.partition_shape for k in range(1 + a1//self.partition_shape)]
                    if a1%self.partition_shape > 0:
                        self.rows_a. append(a1)
                    # We're breaking this into chunks of one thousand rows
                else: 
                    self.rows_a = [0]
                    self.rows_a.append(a1)
                if a2 > self.partition_shape:
                    self.cols_a = [k*self.partition_shape for k in range(1 + a2//self.partition_shape)]
                    if a2%self.partition_shape > 0:
                        self.cols_a.append(a2)
                    self.rows_b = self.cols_a
                    # We're breaking this into chunks of one thousand rows/columns
                else: 
                    self.cols_a = [0]
                    self.cols_a.append(a2)
                    self.rows_b = self.cols_a                
                if b2 > self.partition_shape:
                    self.cols_b = [k*self.partition_shape for k in range(1 + b2//self.partition_shape)]
                    if b2%self.partition_shape > 0:
                        self.cols_b.append(b2)
                    # We're breaking this into chunks of one thousand columns
                else: 
                    self.cols_b = [0]    
                    self.cols_b.append(b2)
    
    def make_A_blocks(self):
        A_block = {}
        for i in range(len(self.rows_a) - 1):
            for j in range(len(self.cols_a) - 1):
                name = "{0}{1}".format(i+1,j+1)
                val = self.A[self.rows_a[i]:self.rows_a[i+1], self.cols_a[j]:self.cols_a[j+1]]
                A_block[name] = val
                #print("A " + name)
                #print(val.shape)
        self.A_block = A_block        
    
    def make_B_blocks(self):
        B_block = {}
        for i in range(len(self.rows_b) - 1):
            for j in range(len(self.cols_b) - 1):
                name = "{0}{1}".format(i+1,j+1)
                val = self.B[self.rows_b[i]:self.rows_b[i+1], self.cols_b[j]:self.cols_b[j+1]]
                B_block[name] = val
                #print("B " + name)
                #print(val.shape)
        self.B_block = B_block
    
    def make_C_blocks(self):
        C_block = {}
        for i in range(len(self.rows_a) - 1):
            for j in range(len(self.cols_b) - 1):
               name = "{0}{1}".format(i+1,j+1)
               val = 0
               for k in range(len(self.cols_a) - 1):
                   temp = "mm(self.A_block['{0}{1}'], self.B_block['{1}{2}'])".format(i+1,k+1,j+1)    
                   val = val + eval(temp) 
               C_block[name] = val
               #print("C " + name)
               #print(val.shape)
        self.C_block = C_block
        
    def store_to_csv(self, path_to_save):
        if path_to_save== '':
            path_to_save = '/home/clark/Computing/python_projects/csvs/'
        for x,y in self.C_block.item():
            y.to_csv(path_to_save +"x.csv")
            
            
        
        
    def main(self):
        self.partition()
        self.make_A_blocks()
        self.make_B_blocks()
        self.make_C_blocks()
        