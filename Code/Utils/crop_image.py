# Copyright (c) 2023 Chenye Yang

from PIL import Image
import os

# List of image paths
image_paths = ["Result/Linear/linear-bsc-output.png",
               "Result/Linear/linear-bsc-output-syndrome-corrected.png",
               "Result/Cyclic/15-5/cyclic-bsc-output.png",
               "Result/Cyclic/15-5/cyclic-bsc-output-trapping-corrected.png"]

for (n, k) in [(3, 1), (7, 4), (15, 11), (31, 26), (63, 57), (127, 120)]:
    image_paths.append(f"Result/Cyclic/{n}-{k}/cyclic-bsc-output.png")
    image_paths.append(f"Result/Cyclic/{n}-{k}/cyclic-bsc-output-syndrome-corrected.png")
    image_paths.append(f"Result/Cyclic/{n}-{k}/cyclic-bsc-output-trapping-corrected.png")

# The area to be cropped out of the images: (left, upper, right, lower)
crop_area = (550, 550, 750, 750)

# Loop through all images
for image_path in image_paths:
    # Open an image file
    with Image.open(image_path) as img:
        # Crop the image
        cropped_img = img.crop(crop_area)

        # Create a new filename with the prefix "cropped-"
        directory, filename = os.path.split(image_path)
        new_filename = "cropped-" + filename
        new_path = os.path.join(directory, new_filename)
        
        # Save the cropped image
        cropped_img.save(new_path)
