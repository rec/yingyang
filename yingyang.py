#!/usr/local/bin/python

import wave

def read_wave(f):
  with wave.open(f, 'rb') as wav:
    print wav.getparams()


def yingyang(f1, f2):
  pass
