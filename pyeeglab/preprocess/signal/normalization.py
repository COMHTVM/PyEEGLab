import logging

import numpy as np
import pandas as pd

from ...pipeline import Preprocessor

from typing import List


class MinMaxNormalization(Preprocessor):
    def run(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:

        def min_max_norm(array: np.ndarray, _min: float, _max: float) -> np.ndarray:
            return (array - _min)/(_max - _min)

        args = (kwargs['min_value'], kwargs['max_value'])
        return data.apply(min_max_norm, args=args, raw=True)


class MinMaxCentralizedNormalization(Preprocessor):
    def run(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:

        def min_max_norm(array: np.ndarray, _min: float, _max: float) -> np.ndarray:
            return (array - ((_max + _min)/2))/((_max - _min)/2)

        args = (kwargs['min_value'], kwargs['max_value'])
        return data.apply(min_max_norm, args=args, raw=True)
