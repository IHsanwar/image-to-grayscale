from flask import Flask, render_template, request, jsonify, send_file
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'img-result'

# Function to process image and return result
def process_image(img_path):
    # Read the image from the specified path
    image_bgr = cv2.imread(img_path)

    # Check if image is successfully loaded
    if image_bgr is None:
        return None, {"error": f"Unable to read image from {img_path}. Please check the file path."}

    result_folder = app.config['RESULT_FOLDER']
    os.makedirs(result_folder, exist_ok=True)

    # Extract filename from the input image path
    filename = os.path.basename(img_path)
    filename_without_extension, extension = os.path.splitext(filename)

    # Convert image to grayscale
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Construct the new filename with '_output_gray' appended before the extension
    output_filename = os.path.join(result_folder, f'{filename_without_extension}_output_gray{extension}')

    # Save the grayscale image using the new filename
    cv2.imwrite(output_filename, image_gray)

    return output_filename, {"message": f"Grayscale image saved as: {output_filename}"}

@app.route('/')
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Process the uploaded image and get the result filename
        result_filename, result_info = process_image(file_path)

        if result_filename:
            # Open a new tab with the processed image
            webbrowser.open_new_tab(result_filename)

            # Send the processed file for download
            return send_file(result_filename, as_attachment=True)

        else:
            return jsonify(result_info), 400  # Return error message if processing failed

    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Process the uploaded image and get the result filename
        result_filename, result_info = process_image(file_path)

        if result_filename:
            # Send the processed file for download
            return send_file(result_filename, as_attachment=True)

        else:
            return jsonify(result_info), 400  # Return error message if processing failed

if __name__ == '__main__':
    app.run(debug=True)
