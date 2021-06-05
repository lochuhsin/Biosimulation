import random
from Object.Creature_Brain.Q_Brain import Brain_Q_table_move
#from Object.Creature_Brain.Deep_QBrain import Brain_Q_table_move
class Objective():
    
    def __init__(self,Type):        
        ### constant attribute
        self.intrinsic_type= 'Objective'
        
        ### define basic params
        self.type = Type

        self.world_boundary_x = None
        self.world_boundary_y = None
        
    def Type(self):
        return self.type
        

    
    
    

class Creature(Objective):
    
    def __init__(self,Type,visual_range = 1,life = 3,track = None,brain_type = None,speed_upper = 1):
        super().__init__(Type=Type)
 
        ### define behavior ###
        self.move = ['up','down','left','right']
        self.move_speed = [0,speed_upper]
        
        ### define combat ###        
        self.combat_interaction  = ['combat','leave']        
        self.combat_status = 'leave'

        ### reproduction
        self.reproduction_status = 0
        self.reproduction_interaction = [0,1]
            
        ### define visual range ###
        self.visual_range = visual_range
        self.visual_map   = None       
        
        ### define object life
        self.life = life
        self.init_life = life        
        
        ### position and index , these are intrinsic , and calulate in system , don't touch this variable
        self.position = None
        self.absolute_position = self.position

        self.index    = None        
        self.status    = 'alive'
        self.count     = 0
              
        ### init brain   
        action_dic = {'move_option': self.move,
                      'move_speed' : self.move_speed,
                      'combat_option':self.combat_interaction,
                      'reproduction_option':self.reproduction_interaction} ### just for temp
        self.action_dic = action_dic
        self.Brain = Brain_Q_table_move(action_dic = action_dic,additional_info = visual_range)

        ### brain type
        self.brain_type = brain_type
        
        ### more info
        self.move_decision         = 0
        self.combat_decision       = 0
        self.reproduction_decision = 0
        self.speed_decision        = 0

        
    def process(self):
        Creature.__Brain(self)

            
    def set_damage(self,damage):       
        self.life = self.life - damage
        
    def set_heal(self,heal):
        self.life = self.life + heal

    def set_position(self,position):
        self.position = position
        self.absolute_position = position

    def set_visual_map(self,vis_map):
        self.visual_map = vis_map
    
    def set_combat_signal(self,status):
        self.combat_signal = status

    def set_index(self,index):
        self.index = index
    
    def set_init_life(self,life):
        self.init_life = life
    
    def set_life(self,life):
        self.life = life
        

