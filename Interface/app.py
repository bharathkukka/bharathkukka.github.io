import time
import random
import base64
from flask import Flask, request, jsonify, render_template

# Initialize the Flask application
app = Flask(__name__)

# --- Mock Inference Logic ---
# In a real application, you would load your pre-trained models here
# (e.g., using TensorFlow, PyTorch, or Scikit-learn)
def run_mock_inference(model_name, image_data):
    """
    Simulates running a CNN model on the back-end.
    
    Args:
        model_name (str): The name of the model to simulate.
        image_data (str): Base64 encoded image data. This is not used in the mock
                          function but would be decoded and processed by a real model.
    
    Returns:
        dict: A dictionary containing the mock prediction and confidence score.
    """
    # Simulate processing time (e.g., model loading, preprocessing, inference)
    time.sleep(random.uniform(0.1, 0.6))
    
    confidence = random.random()
    prediction = "Unknown"

    if model_name == 'Plant Disease Recognition':
        plants = ['Tomato - Early Blight', 'Potato - Late Blight', 'Corn - Common Rust']
        prediction = random.choice(plants)
    elif model_name == 'Emotion Detection':
        emotions = ['Happy', 'Sad', 'Surprised', 'Neutral', 'Angry']
        prediction = random.choice(emotions)
    elif model_name == 'Object Classifier':
        objects = ['Keyboard', 'Mouse', 'Coffee Mug', 'Laptop', 'Phone']
        prediction = random.choice(objects)
    elif model_name == 'Digit Recognizer':
        prediction = f"Digit: {random.randint(0, 9)}"
        
    return {
        "prediction": prediction,
        "confidence": confidence
    }

# --- Flask Routes ---

@app.route('/')
def index():
    """
    Serves the main HTML page for the web application.
    Flask will look for this file in a 'templates' folder.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint to receive image data and return a model prediction.
    """
    try:
        data = request.get_json()
        if not data or 'imageData' not in data or 'modelName' not in data:
            return jsonify({"error": "Invalid request payload"}), 400

        model_name = data['modelName']
        image_data_url = data['imageData']

        # The image data is a Data URL (e.g., "data:image/jpeg;base64,...")
        # For a real model, you would extract the Base64 part and decode it:
        # image_b64 = image_data_url.split(',')[1]
        # image_bytes = base64.b64decode(image_b64)
        # Then process 'image_bytes' with your model.

        # Run the mock inference function
        result = run_mock_inference(model_name, image_data_url)
        
        return jsonify(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

# --- Main Execution ---

if __name__ == '__main__':
    # Runs the Flask app. 'debug=True' allows for auto-reloading when you save changes.
    # In a production environment, you would use a proper WSGI server like Gunicorn.
    app.run(debug=True)
