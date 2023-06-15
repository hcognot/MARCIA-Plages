import numpy as np
import gaussian
from scipy import optimize
from scipy.optimize import fsolve
import mainPeaks
import plotting
import shoulder
"""  ***************************************************  
                    kernel of the project 
     ***************************************************  """

""" plages proposées """
""" proposed ranges """

def plage (x_data, y_data):
    majorPeaks, mean = mainPeaks.majorPeaks(x_data, y_data)
    relevantIndices = majorPeaks

    if (len(relevantIndices) <4): 
        """ add the shoulders if they exist and limit the total number """
        shoulders = shoulder.shoulder_list (x_data, y_data, relevantIndices, mean )
        if (len(shoulders) !=0):
             print("Des épaulements sont ajoutés")
             peaksAndShoulders = joinAndSort( relevantIndices, shoulders)
             """ épaulement très près des extrémités: ce sont les extrémités qui sont anormales, on les supprime """  
             if (peaksAndShoulders[1]- peaksAndShoulders[0] <= 5): 
                  peaksAndShoulders = peaksAndShoulders[1:]
             if (peaksAndShoulders[len(peaksAndShoulders)-1] - peaksAndShoulders[len(peaksAndShoulders)-2] <= 5 ):
                  peaksAndShoulders = peaksAndShoulders[:-1]
             __ , peaksAndShoulders= mainPeaks.basisLow (peaksAndShoulders, y_data)
             relevantIndices = peaksAndShoulders               

    """ paramaters of the gaussians"""
    mu= fmu(x_data, relevantIndices)
    amp= famp(y_data, relevantIndices)
    sigma = fsigma(x_data, y_data, amp, mu, mean)

    """ proposed plages """ 
    lesplages = plage_adjusted(amp, mu, sigma, x_data, y_data)
    print ('Les plages proposées: ')
    print (lesplages)       

    """ plot of the adjusted function""" 
    base =  np.ones(len(x_data))  * mean
    y =  np.ones(len(x_data))
    
    for i in range (0, len(mu)-1):
         y = y+ gaussian.gaussian(x_data,amp[i], mu[i], sigma[i])
    for j in range (0, len(y)-1):
         if (y[j] ==0):
              y[j] = 1

    y_calc = np.maximum(base, np.log10(y))     

    plotting.trace_ajuste(x_data, y_data, y_calc, 'fonction ajustée')
  
    return lesplages

""" fonction retournant la liste ordonnée des valeurs centrales mu"""
""" function providing the sorted list of gaussian central values mu"""
def fmu(x_data, max_locaux):
     
     mu = np.zeros(len(max_locaux))
     for i in range(0,len(max_locaux)):
         mu[i]= x_data[int(max_locaux[i]) ]     

     # print('les mu:')   
     # print(mu)  
    
     return mu

""" fonction retournant la liste ordonnée des amplitudes amp"""
""" function providing the sorted list of gaussian amplitudes amp"""
def famp(y_data, max_locaux):
     
    amp = np.zeros(len(max_locaux))
        
    for i in range(0,len(max_locaux)):
         amp[i]= y_data[int(max_locaux[i]) ]
#     print('les amplitudes:')   
#     print(amp)  
    
    return amp

""" function providing the sorted list of gaussian standard deviations """
def fsigma (x_data, y_data, amp, mu, mean ):
    """ allongement des tableaux amp et mu si necessaire
    par des valeurs les plus neutres possibles
    soit: amp = 0 et mu = 50"""
    """ fill the mu and amp arrays up to 4 data if necessary, with neutral values"""
    nbReel= len(mu)

    while len(mu) < 4:
          mu = np.append(mu, 50.)
    while len(amp) < 4:
          amp = np.append(amp, 0.)      

    sigma= np.ones(4) * 25

    """ adjusted function: sum of gaussians """
    def test_func(x, s0, s1, s2, s3):
        
        array_plateau = np.ones(len(x))*10**mean
        obj= (10**amp[0])*  np.exp(-((x - mu[0])**2) / (2 * (s0**2)))
        obj= obj + (10**amp[1])*  np.exp(-((x - mu[1])**2) / (2 * (s1**2))) 
        obj= obj + (10**amp[2])*  np.exp(-((x - mu[2])**2) / (2 * (s2**2))) 
        obj= obj + (10**amp[3])*  np.exp(-((x - mu[3])**2) / (2 * (s3**2)))                   
        return  np.maximum( array_plateau, np.log10(obj) )
    
    # le tableau p0 fournit des valeurs de départ pour les paramètres s0 à s3
    """ initialization of the parameters given to the test_func"""
    p0=[5,5,5,5]
    """ possibility of adjust the sd by change of mark"""
#     p0 = ajustedStandardDeviations (x_data, y_data, mu, amp)
    """ for future use: if non standard P0, sheck ranges!"""
    sigma, params_covariance = optimize.curve_fit(test_func, x_data, y_data,  p0)
    
#     print('les sigma, approche des écarts-type:')
#     print('Seules les '+ str(nbReel) + ' premières valeurs sont à considérer')
#     print(sigma)

    """ problème de sigma négatifs : remplacement forcé par valeur positive petite"""
    for i in range (0, len(sigma)):
         if (sigma[i] < 0):
              sigma[i] = 1

#     print('nouveaux sigmas: ', sigma) 
    return sigma

""" adjust the plages=ranges to some specificities:
     1 - minimum between 2 peaks
     2 - avoid overlapping """
