import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyeeglab import TUHEEGArtifactLoader, TUHEEGArtifactDataset, \
                     Pipeline, CommonChannelSet, LowestFrequency, BandPassFrequency, ToDataframe, \
                     DynamicWindow, ForkedPreprocessor, BinarizedSpearmanCorrelation, \
                     CorrelationToAdjacency, Bandpower, GraphWithFeatures

class TestTUHEEGArtifact(unittest.TestCase):
    PATH = './tests/samples/tuh_eeg_artifact/v1.0.0/edf'

    def test_index(self):
        TUHEEGArtifactLoader(self.PATH)

    def test_loader(self):
        loader = TUHEEGArtifactLoader(self.PATH)
        loader.get_dataset()
        loader.get_dataset_text()
        loader.get_channels_set()
        loader.get_lowest_frequency()

    def test_dataset(self):
        dataset = TUHEEGArtifactDataset(self.PATH)
        """
        preprocessing = Pipeline([
            CommonChannelSet(['EEG T1-REF', 'EEG T2-REF']),
            LowestFrequency(),
            BandPassFrequency(0.1, 47),
            ToDataframe(),
            DynamicWindow(4),
            ForkedPreprocessor(
                inputs=[
                    [BinarizedSpearmanCorrelation(), CorrelationToAdjacency()],
                    Bandpower()
                ],
                output=GraphWithFeatures()
            )
        ])
        dataset = dataset.set_pipeline(preprocessing).load()
        """
