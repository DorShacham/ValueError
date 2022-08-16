# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 10:48:39 2022

@author: dorsh
"""

import numpy as np
from copy import deepcopy as copy
import math

class Valerr:

    def __init__(self, value, err=0):
        self.val = value
        self.err = err
        self.is_array = False
        if type(value) == Valerr:
            if err != 0:
                raise TypeError
            else:
                self.val = copy(value.val)
                self.err = copy(value.err)

        if type(value) == np.ndarray:
            self.is_array = True
            if (type(err) == float) or (type(err) == int):
               self.err = np.ones(len(value)) * err
               return
            if type(err) != np.ndarray:
                raise TypeError
            if len(err) != len(value):
                raise error
           

    def _dist(*arg):
        sum = 0
        for n in arg:
            sum += n**2
        return sum**0.5

    def value(*parm):
        return ([x.val for x in  list(*parm)])

    def rel_err(self):            
        return self.err/self.val



    def __add__(a, b):
        b = Valerr(b)
        err = Valerr._dist(a.err,b.err)
        return Valerr(a.val+b.val,err)

    def __neg__(a):
        return Valerr(-a.val,a.err)

    def __sub__(a,b):
        return a + (-b)

    def __mul__(a,b):
        b = Valerr(b)
        val = a.val * b.val
        err = val * Valerr._dist(a.rel_err(),b.rel_err())
        return Valerr(val,err)
        
    def __truediv__(a,b):
        b = Valerr(b)
        val = a.val / b.val
        err = val * Valerr._dist(a.rel_err(),b.rel_err())
        return Valerr(val,err)

    def __pow__(a,b):
        if (type(b) != int) and (type(b) != float):
            raise TypeError
        
        val = a.val ** b
        err = val * b * a.rel_err()
        return Valerr(val,err)

    
    def _general_funcion_singel(f,*f_arg):
        arg = []
        values = Valerr.value(f_arg)
        for i in range(len(f_arg)): #calculte drivetive
            if f_arg[i].val ==0: # relitive size delta
                h =  1e-4 * f_arg[i].err
            else:
                h = 1e-4 * f_arg[i].val
            f_arg_h = list(values)
            f_arg_h[i] += h 
            arg.append((f(*f_arg_h)-f(*values))/h * f_arg[i].err)
        err =  Valerr._dist(*arg)
        val = f(*values)
        return Valerr(val,err)

    
    def _general_function_array(f,*f_arg):
        l_val = []
        l_err = []
        for i in range(len(f_arg[0].val)):
            args = [Valerr(a.val[i],a.err[i]) for a in list(f_arg)]
            tmp = Valerr._general_funcion_singel(f,*args)
            l_val.append(tmp.val)
            l_err.append(tmp.err)
        return Valerr(l_val,l_err)
    

    def general_funcion(f,*f_arg):
        print(type(f_arg[0]))
        if f_arg[0].is_array:
            return Valerr._general_function_array(f,*f_arg)
        else: 
            return Valerr._general_funcion_singel(f,*f_arg)

    def __str__(self):
        return str(self.val) + "+-" + str(self.err)


Va = np.array([0.2317, 0.2317, 0.2317, 0.2317, 0.2317, 0.2317, 0.2317, 0.2317, 0.2317, 0.1494, 0.1495, 0.1495, 0.1494, 0.1493, 0.1488, 0.1486, 0.1486])*1e4
Va_err = 0.001 * 1e4
Va = Valerr(Va,Va_err)

I = -np.array([0, 0.057, 0.085, 0.116, 0.143, 0.166, 0.200, -0.157, -0.313, 0, 0.065, 0.112, 0.162, 0.244, -0.140, -0.251, -0.302])
I_err = 0.001
I = Valerr(I,I_err)

A = np.array([0, 0.4, 0.6, 0.8, 1 ,1.2, 1.4, -1, -2, 0, 0.6, 1, 1.4, 2, -1, -2, -2.4] )* 1e-2
A_err = 0.2 * np.ones(len(A)) * 1e-2
A = Valerr(A,A_err)

print("I",I)
print("Va",Va)

f = lambda x,y : x/y**0.5
xData = Valerr.general_funcion(f,I,Va);


print("Xdata.value:",xData.val)
print("\n\nXdata.error:",xData.err)
