import pandas as pd
import numpy as np
from ast import literal_eval
file = pd.read_csv('Save/obj_track.csv')




vis_map = file[['vis_map']]

vis_map = vis_map.applymap(literal_eval)

a = vis_map.iloc[0]['vis_map']
print(a[0][0])


