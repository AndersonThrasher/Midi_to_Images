This repository contains python scripts which can be used to convert MIDI files to color-coded images for

## Requirements
- Python 3
- Python packages
  - Pillow
  - os
  - Music21
  - midiutil

## Usage
To create images from a directory containing MIDI files, run Midi_to_Images.py, changing the filepaths to correspond to your input and ouput directories.
Each track in the MIDI file will be color coded red, green, or blue.

Tiler.py takes these images and crops them into seperate smaller images of a specified length to be used as a dataset for training a generative image model (e.g. PixelCNN++).
By default, Tiler.py will crop any notes with pitches outside of the range of the 88 keys on a piano. You may need to change this if you are using MIDI files with other instruments.

Image_to_Midi.py converts a single image of height 128 to a MIDI file.

