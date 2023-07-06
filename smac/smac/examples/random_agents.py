from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import absl.logging

from smac.env import StarCraft2Env
import numpy as np


def main():
    logging.basicConfig(level=logging.DEBUG,format="[%(levelname)s %(asctime)s] absl %(message)s", datefmt='%H:%M:%S')

    env = StarCraft2Env(map_name="2s_vs_1sc", debug=True, heuristic_ai=False, heuristic_rest=True, difficulty="2")
    env_info = env.get_env_info()

    n_actions = env_info["n_actions"]
    n_agents = env_info["n_agents"]

    n_episodes = 25
    for e in range(n_episodes):
        env.reset()
        env.heuristic_targets = [None] * env.n_agents
        terminated = False
        episode_reward = 0

        while not terminated:
            state = env.get_state()
            obs = env.get_obs()
            # env.render()  # Uncomment for rendering

            actions = []
            for agent_id in range(n_agents):
                if env.get_unit_by_id(agent_id).health>0:
                    actions.append(env.get_agent_action_heuristic(agent_id,None)[1])
                else:
                    actions.append(0)

            reward, terminated, _ = env.step(actions)
            episode_reward += reward
        env.get_state()
        env.get_obs()
        absl.logging.info(f"my_main Episode: {e}")

    env.close()


if __name__ == "__main__":
    main()
