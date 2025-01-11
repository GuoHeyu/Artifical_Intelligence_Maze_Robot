"""my_controller_py controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, DistanceSensor
import numpy as np
import serial
import struct
import time
from controller import Camera
from os import system, name
import os

from PIL import Image
import imageio
from PIL import ImageFile

WHITE=0
GREY=1
RED=2
BLACK=3
N=50*2+5
REFLECT=80.00
DISTANCE=35
TIME_STEP = 64
robot = Robot()
cmd=-1
#initialize moters 
wheels = []
wheelsNames = ["left wheel motor", "right wheel motor"]
for i in range(2):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

#
camera = robot.getDevice("camera")
camera.enable(TIME_STEP )

count=0
state=1
#0 ting
#1 right 2 left 3 forward 4 back

# initialize sensers
rgb_img = camera.getImageArray()
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7','tof'
]

for i in range(9):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)
    

mp=[[0 for i in range(2*N+1)] for j in range(2*N+1)]

def paint_map(color):
    mp=[[color for i in range(2*N+1)] for j in range(2*N+1)]

def paint_square(x,y,color):
    mp[x][y]=color

def paint_point(x,y,color):
    mp[x][y]=color

#将rgb转化为bmp部分
ImageFile.LOAD_TRUNCATED_IMAGES = True

class bmp:
    """ bmp data structure """
 
    def __init__(self, w=1080, h=1920):
        self.w = w
        self.h = h
 
    def calc_data_size (self):
        if ((self.w * 3) % 4 == 0):
            self.dataSize = self.w * 3 * self.h
        else:
            self.dataSize = (((self.w * 3) // 4 + 1) * 4) * self.h
 
        self.fileSize = self.dataSize + 54
 
 
    def conv2byte(self, l, num, len):
        tmp = num
        for i in range(len):
            l.append(tmp & 0x000000ff)
            tmp >>= 8
 
    def gen_bmp_header (self):
        self.calc_data_size();
        self.bmp_header = [0x42, 0x4d]
        self.conv2byte(self.bmp_header, self.fileSize, 4) #file size
        self.conv2byte(self.bmp_header, 0, 2)
        self.conv2byte(self.bmp_header, 0, 2)
        self.conv2byte(self.bmp_header, 54, 4) #rgb data offset
        self.conv2byte(self.bmp_header, 40, 4) #info block size
        self.conv2byte(self.bmp_header, self.w, 4)
        self.conv2byte(self.bmp_header, self.h, 4)
        self.conv2byte(self.bmp_header, 1, 2)
        self.conv2byte(self.bmp_header, 24, 2) #888
        self.conv2byte(self.bmp_header, 0, 4)  #no compression
        self.conv2byte(self.bmp_header, self.dataSize, 4) #rgb data size
        self.conv2byte(self.bmp_header, 0, 4)
        self.conv2byte(self.bmp_header, 0, 4)
        self.conv2byte(self.bmp_header, 0, 4)
        self.conv2byte(self.bmp_header, 0, 4)
 
    def print_bmp_header (self):
        length = len(self.bmp_header)
        for i in range(length):
            print("{:0>2x}".format(self.bmp_header[i]), end=' ')
            if i%16 == 15:
                print('')
        print('')
 
    def paint_bgcolor(self, pixel):
        self.rgbData = []
        self.rgbData += pixel
 
    def save_image(self, name="save.bmp"):
        f = open(name, 'wb')
 
        # write bmp header
        f.write(bytes(self.bmp_header))
 
        # write rgb data
        zeroBytes = self.dataSize // self.h - self.w * 3               #计算图像的每行后面需要的补充0的个数
 
        pixel_array = np.array(self.rgbData).reshape(self.h,self.w*3)  #将像素值list转换成np.array
 
        for r in range(self.h):
            l = []
            for i in range(0,len(pixel_array[r]),3):  #索引图片每行像素
                p = pixel_array[r][i]        # b vaule; 8bit
                l.append(p & 0x00ff)
                p = pixel_array[r][i+1]      # g vaule; 8bit
                l.append(p & 0x00ff)
                p = pixel_array[r][i+2]      # r vaule; 8bit
                l.append(p & 0x00ff)
 
            f.write(bytes(l))                #写入bmp文件中
 
            for i in range(zeroBytes):       #用于每行像素后补0
                f.write(bytes([0x00]))
 
        f.close()
 
 
def convert_img_to_a8rgb565():
    global rgb_img;
    im_bytes = list()
    
    for i in range(0,52):
        for j in range(0,39):
            r = rgb_img[i][j][0]# & 0xF8
            g = rgb_img[i][j][1] #& 0xFC
            b = rgb_img[i][j][2]# & 0xF8
            im_bytes += [b, g, r]    #bmp文件数据位BGR格式
    return im_bytes
 
def convert(picture_path):
    img_width=39
    img_hight=52
    img_bgr = convert_img_to_a8rgb565()   #获取bgr数据,list
    image = bmp(img_width, img_hight)        #创建bmp文件
    image.gen_bmp_header()                   #写入bmp文件头信息#
        #image.print_bmp_header()                #打印出bmp文件头部信息
    image.paint_bgcolor(img_bgr)
    image.save_image('./image/1.bmp')
    print('picture convert over...')
 
def scan(picture_path):
    for filename in os.listdir(picture_path):
        picture = os.path.join(picture_path, filename)
        print(picture)                           #打印文件名称
 
        src_img = Image.open(picture)
        src_img.show()                           #显示图片
 
def main(source_picture_path,convert_picture_path):  #原图路径、转换后的保存路径
    convert(source_picture_path)
    #scan(convert_picture_path)        #预览转换后的bmp图片
 
#rgb to bmp部分结束
#驱动函数

def goforward():
    leftSpeed = 1.0
    rightSpeed = 1.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)

def goback():
    leftSpeed = 1.0
    rightSpeed = 1.0
    wheels[0].setVelocity(-leftSpeed)
    wheels[1].setVelocity(-rightSpeed)  
  
def turnleft():
    leftSpeed = 1.0
    rightSpeed = 1.0
    wheels[0].setVelocity(-leftSpeed)
    wheels[1].setVelocity(rightSpeed)   
  
def turnright():
    leftSpeed = 1.0
    rightSpeed = 1.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(-rightSpeed)    
  
def stop():
    wheels[0].setVelocity(0)
    wheels[1].setVelocity(0)    
  
def right_obstacle():
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    # detect obstacles
    return psValues[1] > REFLECT or psValues[2] > REFLECT

def front_obstacle():
    psValues = []
    for i in range(9):
        psValues.append(ps[i].getValue())

    # detect obstacles
    return psValues[0] > REFLECT or psValues[7] > REFLECT or psValues[8]<DISTANCE
def catchaimage():
    value=ps[8].getValue()
    return value<100
def left_obstacle():
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    # detect obstacles
    
    return psValues[5] > REFLECT or psValues[6] > REFLECT 

def back_obstacle():
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    # detect obstacles
    return psValues[3] > REFLECT or psValues[4] > REFLECT


def turn_right():
    state=1
    count=0
    while(robot.step(TIME_STEP) != -1):
        count+=1
        if count<36:
            turnright()
        else:
            stop()
            count=0
            state=0
            break
def turn_left():
    state=2
    count=0
    while(robot.step(TIME_STEP) != -1):
        count+=1
        if count<36:
            turnleft()
        else:
            stop()
            count=0
            state=0
            break



def go_forward():
    global rgb_img
    state=3
    count=0
    flag=1
    while(robot.step(TIME_STEP) != -1):
        if(flag==1 and catchaimage()):
            rgb_img=camera.getImageArray()
            convert('./image')
            #print(rgb_img)
            flag=0
        count+=1
        if count<76:
            goforward()
        else:
            stop()
            count=0
            state=0
            break
    if(not flag):
        os.system('image\\rot.exe')
        os.system("python classify.py")
        f=open("tmp.txt","r")
        cmd=f.read()
        print(cmd[2])
        if(cmd[2]=='2'):
            turn_left()
        if(cmd[2]=='3'):
            turn_right()
        if(cmd[2]=='1'):
            stop()
            turn_left()
            turn_left()
        f.close()
        """if(front_obstacle()):
            stop()
            count=0
            state=0
            break"""
        #print ('r='+str(red)+'g='+str(green)+' b='+str(blue))
    # display the components of each pixel
        """for x in range(0,camera.getWidth()):
            for y in range(0,camera.getHeight()):
                rgb_img[x][y][0]   = rgb_image[x][y][0]
                rgb_img[x][y][1]= rgb_image[x][y][1]
                rgb_img[x][y][2] = rgb_image[x][y][2]
            #print ('r='+str(red)+'g='+str(green)+' b='+str(blue))
         """   
        
    
def go_back():
    state=4
    count=0
    while(robot.step(TIME_STEP) != -1):
        count+=1
        if count<76:
            goback()
        else:
            stop()
            count=0
            state=0
            break
        """if(back_obstacle()):
            stop()
            count=0
            state=0
            break"""

 #以上是小车部分
 #下面是算法
 
dx=[-1,0,1,0]
dy=[0,1,0,-1]

class status(object):
	def __init__(self,_x,_y,_dir):
		self.x=_x
		self.y=_y
		self.dir=_dir
	def left(self):
		_dir=(3 if self.dir==0 else self.dir-1)
		return status(self.x+dx[_dir],self.y+dy[_dir],_dir)
	def front(self):
		_dir=self.dir
		return status(self.x+dx[_dir],self.y+dy[_dir],_dir)
	def right(self):
		_dir=(0 if self.dir==3 else self.dir+1)
		return status(self.x+dx[_dir],self.y+dy[_dir],_dir)
	def back(self):
		_dir=(self.dir^2)
		return status(self.x+dx[_dir],self.y+dy[_dir],self.dir)

	def __eq__(self,other):
		return self.x==other.x and self.y==other.y and self.dir==other.dir


N=50*2+5
obs=np.zeros((N*2,N*2),dtype=int)
vis=np.zeros((N*2,N*2),dtype=int)
path=[]

def check_left(nw):
	t=nw.left()
	if (obs[t.x][t.y]==-1):
		obs[t.x][t.y]=left_obstacle()
	paint_square(t.x,t.y,RED if obs[t.x][t.y]==1 else WHITE)
	if (obs[t.x][t.y]==1):
		return 0
	t=t.front()
	if (vis[t.x][t.y]):
		return 0
	vis[t.x][t.y]=1
	
	turn_left()
	go_forward()
	paint_point(nw.x,nw.y,WHITE)
	paint_point(t.x,t.y,GREY)
	path.append(t)
	return 1

def check_front(nw):
	t=nw.front()
	if (obs[t.x][t.y]==-1):
		obs[t.x][t.y]=front_obstacle()
	paint_square(t.x,t.y,RED if obs[t.x][t.y]==1 else WHITE)
	if (obs[t.x][t.y]==1):
		return 0
	t=t.front()
	if (vis[t.x][t.y]):
		return 0
	vis[t.x][t.y]=1
	go_forward()
	paint_point(nw.x,nw.y,WHITE)
	paint_point(t.x,t.y,GREY)
	path.append(t)
	return 1

def check_right(nw):
	t=nw.right()
	print("right:",right_obstacle())
	if (obs[t.x][t.y]==-1):
		obs[t.x][t.y]=right_obstacle()
	paint_square(t.x,t.y,RED if obs[t.x][t.y]==1 else WHITE)
	if (obs[t.x][t.y]==1):
		return 0
	t=t.front()
	if (vis[t.x][t.y]):
		return 0
	vis[t.x][t.y]=1
	turn_right()
	go_forward()
	paint_point(nw.x,nw.y,WHITE)
	paint_point(t.x,t.y,GREY)
	path.append(t)
	return 1

paint_map(BLACK)
paint_square(N,N,WHITE)
paint_point(N,N,GREY)
for i in range(N*2):
	for j in range(N*2):
		obs[i][j]=-1
for i in range(0,N*2,2):
	for j in range(0,N*2,2):
		paint_square(i,j,RED)
		obs[i][j]=1
for i in range(1,N*2,2):
	for j in range(1,N*2,2):
		paint_square(i,j,WHITE)
		obs[i][j]=0
vis[N][N]=1
path.append(status(N,N,1))


def get_shortest_dis(x,y,tx,ty,OBS):
	la=np.zeros((N*2,N*2),dtype=int)
	dis=np.zeros((N*2,N*2),dtype=int)
	dis[x][y]=1
	la[x][y],la[tx][ty]=-1,-1
	que=[]
	que.append([x,y])
	fir=0
	while (fir<len(que)):
		x,y=que[fir]
		fir+=1
		if (x==tx and y==ty):
			break
		for d in range(4):
			xx,yy=x+dx[d],y+dy[d]
			if (xx>=N*2 or yy>=N*2 or xx<0 or yy<0):
				continue
			if (OBS[xx][yy]==1 or dis[xx][yy]):
				continue
			dis[xx][yy]=dis[x][y]+1
			if (la[x][y]==-1):
				la[xx][yy]=d
			else:
				la[xx][yy]=la[x][y]
			que.append([xx,yy])
	return la[tx][ty]

def get_shortest_dis_2(x,y,tx,ty,OBS):
	la=np.zeros((N*2,N*2),dtype=int)
	dis=np.zeros((N*2,N*2),dtype=int)
	dis[x][y]=1
	la[x][y],la[tx][ty]=-1,-1
	que=[]
	que.append([x,y])
	fir=0
	while (fir<len(que)):
		x,y=que[fir]
		fir+=1
		if (x==tx and y==ty):
			break
		for d in range(4):
			xx,yy=x+dx[d],y+dy[d]
			if (xx>=N*2 or yy>=N*2 or xx<0 or yy<0):
				continue
			if (OBS[xx][yy]==1 or dis[xx][yy]):
				continue
			dis[xx][yy]=dis[x][y]+1
			if (la[x][y]==-1):
				la[xx][yy]=d
			else:
				la[xx][yy]=la[x][y]
			que.append([xx,yy])
	return dis[tx][ty]


#now_status输入当前状态（变量种类为status），nn为迷宫大小
#如果已经在终点了则不动，否则往终点按决策走一步，然后返回的是一个status
def Floodfill_choice(now_status,nn):
	tx=N+(nn-1)*2
	ty=N+(nn-1)*2
	if (now_status.x==tx and now_status.y==ty):
		return now_status
	
	che_status=now_status.front()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=front_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.left()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=left_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.back()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=back_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.right()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=right_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	obss=obs.copy()
	for i in range(0,N*2):
		for j in range(0,N*2):
			if (obss[i][j]==-1):
				obss[i][j]=0
	for i in range(N-1,tx+2):
		obss[N-1][i],obss[tx+1][i],obss[i][tx+1],obss[i][N-1]=1,1,1,1
	d=get_shortest_dis(now_status.x,now_status.y,tx,ty,obss)
	assert(d!=-1)
	paint_point(now_status.x,now_status.y,WHITE)
	Tx,Ty=now_status.x+dx[d],now_status.y+dy[d]
	che_status=now_status.right()
	if (che_status.x==Tx and che_status.y==Ty):
		che_status=che_status.front()
		paint_point(che_status.x,che_status.y,GREY)
		turn_right()
		
		go_forward()
	else:
		che_status=now_status.front()
		while (che_status.x!=Tx or che_status.y!=Ty):
			turn_left()
			
			now_status.dir=(3 if now_status.dir==0 else now_status.dir-1)
			che_status=now_status.front()
		che_status=che_status.front()
		paint_point(che_status.x,che_status.y,GREY)
		go_forward()
	return che_status

import random
#大体同上
#新增参数times与alpha。其中times表示随机次数，是正整数；alpha表示某个障碍存在的概率，为0到1之间的实数（最好在0.1~0.9之间）。
def Monte_Carlo_choice(now_status,nn,times,alpha):
	tx=N+(nn-1)*2
	ty=N+(nn-1)*2
	if (now_status.x==tx and now_status.y==ty):
		return now_status
	che_status=now_status.front()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=front_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.left()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=left_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.back()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=back_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.right()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=right_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	vote=[0,0,0,0]
	for time in range(times):
		lis=[]
		obss=obs.copy()
		for i in range(N-1,tx+2):
			obss[N-1][i],obss[tx+1][i],obss[i][tx+1],obss[i][N-1]=1,1,1,1
		for i in range(N-1,tx+2):
			for j in range(N-1,ty+2):
				if (obss[i][j]==-1):
					lis.append([i,j])
					obss[i][j]=0
		random.shuffle(lis)
		for x,y in lis:
			if (random.random()>alpha):
				continue
			obss[x][y]=1
			if (get_shortest_dis(now_status.x,now_status.y,tx,ty,obss)==-1):
				obss[x][y]=0
		vote[get_shortest_dis(now_status.x,now_status.y,tx,ty,obss)]+=1
	d=0
	for i in range(1,4):
		if (vote[i]>vote[d]):
			d=i
	paint_point(now_status.x,now_status.y,WHITE)
	Tx,Ty=now_status.x+dx[d],now_status.y+dy[d]
	che_status=now_status.right()
	if (che_status.x==Tx and che_status.y==Ty):
		che_status=che_status.front()
		paint_point(che_status.x,che_status.y,GREY)
		turn_right()
		go_forward()
	else:
		che_status=now_status.front()
		while (che_status.x!=Tx or che_status.y!=Ty):
			turn_left()
			now_status.dir=(3 if now_status.dir==0 else now_status.dir-1)
			che_status=now_status.front()
		che_status=che_status.front()
		paint_point(che_status.x,che_status.y,GREY)
		go_forward()
	return che_status


def get_abs(x):
	return (-x if x<0 else x)

def Monte_Carlo_2_choice(now_status,nn,times,alpha):
	tx=N+(nn-1)*2
	ty=N+(nn-1)*2
	if (now_status.x==tx and now_status.y==ty):
		return now_status
	che_status=now_status.front()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=front_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.left()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=left_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.back()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=back_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	che_status=now_status.right()
	if (obs[che_status.x][che_status.y]==-1):
		obs[che_status.x][che_status.y]=right_obstacle()
	paint_square(che_status.x,che_status.y,RED if obs[che_status.x][che_status.y]==1 else WHITE)
	vote=[0,0,0,0]
	for time in range(times):
		lis=[]
		obss=obs.copy()
		for i in range(N-1,tx+2):
			obss[N-1][i],obss[tx+1][i],obss[i][tx+1],obss[i][N-1]=1,1,1,1
		for i in range(N-1,tx+2):
			for j in range(N-1,ty+2):
				if (obss[i][j]==-1):
					lis.append([i,j])
					obss[i][j]=0
		random.shuffle(lis)
		for x,y in lis:
			if (random.random()>alpha):
				continue
			if (get_abs(x-now_status.x)+get_abs(y-now_status.y)==1):
				continue
			obss[x][y]=1
			if (get_shortest_dis(now_status.x,now_status.y,tx,ty,obss)==-1):
				obss[x][y]=0
		for kk in range(4):
			che_status=now_status.front()
			if (obss[che_status.x][che_status.y]==1):
				vote[now_status.dir]+=1000000
			else:
				vote[now_status.dir]+=get_shortest_dis_2(che_status.x,che_status.y,tx,ty,obss)
			now_status.dir=(3 if now_status.dir==0 else now_status.dir-1)
	d=0
	for i in range(1,4):
		if (vote[i]<vote[d]):
			d=i
	paint_point(now_status.x,now_status.y,WHITE)
	Tx,Ty=now_status.x+dx[d],now_status.y+dy[d]
	che_status=now_status.right()
	if (che_status.x==Tx and che_status.y==Ty):
		che_status=che_status.front()
		paint_point(che_status.x,che_status.y,GREY)
		turn_right()
		go_forward()
	else:
		che_status=now_status.front()
		while (che_status.x!=Tx or che_status.y!=Ty):
			turn_left()
			now_status.dir=(3 if now_status.dir==0 else now_status.dir-1)
			che_status=now_status.front()
		che_status=che_status.front()
		paint_point(che_status.x,che_status.y,GREY)
		go_forward()
	return che_status
nw=status(N,N,1)
while True:
      nw=Floodfill_choice(nw,10)
      #nw=Monte_Carlo_2_choice(nw,10,10,0.6)
      """
	nw=path[-1]
	if (not check_left(nw)):
		if (not check_front(nw)):
			if (not check_right(nw)):
				path.pop()
				if (not path):
					break
				t=path[-1]
				nw=nw.back()
				go_back()
				if (nw==t.left()):
					turn_right()
				elif (nw==t.right()):
					turn_left()
				else:
					assert nw==t.front()
				paint_point(nw.x,nw.y,WHITE)
				paint_point(t.x,t.y,GREY)
"""
#以上为算法


#以下为原始主while
#go_forward()
#go_back()

"""
while robot.step(TIME_STEP) != -1:
   # print(state)
    if state==0:
        stop()
    if state==1:
        count+=1
        if count<35:
            turnright()
        if count>=35:
            stop()
            count=0
            state=0
        continue
    if state==2:
        count+=1
        if count<35:
            turnleft()
        if count>=35:
            stop()
            count=0
            state=0
        continue
    if state==3:
        goforward()
    if state==4:
        goback()
"""