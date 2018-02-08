import Spo2Sensor as Sp2
import time
import wfdb
from smbus2 import SMBus
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import wiringpi
import numpy as np
import processing as pro 
from scipy import signal as sp
from scipy import fftpack as spfft
from gpiozero import Button
GPIO.setmode(GPIO.BCM)

class ECGSensor(pro.Processing):
  

   def __init__ (self):
       self.ECG = np.array([])
       self.HR  = np.array([])

   def configSensor(self, SampleRate):
        CLK = 11
        MISO = 9 
        MOSI = 10 
        CS = 8
        mcp = Adafruit_MCP3008(CLK,CS,MISO,MOSI)
        print "ECG Ready"

   def getECG(self, numSeconds, sampleRate):
        print "Beginning ECG Measure"
        samplePeriod = (1/sampleRate)*1000
        starTime = wiringpi.millis()

        while wiringpi.millis() - starTime < numSeconds*1000:
            ecgSample= round ((mcp.read_adc(1)*3.3)/1024,3)
            np.append (self.ECG, ecgSample) 
            wiringpi.delay(int (samplePeriod))
               
    def preProcECG(self, ECGSignal):
        

    def detectQRS(self, preProcECGSignal):
        pass

    def CalcECGHR (self, ECGQRS):
        pass


        

