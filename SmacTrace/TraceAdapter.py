import pathlib
from typing import Union


class TraceAdapter:
    def __init__(self, trace_file_path: Union[pathlib.Path, str]):
        with open(trace_file_path, 'r') as f:
            self.lines = f.readlines()
        self.remove_duplicate_initial_state()

    def get_lines(self):
        return self.lines

    def remove_duplicate_initial_state(self):
        # Find where each episode starts, find all the
        segments_to_cut = []
        for i, line in enumerate(self.lines):
            if '*Started Episode ' in line:
                unit1_count = 0
                j = i - 1
                while "absl Unit " in self.lines[j]:
                    if "absl Unit 1" in self.lines[j]:
                        unit1_count += 1
                    j -= 1
                j += 1
                if unit1_count < 1:
                    raise ValueError("No units found in episode")
                if unit1_count > 1:
                    segments_to_cut.append((j, (i + j) // unit1_count))
        if len(segments_to_cut) != 0:
            new_lines = []
            current_index = 0
            for segment in segments_to_cut:
                new_lines.extend(self.lines[current_index: segment[0]])
                current_index = segment[1]
            new_lines.extend(self.lines[current_index:])
            self.lines = new_lines