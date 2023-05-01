from music21 import *
import os
from PIL import Image

def extract_arrays_from_midi_file(midi_file_path):
    # Load the MIDI file using music21
    midi_file = converter.parse(midi_file_path)

    # Create the arrays
    pitches = []
    durations = []
    start_times = []
    parts = []

    for part_number, part in enumerate(midi_file.parts):
        # Extract the notes, rests, and chords and add them to the arrays
        for element in part.flat:
            if isinstance(element, note.Note):
                # If the element is a note, add it to the arrays
                pitches.append(element.pitch.midi)
                durations.append(element.duration.quarterLength)
                start_times.append(element.offset)
                parts.append(part_number)
            elif isinstance(element, note.Rest):
                continue
            elif isinstance(element, chord.Chord):
                # If the element is a chord, add each note in the chord seperately to the arrays
                for pitch in element.pitches:
                    pitches.append(pitch.midi)
                    durations.append(element.duration.quarterLength)
                    start_times.append(element.offset)
                    parts.append(part_number)

    print("Total notes saved:", len(pitches))

    return pitches, durations, start_times, parts

def create_piano_roll_image(pitches, durations, start_times, parts, filename):
    # Load the MIDI file
    midi_file = converter.parse(filename)

    # Determine the minimum start time of any element in the MIDI file
    min_start_time = min(start_times)
    
    # Define the pixel size
    time_resolution = 0.1 # Seconds per pixel
    
    # Define the image dimensions and pixel colors for each part
    img_width = int(midi_file.highestTime / time_resolution) + 10  # Calculate width from highest time in MIDI file
    img_height = 128
    part_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] # Red, green, and blue, add more colors if neccesary

    # Create the image
    img = Image.new('RGB', (img_width, img_height), (0, 0, 0))

    # Iterate over all the notes and draw them in the image
    for pitch, duration, start_time, part in zip(pitches, durations, start_times, parts):
        x = round((start_time - min_start_time) / time_resolution) 
        y = pitch 
        w = int(duration / time_resolution)
        h = 1
        
        # Draw the note in the image with the corresponding part color
        img.paste(part_colors[part % len(part_colors)], (x, y, x+w, y+h))

        # Add a black pixel to separate notes
        if w > 4:
            img.putpixel((x+(w-1), y), (0, 0, 0))

    return img

midi_dir = 'path/to/midi/files'
image_dir = 'path/to/save/images'

# Iterate over all midi files in the directory
for filename in os.listdir(midi_dir):
    if filename.endswith('.mid'):
        # Create the full path to the MIDI file
        filepath = os.path.join(midi_dir, filename)
        
        # Load the midi file and extract arrays
        pitches, durations, start_times, parts = extract_arrays_from_midi_file(filepath)
        
        # Create image from arrays
        img = create_piano_roll_image(pitches, durations, start_times, parts, filepath)
        
        # Save the image with the same filename as the MIDI file
        save_path = os.path.join(image_dir, os.path.splitext(os.path.basename(filename))[0] + '_visual.png')
        img.save(save_path)
