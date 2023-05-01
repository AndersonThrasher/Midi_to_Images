from PIL import Image
import midiutil
import os

# Load image
image_path = "path/to/image/file"
image = Image.open(image_path)

# Get dimensions of image
width, height = image.size

# Set tempo and time signature
tempo = 60
time_signature = (4, 4)
time_adjustment = 0.03 #seconds per pixel in the image

# Create MIDI file with one track
midi_file = midiutil.MIDIFile(1)

# Add tempo and time signature to track
midi_file.addTempo(track=0, time=0, tempo=tempo)
midi_file.addTimeSignature(track=0, time=0, numerator=time_signature[0], denominator=time_signature[1], clocks_per_tick=24)

# Loop through each row of the image
for y in range(height):
    # Initialize variables for the current note
    note_pitch = None
    note_start_time = None

    # Loop through each pixel in the row
    for x in range(width):
        # Get the color value of the pixel
        color = image.getpixel((x, y))

        # Check if the pixel is white
        if color[0] == (255) or color[1] == (255) or color[2] == (255):  #used to be if color == (255): this now uses any pixel not equal to zero as a note
            # If this is the first white pixel in the row, start a new note
            if note_pitch is None:
                note_pitch = y
                note_start_time = x
        # If the pixel is not white and a note is currently playing, end the note
        elif note_pitch is not None:
            note_duration = x - note_start_time
            note_velocity = 70
            midi_file.addNote(track=0, channel=0, pitch=note_pitch, time=(note_start_time*time_adjustment), duration=(note_duration*time_adjustment), volume=note_velocity)
            note_pitch = None
            note_start_time = None

    # If a note is still playing at the end of the row, end the note
    if note_pitch is not None:
        note_duration = width - note_start_time
        note_velocity = 70
        midi_file.addNote(track=0, channel=0, pitch=note_pitch, time=(note_start_time*time_adjustment), duration=(note_duration*time_adjustment), volume=note_velocity)

# Get the name of the input image file
image_name = os.path.splitext(os.path.basename(image_path))[0]

# Save the MIDI file with the same name as the input image file
midi_file_name = f"{image_name}_remidi.mid"
with open(midi_file_name, "wb") as file:
    midi_file.writeFile(file)
