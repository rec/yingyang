#!/usr/local/bin/python

import os.path
import random
import sys

import audio

from FrameReader import FrameReader

NUMBER_OF_CUTS = 4
DEBUG = not True

def get_param(waves, name):
  param = set(getattr(w, 'get' + name)() for w in waves)
  if len(param) is not 1:
    raise ValueError('Had more than one %s: %s' % (name, str(list(param))))
  return param.pop()

def poisson(length, cuts):
  rand = lambda: random.randint(0, length - 1)
  p = set(rand() for i in range(cuts))
  while len(p) < cuts:
    p.add(rand())
  return sorted(p)

def yingyang(files):
  waves = [audio.openAudio(f, 'rb') for f in files]

  names = 'nchannels', 'sampwidth', 'framerate'
  params = dict((n, get_param(waves, n)) for n in names)
  n = max(w.getnframes() for w in waves)
  frames = [w.readframes(w.getnframes()) for w in waves]
  cuts = [poisson(n, NUMBER_OF_CUTS) for f in files]
  framesize = params['nchannels'] * params['sampwidth']

  print cuts
  for i, f in enumerate(files):
    out = audio.openAudio('-new'.join(os.path.splitext(f)), 'wb')
    for name in names:
      getattr(out, 'set' + name)(params[name])

    m = len(files) - i - 1
    reader = FrameReader(framesize, frames[i], cuts[i], n, False)
    mirror = FrameReader(framesize, frames[m], cuts[m], n, True)

    nchannels, sampwidth = params['nchannels'], params['sampwidth']
    for sample in range(n):
      f1, f2 = reader.nextFrame(), mirror.nextFrame()
      frame = audio.combineFrames(nchannels, sampwidth, f1, f2)
      # print [audio.sampleToNum(f) for f in [f1, f2, frame]]
      out.writeframes(frame)
      # if DEBUG:
        # print f1, f2, frame

    out.close()


def write_audio(name, data):
  w = audio.openAudio(name, 'wb')
  w.setnchannels(1)
  w.setsampwidth(2)
  w.setframerate(44100)
  for i in data:
    w.writeframes(audio.numToSample(i, 2))



if True:
  yingyang(set(os.path.abspath(s) for s in sys.argv[1:]))

else:
  write_audio('t1.wav', range(-5000, 5000, 1))
  write_audio('t2.wav', range(-25000, 25000, 5))
  write_audio('s1.wav', 5000 * [-10000, 10000])
