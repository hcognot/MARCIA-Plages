import numpy as np
import Smooth
import gaussian
from scipy import optimize
from scipy.optimize import fsolve
import mainPeaks
import plotting


""" function providing maximum from tight-smoothed data
they are above the mean data, they are 1 half-large-window away from other maxima"""
""" if they come in sequence, selection of the y_data maximum 's indice of the sequence"""
def tightPeak(x_data, y_data, mean, peaks):
     
     array_tightPeaks= np.array([])
     _, window_large= Smooth.smooth_large(x_data, y_data)

     y_smooth_tight, window_size= Smooth.smooth_tight(x_data, y_data)
     """ not occurate at the extrema of the x_data values"""
     for i in range(window_large, len(y_smooth_tight)-(window_large+1)):
          """ above the mean value"""
          if (y_smooth_tight[i] > mean): 
               """ away enough of peaks obtained with large smoothing"""
               ok = True
               for j in range (0, len(peaks)): 
                    distance = abs( i - peaks[j])
               
                    if ( distance < window_large):
                         #print (' distance non conservée: ', distance)
                         ok=False         
               if (ok == True) : 
                    """ local high value"""
                    if ((y_smooth_tight[i] > y_smooth_tight[i-1]) and (y_smooth_tight[i] > y_smooth_tight[i+1])):
                         """ that is sufficiently above its neighborood """

                         if (y_smooth_tight[i] > mainPeaks.centralPeak(window_size, y_smooth_tight, i)+0.01):
                            if (y_smooth_tight[i] > mainPeaks.centralPeak(window_large, y_smooth_tight, i)+0.02):
                                print('indice que l\'on reporte:', i)
                                array_tightPeaks = np.append(array_tightPeaks, i)

     print( ' pics en fenêtre étroite: ')
     print(array_tightPeaks)

     if (len(array_tightPeaks) == 0):
          return array_tightPeaks
     else :
        """ treatment of the data"""
        # Define the fixed difference between consecutive numbers in each group
        diff = window_size

        # Find the indices where the groups start
        group_starts = np.where(np.diff(array_tightPeaks) > diff)[0] + 1
        # np.diff(arr) computes the differences between adjacent elements of arr,
        # and the condition np.diff(arr) > diff checks where the differences are above diff.
        # Adding 1 to the result shifts the indices by one, since we are interested in the indices where the groups start.

        # Split the array into groups
        groups = np.split(array_tightPeaks, group_starts)

        print('tous les pics secondaires:')
        print(groups)

        temp= np.array([])
        
        for i, group in enumerate(groups):
            print(f"Group {i+1}: {group}")
            max = group[0]
            ind = 0
            if (len(group)>1):
                for j in range (1, len(group)-1 ) : 
                        if (y_data[int(group[j])] > max):
                            max= group[j]
                            ind = j
                print ('indice : ', ind)
                print('indice des data:', group[ind] )
            temp = np.append(temp, group[ind])
                    
        print('nouveau array de pics sur tights values:', temp)                     
        
        """ for each group, select the item linked to the highest y_data"""

        return temp

""" mean value y, numpy array, around the indice i, from n indices before to n indices after i """     
def calculate_mean(y, i, n):
    start_index = max(0, i - n)  # Starting index of the slice
    end_index = min(len(y), i + n + 1)  # Ending index of the slice

    subset = y[start_index:end_index]  # Slice the array
    mean_value = np.mean(subset)  # Calculate the mean

    return mean_value
