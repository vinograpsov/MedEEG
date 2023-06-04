import mne
import matplotlib.pyplot as plt
import zipfile
from io import BytesIO
import base64
import numpy as np
import matplotlib 
matplotlib.use('Agg')

def find_bad_channels(raw, z_threshold=3.0):
    eeg_data = raw.get_data(picks='eeg')
    channel_means = eeg_data.mean(axis=1)
    channel_stds = eeg_data.std(axis=1)
    mean_thresholds = (channel_means.mean() - z_threshold*channel_means.std(), 
                       channel_means.mean() + z_threshold*channel_means.std())
    std_thresholds = (channel_stds.mean() - z_threshold*channel_stds.std(), 
                      channel_stds.mean() + z_threshold*channel_stds.std())
    bad_channels = []
    for ch_name, ch_mean, ch_std in zip(raw.ch_names, channel_means, channel_stds):
        if not mean_thresholds[0] <= ch_mean <= mean_thresholds[1]:
            bad_channels.append(ch_name)
        elif not std_thresholds[0] <= ch_std <= std_thresholds[1]:
            bad_channels.append(ch_name)
    return bad_channels

def load_data(file_name):
    raw = mne.io.read_raw_egi(file_name, preload=True)
    bad_channels = find_bad_channels(raw)
    raw = raw.drop_channels(bad_channels)

    if 'E257' in raw.ch_names:
        raw = raw.drop_channels('E257')

    return raw

def create_raw_plot_by_chanell(raw, from_ch, to_ch):

    plots_data = {}
    for ch_name in raw.ch_names[from_ch:to_ch]:
        fig = raw.copy().pick_channels([ch_name]).plot_psd(fmax=50)
        fig.suptitle(ch_name)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        data = base64.b64encode(buf.getvalue()).decode('utf-8')

        plots_data[ch_name] = data
    
    return plots_data


def get_events(raw):
    events = mne.find_events(raw)
    event_ids = np.unique(events[:, 2])
    event_dict = {f'event_{id}': id for id in event_ids}

    return event_dict, events

def create_events_plot(raw, event_dict, events):

    plots_data = {}
    fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=raw.info['sfreq'])

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plots_data["events"] = data
    
    return plots_data



def filter_raw(raw, l_freq=12, h_freq=30):
    raw_filtered = raw.copy().filter(l_freq=l_freq, h_freq=h_freq, method='fir', phase='zero-double', verbose=True)
    return raw_filtered


def create_raw_plot(raw):
    
    plots_data = {}
    fig = raw.pick_types(eeg=True).plot_psd(fmax=50)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    data = base64.b64encode(buf.getvalue()).decode('utf-8')
    plots_data["complete_plot"] = data
    
    return plots_data
