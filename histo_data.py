import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
import seaborn as sns

import plotting

def create_data_y_data(finite_data):
        """ create the data of the histogram"""
        
        """Parameters
        ----------
        finite_data : data extracted from the image

        """      

        """ generating of the data of histogram for later use """
        bin_values, bin_edges, _ = plt.hist(finite_data, bins=50)
        y_dat = np.array(bin_values)
        x_data = np.array(bin_edges[:-1])
        
        countzero= 0
        NeedofLinealisation = False
        """ in case of a too small amount of data: replace the missing data by the mean of their neighours"""
        for i in range (0, len(y_dat)):
            if (y_dat[i]== 0):
                countzero=+1

        if (100 * countzero/len(y_dat) >0.3 ):
             NeedofLinealisation = True

        """ replace the 0 by 1 in y_data before using the logarithm """
        for i in range (0, len(y_dat)):
            if (y_dat[i]== 0):
                y_dat[i] = 1  

        """ Thereafter, the y_data are logarithm"""
        y_data = np.log10(y_dat) 

        if (NeedofLinealisation):   
           y_data= linearising(y_data)
               
        """ interpolation for out of the way data """
        y_data = outOfTheWayCorrection(y_data)

        """ Limit the presence of sound into the data"""
        y_data= soundsmoothing(x_data, y_data)
     
        return x_data, y_data

""" in case of partial data """
def linearising (y):
        """ first and last data : use the nearest not zeroed data"""
        j=0
        while (y[j]==0):
             j=+1
        for k in range (0, j):
             y[k] = y[j]
        j=len(y)-1
        while (y[j]==0):
             j=-1
        for k in range (len(y), j):
             y[k] = y[j]
        
        """ central part of the data"""
        for i in range (1, len(y)-1):
             if (y[i]== 0):
                beforenonzero_indices = np.nonzero(y[:i])[0]
                beforefirst_nonzero_index = beforenonzero_indices[-1]
                
                afternonzero_indices = np.nonzero(y[i+1:])[0]  
                afterfirst_nonzero_index = afternonzero_indices[0] + i + 1
                """ linearisation"""         
                y[i] = (i-beforefirst_nonzero_index)/(afterfirst_nonzero_index- beforefirst_nonzero_index)*(y[afterfirst_nonzero_index] - y[beforefirst_nonzero_index] ) + y[beforefirst_nonzero_index]        

        return y    

""" if case of high rate sound """    
def soundsmoothing(x, y):
     valmax= np.max(y)
     valmin= np.min(y)
     delta = valmax-valmin
     count=0
     """ testing: need of get out of the sound """
     for i in range (1, len(y)-1):
          if ( (abs(y[i]- y[i-1]) + abs(y[i+1]- y[i]) > 0.1*delta) and ((y[i]- y[i-1])*(y[i+1]- y[i]) >0 )  ):
               count= count+1
     
     if (count < len(y) *0.05):
          """ no need """
          return y
     else :
          """ suppress minor high excentricities"""
          for i in range (0, len(y)-1):
               if ( (y[i] - (y[i-1]+ y[i+1])/2)  > 0.06*delta ): 
                    y[i]= (y[i]+ y[i+1])/2
          """ change of y data : mean of 2 successive data"""
          for i in range (0, len(y)-1):
               y[i]= (y[i]+ y[i+1])/2
                               
          return y

""" Linear interpolation of data far off their direct neighbours"""
""" do not apply to 3 1st and last data ( dramatic changes accepted at these locations )"""
def outOfTheWayCorrection(y):
     """ massive out of the way data """
     for i in range (3, len(y)-4): 
          # if ( (y[i] > (y[i-1]+y[i+1])/2 +0.2 ) or (y[i] < (y[i-1]+y[i+1])/2 -0.2 ) ):
          """ choice: only the values under the trend"""
          if (y[i] < (y[i-1]+y[i+1])/2 -0.2 ) :    
               y[i] = (y[i-1]+y[i+1])/2
     return y

""" Linear interpolation of data far off their next to direct neighbours"""
""" do not apply to 3 1st and last data ( dramatic changes accepted at these locations )"""
""" HGC 08/06/23 : not in use"""
def RemoteOutOfTheWayCorrection(y):
     for i in range (4, len(y)-5): 
          if ( (y[i] > (y[i-2]+y[i+2])/2 +0.3 ) or (y[i] < (y[i-2]+y[i+2])/2 -0.3 ) ):
               y[i] = (y[i-2]+y[i+2])/2
     return y