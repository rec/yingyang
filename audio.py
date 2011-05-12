#!/usr/local/bin/python

import aifc
import struct
import wave

FORMAT_NAMES = '?bh?i???l'

def getFormat(sampwidth):
  fmt = FORMAT_NAMES[sampwidth]
  if fmt is '?':
    raise ValueError('Unknown sampwidth %d' % sampwidth)
  return '<' + fmt

def sampleToNum(sample, sampwidth=0):
  """Convert a sample to an unsigned integer.

  >>> '%x' % sampleToNum('\\1\\1\\1\\1')
  '1010101'
  """
  return struct.unpack(getFormat(sampwidth or len(sample)), sample)[0]


def numToSample(num, sampwidth):
  """Convert an unsigned integer to a sample.

  >>> numToSample(0, 2)
  '\\x00\\x00'

  >>> numToSample(10452, 2)
  '\\xd4('

  >>> numToSample(3224, 2)
  '\\x98\\x0c'

  >>> numToSample(13676 / 2, 2)
  '\\xb6\\x1a'
"""
  return struct.pack(getFormat(sampwidth), num)


def combineFrames(nchannels, sampwidth, *frames):
  """Combine separate frames and scale.

  >>> combineFrames(1, 2, '(\\xd4', '\\x0c\\x98')
  '\\x1a\\xb6'
  """
  accum = nchannels * [0]

  for frame in frames:
    for ch in range(nchannels):
      offset = ch * sampwidth
      accum[ch] += sampleToNum(frame[offset : offset + sampwidth])
  return ''.join(numToSample(a / len(frames), sampwidth) for a in accum)


def openAudio(f, perms='rb'):
  if f.endswith('.wav'):
    return wave.open(f, perms)
  elif f.endswith('.aif') or f.endswith('.aiff'):
    return aifc.open(f, perms)
  else:
    raise ValueError("Can't open file " + f)


if __name__ == "__main__":
  import doctest
  doctest.testmod()
