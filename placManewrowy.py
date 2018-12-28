"""import matplotlib.pyplot as plt"""
import os

from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
from scipy.io.wavfile import read


def voice(meanfun):
    if meanfun < 0.14:
        return ("K")
    else:
        return ("K")

dobre=0
chosen=''

constlabel = './records/trainall/'

directory = os.fsencode(constlabel)

for file in os.listdir(directory):
    try:
        filename=os.fsdecode(file)
        print(file)
        print(filename)
        (fs, x) = read(constlabel + filename)
        rate, data = wav.read(constlabel + filename)
        #(fs, x) = read('./records/trainall/003_K.wav')
        #'/home/ubuntu/Downloads/4829251_male-voice-hello_by_urbazon_preview.mp3'
        #rate, data = wav.read('./records/trainall/003_K.wav')
        #'/home/ubuntu/Downloads/4829251_male-voice-hello_by_urbazon_preview.mp3'
        #print(x)
        #print(x.size)
        #print(fs)
        fft_out = fft(data)
        #print(fft_out)
        combined = fft(data).ravel()
        #print(combined)
        #print(combined.size)
        #print(sum(combined))
        meanfunfreeq = sum(combined) / combined.size
        #print(meanfunfreeq)
        """a = sum(meanfunfreeq)/2
        print(a)
        """
        print(voice(meanfunfreeq))
        chosen=voice(meanfunfreeq)
        print(filename[-5])
        """
        plt.plot(data, np.abs(fft_out))
        plt.show()"""
    #print(bool(random.getrandbits(1)))


    except Exception as inst:
        print(type(inst))
        print("K")
        chosen="K"
        print(filename[-5])
    if(chosen == filename[-5]):
        dobre+=1

print(dobre,91,dobre/91)