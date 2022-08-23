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
        self.iter_index = 0
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

    def __setitem__(obj,index,value):
        if (type(value) == int) or (type(value) == float):
            value = Valerr(value)
        if (not obj.is_array) or (type(value) != Valerr):
            raise TypeError
        obj.val[index] = value.val
        obj.err[index] = value.err
        return value

    def __getitem__(obj,index):
        if (not obj.is_array):
            raise TypeError
        return Valerr(obj.val[index],obj.err[index])



    
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
        return Valerr(np.array(l_val),np.array(l_err))
    

    def general_funcion(f,*f_arg):
        if f_arg[0].is_array:
            return Valerr._general_function_array(f,*f_arg)
        else: 
            return Valerr._general_funcion_singel(f,*f_arg)

    def __str__(self):
        return str(self.val) + "+-" + str(self.err)


a = Valerr(np.array([1,2,3]),np.array([0.1,0.2,0.3]))
print(a[2])
for x in a:
    print(x)
