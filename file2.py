#!/usr/bin/env python
# coding: utf-8

# # Cartpole DQN

# In[76]:


import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = ""


# ##  Import Dependencies

# In[77]:

from file1 import setup_get_hp, detect_hp, detect_start, detect_paused, get_visual_input
from file1 import actually_act
import random
import pyautogui
import numpy as np
from collections import deque
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten
from keras.optimizers import Adam
#import os
import time


# ## Set Parameters

# In[78]:

env_name = 'Shadow fight 2'

#env = gym.make(env_name)


# In[79]:


state_size = 1



# In[ ]:


action_size = 22


# In[ ]:


batch_size = 8
n_episodes = 2


# In[ ]:


output_dir = 'D:/Python Workshop/Shadow fight 2 MODELS/temp/{}'.format(env_name)
search_dir = 'D:/Python Workshop/Shadow fight 2 MODELS/temp'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# #### Define our agent formally

# In[ ]:


class DQNAgent:


    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        self.memory = deque(maxlen=3000)
        
        self.gamma = 0.80
        
        self.epsilon = 0.20
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        
        self.learning_rate = 0.001
        
        self.model = self._build_model()


    def _build_model(self):

        model = Sequential()

      #  model.add(Dense(24, input_dim = self.state_size, activation='relu'))
       # model.add(Dense(24, activation='relu'))
       # model.add(Dense(self.action_size, activation='softmax'))
       # model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

        model.add(Conv2D(32, kernel_size=(3, 3),
                             activation='relu',
                             input_shape=(459, 811, 1)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(action_size, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))


        return model
    
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        state = state.reshape((1, state.shape[0], state.shape[1], 1))
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size):
        
        minibatch = random.sample(self.memory, batch_size)
    
        for state, action, reward, next_state, done in minibatch:
            target = reward
            state = state.reshape((1, state.shape[0], state.shape[1], 1))

            if not done:
                next_state = next_state.reshape((1, next_state.shape[0], next_state.shape[1], 1))
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            
            self.model.fit(state, target_f, epochs=1, verbose=2)
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load(self, name):
        self.model = load_model(name)

    def save(self, name):
        self.model.save(name)


# In[ ]:
def find_episode_trained(dir):
    result = []
    for filename in os.listdir(dir):

        if filename.endswith('.hdf5'):
            filename = int(filename[15:19])
            result.append(filename)
    try:
        result = max(result)
    except ValueError:
        print("No training_file")
        result = 0
    return result

def keep_only_last_one(dir, episodes):
    for filename in os.listdir(dir):
        if filename.endswith('.hdf5'):
            match = 'Shadow fight 2_{}.hdf5'.format(episodes)
            if match != filename:
                os.remove(dir + '/ '+ filename)

#episodes_trained = 6
episodes_trained = find_episode_trained(search_dir)  # finds episode based on dir
print("found", episodes_trained)

if episodes_trained < 9:
    episodes_trained = '000' + str(episodes_trained)
elif episodes_trained > 9:
    episodes_trained = '00' + str(episodes_trained)

keep_only_last_one(search_dir, episodes_trained)  # this keeps only the best

agent = DQNAgent(state_size, action_size)
agent.epsilon = int(100 - int(episodes_trained) * 2.5) / 100
if int(episodes_trained) > 0:
    agent.model_load_name = 'Shadow fight 2_{}.hdf5'.format(episodes_trained) ####loads

# #### Interact with environment
episodes = episodes_trained
# In[ ]:

region_of_ally, region_of_enemy, bluestacks_position = setup_get_hp()

for e in range(n_episodes):

    visual_input = get_visual_input(bluestacks_position)
    while not detect_paused(visual_input) or not detect_start(visual_input):
        visual_input = get_visual_input(bluestacks_position)
        print('waiting match to start')
        time.sleep(0.1)

    state = get_visual_input(bluestacks_position)
    state = np.array(state / 255)
   # state = np.reshape(state, [1, state_size])
    #state.shape

    for iteration in range(50000):

       # env.render()
        actually_act(agent.act(state), bluestacks_position)
        action = agent.act(state)
        
        #next_state, reward, done, _ = env.step(action)
        reward_data = detect_hp(region_of_ally, region_of_enemy)
        reward = reward_data[0] * 1.5 - reward_data[1]

        done = reward_data[2]

        next_state = get_visual_input(bluestacks_position, delay=0.3)
        next_state = np.array(next_state/255)
        reward = reward if not done else 0
        
      #  next_state = np.reshape(next_state, [1, state_size])



        agent.remember(state, action, reward, next_state, done)
        
        state = next_state


        if done:
            print("episode : {}/{}, score : {}, e : {:.2}".format(e, n_episodes, iteration, agent.epsilon))
            print('done')
            come_back = pyautogui.position()
            pyautogui.click(bluestacks_position[0] + 200, bluestacks_position[1] + 200)
            pyautogui.press('p')
            pyautogui.moveTo(come_back)
            time.sleep(3)
            pyautogui.click(bluestacks_position[0] + 200, bluestacks_position[1] + 200)
            pyautogui.press('esc')
            pyautogui.moveTo(come_back)
            break

    if len(agent.memory) > batch_size:
        print('training')
        come_back = pyautogui.position()
        pyautogui.click(bluestacks_position[0] + 200, bluestacks_position[1] + 200)
        pyautogui.press('p')
        pyautogui.moveTo(come_back)
        agent.replay(batch_size)
        pyautogui.click(bluestacks_position[0] + 200, bluestacks_position[1] + 200)
        pyautogui.press('esc')
        pyautogui.moveTo(come_back)

come_back = pyautogui.position()
pyautogui.click(bluestacks_position[0] + 200, bluestacks_position[1] + 200)
pyautogui.press('p')
pyautogui.moveTo(come_back)
print("done")
#    if e % 50 == 0:
#        agent.save(output_dir + "_" + '{:04d}'.format(e) + ".hdf5")


episodes = int(episodes) + n_episodes
agent.save(output_dir + "_" + '{:04d}'.format(episodes) + ".hdf5")





