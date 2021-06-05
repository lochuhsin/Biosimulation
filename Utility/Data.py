import pandas as pd
from itertools import chain


class Data():
    
    def __init__(self):
        #### info given from the simulator
        self.obj_dic = None
        self.res_dic = None
        self.world   = None
        self.world_time = None
        
        #### obj data container
        self.temp_obj_data_container = []  ## this container is used to contain every single round data  ## as it may be , this could be used to real time training such as reinforcement learning
        self.obj_data_container = []       ## this container contains the entire simulation data , which obviously way more larger than the above one ## for simple neural network 
        
        self.temp_res_data_container = []
        self.res_data_container = []
        #### world data container   
        self.world_data_container = {}
    
    
        self.path = ''


    def insert_info(self,objective_dic = None,resource_dic = None,world = None,world_time = None,save_path = 'Save/'):
        
        self.obj_dic = objective_dic
        self.res_dic = resource_dic
        self.world   = world
        self.world_time = world_time        
        self.path = save_path
        
        
    def unpack_obj_dictionary(self):
        obj_dic = self.obj_dic
        
        obj_data_list = []
            
        for i in obj_dic.keys():
            obj_list = obj_dic[i]
            temp_obj_dic = {}
            
            for j in range(len(obj_list)):
                obj = obj_list[j]
                
                temp_obj_dic = {'Type':obj.get_type(),
                                'obj_time':obj.get_object_time(),
                                'life':obj.get_life(),
                                'reproduction_status':obj.get_reproduction_status(),
                                'visual_range':obj.get_visual_range(),
                                'vis_map':obj.get_visual_map(),
                                'abs_position':obj.get_abs_position(),
                                'combat_status':obj.get_combat_status(),
                                'index':obj.get_index(),
                                'move_option':obj.get_move_option(),
                                'move_decision':obj.get_move_decision(),
                                'combat_decision':obj.get_combat_decision(),
                                'reproduction_decision':obj.get_reproduction_decision(),
                                'world_time':self.world_time}
            
                obj_data_list.append(temp_obj_dic)
                
        self.temp_obj_data_container = obj_data_list
        self.obj_data_container.append(obj_data_list)
        


    def unpack_res_dictionary(self):
        res_dic = self.res_dic
        
        res_data_list = []
        for i in res_dic.keys():
            res_list = res_dic[i]
            temp_res_dic = {}
            
            for j in range(len(res_list)):
                res = res_list[j]
                
                temp_res_dic = {}
                
                res_data_list.append(temp_res_dic)
            
        self.temp_res_data_container = res_data_list
        self.res_data_container.append(res_data_list)
                
                
                
        
    def unpack_world_info(self):
        
        world = self.world
        
        x = len(world[:])
        y = len(world[0])
        
        world_dic = {'x':x,'y':y}
        self.world_data_container = world_dic
        
        
    def get_obj_data(self):
        obj_data = pd.DataFrame(self.temp_obj_data_container)    
        return obj_data


    def get_obj_data_track(self):
        obj_data = self.obj_data_container
        obj_data = list(chain.from_iterable(obj_data))
        obj_data = pd.DataFrame(obj_data)
        obj_data.to_csv(self.path + 'obj_track.csv',index = False)
        
        

    def get_res_data(self):
        res_data = pd.DataFrame(self.temp_res_data_container)
        return res_data
        
    def get_res_data_track(self):
        res_data = self.res_data_container
        res_data = list(chain.from_iterable(res_data))
        res_data = pd.DataFrame(res_data)
        res_data.to_csv(self.path + 'res_track.csv',index = False)
        
        

    def get_world_data(self):
        world_data =  pd.DataFrame(self.world_data_container)    
        return world_data
       
    def get_world_data_track(self):
        world_data =  pd.DataFrame(self.world_data_container)
        world_data.to_csv(self.path + 'world_track.csv',index = False)
                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    