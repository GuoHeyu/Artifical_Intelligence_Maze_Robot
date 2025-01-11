"""my_controller_py controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from unifr_api_epuck import wrapper
import numpy as np

WHITE = 0
GREY = 1
RED = 2
BLACK = 3
N = 50 * 2 + 5
REFLECT = 80

TIME_STEP = 64


def initial(r):
    r.init_sensors()
    r.init_camera('C:\\Users\\Administrator\\PycharmProjects\\AIIRwifi\\image')
    print(r.get_battery_level())


ip_addr = '192.168.6.11'
robot = wrapper.get_robot(ip_addr)
initial(robot)

#

state = 1
# 0 ting
# 1 right 2 left 3 forward 4 back

# initialize sensors


mp = [[0 for i in range(2 * N + 1)] for j in range(2 * N + 1)]


def paint_map(color):
    mp = [[color for i in range(2 * N + 1)] for j in range(2 * N + 1)]


def paint_square(x, y, color):
    mp[x][y] = color


def paint_point(x, y, color):
    mp[x][y] = color


# 驱动函数


def goforward(velocity=7):
    leftSpeed = velocity
    rightSpeed = velocity
    robot.set_speed(velocity, velocity)
    robot.sleep(1)
    # print('go forward')


def goback(velocity=7):
    leftSpeed = -velocity
    rightSpeed = -velocity
    robot.set_speed(-velocity, -velocity)
    robot.sleep(1)
    # print('go back')


def turnback():
    leftSpeed = -5.5
    rightSpeed = 5.5
    robot.set_speed(leftSpeed, rightSpeed)
    robot.sleep(1)
    # print('turn left')


def turnright():
    leftSpeed = 5.5
    rightSpeed = -5.5
    robot.set_speed(leftSpeed, rightSpeed)
    robot.sleep(0.5)
    # print('turn right')


def turnleft():
    leftSpeed = -5.5
    rightSpeed = 5.5
    robot.set_speed(leftSpeed, rightSpeed)
    robot.sleep(0.5)
    # print('turn left')


def stop():
    robot.set_speed(0, 0)


def right_obstacle():
    turnright()
    distance = robot.get_tof() / 10.0
    # print('right distance', distance)
    return distance < 2.5


def front_obstacle():
    distance = robot.get_tof() / 10.0
    # print('front distance', distance)
    return distance < 2.5


def left_obstacle():
    turnleft()
    distance = robot.get_tof() / 10.0
    # print('left distance', distance)
    return distance < 2.5


def back_obstacle():
    turnback()
    distance = robot.get_tof() / 10.0
    turnback()
    # print('back distance', distance)
    return distance < 2.5


def go_forward():
    state = 3
    if front_obstacle():
        stop()
        turnback()
        state = 0
    else:
        goforward()
        state = 0


def go_back():
    state = 4
    if back_obstacle():
        stop()
        state = 0
    else:
        goback()
        state = 0


# 以上是小车部分
# 下面是算法

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


class status(object):
    def __init__(self, _x, _y, _dir):
        self.x = _x
        self.y = _y
        self.dir = _dir

    def left(self):
        _dir = (3 if self.dir == 0 else self.dir - 1)
        return status(self.x + dx[_dir], self.y + dy[_dir], _dir)

    def front(self):
        _dir = self.dir
        return status(self.x + dx[_dir], self.y + dy[_dir], _dir)

    def right(self):
        _dir = (0 if self.dir == 3 else self.dir + 1)
        return status(self.x + dx[_dir], self.y + dy[_dir], _dir)

    def back(self):
        _dir = (self.dir ^ 2)
        return status(self.x + dx[_dir], self.y + dy[_dir], self.dir)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.dir == other.dir


obs = np.zeros((N * 2, N * 2), dtype=int)
vis = np.zeros((N * 2, N * 2), dtype=int)
path = []


def check_left(nw):
    # print('check left')
    t = nw.left()
    if obs[t.x][t.y] == -1:
        obs[t.x][t.y] = left_obstacle()
        # print('left obstacle', obs[t.x][t.y])
    paint_square(t.x, t.y, RED if obs[t.x][t.y] == 1 else WHITE)
    if obs[t.x][t.y] == 1:
        turnright()
        return 0
    t = t.front()
    if vis[t.x][t.y]:
        turnright()
        return 0
    vis[t.x][t.y] = 1
    go_forward()
    paint_point(nw.x, nw.y, WHITE)
    paint_point(t.x, t.y, GREY)
    path.append(t)
    return 1


def check_front(nw):
    # print('check front')
    t = nw.front()
    if obs[t.x][t.y] == -1:
        obs[t.x][t.y] = front_obstacle()
        # print('front obstacle', obs[t.x][t.y])
    paint_square(t.x, t.y, RED if obs[t.x][t.y] == 1 else WHITE)
    if obs[t.x][t.y] == 1:
        return 0
    t = t.front()
    if vis[t.x][t.y]:
        return 0
    vis[t.x][t.y] = 1
    go_forward()
    paint_point(nw.x, nw.y, WHITE)
    paint_point(t.x, t.y, GREY)
    path.append(t)
    return 1


def check_right(nw):
    # print('check right')
    t = nw.right()
    if obs[t.x][t.y] == -1:
        obs[t.x][t.y] = right_obstacle()
        # print('right obstacle', obs[t.x][t.y])
    paint_square(t.x, t.y, RED if obs[t.x][t.y] == 1 else WHITE)
    if obs[t.x][t.y] == 1:
        turnleft()
        return 0
    t = t.front()
    if vis[t.x][t.y]:
        turnleft()
        return 0
    vis[t.x][t.y] = 1
    go_forward()
    paint_point(nw.x, nw.y, WHITE)
    paint_point(t.x, t.y, GREY)
    path.append(t)
    return 1


paint_map(BLACK)
paint_square(N, N, WHITE)
paint_point(N, N, GREY)
for i in range(0, 2 * N, 2):
    for j in range(0, 2 * N, 2):
        paint_square(i, j, RED)
for i in range(N * 2):
    for j in range(N * 2):
        obs[i][j] = -1
obs[N][N] = 0
vis[N][N] = 1
path.append(status(N, N, 0))

while True:
    nw = path[-1]
    if not check_left(nw):
        if not check_front(nw):
            if not check_right(nw):
                path.pop()
                if not path:
                    break
                t = path[-1]
                nw = nw.back()
                go_back()
                # print(nw.x,nw.y,nw.dir)
                # print(t.x,t.y,t.dir)

                if nw == t.left():
                    turnright()
                elif nw == t.right():
                    turnleft()

                else:
                    assert nw == t.front()
                paint_point(nw.x, nw.y, WHITE)
                paint_point(t.x, t.y, GREY)

# 以上为算法


# 以下为原始主while

# while robot.go_on():
#     # print(state)
#     if state == 0:
#         stop()
#     if state == 1:
#         turnright()
#         stop()
#         count = 0
#         state = 0
#         continue
#     if state == 2:
#         turnleft()
#         stop()
#         count = 0
#         state = 0
#     if state == 3:
#         go_forward()
#     if state == 4:
#         go_back()

stop()
robot.clean_up()

# Enter here exit cleanup code.
