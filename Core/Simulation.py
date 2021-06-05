import sys
sys.path.append('../')
import time

from Utility.Dynamics import Dynamics
from Utility.Dynamics import World_info
from Utility.Visualize          import Vis_world
from Utility.Data               import Data

class Simulation():
    
    def __init__(self,world,init_object_position,init_resource_position,duration = None,real_time_info = False,simulation_speed = 1,save_data = None):
        
        if world.intrinsic_type != 'World':
            print('Type error , simulation object type must be world')
            sys.exit()            

        ### basic parameters 
        self.world = world
        
        self.init_object_position = init_object_position
        self.init_resource_position = init_resource_position
        
        self.duration = duration
        self.speed    = simulation_speed
        
        self.init_resource_dic = {}
        self.final_resource_dic = {}
        
        self.init_objective_dic = {}
        self.final_objective_dic = {}
                
        ### extra parameters
        self.real_time_info = real_time_info

        
        ### data_saveing_params
        self.save_data = save_data
        
        Simulation.__extract_objective(self)


              
        #### After everything is set , start processing             
    def process(self,dynamic_params = None,reinitialize = False):
        
        ####
        actual_step_counter = 0
        
        #### data saveing params
        save_data = self.save_data
        
        #### env time
        start_time = time.time() 
        temp_time = start_time        
        
        ### get init variable to local
        world     = self.world
        
        obj_dic = None
        res_dic = None

        if reinitialize == True:
            self.__reinitialize_obj_status()
            obj_dic    = self.final_objective_dic
            res_dic    = self.final_resource_dic  
            print('Simulation init finished')
        else:            
            obj_dic    = self.init_objective_dic
            res_dic    = self.init_resource_dic
            v = Vis_world()
            v.World_vis(world)   
        
        ### save data class
        data = Data()
        
        ### initialize dynamic parameters
        D = Dynamics(dynamic_params = dynamic_params)
        
        print('Start simulation ')        
        while time.time() - start_time < self.duration:
            now = time.time()
            
            
            if now - temp_time >= 1/self.speed:
                ### data taking , in order to save the start map , i'll leave it here , just before Dynamics
                if save_data == None:
                    pass
                else:
                    data.insert_info(objective_dic = obj_dic,resource_dic = res_dic,world_time = now - start_time,save_path = save_data)
                    data.unpack_obj_dictionary()
                    data.unpack_res_dictionary()
                                    
                #### anything related to dynamics please write it here                                                            
                
                D.set_info(object_dic = obj_dic,resource_dic = res_dic,world = world)
                D.renew_obj()                
                obj_dic = D.get_objdic()
                res_dic = D.get_resdic()
 
                #### updating world status in real time
                W = World_info(world = world,obj_dic = obj_dic,res_dic = res_dic)
                world     = W.renew_world()
                vis_world = W.renew_vis_world()
                
                if self.real_time_info == True:
                    v1 = Vis_world()
                    v1.World_vis(vis_world)

                #### don't delete this lol
                print('time has passed : ',now - start_time,' secs')
                actual_step_counter += 1
                temp_time = now
                
        ## saving the final info to data class
        data.get_obj_data_track()
        data.get_res_data_track()
        
        #### return simulation object info to outside
        print('Simulation finished ....')
        print('Simulation step per round : ' ,actual_step_counter)
        v2 = Vis_world()
        v2.World_vis(vis_world)
        self.final_objective_dic = obj_dic
        self.final_resource_dic  = res_dic
        self.world = world
        
    
    def get_world(self):
        return self.world

    def get_final_obj_dic(self):
        return self.final_objective_dic
    
    def get_final_res_dic(self):
        return self.final_resource_dic
                


    def __reinitialize_obj_status(self):
        init_obj = self.init_objective_dic
        init_res = self.init_resource_dic
        
        final_obj = self.final_objective_dic
        final_res = self.final_resource_dic
        
        ### initialize positision , health and so on , but not brain info
        ### if there were child , just skip it
        ### for now there are no mutations that might create new kinds of creatures so 
        ### the keys between init and final must be same
        
        i_obj_keys = init_obj.keys()

        for i in i_obj_keys:
            init_obj_list = init_obj[i]
            final_obj_list = final_obj[i]
            
            #### first we compare the creature index that if it is as same as the init 
            #### we only initialize the creature which were in init obj
            
            for j in range(len(init_obj_list)):
                i_obj = init_obj_list[j]
                for k in range(len(final_obj_list)):
                    f_obj = final_obj_list[k]
                    
                    #### condition ####
                    if i_obj.get_index() == f_obj.get_index():
                        init_life = i_obj.get_init_life()
                        f_obj.set_life(init_life)
                        
                        temp  = i_obj.get_position()
                        init_pos = [temp[0],temp[1]]
                        f_obj.set_position(init_pos)
                        
                        f_obj.count = 0
                        f_obj.status = 'alive'

                        
        i_res_keys = init_res.keys()
        
        for i in i_res_keys:
            init_res_list = init_res[i]
            final_res_list = final_res[i]
            
            for j in range(len(init_res_list)):
                i_res = init_res_list[j]
                for k in range(len(final_res_list)):
                    f_res = final_res_list[k]
                    
                    #### condition ####
                    if i_res.get_index() == f_res.get_index():
                        init_life = i_res.get_init_life()
                        f_res.set_life(init_life)
                        
                        f_res.status = 'alive'        
        
        self.final_objective_dic  = final_obj 
        self.final_resource_dic   = final_res       
        


        
    def __extract_objective(self):
        
        #### objective basically is creature
        init_position_list = self.init_object_position
        keys = init_position_list.keys()
        world = self.world

        obj_dic = {}
        for i in keys:
            p_list = init_position_list[i]
            temp_obj_list = []
            for j in p_list:
                obj = world.get_object(j[0],j[1])
                world.set_object(j[0],j[1],value = obj.type)
                temp_obj_list.append(obj)
            
            obj_dic[i] = temp_obj_list
        
        self.init_objective_dic = obj_dic
        ##### Resources
        
        init_resource_list = self.init_resource_position
        keys = init_resource_list.keys()
        
        res_dic = {}
        for i in keys:
            p_list = init_resource_list[i]
            temp_res_list = []
            for j in p_list:
                res = world.get_object(j[0],j[1])
                world.set_object(j[0],j[1],value = res.type)
                temp_res_list.append(res)
            
            res_dic[i] = temp_res_list        
        
        self.init_resource_dic = res_dic
        self.world = world
        
        ext_dic = {'obj':obj_dic,'res':res_dic,'world':world}
        return ext_dic
              
            