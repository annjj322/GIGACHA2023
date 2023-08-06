import numpy as np
import matplotlib.pyplot as plt
from planner.sub_function.cubic_spline_planner import *
import threading
import json
from numpy import arctan2
from shared.path import Path

# msg (marker1 -> inner points, marker2 -> outer points)

class NarrowDriving():
    def __init__(self,sh,eg, pc):
        super().__init__()
        self.shared = sh
        self.ego = eg
        self.perception = pc
        self.global_path = self.shared.global_path

        self.inner_cone = []
        self.outer_cone = []
        self.inner_path = []
        self.outer_path = []
        self.map_flag = True        
        self.global_path_tmp = Path()

        self.left_cones = np.array([self.perception.left_x,self.perception.left_y])
        self.right_cones = np.array([self.perception.right_x,self.perception.right_y])
        self.left_path = []
        self.right_path = []
        self.local_path = self.shared.local_path
        self.old_position = []

        self.ds = 0.1
        self.length = 0.9

        self.dir = "/home/gigacha/TEAM-GIGACHA/src/semi_pkg/scripts/maps/"
        self.map_name = "narrow"
        self.maptxt = "tmp.txt"
        self.data = {}

    def run(self): 
      
        # local path planning
        if self.perception.local2global == False: # map 형성 x
            print('local path planning')
            # if self.left_cones[0] != self.perception.left_x or self.right_cones[0] != self.perception.right_x:

            self.left_cones = np.array([self.perception.left_x,self.perception.left_y])
            self.right_cones = np.array([self.perception.right_x,self.perception.right_y])
        
            if self.old_position != self.perception.left_x:
                self.local_path.x = []
                self.local_path.y = []
    
                # 후보군 1 한 경로를 기준으로 Wall Following
                left_cone_path = calc_spline_course(self.perception.left_x,self.perception.left_y,self.ds)
                right_cone_path = calc_spline_course(self.perception.right_x,self.perception.right_y,self.ds)
                self.left_path, self.right_path = self.path_maker(np.array([left_cone_path[0],left_cone_path[1]]),np.array([right_cone_path[0],right_cone_path[1]]))
                
                if len(self.left_path[0]) > len(self.right_path):
                    for i in range(len(self.left_path[0])):
                        self.local_path.x.append(self.left_path[0][i])
                        self.local_path.y.append(self.left_path[1][i])
                else:
                    for i in range(len(self.right_path[0])):
                        self.local_path.x.append(self.right_path[0][i])
                        self.local_path.y.append(self.right_path[1][i])

                self.old_position = self.perception.left_x     
            
                
        # global path planning
        else:
            if self.map_flag: 
                print('global map making')
                # path 생성
                self.inner_cone = np.array([self.perception.inner_x,self.perception.inner_y])
                self.outer_cone = np.array([self.perception.outer_x,self.perception.outer_y])
                self.cone_path()
                self.inner_path, self.outer_path = self.path_maker(self.inner_cone,self.outer_cone)
                for i in range(len(self.inner_path[0])):
                    self.data[i] = [self.inner_path[0][i],self.inner_path[1][i],"narrow_driving"]
                with open(self.dir+self.map_name+'_inner.json','w') as outfile:
                    json.dump(self.data, outfile, indent=4)
                
                for i in range(len(self.outer_path[0])):
                    self.data[i] = [self.outer_path[0][i],self.outer_path[1][i],"narrow_driving"]
                with open(self.dir + self.map_name + '_outer.json', 'w') as outfile:
                    json.dump(self.data, outfile, indent=4)
                self.read_global_path() # read global path에 대한 모듈이 생기면 inner와 outer 모두 생성
                # read global path는 아직 완료되지 않은 task
                self.map_flag = False

                ### global path 읽는 모듈 만들기 전까지 사용할 임시 코드 ###
                _tmp_y1 = []
                _tmp_x1 = []
                for i in range(len(self.inner_path[0])):
                    _tmp_x1.append(self.inner_path[0][i])
                    _tmp_y1.append(self.inner_path[1][i])
                    
                _tmp_y2 = []
                _tmp_x2 = []
                for i in range(len(self.outer_path[0])):
                    _tmp_x2.append(self.outer_path[0][i])
                    _tmp_y2.append(self.outer_path[1][i])

                self.left_path = np.array([_tmp_x1,_tmp_y1])
                self.right_path = np.array([_tmp_x2,_tmp_y2])
             
            else:
                print('global path planning')
                target_index = self.ego.index + 10
                target_position = np.array([self.global_path.x[target_index],self.global_path.y[target_index]])
                ego_position = np.array([self.ego.info.x,self.ego.info.y])

                if -15 < arctan2(ego_position-target_position) < 15:
                    pass
                elif arctan2(ego_position-target_position) > 15:
                    self.global_path.x = self.left_path[0]
                    self.global_path.y = self.left_path[1]                    
                elif arctan2(ego_position-target_position) < -15:
                    self.global_path.x = self.right_path[0]
                    self.global_path.y = self.right_path[1]

    ###################### global path planning method ##############################

    def read_global_path(self): # read global path 를 전부 복사해 오는 방식을 사용하거나 모듈로 만들어서 따로 사용할 수 있도록 해야됨.
        with open(f"maps/narrow.json", 'r') as json_file:
            json_data = json.load(json_file)
            for n, (x, y, mission) in enumerate(json_data.values()):
                self.global_path.x.append(x)
                self.global_path.y.append(y)
                self.global_path.mission.append(mission)

    def cone_path(self): # interpolate inner or outer cone path
        '''
        slam을 통해서 marker를 받아온 상황에서 cone path를 생성하는 함수
        1. msg 대신 
        '''
        _x = self.inner_cone[0]
        _y = self.inner_cone[1]
        path = calc_spline_course(_x,_y,self.ds)
        self.inner_cone = np.array([path[0],path[1]])

        _x = self.outer_cone[0]
        _y = self.outer_cone[1]
        path = calc_spline_course(_x,_y,self.ds)
        self.outer_cone = np.array([path[0],path[1]])
    
    def point2vec(self,point1,point2):
        unit_vec = (point2-point1)/np.linalg.norm(point2-point1)
        _angle = np.arctan2(unit_vec[1],unit_vec[0])
        angle = _angle + np.pi/2
        normal_vec = np.array([np.cos(angle),np.sin(angle)])
        return normal_vec

    def path_maker(self,inner=None,outer = None):
        _inner_path_x = []
        _inner_path_y = []
        _outer_path_x = []
        _outer_path_y = []
        for i in range(len(inner[0])-1):
            _tmp = self.point2vec(np.array([inner[0][i],inner[1][i]]),np.array([inner[0][i+1],inner[1][i+1]]))
            _inner_path_x.append(inner[0][i] - _tmp[0]*self.length)
            _inner_path_y.append(inner[1][i] - _tmp[1]*self.length)

        
        for i in range(len(outer[0])-1):
            _tmp = self.point2vec(np.array([outer[0][i],outer[1][i]]),np.array([outer[0][i+1],outer[1][i+1]]))
            _outer_path_x.append(outer[0][i] + _tmp[0]*self.length)
            _outer_path_y.append(outer[1][i] + _tmp[1]*self.length)
            # _tmp = self.point2vec(outer[i],outer[i+1])
            # self.outer_path.append(outer[i] + _tmp*self.length)

        return np.array([_inner_path_x, _inner_path_y]), np.array([_outer_path_x,_outer_path_y])
    
        # self.inner_path = np.array([_inner_path_x,_inner_path_y])
        # self.outer_path = np.array([_outer_path_x,_outer_path_y])