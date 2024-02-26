# app.py

from flask import Flask, render_template, request, send_file
from PIL import Image
import cv2
import numpy as np
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cartoonify', methods=['POST'])
def cartoonify_route():
    # Get the uploaded image from the form
    file = request.files['image']

    # Ensure the file is an allowed format (optional)
    allowed_formats = {'png', 'jpg', 'jpeg', 'gif'}
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_formats:
        return "Invalid file format. Please upload an image."

    # Process the image
    cartoon_image = process_image(file)

    # Display the original and cartoon images
    return render_template('result.html', cartoon_image=cartoon_image)

@app.route('/download_cartoon')
def download_cartoon():
    # Open the cartoonified image using OpenCV
    cartoon_image_path = 'static/cartoon_image.jpg'  # Update with the correct path
    cartoon_image = cv2.imread(cartoon_image_path)

    # Save the cartoonified image to a BytesIO object in JPEG format
    cartoon_buffer = io.BytesIO()
    Image.fromarray(cartoon_image).save(cartoon_buffer, format='JPEG')
    cartoon_buffer.seek(0)

    return send_file(cartoon_buffer, as_attachment=True, download_name='cartoon_image.jpg')

def process_image(file):
    # Open the image using OpenCV
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Check if the image is empty or None
    if img is None or img.size == 0:
        return "Invalid or empty image. Please upload a valid image."

    # Check if the image is grayscale and convert to color
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Apply the provided cartoonize logic
    cartoonized_image = cartoonize_image(img)

    # Save the cartoonified image to a BytesIO object in JPEG format
    cartoon_buffer = io.BytesIO()
    Image.fromarray(cartoonized_image).save(cartoon_buffer, format='JPEG')
    cartoon_buffer.seek(0)

    return cartoon_buffer

def cartoonize_image(img, num_clusters=8):
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, label, center = cv2.kmeans(data, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result

if __name__ == '__main__':
    app.run(debug=True)



