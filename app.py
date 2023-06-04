from flask import Flask, jsonify, request
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename
import mne_procession
import os
import tempfile
from flask import send_file, make_response

global raw
raw = None
predictions = []
file = None


app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/upload', methods = ['POST'])
def upload():
    global raw
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file.save(tmp.name)
        raw = mne_procession.load_data(tmp.name)

    return jsonify({'message': 'File successfully uploaded'}), 200


@app.route('/get_plots', methods = ['GET'])
def get_plots():

    global raw
    from_ch = request.args.get('from_ch', default=0, type=int)
    to_ch = request.args.get('to_ch', default=3, type=int)
    filtered = request.args.get('filtered', default='filtered', type=str)
    # if not from_ch or not to_ch or not filtered:
    #     return jsonify({'message': 'Bad request'}), 400
    
    data = mne_procession.create_raw_plot_by_chanell(raw, from_ch, to_ch, filtered)
    
    # response = make_response(data)
    # response.headers.set('Content-Type', 'application/zip')
    # response.headers.set('Content-Disposition', 'attachment', filename='plots.zip')
    
    return data



@app.route('/get_events', methods = ['GET'])
def get_events():
    global raw
    event_dict, events = mne_procession.get_events(raw)
    data = mne_procession.create_events_plot(raw, events)
    return data
