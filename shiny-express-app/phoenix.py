# import pyaudio
# import audioop

from statistics import mean



def info_smoother(points):
    return mean(points)