def plage_adjusted(amp, mu, sigma, x_data, y_data):
     
     """ use only the standard deviations linked to an actual central value"""
     sigma = np.resize(sigma, (len(mu),))
     lesplages=  np.column_stack(( np.clip(mu - 4*sigma, 0, 100),np.clip(mu + 4*sigma, 0, 100)))
     
     """ if a minimum exists between 2 pics, deplace the limit to this point """
     for i in range (1, len(mu)):
          liminf= int(mu[i-1]/2)        # indice
          limsup = int(mu[i]/2)         # indice
          # Slice the array between mu1 and mu2 (inclusive)
          y_slice = y_data[liminf:limsup+1]             
          # Find the index of the minimum value in the sliced array
          min_index = np.argmin(y_slice)
          # print(' indice au minimum  ', min_index)
          # Calculate the overall index of the minimum value within y_data
          overall_min_index = min_index + liminf
          # print(' indice au over all minimum  ', overall_min_index)
          # Get the minimum value using the index
          minivalue = y_data[overall_min_index]
          """ absolute minimum no part of a plateau """
          if (min_index-2 >0 and min_index+2 < len(y_slice)-1):
               plateau = abs(minivalue - y_slice[min_index-2])<0.2 and abs(minivalue - y_slice[min_index+2])<0.2
          else:
               plateau = True
          if (minivalue*1.4 < max( amp[i-1], amp[i]) and (plateau== False or mu[i]>=96) ):
               lesplages[i-1][1]=x_data[overall_min_index]
               # print(' borne sup de l\'intervalle d\'avant:  ', lesplages[i-1][1])
               lesplages[i][0]= x_data[overall_min_index]
     
     """ limit between plages so that they do not overlap"""
     # si superposition des plages, recherche du point de séparation
     for i in range (1, len(mu)):
          if (lesplages[i-1][1] > lesplages[i][0]):
               # print('plages qui se superposent')
               solution = separation(amp, mu, sigma, i)
               lesplages[i-1][1]=solution
               lesplages[i][0]=solution   

     # print('dernier mu:', mu[len(mu)-1] )
     # print('derniers x_data: ', x_data[len(x_data)-2])
     """ final maximum can be a narrow """
     if ( len(mu)>1 and  mu[len(mu)-1] >= x_data[len(x_data)-2] ):
          # print('on modifie les plages')
          lesplages[-1][0]= ajustLast(mu, y_data, lesplages)
    
     lesplages= np.round(lesplages, decimals=0)

     return lesplages

""" function that is zeroed when the 2 gaussians are equal"""
def f(x, amp, mu, sigma, i):
     return gaussian.diff_gaussian (x, amp[i-1], mu[i-1], sigma[i-1], amp[i], mu[i], sigma[i]) 

""" when 2 plages overlap, limit their extend when the 2 gaussians are equal"""
def separation (amp, mu, sigma, i):
     x_min= mu[i-1]
     x_max=mu[i]
     for x in range(int(x_min), int(x_max), 1):
          if f(x, amp, mu, sigma,i)<0:
               return x
     return x_max

""" function that join and order indices of 2 numpy arrays"""
def joinAndSort( arraya, arrayb):
     temp = np.append(arraya, arrayb)
     temp= np.sort(temp)

     # print('nouvelle liste: ', temp)
     return temp

""" function adjusting the last range"""
def ajustLast(mu, y_data, plage):
     
     ind_final= int(mu[len(mu)-1]/2) 
     ind_begin= int(mu[len(mu)-2]/2) 
     indOfMin= ind_final
     valueOfMin= y_data[indOfMin]

     for i in range (ind_final, ind_begin, -1):
          if ( y_data[i]< valueOfMin):
               valueOfMin= y_data[i]
               indOfMin= i
     # print ('indice du minimum', indOfMin)
     """" do not overlap mith the previous range """
     if (indOfMin*2 >= 96):
          return max(plage[-2][1], 95)
     else:
          return max( plage[-2][1], max ( plage[-1][0], indOfMin*2))
     
""" modify the initial standard deviation array when possible """
""" HGC 08/06/23 : not in use"""
def ajustedStandardDeviations (x_data, y_data, mu, amp):
     s= [5,5,5,5]
     for i in range (0, len(mu)-1):
          s[i] = ajustedSD(x_data, y_data, mu, amp, i)
     # print(" tableau des ecart-types: ", s)
     return s

""" in the range of values of y_data, search of a half heighth"""
""" if possible, use then this halfheigth to personnalize the SD of the i-th peak"""
def ajustedSD (x_data, y_data, mu, amp, i):
     if (i==0):
          liml = 0
     else:
          liml = mu[i-1]
          # print(' liml: ' , liml)
     
     if (i == len(mu)-1):
          limr = x_data[len(x_data)-1]
     else:
          limr = mu [i+1]
          # print(' limr: ' , limr)

     """ half height left side of mu"""
     halfl = -10         # absurd value
     j= int(mu[i]/2)
          
     while ( x_data[j] >= liml and y_data[j]> amp[i]/2 and j>0 )   :
          # print('j avant :', j)
          j=j-1
     if (x_data[j] > liml ):
          halfl= x_data[j]
          # print('halfl: ', halfl)

     """ half height right side of mu"""
     halfr = -10         # absurd value
     k= int(mu[i]/2)
    
     while ( x_data[k] <= limr and y_data[k]> amp[i]/2 and k< len(x_data)-1)   :
          # print('k après: ', k)
          k=k+1
     if (x_data[k] < limr-1):
          halfr= x_data[k]
          # print('halfr: ', halfr)

     
     if ( halfl == -10 and halfr == -10):
          return 5
     if (halfl == -10):
          return (halfr- mu[i] )*0.85
     if (halfr == -10):
          return abs (halfl- mu[i] ) *0.85

     return min(abs (halfl- mu[i] ),(halfr- mu[i] ) )*0.85
