import sys
sys.path.append('../')

from Object.World import World
from Utility  import Utility
from Utility  import Visualize
from Core.Simulation import Simulation

class World_Simulator():
    
    def __init__(self):
        self.world = None
        self.object_position = {}
        self.resource_position = {}
        self.object_status_dic = {}
        self.resource_status_dic = {}
        self.dynamic_params      = {'mode':None}
        
        
        
    def Create_World(self,x_axis,y_axis):
        world = World(x_axis,y_axis)
        print('World creation done')
        print('Area : ',world.Area())
        print('x-axis : ',world.get_x_axis())
        print('y-axis : ',world.get_y_axis())
        self.world = world        
        

    
    def Add_Objective(self,Object_type,amount,center,life = 100,visual_range = 1,brain_type = None,speed_upper = 1):
        
                
        if self.world == None:
            print('please use function Create_world to create a new world first')
            sys.exit()
        
        s_upper = 0
        if type(speed_upper) != int:
            s_upper = int(speed_upper)
        else:
            s_upper = speed_upper
        
        object_p,world = Utility.Objective_creater(world = self.world,
                                                   object_type = Object_type,
                                                   number = amount,
                                                   center = center,
                                                   life = life,
                                                   visual_range = visual_range,
                                                   brain_type = brain_type,
                                                   speed_upper = s_upper )
        keys = self.object_position.keys()
        if Object_type not in keys:
            self.object_position[Object_type] = object_p
        else:
            temp_list = self.object_position[Object_type]
            temp_list += object_p
            self.object_position[Object_type] = temp_list
        
        self.world = world
        

    def Add_Resources(self,Object_type,amount,center,life = None,reproduction = None,heal = None):

        if self.world == None:
            print('please use function Create_world to create a new world first')
            sys.exit()
        
        object_p,world = Utility.Resource_creater(self.world,Object_type,amount,center = center,life = life,reproduction = reproduction,heal = heal)
        keys = self.resource_position.keys()
        if Object_type not in keys:
            self.resource_position[Object_type] = object_p
        else:
            temp_list = self.resource_position[Object_type]
            temp_list += object_p
            self.resource_position[Object_type] = temp_list

        self.world = world
        
        
        
    def Dynamic_mode(self,mode = None):
        
        if mode == 'info':
            print('for now , there are five modes in dynamics')
            print('vision')
            print('process (move)')
            print('combat')
            print('resource')
            print('reproduction')
        elif mode == None:
            self.dynamic_params['mode'] = None
        elif type(mode) != list:
            print('input type does not support , please use list , however the program still continue')
            self.dynamic_params['mode'] = None
        else:
            self.dynamic_params['mode'] = mode 
            
    def Combat_params(self,params = None):
        key_list = ['upper_damage','lower_damage','damage_scaling','damage_formula']
        
        param_dic = {}
        
        if params != dict:
            self.dynamic_params['combat'] = None
        else:
            for i in params.keys():
                if i in key_list:
                    param_dic[i] = [params[i]]
                else:
                    print('extra usless params : ',i,' has been passed , please remove it although it')
                    print('will not effect the following program')
                
    
    
    
    def Start_simulation(self,simulation_duration = None,real_time_info = True,simulation_speed = 1,save_data = None,Round = 1):
        if simulation_duration == None:
            set_duration = 60
        else:
            set_duration = simulation_duration
            
        if self.world == None:
            print('please setup the world first than start simulation')
            sys.exit()
        #### parameters info
        print('initializing params')
        print('duration : ',set_duration)
        print('real time simulation info : ',real_time_info)
        
              
        sim = Simulation(world = self.world,
                         init_object_position   = self.object_position,
                         init_resource_position = self.resource_position,
                         duration               = set_duration,
                         real_time_info         = real_time_info,
                         simulation_speed       = simulation_speed,
                         save_data              = save_data)
        
        #### checking dynamic parameters
        params = self.dynamic_params
        for i in params.keys():
            if i == 'mode':
                if params[i] == None:
                    print('no mode lists has been selected , all mode are activated')
                    params[i] =  ['vision','process','combat','resource','reproduction']
                else:
                    pass
        
        print('Dynamics mode set : ',params['mode'])        

        for i in range(Round):
            print('')
            print('')
            print('Round : ',i+1)
            print('')
            if i == 0:
                reinitialize = False
            else:
                reinitialize = True
            sim.process(reinitialize = reinitialize,dynamic_params = params)
            
        
        self.world = sim.get_world()
        self.object_status_dic = sim.get_final_obj_dic()
        self.resource_status_dic = sim.get_final_res_dic()



    
    def Get_world(self,Type = 'Numpy'):
        world = self.world
        
        world = Visualize.World_object_type(world=world,world_type = Type)

  
        return world

        
        
    def Get_objective_dic(self,status = 'alive'):
        objective = self.object_status_dic
        
        if status == 'all':
            return objective
        
        elif status == 'alive':
            for i in objective.keys():
               obj_list = objective[i]
               new_list = []
               
               for j in obj_list:
                   if j.status == 'alive':
                       new_list.append(j)
               objective[i] = new_list
            return objective
        
        elif status == 'dead':
            for i in objective.keys():
               obj_list = objective[i]
               new_list = []
               
               for j in obj_list:
                   if j.status == 'dead':
                       new_list.append(j)
               objective[i] = new_list
            return objective               
            
           
           
    def Get_resource_dic(self,status = 'alive'):
        objective = self.resource_status_dic
        
        if status == 'all':
            return objective
        
        elif status == 'alive':
            for i in objective.keys():
               obj_list = objective[i]
               new_list = []
               
               for j in obj_list:
                   if j.status == 'alive':
                       new_list.append(j)
               objective[i] = new_list
            return objective
        
        elif status == 'dead':
            for i in objective.keys():
               obj_list = objective[i]
               new_list = []
               
               for j in obj_list:
                   if j.status == 'dead':
                       new_list.append(j)
               objective[i] = new_list
            return objective              

           
           
    def save_objective_dic(self):
        return 0
    
    def save_resource_dic(self):
        return 0
        
        
 
        
        
        
        
        
        