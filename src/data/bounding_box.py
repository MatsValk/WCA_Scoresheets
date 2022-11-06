import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from dataclasses import dataclass, field

from src.data import ScoreDeckObjects, CategoryObjects


@dataclass
class BoundingBox:
    data: str = field(repr = False)

    categoryId: int = field(init = False)
    coordinates: str = field(init = False)

    def __post_init__(self):
        data_split = self.data.split()
        self.categoryId = int(data_split[0])
        self.coordinates = ' '.join(data_split[1:])

    def map_category_label(self, event: str, round: int) -> str:
        """ Get single category label """
        category = ScoreDeckObjects(self.categoryId)

        if category in [
                ScoreDeckObjects.ID, ScoreDeckObjects.MissingSignature,
                ScoreDeckObjects.PlusTwo, ScoreDeckObjects.Misc
        ]:
            mapped_category = CategoryObjects[category.name]
        elif category == ScoreDeckObjects.Event:
            mapped_category = CategoryObjects['E' + event]
        elif category == ScoreDeckObjects.Round:
            mapped_category = CategoryObjects['R' + str(round)]
        else:
            return ''

        return str(mapped_category.value) + ' ' + self.coordinates + '\n'
