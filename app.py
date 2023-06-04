from flask import Flask, jsonify, request
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename
import mne_procession
import os
import tempfile
from flask import send_file, make_response

global raw
raw = None
filtered_raw = None
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
    
    if filtered == 'filtered':
        data = mne_procession.create_raw_plot_by_chanell(filtered_raw, from_ch, to_ch)
    elif filtered == 'raw':
        data = mne_procession.create_raw_plot_by_chanell(raw, from_ch, to_ch)
    # response = make_response(data)
    # response.headers.set('Content-Type', 'application/zip')
    # response.headers.set('Content-Disposition', 'attachment', filename='plots.zip')
    
    return data



@app.route('/get_events', methods = ['GET'])
def get_events():
    global raw
    event_dict, events = mne_procession.get_events(raw)
    data = mne_procession.create_events_plot(raw, event_dict, events)
    return data


@app.route('/filter_raw', methods = ['POST'])
def get_filtered():
    global raw
    global filtered_raw
    l_freq = request.args.get('l_freq', default=0, type=int)
    h_freq = request.args.get('h_freq', default=3, type=int)
    filtered_raw = mne_procession.filter_raw(raw, l_freq, h_freq)
    return jsonify({'message': 'Raw filtered'}), 200


@app.route('/get_complete_raw_plot', methods = ['GET'])
def get_complete_raw_plot():
    global raw
    global filtered_raw
    filtered = request.args.get('filtered', default="raw", type=str)
    if filtered == 'raw':
        data = mne_procession.create_raw_plot(raw)
    elif filtered == 'filtered':
        data = mne_procession.create_raw_plot(filtered_raw)

    return data
    