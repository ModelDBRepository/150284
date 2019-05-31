# Author Michele Mattioni
# Fri Oct 23 15:41:58 BST 2009

import pylab
import numpy as np
from numpy import sin, exp
import matplotlib.pyplot as plt
from helpers.loader import Loader


    

class FitHandler(object):
    """Fit the data with a polynomial"""
    
    def fit(self, data, terms):
       polycoeffs = np.polyfit(data.x, data.y, terms)
       poly = np.poly1d(polycoeffs)
       return poly
    
    def plot_poly(self, pfit):
        
        plt.plot(data.x, pfit(data.x), label="poly %i" %pfit.order)
    
    def fit_and_plot(self, data, order):
        p = self.fit(data, order)
        self.plot_poly(p)
        return p
    
    def plot_data(self, data):
       
       plt.plot(data.x, data.y, 'k.', label="data")
       plt.xlabel("Distance from the soma [um]")
       plt.ylabel("Surface Area [um]/Dendritic Lenght [um^2]")
       
    def integrate_till_value(self, x0, value, poly, increment, 
                             scale_branch):
        """Integrate the polynomial from x0 to the value required
        
        :Params:
            x0: starting point for the integration
            value: objective value to reach
            poly: polynomial to use to calculate
            
        :return:
            x1: ending point of the integration
        """
        delta = 0
        x1 = x0
        while value >= delta:
            x1 += increment
            delta = poly(x1)/scale_branch - poly(x0)/scale_branch
            
        return (x1, delta)
    
    def calc_spines_pos(self, cursor_list, x1_list):
        """Calculate the spines position, returning the mid point 
        of the interval from the two list."""
        
        mid_points = []
        for i, el in enumerate(cursor_list):
            mid_point = cursor_list[i] + (x1_list[i] - cursor_list[i])/2
            mid_points.append(mid_point)
        return mid_points


if __name__ == "__main__":
    from scipy.optimize import leastsq
    data = pylab.csv2rec('spines_distribution_Wilson_1992.csv')
    pfh = FitHandler()
    pfh.plot_data(data)
    
    order = 17
    pfit = pfh.fit_and_plot(data, order)
    plt.title("Fitting the data")
    plt.legend()
    plt.savefig("Fitted_data.png")
    
    
    # Integrating
    pInteg = pfit.integ()
    
    plt.figure()
    pfh.plot_poly(pInteg)
    plt.title("Integral area")
    # We get the area per number of branch (4):
    scale_branch = 4
    area_per_branch = pInteg(data.x)/scale_branch
    plt.plot(data.x, area_per_branch, label='area branch')
    plt.legend(loc=0)
    plt.savefig('integral_area.png')
    
    
    # Calculating the spine dimension
    
    """
    Procedure to get this right:
    
    - Compute the total surface from Wolf of all the spines
        # 1525 spines total, 381 per branch
    - Rescale the whole surface Wolf spines surface to the Wilson one
    - Compute the spine equivalent surface Wilson2Wolf 
    - Integrate until the surface in the Wilson world match one spine surface
    - take the (x_end - x_start)/2 position
    - iterate 
    
    """
    
    spine_Wolf = 6.35 # um^2
    total_number_spines = 1525
    spines_per_branch = 381
    
    
    total_Wolf = spines_per_branch * spine_Wolf
    
    total_Wilson = pInteg(220)/scale_branch #Value of the integral at the last bit
    
    # spine_Wolf : spine_Wilson = total_Wolf : total_Wilson
    spine_Wilson = (spine_Wolf * total_Wilson)/ total_Wolf
    increment =0.001

    cursor = 0 
    cursor_list = []
    x1_list = []
    delta_list = []
    
    print "Calculating the spines' position. It will take a bit."
     
    while cursor <= data.x[-1]:
            x1, delta = pfh.integrate_till_value(cursor, spine_Wilson, pInteg, 
                             increment, scale_branch)
            cursor_list.append(cursor)
            x1_list.append(x1)
            delta_list.append(delta)
            cursor = x1 # Resetting the cursor to the x1
            
    spines_pos = pfh.calc_spines_pos(cursor_list, x1_list)
    plt.figure()
    plt.hist(spines_pos, bins=30)
    plt.title("spines distribution for branch")
    #plt.savefig('spines_distribution.png')
    
    #filename = 'spines_pos.pickle'
    #l = Loader()
    #l.save(spines_pos, '.', filename)
        
    plt.show()