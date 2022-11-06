from dataclasses import dataclass, field
import numpy as np
import re

from src.data import ResultTypes


@dataclass
class Result:
    time: str
    penalty: int

    minutes: int = field(init = False)
    seconds: int = field(init = False)
    milliseconds: int = field(init = False)

    result_type: ResultTypes = field(init = False)

    def __post_init__(self):
        self.time = self.time.strip('()')
        self.penalty = 0 if np.isnan(self.penalty) else int(self.penalty)

        if self.time == ResultTypes.DNF.value:
            self.result_type = ResultTypes.DNF
        elif self.time == ResultTypes.DNS.value:
            self.result_type = ResultTypes.DNS
        elif self.time == ResultTypes.Extra.value:
            self.result_type = ResultTypes.Extra
        elif (self.time == '') or (self.time == ResultTypes.Empty.value):
            self.result_type = ResultTypes.Empty
        else:
            self.result_type = ResultTypes.Time
            self.read_time()

    def read_time(self) -> None:
        """ Read time and assign to minutes, seconds and milliseconds attribute """
        time_split = re.split(r':|\.', self.time)
        assert len(time_split) <= 3

        self.milliseconds = int(time_split[-1])
        self.seconds = int(time_split[-2]) - self.penalty

        if len(time_split) == 3:
            self.minutes = int(time_split[-3])
        else:
            self.minutes = 0

        if self.seconds < 0:
            self.seconds %= 60
            self.minutes -= 1
