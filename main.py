#importing all required libraries

import math
import pandas as pd
import numpy as np
from geopy.distance import distance
from Levenshtein import distance as string_distance
from sklearn.neighbors import KDTree


#Loading the dataset
df = pd.read_csv("assignment_data.csv")
dataset = np.array(df)

#taking first entry as origin to convert longitude and latitude system to xy grid system
lon1 = df.iloc[0,2]
lat1 = df.iloc[0,1]


#function for converting longitude and latitude to xy grid system
def latlong_to_xy(lon2,lat2):
    dx = ((lon1-lon2)*40000*math.cos((lat1+lat2)*math.pi/360)/360)*1000
    dy = ((lat1-lat2)*40000/360)*1000
    
    return (dx,dy)
    
    
    
# Build a k-d tree of the points
tree = KDTree([latlong_to_xy(point[2],point[1]) for point in dataset])

#adding empty column 'is_simillar'
df['is_simillar'] = 0


for i, point1 in enumerate(dataset):

    # Query the k-d tree for nearby points
    #for query we have taken r = 210 (radius) as there will be small error while converting long-lat to xy grid sysyem
    
    nearby_points = tree.query_radius([latlong_to_xy(point1[2],point1[1])], r=210)
    for j in nearby_points[0]:
    
        if j > i and df.iloc[j,3] == 0:
            #calculating the distance between two points
            dist = distance(dataset[i,1:3],dataset[j,1:3]).meters
            
             #Calculate the string distance between two names
            str_dist = string_distance(point1[0], dataset[j][0])
            
            if str_dist < 5 and dist <= 200 :
                df.iloc[i,3] = 1
                df.iloc[j,3] = 1
                
                
                
#writing to output csv file
df.to_csv('output.csv',sep=',')


