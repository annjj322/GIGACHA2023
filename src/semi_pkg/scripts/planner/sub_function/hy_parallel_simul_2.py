from math import atan2, cos, sin, hypot,asin,sqrt,tan
from matplotlib import pyplot as plt
import numpy as np
from cubic_spline_planner import main
import json
global_path_x=[]
global_path_y=[]


# ############global_path 불러 오는 곳 ##########################        
# with open("C:/Users/son46/Desktop/parking/semi_map.json", 'r') as json_file:
#     json_data = json.load(json_file)
#     for n, (x, y, mission, map_speed) in enumerate(json_data.values()):
#         if 3600<n<3684:    
#             global_path_x.append(x)
#             global_path_y.append(y)

# # # songdo             
# with open("C:/Users/son46/Desktop/parking/spring_reverse_parking.json", 'r') as json_file:
#     json_data = json.load(json_file)
#     for n, (x, y, mission, map_speed) in enumerate(json_data.values()):
#         if 700<n<760:    
#             global_path_x.append(x)
#             global_path_y.append(y)
# ########################################################################

def make_yegak(angle):
    if abs(np.degrees(angle))>90:
        angle=np.pi-abs(angle)
        angle=angle%360
    else:
        angle=abs(angle)
        angle=angle%360
    return angle
#kcity
# a=[[74.83,83.24],[72.46,78.80],[72.46,84.53],[69.95,80.28]] # 1 3 
#                                                               # 0 2
# me=[73.87533165963201,
#         75.70141785451007]
a=[[72.46,78.80],[74.83,83.24]]
me=[74.19476148398357,
        76.32292212859726] #leg, reg 
# songdo
# a=[[12.8, 17.00],[16.06, 19.24]] # 임시로 딴 점 
# a=[[9.6473, 11.075],[12.844, 15.1823]]
# me=[11.042374185806736,
#         6.900586569022501]
# me = [11.347067507905024,
#         7.297023171102467] # 750 멈출 때 index + 20 

ax=[]#주차칸 만들 때 쓰는 리스트입니다. 
ay=[]
#################################################################
p0=a[1]#[74.83,83.24] #reg
p1=a[0]#[72.46,78.88] #leg 
m2=atan2((a[0][1]-a[1][1]),(a[0][0]-a[1][0])) # 세로가 이루는 예각
m2=make_yegak(m2)
m=atan2(-(a[0][0]-a[1][0]),(a[0][1]-a[1][1])) #가로가 이루는 둔각 
if np.degrees(m)<0:
    m+=np.pi
    m=m%360   
#################################################################
print('m',np.degrees(m))
print('m2',np.degrees(m2))
print('ww',np.degrees(m2+0.5*np.pi))
print(np.degrees(2.069))
#################################################################
#우회전 , 좌회전 x에대해서 2.736, 2.175
#우회전 , 좌회전 y에대해서 2.736, 2.195
r2=2.8# reg점 근처 원의 반지름 
garo=2.914 
sero=5.03
x1=[]
y1=[]
x=[]
y=[]
'''
 p0=reg
 p1=leg
'''
       ####
        #   g a  r  o
        # s           s
        # e           e
        # r           r
        # o           o
        #     g a r o 
#######주차칸 plot을 위한 안쪽 점 까지 구하기 ##########3
p2x=p1[0] + garo * cos(m) # 2번점 구하기
p2y=p1[1] + garo * sin(m)
a.append([p2x,p2y])
p3x=p0[0] + garo * cos(m) # 3번점 구하기 
p3y=p0[1] + garo * sin(m)
a.append([p3x,p3y])
##################################

