import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from dataclasses import dataclass, field
from typing import Dict, Union, List, Literal
import numpy as np

from src.data import ResultTypes
from src.data.result import Result


@dataclass
class ScoreCard:
    data: Dict[str, Union[str, int]] = field(repr = False)

    filename: str = field(init = False)
    event: str = field(init = False)
    round: int = field(init = False)
    id: int = field(init = False)
    wca_result: str = field(init = False)
    extra_solve: int = field(init = False)
    results: Dict[Union[int, Literal['Extra']], Result] = field(default_factory = dict)

    def __post_init__(self):
        self.filename = self.data['Filename']
        self.event = self.data['Event']
        self.round = self.data['Round']
        self.id = None if np.isnan(self.data['Id']) else int(self.data['Id'])
        self.wca_result = self.data['WCA Result']
        self.extra_solve = None if np.isnan(self.data['Extra solve']) else int(
            self.data['Extra solve'])
        self.load_results()

    def load_results(self) -> List[Result]:
        """ Load results objects for all results """
        for ind, result in enumerate(self.wca_result.split(), start = 1):
            if self.extra_solve == ind:
                self.results[ind] = Result(ResultTypes.Extra.value, 0)
                self.results['Extra'] = Result(result, self.data[f'Penalty solve {6}'])
            else:
                self.results[ind] = Result(result, self.data[f'Penalty solve {ind}'])
