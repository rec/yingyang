#!/usr/local/bin/python

import aifc
import wave

def sampleToNum(sample):
  """Convert a sample to an unsigned integer.

  >>> sampleToNum('')
  0
  >>> '%x' % sampleToNum('\1\1\1\1')
  '1010101'
  """
  return reduce(lambda x, y: x * 256 + ord(y), sample, 0)


def numToSample(num, sampwidth):
  """Convert an unsigned integer to a sample.

  >>> numToSample(0, 2)
  '\\x00\\x00'

  >>> numToSample(10452, 2)
  '(\\xd4'

  >>> numToSample(3224, 2)
  '\\x0c\\x98'

  >>> numToSample(13676, 2)
  '5l'
"""
  parts = []
  for j in range(sampwidth):
    parts.insert(0, chr(num % 256))
    num /= 256;
  return ''.join(parts)


def combineFrames(nchannels, sampwidth, *frames):
  """Combine separate frames and scale.

  >>> combineFrames(1, 2, '(\\xd4', '\\x0c\\x98')
  '5l'
  """
  accum = nchannels * [0]

  for frame in frames:
    for ch in range(nchannels):
      offset = ch * sampwidth
      accum[ch] += sampleToNum(frame[offset : offset + sampwidth])
  return ''.join(numToSample(a / nchannels, sampwidth) for a in accum)


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
