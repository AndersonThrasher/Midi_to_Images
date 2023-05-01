import os
from PIL import Image

# Set input and output directories
input_dir = "/path/to/image/directory" # Directory for all images created by Midi_to_Images.py
output_dir = "/path/to/training/directory" # Directory to save the created training images to

# Choose length of each training image in pixels
length = 200

# Loop through all images in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.png'):
        image = Image.open(os.path.join(input_dir, filename))
        width, height = image.size
        
        # First crop any unneccesary columns of black pixels at the beginning or end of the track
        left = 0
        while left < width and all(image.getpixel((left, y)) == (0, 0, 0) for y in range(height)):
            left += 1
        right = width - 1
        while right >= 0 and all(image.getpixel((right, y)) == (0, 0, 0) for y in range(height)):
            right -= 1        
        if left > 0 or right < width - 1:
            image = image.crop((left, 0, right + 1, height))
            
        # Rotate the image 90 degrees clockwise
        rotated_image = image.rotate(-90, expand=True)
        width, height = rotated_image.size

        # Calculate the number of new images that will be created
        num_images = (height + (length-1)) // length

        # Loop through the new images and save each one
        for i in range(num_images):
            # Calculate the y-coordinates for the new image
            y1 = i * length
            y2 = min((i + 1) * length, height)

            # If using piano music, crop the training images so that each has a width of 88 pixels corresponding to 88 keys
            cropped_image = rotated_image.crop((20, y1, width-20, y2))
            
            # Only save training images with the correct size
            if cropped_image.size[1] == length:
                final_image = cropped_image
                output_filename = os.path.join(output_dir, f"tile_{i+1}_{os.path.splitext(filename)[0]}.png")
                final_image.save(output_filename)
