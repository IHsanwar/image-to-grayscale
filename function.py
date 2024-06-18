import cv2
import os

# Input for the image path
img_path = input('Enter the image path: ')

# Read the image from the specified path
image_bgr = cv2.imread(img_path)

# Check if image is successfully loaded
if image_bgr is None:
    print(f"Error: Unable to read image from {img_path}. Please check the file path.")
    exit()

result_folder = 'img-result'
os.makedirs(result_folder, exist_ok=True)

# Define function to convert to grayscale and save
def gray(image_bgr):
    # Extract filename from the input image path
    filename = os.path.basename(img_path)
    filename_without_extension, extension = os.path.splitext(filename)

    # Convert image to grayscale
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Construct the new filename with '_output_gray' appended before the extension
    output_filename = os.path.join(result_folder, f'{filename_without_extension}_output_gray{extension}')

    # Save the grayscale image using the new filename
    cv2.imwrite(output_filename, image_gray)
    print(f"Grayscale image saved as: {output_filename}")

    return image_gray

# Convert the input image to grayscale and save
gray(image_bgr)
