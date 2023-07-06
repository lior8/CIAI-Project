import pathlib
from typing import List, Union

from Episode import Episode


class Trace:
    def __init__(self, trace:Union[pathlib.Path,str, List[str]]):
        self.episodes: List[Episode] = []
        self.load_trace(trace)
    def load_trace(self, trace):
        if type(trace) is not list:
            with open(trace, 'r') as f:
                lines = f.readlines()
        else:
            lines = trace
        episode_begin: int = -1
        episode_end: int = -1
        for i, line in enumerate(lines):
            if "Sending ResponseJoinGame" in line:
                episode_begin = i + 1
                break

        for i, line in enumerate(lines[episode_begin:], start=episode_begin):
            if "my_main Episode:" in line:
                episode_end = i
                self.episodes.append(Episode(lines[episode_begin:episode_end+1]))
                episode_begin = episode_end + 1

    def __getitem__(self, arg):
        return self.episodes[arg]

    def __len__(self):
        return len(self.episodes)

    def __iter__(self):
        return iter(self.episodes)