################### division line ########################

        
    def get_position(self):
        return self.position
    
    def get_life(self):
        return self.life
    
    def get_init_life(self):
        return self.init_life
    
    def get_type(self):
        return self.type
      
    def get_abs_position(self):
        return self.absolute_position
        
    def get_reproduction_status(self):
        return self.reproduction_status
    
    def get_reproduction_interaction(self):
        return self.reproduction_interaction
         
    def get_visual_map(self):
        return self.visual_map
          
    def get_visual_range(self):
        return self.visual_range
            
    def get_combat_status(self):
        return self.combat_status
    
    def get_combat_interaction(self):
        return self.combat_interaction
        
    def get_index(self):
        return self.index
    
    def get_object_time(self):
        return self.count
    
    def get_move_option(self):
        return self.move
    
    def get_status(self):
        return self.status
    
    def get_brain_type(self):
        return self.brain_type
    
    def get_move_decision(self):
        return self.move_decision
    
    def get_combat_decision(self):
        return self.combat_decision
    
    def get_reproduction_decision(self):
        return self.reproduction_decision
    
    def get_speed_decision(self):
        return self.speed_decision
    
                
    def __Brain(self):
        
        '''this function '__Brain' contains the functionality of getting information to the q_brain and recieve '''
        '''the output to make decisions '''
        
        ### get information for outside world
        info_dic = {
                    'Type':self.type,
                    'obj_time':self.count,
                    'life':self.life,
                    'vis_map':self.visual_map,
                    'vis_range':self.visual_range,
                    'abs_position':self.absolute_position,
                    'index':self.index,
                    }
        
        ### make decisions        
        brain_decision = Creature.__Brain_decision(self,info_dic)
        move_decision         = brain_decision['move_decision']
        combat_decision       = brain_decision['combat_decision']
        reproduction_decision = brain_decision['reproduction_decision']
        speed_decision        = brain_decision['speed_decision']  
      

        Creature.__set_combat_status(self,combat_decision)      
        Creature.__set_position(self,decision = move_decision,speed_decision = speed_decision)
        Creature.__life(self)
        Creature.__set_reproduction(self,reproduction_decision)
    
    
    def __Brain_decision(self,brain_info):
        ''' write something here to make decisions , i might make a reinforcement learning in the future '''
        ''' for now , it's just random choice for movement and for combat'''
        
        info = brain_info
        action = self.action_dic
        
        '''True Brain right here'''
        
        #if self.brain_type == 'q-brain':
            #Brain = self.Brain
            #Brain.set_observation(info = info)
            #move_action = Brain.get_action()
            #self.Brain = Brain

        ''' move_decision '''
        move_decision = random.choice(action['move_option'])
        
        ''' speed_decision '''
        speed_decision = random.randint(action['move_speed'][0],action['move_speed'][1])
        
        ''' make combat decision '''
        combat_decision = random.choice(action['combat_option'])
             
        ''' make reproduction decision '''
        reproduction_decision = random.choice(action['reproduction_option'])
        
        decision_dic = {}
        decision_dic['move_decision']         = move_decision
        decision_dic['speed_decision']        = speed_decision
        decision_dic['combat_decision']       = combat_decision
        decision_dic['reproduction_decision'] = reproduction_decision
        
        
        #### get decision info
        self.move_decision         = move_decision
        self.speed_decision        = speed_decision
        self.combat_decision       = combat_decision
        self.reproduction_decision = reproduction_decision
        
        
        
        return decision_dic



    def __life(self):
        
        count = self.count
        if self.life > 0:
            self.life = self.life -1
            count += 1
        else:
            self.status = 'dead'
        self.count = count
        
            
    def __set_position(self,decision,speed_decision):        
        move_speed = speed_decision
               
        if decision == 'up':
            if self.position[0] - move_speed < 0:
                self.position[0] = self.position[0] - move_speed + self.world_boundary_x
            else :           
                self.position[0] = self.position[0] -move_speed
                
        elif decision == 'down':
            if self.position[0] + move_speed >= self.world_boundary_x:
                self.position[0] = self.position[0] +move_speed - self.world_boundary_x
            else:           
                self.position[0] = self.position[0] +move_speed
                
        elif decision == 'left':
            if self.position[1] - move_speed < 0:
                self.position[1] =  self.position[1] - move_speed + self.world_boundary_y
            else:           
                self.position[1] = self.position[1] -move_speed
            
        elif decision == 'right':
            if self.position[1] + move_speed >= self.world_boundary_y:
                self.position[1] =  self.position[1] - move_speed - self.world_boundary_y
            else:           
                self.position[1] = self.position[1] +move_speed   
        else:
            print('error , object stay')
            
        abs_pos = []
        x = 0
        y = 0
        if self.position[0] < 0:
            x = self.world_boundary_x - abs(self.position[0])
        else:
            x = self.position[0]
                        
        if self.position[1] < 0:
            y = self.world_boundary_y - abs(self.position[1])
        else:
            y = self.position[1]
                
        abs_pos = [x,y]      
        self.absolute_position = abs_pos      

    def __set_combat_status(self,combat):
        self.combat_status = combat
    
    def __set_reproduction(self,reproduction):
        self.reproduction_status = reproduction
          
    def __str__(self):       
        return str(self.type)
           
    def __repr__(self):
        return str(self.type)
        
        





    
   
class Resource(Objective):
    
    def __init__(self,Type,size = None,life = 100,reproduction = 2):
        super().__init__(Type=Type)
            
        ### define object life
        self.life = life
        self.init_life = life
        
        ### reproduction
        self.reproduction = reproduction
        self.reproduction_status = False

        ### position and index , these are intrinsic , and calulate in system , don't touch this variable
        self.position = None
        self.index    = None
        self.status    = 'alive'
        self.count     = 0
        
        ### recover 
        self.heal = 50

    def process(self):
        Resource.__life(self)
        
    def set_status(self,status):
        self.status = status
    
    def get_status(self):
        return self.status
    
    def set_position(self,position):
        self.position = position
        
    def get_position(self):
        return self.position
    
    def get_type(self):
        return self.type
              
    def get_reproduction_status(self):
        return self.reproduction_status
    
    def set_index(self,index):
        self.index = index
    
    def get_index(self):
        return self.index
            
    def set_heal(self,value):     
        self.heal = value
        
    def get_heal(self):
        return self.heal
      
    def set_damage(self,value):
        self.life = self.life - value
        if self.life <= 0:
            self.status = 'dead'
    
    def get_init_life(self):
        return self.init_life
    
    def set_life(self,life):
        self.life = life
    
    def __str__(self):        
        return str(self.type)
            
    def __repr__(self):
        return str(self.type)        
                    
    def __life(self):
        
        if self.life < self.init_life and self.status == 'alive':
            self.life = self.life + 1  

    
    
    
    
    
    
    
    
    
    
    
