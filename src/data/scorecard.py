import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from dataclasses import dataclass, field
from typing import Dict, Union, List, Literal, Optional
import numpy as np

from src.data import ResultTypes
from src.data.result import Result
from src.data.bounding_box import BoundingBox


@dataclass
class ScoreCard:
    data: Dict[str, Union[str, int]] = field(repr = False)
    labels_folder: Path = field(repr = False)

    filename: str = field(init = False)
    event: str = field(init = False)
    round: int = field(init = False)
    id: Optional[int] = field(init = False)
    wca_result: str = field(init = False)
    extra_solve: Optional[int] = field(init = False)

    results: Dict[Union[int, Literal['Extra']], Result] = field(init = False)
    bounding_boxes: List[BoundingBox] = field(init = False)

    def __post_init__(self):
        self.filename = str(self.data['Filename'])
        self.event = str(self.data['Event'])
        self.round = int(self.data['Round'])
        self.id = None if np.isnan(self.data['Id']) else int(self.data['Id'])
        self.wca_result = str(self.data['WCA Result'])
        self.extra_solve = None if np.isnan(self.data['Extra solve']) else int(
            self.data['Extra solve'])

        self.load_results()
        self.load_bounding_boxes()

    def load_results(self) -> None:
        """ Load results objects for all results """
        results = {}
        for ind, result in enumerate(self.wca_result.split(), start = 1):
            if self.extra_solve == ind:
                results[ind] = Result(ResultTypes.Extra.value, 0)
                results['Extra'] = Result(result, int(self.data[f'Penalty solve {6}']))
            else:
                results[ind] = Result(result, int(self.data[f'Penalty solve {ind}']))
        self.results = results

    @property
    def labels_filename(self) -> str:
        return self.filename[:-4] + '.txt'

    def load_bounding_boxes(self) -> None:
        """ Load bounding boxes from labels file """
        with open(self.labels_folder / self.labels_filename, 'r') as file:
            self.bounding_boxes = [BoundingBox(line) for line in file.readlines()]
        file.close()

    def get_categories_labels(self) -> str:
        """ Get all categories labels as to be saved """
        category_labels = ''
        for bounding_box in self.bounding_boxes:
            category_labels += bounding_box.map_category_label(self.event, self.round)
        return category_labels
