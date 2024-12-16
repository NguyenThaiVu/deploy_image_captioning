from flask import Flask, request, jsonify
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
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
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


@app.route('/')
def home():
    logger.info("Home endpoint was reached")
    return "Image Captioning Backend"

@app.route('/device')
def get_device():
    logger.info("Device endpoint was reached")
    return jsonify({"device": device})

@app.route('/caption', methods=['POST'])
def generate_caption():
    try:
        # Get the image file from the request
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read())).convert("RGB")
        
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)
        

        # Generate caption
        output_ids = model.generate(pixel_values, max_length=16, num_beams=4)
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Return the generated caption
        logger.info(f"Caption generated successfully.")
        return jsonify({"caption": caption})

    except Exception as e:
        logger.error(f"Error generating caption: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
