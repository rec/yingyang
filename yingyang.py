#!/usr/local/bin/python

import os.path
import random
import sys

import audio

from FrameReader import FrameReader

NUMBER_OF_CUTS = 32

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

  for i, f in enumerate(files):
    out = audio.openAudio('-new'.join(os.path.splitext(f)), 'wb')
    for name in names:
      getattr(out, 'set' + name)(params[name])

    m = len(files) - i - 1
    reader = FrameReader(framesize, frames[i], cuts[i], n, False)
    mirror = FrameReader(framesize, frames[m], cuts[m], n, True)

    for sample in range(n):
      out.writeframes(audio.combineFrames(params['nchannels'],
                                          params['sampwidth'],
                                          reader.nextFrame(),
                                          mirror.nextFrame()))

    out.close()

yingyang(set(os.path.abspath(s) for s in sys.argv[1:]))
