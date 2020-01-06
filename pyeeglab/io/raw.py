import logging
from abc import ABC, abstractmethod
from typing import List
from importlib.util import find_spec
import mne

class Raw(ABC):
    _reader = None

    def __init__(self, fid: str, path: str, label: str) -> None:
        self.id = fid
        self.path = path
        self.label = label

    def close(self) -> None:
        if self._reader is not None:
            logging.debug('Close Raw %s reader', self.id)
            self._reader.close()
        self._reader = None

    def crop(self, offset: int, length: int) -> None:
        logging.debug('Crop Raw %s data to %s seconds from %s', self.id, length, offset)
        tmax = self.open().n_times / self.open().info['sfreq'] - 0.1
        if offset + length < tmax:
            tmax = offset + length
        self.open().crop(offset, tmax)

    @abstractmethod
    def open(self) -> mne.io.Raw:
        pass

    def get_events(self):
        events = self.open().annotations
        events = list(zip(events.onset, events.duration, events.description))
        events = [(event[0], event[0] + event[1], event[2]) for event in events]
        keys = ['begin', 'end', 'label']
        events = [dict(zip(keys, event)) for event in events]
        return events

    def set_channels(self, channels: List[str]) -> None:
        channels = set(self.open().ch_names) - set(channels)
        logging.debug('Set Raw %s channels drop %s', self.id, '|'.join(channels))
        self.open().drop_channels(list(channels))

    def set_frequency(self, frequency: float, low_freq: float = 0, high_freq: float = 0) -> None:
        sfreq = self.open().info['sfreq']
        n_jobs = 1
        if find_spec('cupy') is not None:
            n_jobs = 'cuda'
        if low_freq > 0 and high_freq > 0:
            self.open().filter(low_freq, high_freq, n_jobs=n_jobs)
        if sfreq > frequency:
            logging.debug('Downsample %s from %s to %s', self.id, sfreq, frequency)
            self.open().resample(frequency, n_jobs=n_jobs)


class RawEDF(Raw):

    def open(self) -> mne.io.Raw:
        if self._reader is None:
            logging.debug('Open RawEDF %s reader', self.id)
            try:
                self._reader = mne.io.read_raw_edf(self.path)
            except RuntimeError:
                logging.debug('Using preload for RawEDF %s reader', self.id)
                self._reader = mne.io.read_raw_edf(self.path, preload=True)
        return self._reader


class RawFIF(Raw):

    def open(self) -> mne.io.Raw:
        if self._reader is None:
            logging.debug('Open RawFIF %s reader', self.id)
            self._reader = mne.io.read_raw_fif(self.path)
        return self._reader
