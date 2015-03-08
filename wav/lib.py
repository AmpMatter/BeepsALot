from __future__ import division
import scipy.constants as const
import scipy
from scipy.io import wavfile
from IPython.core.display import HTML
import numpy as np
import matplotlib.pyplot as plt

#def wavPlayer(filepath):
#src =
"""
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Simple Test</title>
    </head>
        
    <body>
    <audio controls="controls" style="width:600px" >
    <source src="files/%s" type="audio/wav" />
    Your browser does not support the audio element.
    </audio>
    </body>
"""
#%(filepath)
#display(HTML(src))

rate = 44100 #44.1 khz
duration = 5 # in sec
element = 'lithium+2'

normedsin = lambda f,t : 2**13*np.sin(2*np.pi*f*t) # right values for wav file
time = np.linspace(0,duration, num=rate*duration)

f0 = const.Rydberg*const.c #highest frequency of hydrogen
Z = 3 # number of protons
helium_array = numpy.array([438.793, 443.755, 447.148, 471.314, 492.193, 501.567, 504.774, 587.562, 667.815])
mercury_array = numpy.array([435.835, 546.074, 576.959, 579.065])
neon_array = numpy.array([540.1, 585.2, 588.2, 603.0, 607.4, 616.4, 621.7, 626.6, 633.4, 638.3, 640.2, 650.6, 659.9, 692.9, 703.2])
fshift = 440*Z**2

ryd = lambda n,m: fshift*(1/(n**2)-1/(m**2))
lyman = lambda x: ryd(1,x)
balmer = lambda x: ryd(2,x)
paschen = lambda x: ryd(3,x)
brackett = lambda x: ryd(4,x)
pfdun = lambda x: ryd(5,x)
humphreys = lambda x: ryd(6,x)

#ser = lambda t: sum([normedsin(lyman(i),t)+normedsin(balmer(i+1),t) for i in range(2,8)])
ser = lambda t: sum([normedsin(lyman(i),t)+normedsin(balmer(i+1),t)+normedsin(paschen(i+2),t)+normedsin(brackett(i+3),t)+normedsin(pfdun(i+4),t)+normedsin(humphreys(i+5),t) for i in range(2,8)])
#ser = lambda t: sum([normedsin(helium_array[i]*440/helium_array[0],t) for i in range(0, len(helium_array))])
#ser = lambda t: sum([normedsin(mercury_array[i]*440/mercury_array[0],t) for i in range(0, len(mercury_array))])
#ser = lambda t: sum([normedsin(neon_array[i]*440/neon_array[0],t) for i in range(0, len(neon_array))])
serv = scipy.vectorize(ser)

ss = serv(time)
ss = 2**15*ss/ss.max()

wavfile.write('{0}.wav'.format(element), rate, ss.astype(np.int16))
wavPlayer('{0}.wav'.format(element))
