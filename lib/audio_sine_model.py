import sys, os, time
import numpy as np
import stft as STFT
import math
import sineModel as SM
import IPython
import utilFunctions as UF
from IPython.core.debugger import set_trace

class AudioSineModel:
  def __init__(self, file_path):
    self.file_path= file_path
    self.frequencies = None
    self.magnitudes = None
    self.phases = None
    self.sample_rate, self.signal = UF.wavread(file_path)

  def sine_model_analysis(self, window_size=2047, fft_size=4096, hop_size=150, threshold_db=-80, min_sine_dur=0.15, max_sines=15):
    window = np.blackman(window_size)
    self.fft_size = fft_size
    self.window_size = window_size
    self.hop_size = hop_size
    self.threshold_db = threshold_db
    self.min_sine_dur = min_sine_dur
    self.max_sines = max_sines
    self.stft_magnitudes, self.stft_phases = STFT.stftAnal(self.signal, window, fft_size, hop_size)
    self.frequencies, self.magnitudes, self.phases = SM.sineModelAnal(self.signal, self.sample_rate, window, fft_size, hop_size, threshold_db, max_sines, min_sine_dur)
    self.compute_lines()

  def compute_lines(self):
    fvar = 150
    start_val = None
    last_val = None
    lines = []
    x0 = None
    for sine_idx in range(0, self.frequencies[0].size):
        for idx, val in enumerate(self.frequencies[:, sine_idx]):
            if val > 0 and start_val==None:
                start_val = val
                x0 = idx
            elif val == 0 and start_val!=None:
                pos0 = round((math.floor((self.hop_size * x0)/10)*10)/self.sample_rate, 2)
                pos1 = round(math.floor((self.hop_size * idx)/10)*10/self.sample_rate, 2)

                val0 = math.floor(start_val/10)*10
                val1 = math.floor(last_val/10)*10
                lines.append([pos0, pos1, val0, val1, (val1-val0)/(pos1-pos0)])
                start_val = None
            last_val = val
    self.lines = sorted(lines, key=lambda a_entry: a_entry[0]*10000 + a_entry[1])

