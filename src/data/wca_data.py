import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from dataclasses import dataclass, field
from typing import List
import glob

from src.data.scoredeck import ScoreDeck


@dataclass
class WCA_Data:

    competitions: List[str] = field(init = False)
    scoredecks: List[ScoreDeck] = field(init = False)

    def __post_init__(self) -> None:
        self.competitions = self.read_competitions()
        self.scoredecks = self.read_scoredecks()

    def read_competitions(self) -> List[str]:
        """ Return list of all competitions in raw/data """
        return [comp.split('/')[-1] for comp in glob.glob('data/raw/*', recursive = True)]

    def read_scoredecks(self) -> List[ScoreDeck]:
        """ Return list of all available scorecards """
        return [ScoreDeck(competition) for competition in self.competitions]


if __name__ == '__main__':
    WCA_Data()
