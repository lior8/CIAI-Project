from dataclasses import dataclass
from typing import List
from typing import NamedTuple


@dataclass()
class Observation():
    available_actions: List[bool]
    move_feats: List[float]
    enemy_feats: List[List[float]]
    ally_feats: List[List[float]]
    own_feats: List[float]


class Step:
    def __init__(self, lines: List[str], last_step=False):
        self.ally_state: List[List[float]] = []
        self.enemy_state: List[List[float]] = []
        self.last_actions: List[List[bool]] = []
        self.observations: List[Observation] = []
        # Note that for each episode, the actions and the reward of the last step are meaningless, as the last step is
        # simply the final state
        self.actions: List[str] = []
        self.reward: float = 0.0
        self._load_step(lines, last_step)

    def _load_step(self, lines: List[str], last_step:bool):
        cur_start: int = 1
        cur_end: int = self._find_first_line_that_contains(lines, "[DEBUG ", cur_start + 1)
        self.ally_state = self._load_matrix(lines[cur_start:cur_end])
        cur_start = cur_end
        cur_end: int = self._find_first_line_that_contains(lines, "[DEBUG ", cur_start + 1)
        self.enemy_state = self._load_matrix(lines[cur_start:cur_end])
        cur_start = cur_end
        cur_end: int = self._find_first_line_that_contains(lines, "[DEBUG ", cur_start + 1)
        self.last_actions = self._load_matrix(lines[cur_start:cur_end], True)
        cur_start = cur_end + 1
        agent_counter = 0
        for cur_end, line in enumerate(lines[cur_start:], start=cur_start):
            if "absl -----" not in line:
                continue
            self.observations.append(self._load_observation(lines[cur_start:cur_end]))
            cur_start = cur_end + 1

            agent_counter += 1
            if agent_counter == len(self.last_actions):
                break

        for line in lines[cur_end + 1:-1]:
            self.actions.append(' '.join(line.split()[5:]))

        if not last_step:
            if "." in lines[-1]:
                line_parts = lines[-1].split("=")[-1].split(".")
                line_parts[0].strip()
                line_parts[1] = line_parts[1].replace('-', '')
                self.reward = float(line_parts[0] + '.' + line_parts[1])
            else:
                line = lines[-1].split("=")[-1]
                line = line.replace('-', '')
                self.reward = float(line)

    def _load_observation(self, lines: List[str]):
        observation: Observation = Observation(None, None, None, None, None)
        observation.available_actions = self._load_array(lines[0], True, ", ")
        observation.move_feats = self._load_array(lines[1], True)
        sep_line_idx = self._find_first_line_that_contains(lines, "absl Ally feats", 3)
        observation.enemy_feats = self._load_matrix(lines[2:sep_line_idx])
        observation.ally_feats = self._load_matrix(lines[sep_line_idx:-1])
        observation.own_feats = self._load_array(lines[-1])
        return observation

    def _load_matrix(self, lines: List[str], convert_to_bool=False):
        return_matrix=[]
        full_matrix_lines = ' '.join(lines).replace('\n','').replace(']','').split('[[')[-1].split('[')
        for line in full_matrix_lines:
            return_matrix.append([float(_) for _ in line.split()])



        if convert_to_bool:
            for row in return_matrix:
                for i in range(len(row)):
                    if row[i] != 1 and row[i] != 0:
                        raise ValueError("Trying to convert none binary value to boolean")
                    row[i] = True if row[i] == 1 else False
        return return_matrix

    def _load_array(self, line: str, convert_to_bool: bool = False, sep: str = None):
        line = line.split("[")[-1][:-2]
        return_array = [float(_) for _ in line.split(sep)]
        if convert_to_bool:
            for i in range(len(return_array)):
                if return_array[i] != 1 and return_array[i] != 0:
                    raise ValueError("Trying to convert none binary value to boolean")
                return_array[i] = True if return_array[i] == 1 else False
        return return_array

    def _find_first_line_that_contains(self, lines: List[str], to_search: str, begin: int = 0):
        for i, line in enumerate(lines[begin:], start=begin):
            if to_search in line:
                return i

    def get_observation(self, agent_id: int):
        return self.observations[agent_id]

    def __getitem__(self, item: int):
        return self.get_observation(item)