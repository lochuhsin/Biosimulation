import sys
sys.path.append('../')



class World():
    
    def __init__(self,int x_axis,int y_axis):
        
        self.x = x_axis
        self.y = y_axis
        
        
        #### constant attribute
        self.intrinsic_type = 'World'
        
        ####
        
        #### create world
        cdef int i
        cdef int j
        cdef list world = [[0 for i in range(y_axis)]for j in range(x_axis)]
        self.world = world
        
        
    def Area(self):
        
        return self.x*self.y
    
    def get_x_axis(self):
        return self.x
    
    def get_y_axis(self):
        return self.y
    
    
    def get_world(self):
        world = self.world
        return world
    
    def get_object(self,x = None,y = None):        
        world = self.world        
        value = world[x][y]
        
        return value
    
    def set_object(self,x = None,y = None,value = None):  
        self.world[x][y] = value
        