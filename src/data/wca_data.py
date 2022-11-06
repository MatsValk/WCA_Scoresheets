import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from dataclasses import dataclass, field
from typing import List, Dict
import glob

from src.utils.utils import load_yaml, create_or_empty_folder
from src.data import SetTypes
from src.data.scoredeck import ScoreDeck


@dataclass
class WCA_Data:

    scoredecks: List[ScoreDeck] = field(init = False)
    training_config: Dict = field(init = False, repr = False)

    categories_data_train_path: Path = field(init = False, repr = False)
    train_threshold: float = field(init = False)
    test_threshold: float = field(init = False)

    def __post_init__(self) -> None:
        self.scoredecks = self.read_scoredecks()

    def read_scoredecks(self) -> List[ScoreDeck]:
        """ Return list of all available scorecards """
        return [ScoreDeck(competition) for competition in self.read_competitions()]

    def read_competitions(self) -> List[str]:
        """ Return list of all competitions in raw/data """
        return [comp.split('/')[-1] for comp in glob.glob('data/raw/*', recursive = True)]

    def load_training_config(self) -> None:
        """ Load training config """
        self.training_config = load_yaml(ROOT / 'src/configs/training.yaml')

        self.categories_data_train_path = (
            ROOT / Path(self.training_config['categories_data_train_path'])).resolve()
        self.train_threshold = self.training_config['train_frac']
        self.test_threshold = self.train_threshold + self.training_config['test_frac']

    def create_model_training_folders(self, target_path: Path) -> None:
        """ Create folders to store training data """
        for settype in SetTypes:
            for data_type in ['images', 'labels']:
                create_or_empty_folder(target_path / settype.value / data_type)

    def prepare_categories_data(self) -> None:
        """ Prepare category data for training """
        self.load_training_config()
        self.create_model_training_folders(self.categories_data_train_path)

        for scoredeck in self.scoredecks:
            scoredeck.prepare_categories_data(self.categories_data_train_path,
                                              self.train_threshold, self.test_threshold)


if __name__ == '__main__':
    w = WCA_Data()
    w.prepare_categories_data()
