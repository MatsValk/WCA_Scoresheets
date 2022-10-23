import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import os
from typing import List, Dict

from src.utils.utils import load_yaml, save_as_yaml
from src.data.scorecard import ScoreCard


@dataclass
class ScoreDeck:
    competition: str

    results_df: pd.DataFrame = field(init = False)
    scorecards: List[ScoreCard] = field(init = False)
    train_test_values: Dict[str, float] = field(init = False)

    def __post_init__(self):
        self.results_df = self.read_competition_results_df()
        self.train_test_values = self.read_train_test_values()
        self.scorecards = self.read_scorecards()
        self.update_train_test_values()

    @property
    def train_test_values_path(self) -> Path:
        return ROOT / f'data/interim/train_test_split/{self.competition}.yaml'

    @property
    def resultd_df_path(self) -> Path:
        return ROOT / f'data/raw/{self.competition}/results.csv'

    def read_competition_results_df(self) -> pd.DataFrame:
        """ Read excel with results from competition """
        return pd.read_csv(self.resultd_df_path, sep = ';')

    def read_train_test_values(self) -> Dict[str, float]:
        """ Read train/test split as already configured """
        if not os.path.exists(self.train_test_values_path):
            return {}
        else:
            return load_yaml(self.train_test_values_path)

    def read_scorecards(self) -> List[ScoreCard]:
        """ Return list of ScoreCards based on self.results_df """
        return [
            ScoreCard(result) for result in self.results_df.to_dict(orient = 'records')
        ]

    def update_train_test_values(self) -> None:
        """ Update missing filenames """
        missing_train_test_filenames = [
            scorecard.filename for scorecard in self.scorecards
            if scorecard.filename not in self.train_test_values
        ]

        if len(missing_train_test_filenames) > 0:
            for filename in missing_train_test_filenames:
                seed = int.from_bytes(filename.encode('utf-8'), byteorder = 'big') % 10**9
                np.random.seed(seed)
                self.train_test_values[filename] = np.random.uniform(0, 1)
            save_as_yaml(self.train_test_values_path, self.train_test_values)
