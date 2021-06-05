import sys 
sys.path.append('../')
from Object.Object import Creature
from Object.Object import Resource



def Objective_creater(world,object_type,number = None,center = None,life = 100,visual_range = 1,brain_type = None,speed_upper = 1):
    
    if brain_type == None:
        print('no specific brain has been choosen, retarded random brain is on , ohhh yeah its on ~~')
        print('')



    if world.intrinsic_type != 'World':
        print('first input must be world type , second one must be one in the objectives')
        sys.exit()    
        
    if number == None or type(number) != int:
        print('number must be specify in interger')
        sys.exit()
        
    position = [None,None]
    
    if center == None:
        position[0] = 0
        position[1] = 0
        print('initialize center to 0,0')
    else:
        position = center
        
        
                
    ### start to insert objectives
    if number**(0.5)*number**(0.5) == number:
        row_number = int(number**(0.5))
    else:
        row_number = int(number**(0.5)) + 1

    ori_row_index = 0 + position[0]    
    row_index     = 0 + position[0]
    column_index  = 0 + position[1]
    object_position = [None]*number


    for i in range(number):    
        if i%row_number == 0 and i != 0:
            column_index += 1
            row_index = ori_row_index
        if world.get_object(row_index,column_index) != 0:
            print(world.get_object(row_index,column_index))
            print( 'when inserting objects , objects has already occur in this position : ',(row_index,column_index))
            sys.exit()

         
        #### defining object and set initial parameters     
        Objective = Creature(Type = object_type,
                             life = life,
                             visual_range = visual_range,
                             brain_type = brain_type,
                             speed_upper = speed_upper)    
        Objective.set_position(position = [row_index,column_index])
        Objective.world_boundary_x = world.x
        Objective.world_boundary_y = world.y
        Objective.set_index(i)
                
        world.set_object(row_index,column_index,Objective)
        object_position[i] = [row_index,column_index]

               
        row_index += 1


    
    return object_position,world



def Resource_creater(world,object_type,number = None,center = None,life = None,reproduction = None,heal = 50):
    
    if world.intrinsic_type != 'World':
        print('first input must be world type , second one must be one in the objectives')
        sys.exit()    
        
    if number == None or type(number) != int:
        print('number must be specify in interger')
        sys.exit()
        
    position = [None,None]
    
    if center == None:
        position[0] = 0
        position[1] = 0
        print('initialize center to 0,0')
    else:
        position = center
        
        
        
        
    ### start to insert objectives
    if number**(0.5)*number**(0.5) == number:
        row_number = int(number**(0.5))
    else:
        row_number = int(number**(0.5)) + 1
    
    ori_row_index = 0 + position[0]    
    row_index     = 0 + position[0]
    column_index  = 0 + position[1]
    object_position = [None]*number
    

    for i in range(number):  
        if i%row_number == 0 and i != 0:
            column_index += 1
            row_index = ori_row_index
        if world.get_object(row_index,column_index) != 0:
            print(world.get_object(row_index,column_index))
            print( 'when inserting objects , objects has already occur in this position : ',(row_index,column_index))
            sys.exit()
       
        Objective = Resource(Type = object_type,life = life)
                
        Objective.set_position(position = [row_index,column_index])
        Objective.set_heal(heal)
        Objective.world_boundary_x = world.x
        Objective.world_boundary_y = world.y
        Objective.set_index(i)
        world.set_object(row_index,column_index,Objective)
        object_position[i] = [row_index,column_index]

               
        row_index += 1


    
    return object_position,world

