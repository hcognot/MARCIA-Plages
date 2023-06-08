import numpy as np
import Smooth
import gaussian
from scipy import optimize
from scipy.optimize import fsolve


""" initial treatment of the y data : major peaks """
""" provide 4 or less major peaks and the mean of the discarded peaks """

def majorPeaks(x_data, y_data):
     """ all peaks obtained from large smoothing """
     array_peaks = peak(x_data, y_data)
     """ mean from discarted peaks"""
     mean, array_peaks = meanLow (array_peaks, y_data)
     """ remaining major peaks """
     majorPeaks = getPlateauOut (array_peaks, y_data, mean)
     
     return majorPeaks, mean

""" detection of all peaks
on the large_window smoothed curve """
def peak(x_data, y_data):
     # initialisation du tableau de taille inconnue
     array_Peaks= np.array([])
     # smoothed data
     y_smooth_large, window_size= Smooth.smooth_large(x_data, y_data)

     """ start of the data: major peak OR tight and relative peak """
     if ((y_smooth_large[0] > y_smooth_large[window_size]) or  (y_data[0]+ y_data[1]> y_data[2]+ y_data[3] )):   
          print('1 max en zéro')
          array_Peaks = np.append(array_Peaks, 0)
     
     """ central part of the data : significative enough peaks """
     # maxima except at the start and the end
     # smoothed data: the window_size'de first and last data are to be avoided    
     for i in range(window_size-1, len(y_smooth_large)-(window_size+1)):
           
          if ((y_smooth_large[i] > y_smooth_large[i-1]) and (y_smooth_large[i] > y_smooth_large[i+1])):
               print("un max large possible en ", i )
               """ plate sommit """
               largesommit= y_smooth_large[i] > y_smooth_large[i-2] and  y_smooth_large[i] > y_smooth_large[i+ 2]
               verylargesommit = largesommit and  y_smooth_large[i] > y_smooth_large[i-3] and  y_smooth_large[i] > y_smooth_large[i+ 3]
               if (y_smooth_large[i] > centralPeak(window_size, y_smooth_large, i)+0.05) or ( y_smooth_large[i]== np.max(y_smooth_large) or largesommit) :
                    array_Peaks = np.append(array_Peaks, i)
     
     """ end of the data: (major peak) OR (tight and relative peak) OR (final value above its smoothed data and its n-1 neigbour value) """
     if ((y_smooth_large[len(y_smooth_large)-1] > y_smooth_large[len(y_smooth_large)-window_size-1]) or  (y_data[len(y_data)-1- 0]+ y_data[len(y_data)-1-1]> y_data[len(y_data)-1-2]+ y_data[len(y_data)-1-3] ) or (y_data[len(y_data)-1- 0] >y_smooth_large[len(y_smooth_large)-1] and y_data[len(y_data)-1- 0] >y_data[len(y_data)-1-2])):
          print('1 max en 100')
          array_Peaks = np.append(array_Peaks,len(y_smooth_large)-1 ) 

     """ if the array is void , fill it with the maximum of the whole y_smooth_large """ 
     if (len( array_Peaks)== 0)    :
          print("pas de peaks repéré")
          maxindice=0
          for i in range (1, len(y_smooth_large)-1) :
               print (i)
               if (y_smooth_large[i] > maxindice):
                    maxindice= i
          array_Peaks = np.append(array_Peaks, maxindice )

     print("les pics larges bruts de bruts:")
     print(array_Peaks)
     return array_Peaks

""" detection of peaks into the central part: avoid too small peaks
by checking them against a local mean value"""
def centralPeak(window_size, y_smooth_large, i):
     
     return np.mean(y_smooth_large[i-(window_size-2):i+(window_size-2)+ 1])

""" minimum value of an array and its indice """
def min (array, y_data):

     mini=1000      # absurd value
     k=1000         # absurd value
     for i in range (0, len(array)):
          if (y_data[int(array[i])] < mini):
               mini=y_data[int(array[i])]
               k=i
     return mini, k         

""" limitation of the size of an array ( 4 peaks ) if needed + 
obtention of the mean value of the y_data of the excluded points """
def meanLow (array_pics, y_data):
     # valeur d'attente
     mean=0

     if len(array_pics)<=4:
          """ recherche du minimum des y_data correspondants, et on lui ôte par défaut 0.2 """
          """ retrieve the minimum value of the relevant data , diminished of 0.2 """
          
          mini,k = min(array_pics, y_data)
          mean = mini - 0.2
     
     if len(array_pics)>4:
          """ keep the 4 highest values of array_pics and set aside the other values """         

          """ void array filled with the 4 first indices of the peakvalues """
          arr_short = np.array(array_pics[:4])
          """ minimum y_data value and its indice"""
          mini, k= min(arr_short, y_data)

          for i in range(4, len(array_pics)):
               if (y_data[int(array_pics[i])] > mini):
                    """ remplacement du minimum conservé par une valeur supérieure """
                    """ for each element exceding the 4th indice un array_pics: if it is bigger than the known minimum"""
                    arr_short[k] = array_pics[i]
                    mini, k= min(arr_short, y_data)
          """ array of the 4 highest major peaks """
          arr_short= np.sort(arr_short)
          
          """ recherche de la moyenne des valeurs de y_data , en excluant les 4 + fortes """
          """ mean of the non used major peaks """
          # find the values in xdata that are not in ydata
          diff_data = np.setdiff1d(array_pics, arr_short)
          
          sum = 0
          for i in range(0, len(diff_data)):
               sum = sum + y_data[int(diff_data[i])]
          mean= sum/len(diff_data)

          array_pics= arr_short

     print('fin de meanLow')
     return mean, array_pics

""" fonction éliminant des pics si leur valeur est marginalement supérieure au plateau: 
pics à l'intérieur du plateau """    
""" cleaning of the major peaks: discard them if their value is only marginally higher than the mean """ 
def getPlateauOut (array, y_data, mean):
     
     array_temp = np.array([])

     for i in range (0, len(array)):
         if ( y_data[int(array[i])] > mean+ 0.1 ) :
             array_temp= np.append(array_temp, array[i])
     print(' les indices conservés:')
     print(array_temp)
     print('fin de getPlateauOut')

     return array_temp