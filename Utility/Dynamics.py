import sys
import random
from itertools  import chain
sys.path.append('../')
from Object.World import World
from Object.Object import Creature

class Dynamics():
    
    def __init__(self,dynamic_params = None):
        self.dynamic_params = dynamic_params
        
        self.mode_list = dynamic_params['mode']
        

    
    def set_info(self,object_dic = None,resource_dic = None,world = None):
        self.obj_dic = object_dic
        self.res_dic = resource_dic
        self.world   = world        
        
    def renew_obj(self):
        
        mode = self.mode_list
        function_dic = {'vision':self.__vision,
                        'process':self.__obj_res_process,
                        'combat':self.__combat,
                        'resource':self.__get_resource,
                        'reproduction':self.__reproduction}
        
        for i in mode:
            if i in function_dic.keys():
                function_dic[i]()
        
    
        #### this is a test function
        #Dynamics.test(self)

    def get_objdic(self):
        return self.obj_dic
    
    def get_resdic(self):
        return self.res_dic
        
    def __vision(self):
        before_world = self.world
        
        obj_dic_keys = self.obj_dic.keys()
        obj_dic      = self.obj_dic
        
        for i in obj_dic_keys:
            obj_list = obj_dic[i]
            for j in range(len(obj_list)):
                obj = obj_list[j]
                vis_range = obj.get_visual_range()
                vis_map = [[0 for i in range(vis_range)]for j in range(vis_range)]
                
                temp_range = int((vis_range-1)/2)
                obj_position = obj.get_abs_position()
                
                boundary_x = obj.world_boundary_x
                boundary_y = obj.world_boundary_y
                
                ### looping vision range to get object in the world
                for x_axis in range(-temp_range,temp_range+1):
                    for y_axis in range(-temp_range,temp_range+1):
                        
                        px = obj_position[0]+x_axis
                        py = obj_position[1]+y_axis
                                                
                        if px >= boundary_x and px > 0:
                            px = abs(obj_position[0]+x_axis - boundary_x)

                        if py >= boundary_y and py > 0:
                            py = abs(obj_position[1]+y_axis - boundary_y)
                        
                        
                        world_obj = before_world.get_object(x = px,y = py)
                        if world_obj != 0 and type(world_obj) != list:
                            vis_map[x_axis + temp_range][y_axis + temp_range] = [world_obj]
                        else:
                            vis_map[x_axis + temp_range][y_axis + temp_range] = world_obj
                        
                obj.set_visual_map(vis_map = vis_map)
                obj_list[j] = obj
                
            obj_dic[i] = obj_list
        
        self.obj_dic = obj_dic
        
    
    #### start process as here is the decision making point ~~~~~~~~~~~~~
    def __obj_res_process(self):
        
        obj_dic_keys = self.obj_dic.keys()
        obj_dic = self.obj_dic
        
        for i in obj_dic_keys:
            obj_list = obj_dic[i]
            for j in range(len(obj_list)):
                obj = obj_list[j]
                if obj.get_status() == 'alive':
                    obj.process()
                obj_list[j] = obj        
            obj_dic[i] = obj_list        
        self.obj_dic = obj_dic        
        
        res_dic_keys = self.res_dic.keys()
        res_dic = self.res_dic
        
        for k in res_dic_keys:
            res_list = res_dic[k]
            for l in range(len(res_list)):
                res = res_list[l]
                if res.get_status() == 'alive':
                    res.process()
                res_list[l] = res                
            res_dic[k] = res_list
        self.res_dic = res_dic
        

    #### outcome of making decisions
    def __combat(self):
        
        ##### set combat damage value limit
        ##### for now it uses random 
        combat_lower_damage = 30
        combat_upper_damage = 50
        
        obj_dic_keys = list(self.obj_dic.keys())
        obj_dic = self.obj_dic

        #### check if two speices were in the same spot     
        #### it might have a more efficient way to implement the same algorithm
                
        for i in range(len(obj_dic_keys)):
            for j in range(i+1,len(obj_dic_keys)):
                obj_list1 = obj_dic[obj_dic_keys[i]]            
                obj_list2 = obj_dic[obj_dic_keys[j]]
                
                for k in range(len(obj_list1)):
                    for l in range(len(obj_list2)):
                        obj1 = obj_list1[k]
                        obj2 = obj_list2[l]
                        
                        if obj1.get_abs_position() == obj2.get_abs_position() and obj1.get_status() == 'alive' and obj2.get_status() == 'alive':
                            
                            #### for now , combat damage is random int 
                            status1 = obj1.get_combat_status()
                            status2 = obj2.get_combat_status()
                            
                            damage = random.randint(combat_lower_damage, combat_upper_damage)
                            
                            
                            if status1 == 'combat' and status2 == 'combat':                                
                                obj1.set_damage(2*damage)
                                obj2.set_damage(2*damage)
                                
                            elif status1 == 'leave' and status2 == 'combat':
                                obj1.set_damage(1*damage)
                            
                            elif status1 == 'combat' and status2 == 'leave':
                                obj2.set_damage(1*damage)
                                
                            elif status1 == 'leave' and status2 == 'leave':
                                pass
                            else:
                                print('Something went wrong when given combat options , although the system still work ')
                                print('this bug must be fixed')
                            
                            
                            obj_list1[k] = obj1
                            obj_list2[l] = obj2
                        else:
                            pass
        
                obj_dic[obj_dic_keys[i]] = obj_list1
                obj_dic[obj_dic_keys[j]] = obj_list2 
        
        self.obj_dic = obj_dic  

    
    
    def __get_resource(self):
        res_dic = self.res_dic
        res_keys = list(res_dic.keys())
    
        obj_dic_keys = list(self.obj_dic.keys())
        obj_dic = self.obj_dic    
        
        if len(res_keys) == 0:
            pass
        else:
            for i in res_keys:
                res_list = res_dic[i]
                for j in range(len(res_list)):
                    resource = res_list[j]
                                       
                    ### loop over all objs to see if any obj is on the resource                    
                    for k in obj_dic_keys:
                        obj_list = obj_dic[k]
                        for l in range(len(obj_list)):
                            obj = obj_list[l]                            
                            if obj.get_abs_position() == resource.get_position() and resource.get_status() == 'alive' and obj.get_status()=='alive':
                                resource.set_damage(10) ## resources get damaged if something consumed them
                                heal = resource.get_heal()
                                obj.set_heal(heal)
                                obj_list[l] = obj                                  
                        obj_dic[k] = obj_list                                           
                    res_list[j] = resource
                res_dic[i] = res_list
                        
        self.obj_dic = obj_dic
        self.res_dic = res_dic
        
    

    def __reproduction(self):
        obj_dic_keys = list(self.obj_dic.keys())
        obj_dic = self.obj_dic

        for i in obj_dic_keys:
            obj_list = obj_dic[i]
            
            ### in the same list , grab two objects see if they can reproduct ............ lololol
            new_obj_list = []
            for j in range(len(obj_list)):
                for k in range(j+1,len(obj_list)):
                    obj1 = obj_list[j]
                    obj2 = obj_list[k]
                    
                    if obj1.get_abs_position() == obj2.get_abs_position() and (obj1.get_reproduction_status() == 1 and obj2.get_reproduction_status() == 1) and (obj1.get_status() == 'alive' and obj2.get_status() == 'alive'):

                        ### get some damage because of th reproduction
                        ### damage equation ###
                        damage1 = obj1.get_life()*0.1   # reduce 10 percent current health
                        damage2 = obj2.get_life()*0.1
                        
                        obj1.set_damage(damage1)
                        obj2.set_damage(damage2)
                        
                        ### get obj info 
                        position = obj1.get_abs_position()
                        Type = obj1.type
                        life = obj1.init_life
                        visual_range = obj1.visual_range
                        world_x = obj1.world_boundary_x
                        world_y = obj1.world_boundary_y
                        brain_type = obj1.get_brain_type()
                                                
                        ### create new obj
                        new_obj = Creature(Type = Type,life = life,visual_range=visual_range,brain_type = brain_type)
                        new_obj.world_boundary_x = world_x
                        new_obj.world_boundary_y = world_y
                        new_obj.set_position(position=[position[0],position[1]])
                        new_obj.set_index('o'+ str(obj1.index) + '+' + str(obj2.index) + 'o' )
                        
                        new_obj_list.append(new_obj)
            obj_list = [obj_list,new_obj_list]
            obj_list = list(chain.from_iterable(obj_list))
            obj_dic[i] = obj_list 
        self.obj_dic = obj_dic  




        
        
