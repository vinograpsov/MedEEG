from flask import Flask, jsonify, request
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename
import mne_procession
import os
import tempfile


raw = None
predictions = []
file = None


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/upload', methods = ['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        raw = mne_procession.load_data(tmp.name)
        print(raw.info)

    return jsonify({'message': 'File successfully uploaded'}), 200


@app.route('/get_plots', methods = ['GET'])
def get_plots():

    plot = plt.figure()
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')

    print(file)
    return jsonify({'message': 'Here are the plots'}), 200

@app.route('/get_predictions', methods = ['GET'])
def get_predictions():
    mne_prediction = [1,2,3]
    # must get mne predicitons from my class
    for prediction in mne_prediction:  
        prediction.append(
            {
                "main feture": "value",
                "main feture": "value",
                "main feture": "value",
                "main feture": "value",
                "main feture": "value",
                "precition": "value"
            }
        )


    return jsonify({
            'message': 'Here are the predictions',
            "predictions": predictions
        }), 200