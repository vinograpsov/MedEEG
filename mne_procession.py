import mne

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

class MneProcessor:
    pass

class MnePredictor:
    pass

class MnePlotter:
    pass