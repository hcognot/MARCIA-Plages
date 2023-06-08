import numpy as np
import matplotlib.pyplot as plt


""" Fonction de lissage large"""
def smooth_large(x,y):
     window_size= round(len(x)*10/100)
     return smooth(window_size, x, y), window_size

"""Fonction de lissage étroit"""
def smooth_tight (x,y):
     # smallest value
     window_size = 3
     return smooth(window_size, x, y), window_size

""" Fonction de lissage """        
def smooth (window_size, x, y):
    # modification de la valeur de la window_size si valeurs négative ou paire
    if (window_size <= 0):
         window_size= 3
    if (window_size%2 ==0):
         window_size= window_size+1
    window = np.ones(window_size)/window_size

    # Apply the smoothing window with convolution
    y_smooth = np.convolve(y, window, mode='valid')

    # Store the smoothed data in a new array
    smoothed_data = np.zeros_like(y)
    smoothed_data[window_size//2:-window_size//2+1] = y_smooth

    # Fill in the first window_size//2 elements with the first non-zero value
    first_nonzero = np.nonzero(y_smooth)[0][0]
    smoothed_data[:window_size//2] = y_smooth[first_nonzero]

    # Fill in the last window_size//2 elements with the last non-zero value
    last_nonzero = np.nonzero(y_smooth)[0][-1]
    smoothed_data[-window_size//2:] = y_smooth[last_nonzero]

    # Plot the original and smoothed data
    plt.plot(x, y, 'b', alpha=0.5)
    #plt.plot(x[window_size//2:-window_size//2+1], y_smooth, 'r', label='window size: '+str(window_size))
    plt.plot(x, smoothed_data, 'r', label='window size: '+str(window_size))
    plt.legend(loc='best')
    
    return smoothed_data
