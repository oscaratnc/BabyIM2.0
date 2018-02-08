import spo2SensorDriver as Sp2

import time 
from smbus2 import SMBus
import RPi.GPIO as GPIO
import wiringpi 
from processing import Processing as pro
import numpy as np
from scipy import signal as sp
from scipy import fftpack as spfft
from gpiozero import Button


class SensorSpo2:
    GPIO.setmode(GPIO.BCM)
    def __init__(self):
        #Array variables to store samples
        self.Red = np.array([])
        self.IR = np.array([])
        self.RedRaw = np.array([])
        self.IRRaw = np.array([])
        self.Spo2Value = 0
        self.spO2 = np.array([])

    def configSensors(self,samplerateSpo2):
        #Definitions fot Spo2 acquisition
        self.samplerateSpo2 = samplerateSpo2
        self.Spo2 = Sp2.Spo2Sensor(sampleAvg= 4,sampleRate=self.samplerateSpo2)
        AFthreshold= 20
        self.Spo2.enableAfull()
        self.Spo2.setFIFOAF(AFthreshold)
        print "SpO2 config ready"

    def getSpo2read(self,numSeconds):
        print "begin SPO2 measure"
        startTime = wiringpi.millis()
        newSample = False
        interrupt  = Button(7)
        
        while wiringpi.millis()-startTime < numSeconds*1000:
            interrupt.when_activated = self.Spo2.sampleAvailable()
            if self.Spo2.newSample == True:
                self.Spo2.readSample()
                self.Spo2.newSample = False    
                
        

        #get Red and Ir buffers
        self.IR =  self.Spo2.buffer_ir 
        self.Red = self.Spo2.buffer_red

         # #Normalize Red and IR signals
        self.Red = pro.Normalize(self.Red)
        self.IR =  pro.Normalize(self.IR)

         #Butterword 4th order bandpass filter .5-6Hz
        self.IR = pro.BPButterFilter(self.IR, 0.5, 4.0,self.samplerateSpo2,4)
        self.Red = pro.BPButterFilter(self.Red, 0.5, 4.0,self.samplerateSpo2,4)

         #fft filtered dignal
        self.IR_Filtered_FFT = spfft.fft(self.IR)
        self.Red_Filtered_FFT= spfft.fft(self.Red)

          #Mean filter widnow = 4
        # self.IR  = pro.movMean(self.IR,4)
        # self.Red = pro.movMean(self.Red,4)
        self.Red = sp.medfilt(self.Red,3) *- 1
        self.IR = sp.medfilt(self.IR,3) * -1
        
        self.Spo2Value = self.calcSpO2(self.Red, self.IR)
        np.append(self.spo2,self.Spo2Value)
        print "Spo2: ", self.Spo2Value, "%"
    
    def calcSpO2(self,signalRed, signalIR):
       
        DCRed = pro.getDCComponent(signalRed)
        acRed = pro.getACcomponent(signalRed)
        DCIR = pro. getDCComponent(signalIR)
        acIR = pro.getACcomponent(signalIR)
        
        RR =round(np.mean((acRed/DCRed)/(acIR/DCIR)),4)
        print "RR: ", RR
        spO2Value =  96.545 + 0.616 * RR
        Spo2Value =int(np.round(spO2Value,0))
        return Spo2Value