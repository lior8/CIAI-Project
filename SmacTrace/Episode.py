import warnings
from typing import List

from Step import Step


class Episode:
    def __init__(self, episode_lines: List[str]):
        self.initial_state = []
        self.steps: List[Step] = []
        self._load_episode(episode_lines)

    def __getitem__(self, arg: int):
        return self.steps[arg]

    def _load_episode(self, lines: List[str]):
        episode_begin: int = -1
        for i, line in enumerate(lines):
            if "Started Episode" in line:
                episode_begin = i
                break
        # First we read the initial state of our agents
        for line in lines[:episode_begin]:
            line = line.split()
            self.initial_state.append((int(line[4]), int(line[6][:-1]), float(line[9][:-1]), float(line[12])))
        # Then, for some reason, the observations and state of the 0th stage are repeated, probably due to printing in
        # the initialization process as well. Therefore, we find the true beginning of step 1.
        # Furthermore, for some reason, this weird thing begins with observations and ends with the state, instead of
        # opposite which is the repeated pattern in the following steps.
        seenState: bool = False
        first_step_idx: int = -1
        for first_step_idx, line in enumerate(lines[episode_begin:], start=episode_begin):
            if "-STATE-" in line:
                if seenState:
                    break
                else:
                    seenState = True
        step_begin: int = first_step_idx
        for i, line in enumerate(lines[step_begin:], start=step_begin):
            if "-Reward = " in line or "my_main Episode:" in line:
                self.steps.append(Step(lines[step_begin: i + 1], ("my_main Episode:" in line)))
                step_begin = i + 1

    def __iter__(self):
        return iter(self.steps)

    def get_last_reward(self):
        return self.steps[-2].reward

    def is_win(self, quiet: bool = False):
        are_enemies_dead = all([enemy_state[0] == 0 for enemy_state in self.steps[-1].enemy_state])
        if are_enemies_dead:
            return True
        if self.get_last_reward() > 200:
            if not quiet:
                warnings.warn("Not all enemies are reported dead, but reward indicates win, this counts as a win then")
            return True
        return False
