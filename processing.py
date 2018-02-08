from scipy import signal as sp
import numpy as np

class Processing:
    def movMean (self, signal, window):
        WinFilt = np.repeat(1.0,window)/window
        meanfilSignal = np.convolve(signal,WinFilt,'valid')
        return meanfilSignal  
    
    def BPButterFilter(self,signal,flow,fhigh,sampleF,order):
        sampleRate = sampleF
        nyq_rate = sampleRate/2.0
        Wn = [flow/nyq_rate,fhigh/nyq_rate]
        n = order
        [b,a] = sp.butter(n,Wn,'bandpass')
        filtered = sp.filtfilt(b,a,signal)
        return filtered

        def getACcomponent(self, measure):
        mean = np.mean(measure)
        measure = (measure-mean)
        return measure
    
    def getDCComponent(self,measure):
        DCcomponent  = np.mean(measure)
        return DCcomponent
        
    def Normalize(self, measure):
        abs = np.max(np.abs(measure))
        measureN = measure/abs
        measureN = np.round(measureN,4)
        return measureN



    def heartRateCalc(self, signal,numSeconds):
        signalHR = np.ediff1d(signal)
        threshold = np.max(signalHR) * 0.5
        for x in np.nditer(signalHR, op_flags=['readwrite']):
            if x < threshold:
                x [...]= 0
        beat =0
        #Direction False = Down True = Up     
        direction = False
        for x in np.nditer(signalHR): 
            if x > threshold:
                direction = True
            if x < threshold:
                if direction == True:
                    direction = False
                    beat +=1
        print beat            
        HeartRate = (60* beat)/numSeconds
        return HeartRate
