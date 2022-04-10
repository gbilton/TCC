from itertools import count

import numpy as np
import torch
import torch.nn.functional as F

from environment import Environment
from levels import Level1
from utils import Experience, extract_tensors


def main():
    level = Level1
    env = Environment(level)
    intersection = level.intersections[0]
    device = torch.device("cuda")


    # Hyper-parameters
    batch_size = 64
    gamma = 0.99
    target_update = 100
    num_episodes = 100000


    for episode in range(num_episodes):
            state = env.reset(level)
            for timestep in count():
                action = intersection.select_action(state)
                next_state, reward, done = env.step({intersection.id:action})

                if done:
                    next_state = np.zeros(len(next_state))

                intersection.memory.push(Experience(state, action, next_state, reward, done))
                
                state = next_state

                if intersection.memory.can_provide_sample(batch_size):
                    experiences = intersection.memory.sample(batch_size)

                    states, actions, rewards, next_states, dones = extract_tensors(
                        experiences)
                    rewards = rewards.to(device)
                    current_q_values = intersection.get_current(states, actions)
                    next_q_values = intersection.get_next(next_states)

                    for idx, next_state in enumerate(next_states):
                        if dones[idx] == True:
                            next_q_values[idx] = 0

                    target_q_values = (next_q_values * gamma) + rewards

                    loss = F.mse_loss(current_q_values,
                                        target_q_values).to(device)
                    intersection.optimizer.zero_grad()
                    loss.backward()
                    intersection.optimizer.step()

            if (episode+1) % target_update == 0:
                intersection.update_target_net()
                print("target net updated")


if __name__ == "__main__":
    main()