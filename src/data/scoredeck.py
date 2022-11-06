import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import os
from typing import List, Dict
import shutil

from src.utils.utils import load_yaml, save_as_yaml
from src.data import SetTypes
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
    def resultd_df_path(self) -> Path:
        return ROOT / 'data/raw/' / self.competition / 'results.csv'

    @property
    def train_test_values_path(self) -> Path:
        return ROOT / 'data/interim/train_test_split' / f'{self.competition}.yaml'

    @property
    def images_folder(self) -> Path:
        return ROOT / 'data/raw' / self.competition / 'images'

    @property
    def labels_folder(self) -> Path:
        return ROOT / 'data/raw' / self.competition / 'labels'

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
            ScoreCard(result, self.labels_folder)
            for result in self.results_df.to_dict(orient = 'records')
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

    def prepare_categories_data(self, target_path: Path, train_threshold: float,
                                test_threshold: float) -> None:
        """ Prepare categories data for yolov5 training """
        for scorecard in self.scorecards:
            set_type = self.get_set_type(scorecard, train_threshold, test_threshold)
            self.copy_image(scorecard, target_path / set_type.value / 'images')
            labels = scorecard.get_categories_labels()
            self.write_labels(scorecard, target_path / set_type.value / 'labels', labels)

    def get_set_type(self, scorecard: ScoreCard, train_threshold: float,
                     test_threshold: float) -> SetTypes:
        """ Decide on train, test or validate set """
        if self.train_test_values[scorecard.filename] < train_threshold:
            return SetTypes.Train
        elif self.train_test_values[scorecard.filename] < test_threshold:
            return SetTypes.Test
        return SetTypes.Validate

    def copy_image(self, scorecard: ScoreCard, target_path: Path) -> None:
        """ Copy image from related to scorecard to to target path """
        shutil.copy(self.images_folder / scorecard.filename,
                    target_path / scorecard.filename)

    def write_labels(self, scorecard: ScoreCard, target_path: Path, labels: str) -> None:
        """ Write labels to txt file in target_path """
        with open(target_path / scorecard.labels_filename, 'w') as f:
            f.write(labels)
        f.close()
