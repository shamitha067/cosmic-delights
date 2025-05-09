from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib  # Import joblib
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# Load the trained model using joblib
model = joblib.load(r"C:\Users\SHAMITHA\Downloads\asl_sign_language_app\asl_sign_language_app\model.joblib")

@app.route("/")
def index():
    return render_template("index.html")  # Your HTML page for uploading images

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the base64 encoded image from the request
        data = request.json.get("image")
        
        if not data:
            return jsonify({"error": "No image data found"}), 400  # Error if no image is uploaded
        
        # Split the base64 string to remove the metadata part and decode it
        encoded = data.split(",")[1]  # Remove metadata from base64
        decoded = base64.b64decode(encoded)  # Decode the image
        
        # Convert the image to grayscale and resize it to the model's expected input size
        img = Image.open(BytesIO(decoded)).convert("L")  # Convert to grayscale
        img = img.resize((64, 64))  # Resize to 64x64 pixels, same size used during model training
        
        # Convert image to numpy array and flatten it (to match model's input shape)
        img_array = np.array(img).flatten().reshape(1, -1)  # Flatten the image to match model input
        
        # Make the prediction
        prediction = model.predict(img_array)[0]
        
        return jsonify({"prediction": prediction})  # Return prediction result as JSON

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors that occur during processing

if __name__ == "__main__":
    app.run(debug=True)
