from PIL import Image

# List of image paths
image_paths = ["Resource/image.png",
               "Result/linear-bsc-output.png",
               "Result/linear-bsc-output-syndrome-corrected.png",
               "Result/cyclic-bsc-output.png",
               "Result/cyclic-bsc-output-syndrome-corrected.png"]

# The area to be cropped out of the images: (left, upper, right, lower)
crop_area = (550, 550, 750, 750)

# Loop through all images
for image_path in image_paths:
    # Open an image file
    with Image.open(image_path) as img:
        # Crop the image
        cropped_img = img.crop(crop_area)
        # Save the cropped image
        cropped_img.save(image_path.split("/")[0] + "/cropped-" + image_path.split("/")[-1])
