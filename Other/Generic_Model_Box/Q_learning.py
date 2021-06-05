import numpy as np
import pandas as pd

''' Some describtion to this package Q-learning'''
''' First, insert the action list (option or whatever) to create a new q_table to contain states and values'''
''' Second, use set_observation to insert the information that need to be used to determind and refresh the q-value '''
''' Third,  use get_action_move to get the result '''




class Brain_Q_table_move():
    
    def __init__(self,action_list):             
        ### q-learning parameters   
        self.lr = 0.01
        self.gamma = 0.9
        self.epsilon = 0.9
        self.move = ''
        
        
        self.origin_state = 0
        self.new_state = 0
        self.reward = 0

        ### create q-table
        ### remeber that action_list can be a dictionary or list ,which is used to contain
        ### Options for model to choose
        
        self.move_action = action_list
        self.q_table_column = action_list + ['state'] ## create a seperate column name called state
        self.q_table = pd.DataFrame(columns = self.q_table_column,dtype = np.float64)        
        
    def set_observation(self,info):
        self.vis_map = info['vis_map']
        self.vis_range = info['vis_range']
                 
              
    def get_action_move(self):
        ''' in this example , we chooses vis_map'''
        
        
        observation = self.vis_map 
        self.__check_state_exist(observation)
        state_df = self.q_table['state']
        
        count = 0
        ori_index = 0
        for i in state_df:
            if i == observation:
                ori_index = count
            else:
                count += 1

        if np.random.uniform() < self.epsilon:            
            state_action = self.q_table.iloc[ori_index, :-1]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            action = np.random.choice(self.move_action)
            

        self.move = action
        self.__Imagin_Reward_function_for_Brain_move()
        self.__learn()
        
        return action


    def __Imagin_Reward_function_for_Brain_move(self):
        ''' we are in the middle of the vis map'''
        ''' calculate the exact coordinate '''
        vis_map = self.vis_map  
        vis_range = self.vis_range        
        map_position = int((vis_range-1)/2)

        position = [map_position,map_position]
        
      
        self.origin_state = vis_map
        new_vis_map = [[0 for i in range(vis_range)]for j in range(vis_range)]
        
        
        move_action = self.move
        if move_action =='up':
            position[0] = position[0] -1
            
            for i in range(0,vis_range-1):
                for j in range(0,vis_range):
                    value = vis_map[i][j]
                    new_vis_map[i+1][j] = value
                         
        elif move_action == 'down':
            position[0] = position[0] +1

            for i in range(1,vis_range):
                for j in range(0,vis_range):
                    value = vis_map[i][j]
                    new_vis_map[i-1][j] = value
            
        elif move_action =='left':
            position[1] = position[1] -1
            
            for i in range(0,vis_range):
                for j in range(0,vis_range-1):
                    value = vis_map[i][j]
                    new_vis_map[i][j+1] = value            
                        
        elif move_action == 'right':
            position[1] = position[1] +1        
        
            for i in range(0,vis_range):
                for j in range(1,vis_range):
                    value = vis_map[i][j]
                    new_vis_map[i][j-1] = value   
                    
        reward = 0
        if vis_map[position[0]][position[1]] < 0:
            reward = 1
            self.count = 0
        else:
            reward = 0  
            self.count += 1
        
        ### the imagin new vis map will be the new vis map , after the imagination action
        self.new_state = new_vis_map
        self.reward = reward
     

    
    #### core algorithm    
    def __learn(self):
        s  = self.origin_state
        s_ = self.new_state
        a  = self.move
        r  = self.reward
        
        
        self.__check_state_exist(s_)
        
        ### loop df['state'] to get index
        state_df = self.q_table['state']
        count = 0
        ori_index = 0
        new_index = 0
        
        for i in state_df:
            if i == s:
                ori_index = count
            elif i == s_:
                new_index = count
            else:
                count += 1

        q_predict = self.q_table.loc[ori_index, a]
        q_target = r + self.gamma * self.q_table.iloc[new_index, :-1].max()  # next state is not terminal
        self.q_table.iloc[ori_index, self.q_table.columns.get_loc(a)] += self.lr * (q_target - q_predict)
        self.q_table.loc[ori_index, a] += self.lr * (q_target - q_predict)
        
       

    def __check_state_exist(self, state):
        if state not in list(self.q_table['state'].values):
            # append new state to q table
            
            new_rows = {}
            for i in self.q_table_column:
                if i == 'state':
                    new_rows[i] = [state]
                else:
                    new_rows[i] = 0
            new_rows_df = pd.DataFrame(new_rows)
        
            self.q_table = pd.concat([self.q_table,new_rows_df],axis = 0,ignore_index = True)
                        
       
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    