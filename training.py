from itertools import count
from environment import Environment
from intersection import Intersection
from levels import Level1

env = Environment()
level = Level1

# Hyper-parameters
batch_size = 64
gamma = 0.99
target_update = 100
num_episodes = 100000
save_checkpoint = 1000
current_step = 1000000
limite = 10

for episode in range(num_episodes):
        state = env.reset(level)
        for timestep in count():
            action = player.select_action(state)
            next_state, reward1, reward2, done = env.step(action)

            if done:
                next_state = np.zeros(len(next_state))

            player.memory.push(Experience(state, action2, next_state, reward2, done))
            
            state = next_state

            if player.memory.can_provide_sample(batch_size):
                experiences = player.memory.sample(batch_size)

                states, actions2, rewards2, next_states, dones = Tools.extract_tensors(
                    experiences)
                rewards = rewards.to(device)
                current_q_values = player.get_current(states, actions2)
                next_q_values = player.get_next(next_states)

                for idx, next_state in enumerate(next_states):
                    if dones[idx] == True:
                        next_q_values[idx] = 0

                target_q_values = (next_q_values * gamma) + rewards

                loss = F.mse_loss(current_q_values,
                                     target_q_values).to(device)
                player.optimizer.zero_grad()
                loss.backward()
                player.optimizer.step()

        if (episode+1) % target_update == 0:
            player.update_target_net()
            print("target net updated")
