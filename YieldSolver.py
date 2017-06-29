"""
igridcoupon should be annual rate as percentage: (eg. 5 percent is as 5)
returning yield is as is: (eg. 5 percent is 0.05)
"""

import time
import traceback
import sys

class FixedIncomeYieldSolver(object):

    def __init__():
        """
        to be organized with a better class structure
        derivative calculation should be seperate function
        instrument configuration should be seperate function
        """
    def dirtyPrice(igridcoupon=4., ifreq=2., iyield=.03323996631, ikgs=82., idgs=182., iremainingcoupons=2., ifacevalue=100.):
        iLOGDIR = os.path.join(os.path.sep,os.getcwd(),"mylogs")
        FNCNAME = sys._getframe().f_code.co_name
        try:  
            dp_a = (1.+iyield/ifreq)
            dp_a = dp_a**(ikgs/idgs)
            dp_a = igridcoupon/dp_a
            dp_b = (1.+iyield/ifreq)
            dp_b = dp_b**(iremainingcoupons-1)
            dp_b = 1./dp_b
            dp_b = 1. - dp_b
            dp_b = dp_b/(iyield/ifreq)
            dp_b = 1. + dp_b
            dp_c = (1.+iyield/ifreq)
            dp_c = dp_c**(iremainingcoupons-1.+ikgs/idgs)
            dp_c = ifacevalue/dp_c
            dp = dp_a*dp_b + dp_c
            return dp
        except Exception as e:
            print "**Error**", e 
            with open(iLOGDIR+time.strftime("%Y%m%d_%H%M%S-")+str(FNCNAME)+"-"+str(e)+".log", "w") as f:
                f.write(str(traceback.format_exc()+"\n\n"+str(locals())))

    ##NEWTON RAPHSON METHOD WITH CRITICAL POINT CONTROLS    
    def calcYieldNewtonRaphson(dp,deriv_eps=0.0001,iyieldguess=.10,igridcoupon=4., ifreq=2., ikgs=82.,idgs=182.,iremainingcoupons=2.,ifacevalue=100.):
        iLOGDIR = os.path.join(os.path.sep,os.getcwd(),"mylogs")
        FNCNAME = sys._getframe().f_code.co_name
        MINYIELD = -1*ifreq+0.0001
        try:
            counter = 0
            f_x = dp - dirtyPrice(igridcoupon=igridcoupon, ifreq=ifreq, iyield=iyieldguess, ikgs=ikgs, idgs=idgs,iremainingcoupons=iremainingcoupons, ifacevalue=ifacevalue)
            while (counter < 50 and abs(f_x) > 0.000001 and iyieldguess != 0):  #CONTROL 1: control when yield is 0
                    f_x = dp - dirtyPrice(igridcoupon=igridcoupon, ifreq=ifreq, iyield=iyieldguess, ikgs=ikgs, idgs=idgs,iremainingcoupons=iremainingcoupons, ifacevalue=ifacevalue)
                    f_xpluseps = dp - dirtyPrice(igridcoupon=igridcoupon, ifreq=ifreq, iyield=iyieldguess+deriv_eps, ikgs=ikgs, idgs=idgs,iremainingcoupons=iremainingcoupons, ifacevalue=ifacevalue)
                    deriv_f = (f_xpluseps - f_x)/deriv_eps
                    ##CONTROL 2: control when derivative is 0
                    if deriv_f == 0:
                        deriv_f = 0.000000001
                        print "derivative of the function was zero, updated to 0.000000001"
                        with open(iLOGDIR+time.strftime("%Y%m%d_%H%M-")+str(FNCNAME)+"-"+"derivzero"+".log", "a") as f:
                            f.write("derivative of the function was zero, updated to 0.000000001"+"\n\n"+str(locals())+"\n\n\n")
                    iyieldguess = iyieldguess - f_x/deriv_f
                    ##CONTROL 3: control when denominator in first part of yield formula is 0
                    if iyieldguess < -1*ifreq:
                        print "yield guess %.f is less then frequency, updated to %.4f" %(iyieldguess,MINYIELD)
                        with open(iLOGDIR+time.strftime("%Y%m%d_%H%M-")+str(FNCNAME)+"-"+"toolowyieldguess"+".log", "a") as f:
                            f.write("yield guess %.f is less then frequency, updated to %.4f" %(iyieldguess,MINYIELD)+"\n\n"+str(locals())+"\n\n\n")
                        iyieldguess = MINYIELD 
                    counter = counter + 1
                    dpguess = dirtyPrice(igridcoupon=igridcoupon, ifreq=ifreq, iyield=iyieldguess, ikgs=ikgs, idgs=idgs,iremainingcoupons=iremainingcoupons, ifacevalue=ifacevalue) ##print edebilmek icin
                    print "guess number %d: %.9f for yield, %.9f for dirtyprice" %(counter,iyieldguess,dpguess)
            return iyieldguess
        except Exception as e:
            print "**Error**", e 
            with open(iLOGDIR+time.strftime("%Y%m%d_%H%M%S-")+str(FNCNAME)+"-"+str(e)+".log", "w") as f:
                f.write(str(traceback.format_exc()+"\n\n"+str(locals())))


    ##ALTERNATIVE METHOD, SLOWER CONVERGENCE, HAS UPPER BOUND         
    def calcYieldBinarySearch(dp,ubound=1000.,igridcoupon=4., ifreq=2., ikgs=82., idgs=182.,iremainingcoupons=2.,ifacevalue=100.):
        import time
        import traceback
        import sys
        iLOGDIR = os.path.join(os.path.sep,os.getcwd(),"mylogs")
        FNCNAME = sys._getframe().f_code.co_name
        try:
            lbound=-1*ifreq+0.0001
            iyield = (lbound+ubound)/ 2.
            dp_guess = dirtyPrice(igridcoupon=igridcoupon, ifreq=ifreq, iyield=iyield, ikgs=ikgs, idgs=idgs,iremainingcoupons=iremainingcoupons, ifacevalue=ifacevalue)
            counter = 0
            while (abs(dp_guess - dp)>0.000001 and counter < 50):
                    counter = counter + 1
                    if dp_guess - dp > 0.000001:
                            lbound = iyield
                            iyield = (lbound+ubound)/ 2.
                            dp_guess = dirtyPrice(igridcoupon=igridcoupon, ifreq=ifreq, iyield=iyield, ikgs=ikgs, idgs=idgs,iremainingcoupons=iremainingcoupons, ifacevalue=ifacevalue)
                            print "guess number %d is: %.9f yield and %.9f dirty price" %(counter,iyield,dp_guess)
                    elif dp_guess - dp < 0.0000001:
                            ubound = iyield
                            iyield = (lbound+ubound)/ 2.
                            dp_guess = dirtyPrice(igridcoupon=igridcoupon, ifreq=ifreq, iyield=iyield, ikgs=ikgs, idgs=idgs,iremainingcoupons=iremainingcoupons, ifacevalue=ifacevalue)
                            print "guess number %d is: %.9f yield and %.9f dirty price" %(counter,iyield,dp_guess)
                    else:
                            return iyield
            return iyield
        except Exception as e:
            print "**Error**", e 
            with open(iLOGDIR+time.strftime("%Y%m%d_%H%M%S-")+str(FNCNAME)+"-"+str(e)+".log", "w") as f:
                f.write(str(traceback.format_exc()+"\n\n"+str(locals())))

def main():

    print "Example report on solver iterations when Dirty Price is 100 of default instrument" 
    fi = FixedIncomeYieldSolver()
    fi.calcYieldNewtonRaphson(dp=100,deriv_eps=0.0001,iyieldguess=.10,igridcoupon=4., ifreq=2., ikgs=82.,idgs=182.,iremainingcoupons=2.,ifacevalue=100.)

if __name__ == "__main__":
    main()