###################네모박스 생성기###########3
mmm1=[(a[0][0]+a[2][0])*0.5, (a[0][1]+a[2][1])*0.5]
mmm2=[(a[1][0]+a[3][0])*0.5,(a[1][1]+a[3][1])*0.5]
mdx=[mmm1[0],mmm2[0]]
mdy=[mmm1[1],mmm2[1]]
mx,my=main(mdx,mdy)
ax1,ay1=main((a[0][0],a[2][0]),[a[0][1],a[2][1]])
ax2,ay2=main((a[2][0],a[3][0]),[a[2][1],a[3][1]])
ax3,ay3=main((a[3][0],a[1][0]),[a[3][1],a[1][1]])
ax,ay= (ax1+ax2+ax3), (ay1+ay2+ay3)
############################################
r=2.8
##########파라미터 조정공간 ##################
n11a=0.6#reg 점에서 가로 방향으로 중심을 옮김
n11b=0.5#0.6#0.9#1.2 #reg 점에서 세로 방향으로 중심을 옮김
############################################

############################################
n1x=p0[0] - n11a*cos(m) - n11b * cos(m2) # reg점에서  
n1y=p0[1] - n11a*sin(m) - n11b * sin(m2)
#####################################
min_r=2.8
d=1
d99=sqrt(min_r**2+d**2)
inc=atan2(d,min_r)
inc=make_yegak(inc)
inc*=2
##########점 사이를 0.1로 만들기 위한####
n1=int((np.pi/(asin(1/(20*r)))))
n2=int((np.pi/(asin(1/(20*r2)))))
###################################
d52=hypot((me[0]-n1x),(me[1]-n1y))
d100=sqrt(d52**2-r2**2)
print('d100',d100)
inc2=asin(r2/d52)
inc2=make_yegak(inc2)
print('inc2',np.degrees(inc2))
########################################## 
inc3=atan2((n1y-me[1]),(n1x-me[0]))  
inc3=make_yegak(inc3) 
print('inc3',np.degrees(inc3))
##############################
tot_inc=inc2+inc3
print('tot',np.degrees(tot_inc))
tmp_x=me[0] - 1 * cos(np.pi-tot_inc)
tmp_y=me[1] + 1 * sin(np.pi-tot_inc)
#############################
inter_x=me[0] - d100 * cos(np.pi-tot_inc)
inter_y=me[1] + d100 * sin(np.pi-tot_inc)

tmtm=atan2(-1,tan(tot_inc))
tmtm=make_yegak(tmtm)
tmtm+=np.pi
print('tmm',np.degrees(tmtm))
#################고정#####################
for j in range(n2): #reg 점 근처
   if m<=j*2*np.pi/n2<=tmtm:
        x.append(n1x+r2*cos(j*2*np.pi/n2)) 
        y.append(n1y+r2*sin(j*2*np.pi/n2))    
########################################
##########평행이동만######################
n2x=me[0]- 1 * cos(m2) - r * cos(0.5*np.pi - m2)#p1[0] - n1a*cos(m) - n1b * cos(m2) #leg점에서
n2y=me[1]- 1 * sin(m2) + r * sin(0.5*np.pi - m2)#p1[1] - n1a*sin(m) - n1b * sin(m2)

for i in range(n1): #leg 모서리     
    if 0<=(i*2*np.pi/n1)<=inc: 
        x1.append(n2x + r*cos(i*2*np.pi/n1-(np.pi-abs(m))))
        y1.append(n2y + r*sin(i*2*np.pi/n1-(np.pi-abs(m))))
############################################
x=x[::-1]
y=y[::-1]
# tmpp_x,tmpp_y=main((tmp_x,inter_x),(tmp_y,inter_y))
tmpp_x,tmpp_y=main((x1[-1],inter_x),(y1[-1],inter_y))
forward_x,forward_y=main((me[0]- 1 * cos(m2),me[0]- 2 * cos(m2)),(me[1] - 1 * sin(m2) ,me[1]- 2 * sin(m2)))
final_x= forward_x + x1 + tmpp_x + x 
final_y= forward_y + y1 + tmpp_y + y 
f_x=[]
f_y=[]


plt.plot(x1,y1)
plt.plot(global_path_x,global_path_y)
plt.scatter(me[0],me[1])
plt.scatter(n1x,n1y)
plt.scatter(n2x,n2y)
plt.plot(ax,ay)
plt.plot(mx,my)
plt.plot(final_x,final_y)
plt.scatter(tmp_x,tmp_y)
plt.axis('square')
plt.grid()
plt.show()