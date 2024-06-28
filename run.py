from flask import Flask, render_template, request, send_file, jsonify
import cv2
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'img-result'

def process_image(img_path, transformation_type):
    # Read the image from the specified path
    image_bgr = cv2.imread(img_path)

    # Chec
    if image_bgr is None:
        return None, {"error": f"Unable to read image from {img_path}. Please check the file path."}

    result_folder = app.config['RESULT_FOLDER']
    os.makedirs(result_folder, exist_ok=True)

    if transformation_type == 'gray':
        image_transformed = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    elif transformation_type == 'saturation':
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        image_hsv[:, :, 1] = cv2.add(image_hsv[:, :, 1], 50)  # Increase saturation
        image_transformed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    elif transformation_type == 'hue':
        hue_shift = 50
        # Convert BGR to HSV
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        image_hsv[:, :, 0] = (image_hsv[:, :, 0] + hue_shift) % 180
        image_transformed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    else:
        return None, {"error": "Unsupported transformation type."}

    # Extract filename from the input image path
    filename = os.path.basename(img_path)
    filename_without_extension, extension = os.path.splitext(filename)

    # Construct the new filename with the transformation type appended before the extension
    output_filename = os.path.join(result_folder, f'{filename_without_extension}_output_{transformation_type}{extension}')

    # Save the transformed image using the new filename
    cv2.imwrite(output_filename, image_transformed)

    return output_filename, {"message": f"Image saved as: {output_filename}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        transformation_type = request.form.get('type')
        if transformation_type not in ['gray', 'saturation','hue']:
            return jsonify({"error": "Invalid transformation type selected"}), 400

        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
 
        result_filename, result_info = process_image(file_path, transformation_type)

        if result_filename:
            return send_file(result_filename, as_attachment=True)
        else:
            return jsonify(result_info), 400  # Return error message if processing failed

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
