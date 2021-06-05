from Core.Core import World_Simulator


world = World_Simulator()
world.Create_World(200,200)



world.Add_Objective(amount=200,center=[0,0],Object_type=10,life=1000,visual_range=3,brain_type=None,speed_upper=10)
world.Add_Objective(amount=200,center=[50,50],Object_type=-10,life=1000,visual_range=3,brain_type=None,speed_upper=20)
#world.Add_Resources(amount=1,center=[5,5],Object_type=-40,life=1000,heal = 10)


mode = ['vision','process','combat']
world.Dynamic_mode(mode=mode)


world.Start_simulation(real_time_info = True,simulation_duration = 10,simulation_speed =50,save_data = 'Save/',Round=1)


obj_dic = world.Get_objective_dic()
keys = obj_dic.keys()
for i in keys:
    obj_dic[i] = len(obj_dic[i])
        
print(obj_dic)

