from flask import Flask, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import io
import logging
import os
from backend_utils import create_logger

# Initialize Flask app
app = Flask(__name__)

logger = create_logger()

# Load the pre-trained model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)


@app.route('/')
def home():
    logger.info("Home endpoint was reached")
    return "Image Captioning Backend"

@app.route('/caption', methods=['POST'])
def generate_caption():
    try:
        # Get the image file from the request
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read())).convert("RGB")

        # Preprocess the image
        inputs = processor(images=image, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Generate the caption
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)

        # Return the generated caption
        logger.info(f"Caption generated successfully.")
        return jsonify({"caption": caption})

    except Exception as e:
        logger.error(f"Error generating caption: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