class World_info():
    
    def __init__(self,world = None,obj_dic = None,res_dic = None):
        self.world = World(x_axis = world.x,y_axis = world.y)
        self.obj_dic = obj_dic
        self.res_dic = res_dic
        
        self.vis_world = World(x_axis = world.x,y_axis = world.y)
        
        World_info.__renew_position(self)
        World_info.__renew_vis_position(self)
        
    def renew_world(self):               
        return self.world
    
    def renew_vis_world(self):
        return self.vis_world
    
    def __renew_position(self):
        
        obj_dic = self.obj_dic
        res_dic = self.res_dic
        world   = self.world
        
        obj_keys = obj_dic.keys()
        res_keys = res_dic.keys()
        
                
        for i in obj_keys:
            obj_list = obj_dic[i]
            for j in range(len(obj_list)):
                
                obj = obj_list[j]                
                if obj.get_status()== 'dead':
                    pass
                else:                
                    new_pos = obj.get_position()
                    temp_obj = world.get_object(x = new_pos[0],y = new_pos[1])
                    if type(temp_obj) != int:
                        temp_obj.append(obj.get_type())
                        world.set_object(x = new_pos[0],y = new_pos[1],value = temp_obj)
                    else:
                        container = [obj.get_type()]
                        world.set_object(x = new_pos[0],y = new_pos[1],value = container)    
                        
        
        for i in res_keys:
            res_list = res_dic[i]
   
            for j in range(len(res_list)):
                res = res_list[j]
                if res.status == 'dead':
                    pass
                else:                
                    new_pos = res.position
                    temp_res = world.get_object(x = new_pos[0],y = new_pos[1])
                    if type(temp_res) != int:
                        temp_res.append(res.get_type())
                        world.set_object(x = new_pos[0],y = new_pos[1],value = temp_res) 
                    else:
                        container = [res.get_type()]
                        world.set_object(x = new_pos[0],y = new_pos[1],value = container)               
        self.world = world
                    
    def __renew_vis_position(self): 
        obj_dic = self.obj_dic
        res_dic = self.res_dic
        world   = self.vis_world
        
        obj_keys = obj_dic.keys()
        res_keys = res_dic.keys()
        
                
        for i in obj_keys:
            obj_list = obj_dic[i]
   
            for j in range(len(obj_list)):
                obj = obj_list[j]                
                if obj.get_status() == 'dead':
                    pass
                else:                
                    new_pos = obj.get_position()
                    world.set_object(x = new_pos[0],y = new_pos[1],value = obj.get_type())
                    

        for i in res_keys:
            res_list = res_dic[i]
   
            for j in range(len(res_list)):
                res =res_list[j]
                if res.status == 'dead':
                    pass
                else:                
                    new_pos = res.position
                    world.set_object(x = new_pos[0],y = new_pos[1],value = res.get_type())              
        
        self.vis_world = world
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        