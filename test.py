from collections import namedtuple


class Player:
    def __init__(self, x, y, height, width, vel, up_key, down_key, num_actions, state_size, device, current_step, *args):
        self.current_step = current_step
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = vel
        self.up_key = up_key
        self.down_key = down_key
        self.num_actions = num_actions
        self.policy_net = DQN(*args).to(device)
        self.target_net = DQN(*args).to(device)
        self.memory = ReplayBuffer(1000000)
        self.strategy = EpsilonGreedyStrategy(start=1, end=0.003, decay=0.0001)
        self.optimizer = optim.Adam(
            params=self.policy_net.parameters(), lr=0.001)
        self.device = device
        self.hidden_layers = args

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255),
                         (self.x, self.y, self.width, self.height))

    def key_movement(self, keys):
        if keys[getattr(pygame, self.up_key)]:
            self.moveup()
        if keys[getattr(pygame, self.down_key)]:
            self.movedown()

    def movement(self, action):
        if action == 0:
            self.moveup()
        if action == 1:
            self.movedown()

    def moveup(self):
        if self.y <= 0:
            self.y -= 0
        else:
            self.y -= self.vel

    def movedown(self):
        if self.y + self.height >= screen_height:
            self.y += 0
        else:
            self.y += self.vel

    def select_action(self, state):
        rate = self.strategy.get_exploration_rate(self.current_step)
        # if self.memory.can_provide_sample(self.memory.capacity):
        self.current_step += 1
        if rate > random.random():
            # explore
            return torch.tensor(random.randrange(self.num_actions)).to(self.device)
        else:
            with torch.no_grad():
                return self.policy_net(state).argmax(dim=1)  # exploit

    def get_current(self, states, actions):
        return self.policy_net(states).gather(dim=1, index=actions)

    def get_next(self, next_states):
        return self.target_net(next_states).max(dim=1, keepdim=True).values

    def update_target_net(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def follow(self):
        if ball.y > self.y + self.height/2:
            return 1
        if ball.y < self.y + self.height/2:
            return 0

    def hardcodedai(self):
        return self.follow()

class Ball:
    def __init__(self, x, y, r, velx, vely):
        self.x = x
        self.y = y
        self.r = r
        self.velx = velx
        self.vely = vely

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.r)

    def move(self):
        self.x += self.velx
        self.y += self.vely

    def bounce_x_increase(self, maxvel):
        if abs(ball.velx) > maxvel:
            if ball.velx > 0:
                ball.velx = (ball.velx) * -1
            else:
                ball.velx = (ball.velx) * -1
        else:
            if ball.velx > 0:
                ball.velx = (ball.velx + 1) * -1
            else:
                ball.velx = (ball.velx - 1) * -1
        return ball.velx

    def bounce(self):
        bounce, x, _, _ = self.collision()
        if bounce:
            if x == 1:
                self.bounce_x_increase(maxvel)
                self.vely = self.vely - 5
            if x == 2:
                self.bounce_x_increase(maxvel)
                self.vely = self.vely - 1
            if x == 3:
                self.bounce_x_increase(maxvel)
            if x == 4:
                self.bounce_x_increase(maxvel)
                self.vely = self.vely + 1
            if x == 5:
                self.bounce_x_increase(maxvel)
                self.vely = self.vely + 5

        if self.groundcollision():
            self.vely = (self.vely) * -1

    def collision(self):
        collision = False
        P1 = False
        P2 = False
        x = 0
        reward1 = 0
        reward2 = 0
        if ball.x + ball.r >= player1.x and ball.x - ball.r <= player1.x + player1.width:
            if ball.y + ball.r >= player1.y and ball.y + ball.r <= player1.y + player1.height:
                collision = True
                P1 = True
        if ball.x - ball.r <= player2.x + player2.width and ball.x + ball.r >= player2.x:
            if ball.y + ball.r >= player2.y and ball.y + ball.r <= player2.y + player2.height:
                collision = True
                P2 = True

        if collision & P1:
            ball.x = player1.x - ball.r
            if ball.y + ball.r > player1.y and ball.y <= math.floor(player1.y + player1.height/8):
                x = 1
            if ball.y > math.floor(player1.y + player1.height/8) and ball.y <= math.floor(player1.y + 3*player1.height/8):
                x = 2
            if ball.y > math.floor(player1.y + 3*player1.height/8) and ball.y <= math.floor(player1.y + 5*player1.height/8):
                x = 3
            if ball.y > math.floor(player1.y + 5*player1.height/8) and ball.y <= math.floor(player1.y + 7*player1.height/8):
                x = 4
            if ball.y > math.floor(player1.y + 7*player1.height/8) and ball.y - ball.r <= math.floor(player1.y + player1.height):
                x = 5
            reward1 = 0
        if collision & P2:
            ball.x = player2.x + player2.width + ball.r
            if ball.y + ball.r > player2.y and ball.y <= math.floor(player2.y + player2.height/8):
                x = 1
            if ball.y > math.floor(player2.y + player2.height/8) and ball.y <= math.floor(player2.y + 3*player2.height/8):
                x = 2
            if ball.y > math.floor(player2.y + 3*player2.height/8) and ball.y <= math.floor(player2.y + 5*player2.height/8):
                x = 3
            if ball.y > math.floor(player2.y + 5*player2.height/8) and ball.y <= math.floor(player2.y + 7*player2.height/8):
                x = 4
            if ball.y > math.floor(player2.y + 7*player2.height/8) and ball.y - ball.r <= math.floor(player2.y + player2.height):
                x = 5
            reward2 = 0
        return collision, x, reward1, reward2

    def groundcollision(self):
        groundcollision = False
        if ball.y + ball.r >= screen_height:
            groundcollision = True
        if ball.y - ball.r <= 0:
            groundcollision = True
        return groundcollision

class EpsilonGreedyStrategy():
    def __init__(self, start, end, decay):
        self.start = start
        self.end = end
        self.decay = decay

    def get_exploration_rate(self, current_step):
        return self.end + (self.start - self.end) * \
            math.exp(-1 * current_step * self.decay)

class ReplayBuffer():
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0

    def push(self, experience):
        if len(self.memory) < self.capacity:
            self.memory.append(experience)
        else:
            self.memory[self.push_count % self.capacity] = experience
            self.push_count += 1

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def can_provide_sample(self, batch_size):
        return len(self.memory) >= batch_size

class Tools():
    def np_to_torch(state):
        state = torch.tensor(state, dtype=torch.float32)
        state = torch.reshape(state, (1, len(state)))
        state = state.to(device)
        return state

    def extract_tensors(experiences):

        batch = Experience(*zip(*experiences))

        t1 = torch.cat(batch.state)
        t2 = torch.cat(batch.action2)
        t3 = torch.cat(batch.reward)
        t4 = torch.cat(batch.next_state)
        t5 = batch.done
        return (t1, t2, t3, t4, t5)

    def preprocess(action):
        action = torch.tensor(action)
        action = torch.reshape(action, (1, 1))
        return action

    def invert(state):
        p1_y = state[0]
        p2_y = state[1]
        bx = state[2]
        by = state[3]
        bvx = state[4]
        bvy = state[5]
        return np.array([p2_y, p1_y, screen_width/800 - bx, by, -bvx, bvy])


