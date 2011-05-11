#!/usr/local/bin/python

class FrameReader(object):
  def __init__(self, framesize, frames, cuts, length, rev=False):
    self.frames = frames
    if rev:
      self.cuts = list(reversed([(length - x) for x in cuts]))
    else:
      self.cuts = cuts
    self.cuts += [length]
    self.reversed = rev

    self.framesize = framesize
    self.nframes = len(frames) / self.framesize
    self.pad = (length - self.nframes) / 2
    self.empty = self.framesize * chr(0)

    self.playing = (not rev) or (0 == len(cuts) % 2)
    self.cut_index = 0
    self.index = 0

  def nextFrame(self):
    self.index += 1
    if self.index >= self.cuts[self.cut_index]:
      self.playing = not self.playing
      self.cut_index += 1

    index = self.index - self.pad
    if not self.playing or index < 0 or index >= self.nframes:
      return self.empty

    if self.reversed:
      index = self.nframes - index - 1;

    return self.frames[index * self.framesize : (index + 1) * self.framesize]
