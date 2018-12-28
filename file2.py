#!/usr/bin/env python
# coding: utf-8

# # Cartpole DQN

# In[76]:


import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = ""


# ##  Import Dependencies

# In[77]:


import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
#import os


# ## Set Parameters

# In[78]:

env_name = 'MountainCar-v0'

env = gym.make(env_name)


# In[79]:


state_size = env.observation_space.shape[0]



# In[ ]:


action_size = env.action_space.n


# In[ ]:


batch_size = 32
n_episodes = 1001


# In[ ]:


output_dir = 'model_output/{}'.format(env_name)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# #### Define our agent formally

# In[ ]:


class DQNAgent:
    

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        self.memory = deque(maxlen=3000)
        
        self.gamma = 0.90
        
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        
        self.learning_rate = 0.001
        
        self.model = self._build_model()
            
    def _build_model(self):

        model = Sequential()

        model.add(Dense(24, input_dim = self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

        return model
    
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size):
        
        minibatch = random.sample(self.memory, batch_size)
    
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            
            self.model.fit(state, target_f, epochs=1, verbose=0)
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load(self, name):
        self.model.load_weights(name)
        
    def save(self, name):
        self.model.save_weights(name)


# In[ ]:


agent = DQNAgent(state_size, action_size)


# #### Interact with environment

# In[ ]:


done = False
for e in range(n_episodes):
    
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    
    for time in range(50000):
        

       # env.render()
        
        action = agent.act(state)
        
        next_state, reward, done, _ = env.step(action)
        
        reward = reward if not done else -10
        
        next_state = np.reshape(next_state, [1, state_size])
        
        agent.remember(state, action, reward, next_state, done)
        
        state = next_state
        
        if done:
            print("episode : {}/{}, score : {}, e : {:.2}".format(e, n_episodes, time, agent.epsilon))
            break
    
    if len(agent.memory) > batch_size:
        agent.replay(batch_size)
    
    if e % 50 == 0:
        agent.save(output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")






