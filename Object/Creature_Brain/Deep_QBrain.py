from itertools import chain

from tf_package import Layers as layers
import tensorflow as tf

import numpy as np
import pandas as pd
class Brain_Q_table_move():
    
    def __init__(self,action_dic,additional_info):             
        ### globle params        
        self.output_graph        = False
        
        ### model parameters
        self.memory_size         = 500

        ### internal varaible ###
        self.learn_step_counter  = 0 
        self.actions             = action_dic['move_option']  
        self.n_actions           = len(action_dic['move_option'])
        self.addtional_info      = additional_info

        
        ### memory ###
        self.columns_names = action_dic['move_option'] + ['state']
        self.memory = pd.DataFrame(columns = self.columns_names,dtype = np.float32)

        
        ### tf ###
        self.x_shape = additional_info**2
        #self.__build_network()
        
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
        
                
    def set_observation(self,info):
        vis_map = list(chain.from_iterable(info['vis_map']))
        new_map = [[0 for j in range(len(vis_map))] for j in range(len(vis_map))]
        
        for i in range(len(vis_map)):
            if type(vis_map[i]) == list:
                for j in range(len(vis_map[i])):
                    new_map[j][i] = vis_map[i][j]
        
                                    
        self.features = new_map
        self.__check_state_exist(new_map)
        
        
    def get_action(self):        
        return 0






    
    def __check_state_exist(self, state):
        if state not in list(self.memory['state'].values):
            # append new state to q table
            new_rows = {}
            for i in self.columns_names:
                if i == 'state':
                    new_rows[i] = [state]
                else:
                    new_rows[i] = 0
                    
            new_rows_df = pd.DataFrame(new_rows)
            
            if self.memory.shape[0] <= self.memory_size:
                self.memory = pd.concat([self.memory,new_rows_df],axis = 0,ignore_index = True)
            else:
                drop_indices = np.random.choice(self.memory.index, 1, replace=False)
                self.memory = self.memory.drop(drop_indices)
                self.memory = pd.concat([self.memory,new_rows_df],axis = 0,ignore_index = True)

        #### object type which is stored in memeory['state'] is list , use df.loc[index,column_name] to access ####
    

    def __build_network(self):
        

        
        x  = tf.placeholder(tf.float32,shape = [None,self.x_shape**2])
        y_ = tf.placeholder(tf.float32,shape = [None,1]) ## veiw reward as label
        
        reshape_x = tf.reshape(x,[-1,self.x_shape,self.x_shape,1])
     
        conv1 = layers.Conv2d_layer(reshape_x)
        conv2 = layers.Conv2d_layer(conv1)
        
        flat = layers.Flatten(conv2)
        
        dense1 = layers.Dense_layer(flat,n_units=30)
        q_values = layers.Dense_layer(dense1,n_units=4) ## four q values
        
        loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        lr = 0.01
        _train_op = tf.train.RMSPropOptimizer(lr).minimize(loss)

        
        
    def __reward(self):
        ''' we are in the middle of the vis map'''
        ''' calculate the exact coordinate '''
        vis_map = self.vis_map  
        vis_range = self.vis_range        
        map_position = int((vis_range-1)/2)

        position = [map_position,map_position]
                
        self.origin_state = vis_map
                
        move_action = self.move
        if move_action =='up':
            position[0] = position[0] -1
            
                        
        elif move_action == 'down':
            position[0] = position[0] +1


        elif move_action =='left':
            position[1] = position[1] -1
            
                                
        elif move_action == 'right':
            position[1] = position[1] +1        
        


        
    
    
    