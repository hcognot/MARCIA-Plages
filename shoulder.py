import numpy as np
import Smooth
# from scipy import optimize
from scipy.optimize import fsolve

""" fonction retournant une liste avec les (maxi 4) maxima locaux et les minima locaux entre les paires de maximum"""
""" function providing a numpy array containing the (max 4) relevant local maxima and
the local minima found between them 
as well as the minima between 1st item and 1st maxima and the minima between last maxima and last item
"""
def extrema (max_locaux, y_data):
     array_extrema = np.array([])
     """ include the first item"""
     array_extrema= np.append(array_extrema, 0)
     
     """ include the 1st mini and the 1st maxi if the maxi is not at the 2 1st indices """
     if  (max_locaux[0] != 0 and max_locaux[0] != 1)  : 
          borne_inf=0
          borne_sup= max_locaux[0]
          min_idx = borne_inf + int(np.argmin(y_data[int(borne_inf):int(borne_sup)+1]) )
          if (min_idx != borne_inf and min_idx!= borne_sup): 
               array_extrema= np.append(array_extrema, min_idx)
          
          array_extrema= np.append(array_extrema, max_locaux[0])
               
     """ include the next extrema : mini if pertinent, maxi always """
     for i in range (1, len(max_locaux)):
          #print('first max local in main zone is ',i)
          borne_inf=int(max_locaux[i-1])
          print('borne inf  is ',borne_inf)
          borne_sup= int(max_locaux[i])
          print('borne sup  is ',borne_sup)
          
          min_idx = borne_inf
          min_y_value= y_data[min_idx]
                    
          for j in range (borne_inf, borne_sup):
               if ( y_data[j] < min_y_value):
                    min_idx = j
                    min_y_value= y_data[j]
          print( 'minimum en', min_idx )
          
          if (min_idx != int(max_locaux[i-1]) and min_idx!= int(max_locaux[i])): 
               array_extrema= np.append(array_extrema, min_idx)
          array_extrema= np.append(array_extrema, max_locaux[i])

     """ include the last items"""
     """ if the last maximum is not one of the 2 last data, search for a minimum"""
     if  (max_locaux[len(max_locaux)-1] != len(y_data)-1  and max_locaux[len(max_locaux)-1] != len(y_data)-2)  : 
          
          borne_inf=int(max_locaux[len(max_locaux)-1])
          borne_sup= len(y_data)-1
          
          min_idx = borne_inf
          min_y_value= y_data[min_idx]
          for j in range (borne_inf, borne_sup+1):
                         if ( y_data[j] < min_y_value):
                              min_idx = j
                              min_y_value= y_data[j]
          print( 'minimum final en', min_idx )
          array_extrema= np.append(array_extrema, min_idx)
          
     print(" les minima placés entre les maxima locaux:")
     print (array_extrema)
     return array_extrema

""" function listing the shoulders """
def shoulder_list (x_data, y_data, pics, mean ):
     """ work on small_windowed data """
     array_shoulder= np.array([])
     y, nb= Smooth.smooth_tight(x_data, y_data)
     yl, nbl= Smooth.smooth_large(x_data, y_data)
     extrem = extrema (pics, y_data)

     """ search between extrema """
     print('array shoulder initial: ')
     print(array_shoulder)
     for e in range (0 , len(extrem)-1):
          print('début d\'intervalle: ', e)
          """ not too small interval """
          if (extrem[e+1]- extrem[e]> 2*(nb+1)):
               """ no too close from the extrema """
               for i in range(int(extrem[e])+ nb+1, int(extrem[e+1] - nb-1)):
                    print('ieme élément: ', i)
               
                    if (i>nb and i<len(y)-nb-1 and y[i] > mean):
                         print('on rentre dans la boucle pour ', i)
                         # épaulement après un mu
                         # during a descent............
                         """ acceleration or steady change """
                         decreasing_curve= (y[i]-y[i-1])<0 
                         massive_change =  (abs(y[i]-y[i-1])*1.4 < abs(y[i+1]-y[i])) and (abs(y[i+1]-y[i])*1.4 < abs(y[i+2]-y[i+1]))
                         if (massive_change): print('massive change')
                         if (i < (nbl+1 ) or i > (len(y)- nbl-1-1) ):
                               steady_change = False
                         else: 
                              
                              steady_change= abs((yl[i]-yl[i-1]) )> 0.9* abs((yl[i-1]-yl[i-2])) and abs( (yl[i]-yl[i-1]) ) < 1.1* abs((yl[i-2]-yl[i-1])) and ( abs(yl[i]-yl[i-1])*1.35 < abs(yl[i+1]-yl[i]) or abs(yl[i]-yl[i-1])*1.35 < abs(yl[i+2]-yl[i+1]))
                         if (steady_change): print('steady change decrease')
                         
                         if ( massive_change or steady_change) and decreasing_curve :
                         
                              print('ajout d\'une valeur')
                              array_shoulder = np.append(array_shoulder, i)
                              print( 'array_shoulder en descente temp pour i = ',i)
                              print(array_shoulder)
                              #  only one shoulder in this intervall
                              if len(array_shoulder) !=0:
                                   break
                    #épaulement avant un mu
                    # during a rise
                         ascending_curve= (y[i]-y[i-1])>0 
                         massive_change =  abs(y[i+1]-y[i])*1.4 < abs(y[i]-y[i-1]) and (abs(y[i- 1]-y[i])*1.4 < abs(y[i-2]-y[i-1]))
                         if (massive_change): print('massive change')
                         if (i < (nbl*2+1 ) or i > (len(y)- nbl*2-1-1) ):
                              steady_change = False
                         else:
                              steady_change= abs((yl[i]-yl[i-1]) )> 0.9* abs((yl[i-1]-yl[i-2])) and abs( (yl[i]-yl[i-1]) ) < 1.1* abs((yl[i-2]-yl[i-1])) and (abs(yl[i]-yl[i-1])*1.35 > abs(yl[i+1]-yl[i]) or abs(yl[i]-yl[i-1])*1.35 > abs(yl[i+2]-yl[i+1]))
                         if (steady_change): print('steady change ascend')
                         if ( massive_change or steady_change) and ascending_curve :
                              array_shoulder = np.append(array_shoulder, i)
                              print( 'array_shoulder en montée temp pour i = ',i)
                              print(array_shoulder)   
                              #  only one shoulder in this intervall
                              if len(array_shoulder) !=0:
                                        break   
               print('sortie de l\' intervalle',  e)               
     print('indice(s) d\'épaulement:')
     print(array_shoulder)
          
     return array_shoulder