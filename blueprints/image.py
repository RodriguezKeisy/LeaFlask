from flask import Blueprint, request, jsonify
import os

image_bp = Blueprint('image', __name__)

@image_bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('/path/to/save', filename))
        return jsonify({"message": "Image successfully uploaded"}), 200

    return jsonify({"error": "Failed to upload image"}), 500

def secure_filename(filename):
    return filename.replace(" ", "_").replace("/", "_")


