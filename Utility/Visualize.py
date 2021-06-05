import numpy as np
import matplotlib.pyplot as plt

def World_object_type(world,world_type = 'Numpy'):
    
    if world_type == 'Numpy':
        return np.array(world.get_world())
    else:
        return world.get_world()
    
    
    
    
    
    
    
    
class Vis_world():
    

    
    def __init__(self):
        self.plt = plt
        
        
        
    
    def World_vis(self,world,figsize = [5,5]):

        ### change the color map here
        cmap = self.plt.cm.Pastel1
        
        temp =  np.array(world.get_world())
        norm = self.plt.Normalize(temp.min(), temp.max())
                
        world = cmap(norm(temp))
        
        self.plt.figure(figsize = (figsize[0],figsize[1]))
        self.plt.imshow(world,interpolation=None)
        self.plt.grid(True)
        self.plt.show()
        self.plt.close("all")
        
        


    def Map_vis(self,Map,figsize = [2,2]):
        cmap = self.plt.cm.RdYlBu

        temp =  np.array(Map)
        norm = self.plt.Normalize(temp.min(), temp.max())
        

        
        world = cmap(norm(temp))
        
        self.plt.figure(figsize = (figsize[0],figsize[1]))
        self.plt.imshow(world,interpolation='hamming')
        self.plt.grid(True)
        self.plt.show()
        self.plt.close("all")
                
        
        
    