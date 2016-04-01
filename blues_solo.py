""" 
Anna Buchele

This is my Algorithmic Music toolbox
Synthesizes an 8-bit track algorithmically """

from Nsound import *
import numpy as np
from random import choice

def add_note(out, instr, key_num, duration, bpm, volume):
	""" Adds a note from the given instrument to the specified stream

		out: the stream to add the note to
		instr: the instrument that should play the note
		key_num: the piano key number (A 440Hzz is 49)
		duration: the duration of the note in beats
		bpm: the tempo of the music
		volume: the volume of the note
	"""
	freq = (2.0**(1/12.0))**(key_num-49)*440.0
	stream = instr.play(duration*(60.0/bpm),freq)
	stream *= volume
	out << stream

# this controls the sample rate for the sound file you will generate
# I like 8-bit music so I made it into that
sampling_rate = 44100.0
Wavefile.setDefaults(sampling_rate, 8)

bass = GuitarBass(sampling_rate)	# use a guitar bass as the instrument
solo = AudioStream(sampling_rate, 1)

""" these are the piano key numbers for a 3 octave blues scale in A
	See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
beats_per_minute = 60				

# making the lower/middle notes more likely to be selected than the higher ones
# the higher notes kind of hurt my ears
mod_blues_scale = blues_scale 
mod_blues_scale += blues_scale[:14]
mod_blues_scale += blues_scale[:10]

# how far away +/- from the previous note the next note can be
max_interval = 3
intervals = []
for i in range (-max_interval, max_interval+1):
	intervals.append(i)

# minimum note length
eigth_note = 0.5/2

prev_durations = []

#controls whether the notes swing or not
swing = False

#main loop, randomly selects durations while still making them all fit into the beat
for i in range(100):
	bar = 4
	bar_durations = []
	a = 0
	while bar is not 0:
		durations = np.arange(eigth_note,min(2,bar),eigth_note)
		if len(durations) == 0:
			duration = bar
			bar = bar - duration
		else:
			duration = choice(durations)
			bar = bar - duration
			if swing == True:
				if a % 2 == 0:
					duration = duration * 0.9
				else:
					duration = duration * 1.1
		if bar == 0:
			break
		a = a + 1
	add_note(solo, bass, choice(mod_blues_scale), duration, beats_per_minute, 1.0)

solo >> "blues_solo1.wav"

#optional add-in of back track
# backing_track = AudioStream(sampling_rate, 1)
# Wavefile.read('backing.wav', backing_track)

# m = Mixer()

# solo *= 0.4             # adjust relative volumes to taste
# backing_track *= 2.0

# m.add(2.25, 0, solo)    # delay the solo to match up with backing track   
# m.add(0, 0, backing_track)

# m.getStream(500.0) >> "slow_blues.wav"