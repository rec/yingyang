#!/usr/local/bin/python

import random
import sys
import wave

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


def combine(params, *frames):
  nchannels = params['nchannels']
  sampwidth = params['sampwidth']
  accum = nchannels * [0]

  for frame in frames:
    for ch in range(nchannels):
      t = 0
      for i in range(samplewidth):
        t = t * 256 + ord(frame[ch * samplewidth + i])

      accum[ch] += t

  parts = []
  for acc in accum:
    subparts = []
    for j in range(samplewidth):
      subparts.insert(0, char(acc % 256))
      acc /= 256;
    parts.extend(subparts)
  return parts.join('')

def yingyang(files):
  waves = [wave.open(f, 'rb') for f in files]

  names = 'nchannels', 'sampwidth', 'framerate'
  params = dict((n, get_param(waves, n)) for n in names)
  n = max(w.getnframes() for w in waves)
  frames = [w.readframes(w.getnframes()) for w in waves]
  cuts = [poisson(n, NUMBER_OF_CUTS) for f in files]
  framesize = params['nchannels'] * params['sampwidth']

  for i, f in enumerate(files):
    out = wave.open('out-' + f, 'wb')
    for name in names:
      getattr(out, 'set' + name)(params[name])

    m = len(files) - i - 1
    reader = FrameReader(framesize, frames[i], cuts[i], length, false)
    mirror = FrameReader(framesize, frames[m], cuts[m], length, true)

    for sample in range(length):
      out.writeframes(combine(params, reader.nextFrame(), mirror.nextFrame()))

    out.close()

yingyang(set(sys.argv[1:]))
