This repository contains python scripts which can be used to convert MIDI files to color-coded images (and vice-versa) for training an image-generation model to write music.

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

## Results
Below are some of the results I was able to achieve after training a PixelCNN model based on work by [Tim Salimans, Andrej Karpathy, Xi Chen, and Diederik P. Kingma](https://github.com/openai/pixel-cnn) for 50 epochs on a dataset of  over 2,000 training images created from Bach's Goldberg Variations, WTC books 1 and 2, The Art of Fugue, 400+ Chorales, and other miscellaneous keyboard works. 


https://user-images.githubusercontent.com/132303976/235535176-22f98596-765d-4da1-8ae9-873f6d78dfd5.mov


https://user-images.githubusercontent.com/132303976/235535306-2f3551c1-b7e9-481a-aeab-62f70a1a363d.mov


