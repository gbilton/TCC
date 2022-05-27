from itertools import count

import numpy as np
import pygame
import torch
import torch.nn.functional as F

from simulation.environment import Environment
from simulation.levels import Level1
from helper.utils import Experience, extract_tensors, np_to_torch


def main():
    level = Level1
    env = Environment(level)
    env.render = False
    intersection = level.intersections[0]
    device = torch.device("cuda")

    # Hyper-parameters
    batch_size = 64
    gamma = 0.99
    target_update = 10
    num_episodes = 100000
    K = 10

    losses = []
    scores = np.array([])

    # try:
    #     scores = np.load("results/scores.npy")
    # except Exception as e:
    #     print(e)

    current_record = 0
    for i in range(len(scores) - 10):
        avg = np.average(scores[i : i + 10])
        if avg > current_record:
            current_record = avg

    for episode in range(num_episodes):
        print("episode: ", episode)
        score = 0
        state, _ = env.reset(level)
        for timestep in count():
            if env.render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                env.draw_window()
                # env.clock.tick(env.FPS)
            action = intersection.select_action(state)
            for _ in range(K):
                next_state, reward, done = env.step({intersection.id: action})
                action = 0
                if done:
                    break

            intersection_observation = torch.reshape(
                np_to_torch(intersection.get_observation(state), device), (1, 4)
            )
            action = torch.reshape(torch.tensor([action], dtype=torch.int64, device=device), (1, 1))
            reward = torch.reshape(np_to_torch([reward], device), (1, 1))
            intersection_next_observation = torch.reshape(
                np_to_torch(intersection.get_observation(next_state), device), (1, 4)
            )
            if done:
                score += reward.item()
                print(f"Reward = {reward.item()}")
                intersection_next_observation = torch.reshape(
                    torch.tensor(np.zeros(4), dtype=torch.float32, device=device), (1, 4)
                )
            intersection.memory.push(
                Experience(
                    intersection_observation,
                    action,
                    intersection_next_observation,
                    reward,
                    done,
                )
            )

            state = next_state

            if intersection.memory.can_provide_sample(batch_size):
                experiences = intersection.memory.sample(batch_size)

                states, actions, rewards, next_states, dones = extract_tensors(experiences)
                next_q_values = intersection.get_next(next_states)
                current_q_values = intersection.get_current(states, actions)

                for idx, next_state in enumerate(next_states):
                    if dones[idx] is True:
                        next_q_values[idx] = 0

                target_q_values = (next_q_values * gamma) + rewards

                loss = F.mse_loss(current_q_values, target_q_values).to(device)
                intersection.optimizer.zero_grad()
                loss.backward()
                intersection.optimizer.step()

                if done:
                    losses.append(loss.item())
                    scores = np.append(scores, score)
                    if episode % 20 == 0:
                        np.save("results/losses.npy", losses)
                        np.save("results/scores.npy", scores)
                    break

        if (episode + 1) % target_update == 0:
            intersection.update_target_net()
            print("target net updated")

        if len(scores) > 10:
            if not current_record:
                current_record = np.average(scores[-10:])
            if np.average(scores[-10:]) >= current_record:
                try:
                    torch.save(
                        {
                            "policy_net": intersection.policy_net.state_dict(),
                            "optimizer": intersection.optimizer.state_dict(),
                        },
                        "simulation/ai/models/model.tar",
                    )
                    print(f"UPDATED SAVED POLICY! - Current Record = {current_record}")
                except Exception as e:
                    raise Exception(e)

                current_record = np.average(scores[-10:])


if __name__ == "__main__":
    main()
