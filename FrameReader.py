#!/usr/local/bin/python

class FrameReader(obj):
  def __init__(self, framesize, frames, cuts, length, reversed=False):
    self.frames = frames
    if reversed:
      self.cuts = reversed(length - x for x in cuts)
    else:
      self.cuts = cuts
    self.cuts += [length]
    self.reversed = reversed

    self.framesize = framesize
    self.nframes = len(frames) / self.framesize
    self.pad = (length - self.nframes) / 2
    self.empty = self.framesize * chr(0)

    self.playing = not reversed or len(cuts) % 2
    self.cut_index = 0
    self.index = 0

  def nextFrame(self):
    self.index += 1
    if self.index <= self.cuts[self.cut_index]:
      self.playing = not self.playing
      self.cut_index += 1

    index = self.index - self.pad
    if not self.playing or index < 0 or index >= self.nframes
      return self.empty

    if self.reversed:
      index = self.nframes - index - 1;

    return self.frames[index * framesize : (index + 1) * framesize]
