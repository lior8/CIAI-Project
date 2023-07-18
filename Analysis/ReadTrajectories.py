
from Trace import Trace
import pandas as pd
import os

def tajectories_to_csv(input_dir, output_dir):
    for setting in os.listdir(input_dir):
        curr_dir = input_dir + "\\" + setting
        filenames = os.listdir(curr_dir)
        for filename in filenames:
            trace = Trace(input_dir + "\\" + setting + "\\" + filename)
            for i, episode in enumerate(trace):
                episode_dict = {}
                for step in episode.steps:
                    for j, action in enumerate(step.actions):
                        if j not in episode_dict.keys():
                            episode_dict[j] = []
                        episode_dict[j].append(action)
#
                # win_df = win_df.append(pd.DataFrame({"is_win": episode.is_win()}, index=[i]))
                episode_df = pd.DataFrame(episode_dict)
                episode_df.to_csv(output_dir + setting + "_" + filename.split(".")[0] + str(i) + ".csv", header=False, index=False)


# Fill these:
input_dir = ""
output_dir = ""
tajectories_to_csv(input_dir, output_dir)