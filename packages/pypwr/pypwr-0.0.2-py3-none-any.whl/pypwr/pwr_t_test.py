# -*- coding: utf-8 -*-
"""
Created in Jul 2022

@author: Ernest Namdar
"""
import sys
import numpy as np
from pypwr.cohen_ES import cohen_ES
from scipy.stats import t
from scipy.stats import nct
from scipy.stats import norm
from scipy.optimize import brentq

def pwr_t_test(alternative, test_type, n=None, d=None, sig_level=0.05, power=None):
    assert alternative in ["two.sided","less","greater"]
    assert test_type in ["two.sample", "one.sample", "paired"]
    alternative_options = ["less", "two.sided", "greater"]
    test_type_options = ["one.sample", "two.sample", "paired"]
    if sum(x is None for x in [n, d, power, sig_level]) != 1:
        raise Exception("exactly one of n, d, power, and sig.level must be NULL")
        sys.exit(0)
    if (d is not None) and isinstance(d,str):
        d = cohen_ES(test="t",size=d)["effect_size"]
    if (sig_level is not None):
        #print(type(sig_level))
        if type(sig_level)!=int and type(sig_level)!=float:
            raise Exception("sig_level should be numerical")
            sys.exit(0)
        elif sig_level<0 or sig_level>1:
            raise Exception("sig_level should be in [0, 1]")
            sys.exit(0)
    if (power is not None):
        if type(power)!=int and type(power)!=float:
            raise Exception("power should be numerical")
            sys.exit(0)
        elif power<0 or power>1:
            raise Exception("power should be in [0, 1]")
            sys.exit(0)
    tsample = test_type_options.index(test_type)
    if tsample == 2:
        tsample=0
    tsample +=1
    ttside = alternative_options.index(alternative)
    if ttside == 1:
        tside = 1
    else:
        tside=0
    tside += 1 #to avoid div by 0
    if tside==2 and (d is not None):
        d = np.abs(d)
    if ttside == 0:
        p_body = "nct.cdf(t.ppf(sig_level/tside, df=(n-1)*tsample), df=(n-1)*tsample, nc=np.sqrt(n/tsample)*d)"
        # nu = (n-1)*tsample
        # qu = t.ppf(sig_level/tside, df=nu)
        # nct.cdf(qu, df=nu, nc=np.sqrt(n/tsample)*d)
    elif ttside == 1:
        p_body = "nct.sf(t.isf(sig_level/tside, df=(n-1)*tsample), df=(n-1)*tsample, nc=np.sqrt(n/tsample)*d)+nct.cdf(-(t.isf(sig_level/tside, df=(n-1)*tsample)), df=(n-1)*tsample, nc=np.sqrt(n/tsample)*d)"
        # nu = (n-1)*tsample
        # qu = t.isf(sig_level/tside, df=nu)
        # nct.sf(qu, df=nu, nc=np.sqrt(n/tsample)*d)+nct.cdf(-qu, df=nu, nc=np.sqrt(n/tsample)*d)
    elif ttside == 2:
        p_body = "nct.sf(t.isf(sig_level/tside, df=(n-1)*tsample), df=(n-1)*tsample, nc=np.sqrt(n/tsample)*d)"
        # nu = (n-1)*tsample
        # qu = t.isf(sig_level/tside, df=nu)
        # nct.sf(qu, df=nu, nc=np.sqrt(n/tsample)*d)
    if power is None:
        power = eval(p_body)
    elif d is None:
        loc = {}
        target_function_def = "def target_function(d):return "+p_body+"-power"
        exec(target_function_def, loc)
        #print(loc)
        loc.update(globals())
        loc.update(locals())
        if tside-1==0:
            d = brentq(loc["target_function"], -10, 5)
        elif tside-1==1:
            d = brentq(loc["target_function"], 1e-07, 10)
        elif tside-1==2:
            d = brentq(loc["target_function"], -5, 10)
    elif n is None:
        loc = {}
        target_function_def = "def target_function(n):return "+p_body+"-power"
        exec(target_function_def, loc)
        #print(loc)
        loc.update(globals())
        loc.update(locals())
        n = brentq(loc["target_function"], 2+1e-10, 1e+09)
    elif sig_level is None:
        loc = {}
        target_function_def = "def target_function(sig_level):return "+p_body+"-power"
        exec(target_function_def, loc)
        #print(loc)
        loc.update(globals())
        loc.update(locals())
        sig_level = brentq(loc["target_function"], 1e-10, 1-1e-10)
    else:
        raise Exception("internal error")
        sys.exit(0)
    if test_type=="paired":
        NOTE = "n is number of *pairs*"
        METHOD = "Paired t test power calculation"
    elif test_type=="two.sample":
        NOTE = "n is number in *each* group"
        METHOD = "Two-sample t test power calculation"
    else:
        NOTE = ""
        METHOD = "One-sample t test power calculation"
    # print("h=",h, "n=", n, "power=",power, "sig_level=", sig_level)
    return {"n":n, "d":d, "sig_level":sig_level, "power":power,
            "alternative":alternative, "method":METHOD, "note":NOTE}
