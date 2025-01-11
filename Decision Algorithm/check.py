# 使用方法：
# 更改第399行的get_dict的参数，其中第一个参数为迷宫大小N (N*N)，第二个参数为迷宫里的障碍数（需要保证存在左下到右上的最短路）。dict的返回值含义见群里。
# 如果要更改Monte_Carlo的参数，那就更改391行的代码。参数释义见第248行与第298行。


import numpy as np
import random
import time
import matlab
import matlab.engine
import matplotlib.pyplot as plt
from matplotlib import colors


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


def get_shortest_dis(x, y, tx, ty, OBS):
    la = np.zeros((N * 2, N * 2), dtype=int)
    dis = np.zeros((N * 2, N * 2), dtype=int)
    dis[x][y] = 1
    la[x][y], la[tx][ty] = -1, -1
    que = []
    que.append([x, y])
    fir = 0
    while fir < len(que):
        x, y = que[fir]
        fir += 1
        if x == tx and y == ty:
            break
        for d in range(4):
            xx, yy = x + dx[d], y + dy[d]
            if xx >= N * 2 or yy >= N * 2 or xx < 0 or yy < 0:
                continue
            if OBS[xx][yy] == 1 or dis[xx][yy]:
                continue
            dis[xx][yy] = dis[x][y] + 1
            if la[x][y] == -1:
                la[xx][yy] = d
            else:
                la[xx][yy] = la[x][y]
            que.append([xx, yy])
    return la[tx][ty], dis[tx][ty] // 2


WHITE = 0
GREY = 1
RED = 2
BLACK = 3

N = 50 * 2 + 5
map = np.zeros((2 * N, 2 * N), dtype=int)
pos = status(N, N, 0)
sizeOfMaze = 10

# fig, ax0 = plt.subplots()
# A = np.ones([2 * sizeOfMaze + 1, 2 * sizeOfMaze + 1]) * 3
# cMap = colors.ListedColormap(['white', 'lightgrey', 'red', 'black'])
# # cMap = plt.cm.get_cmap('Blues', 6)
# plt.ion()
f = open('test.txt', 'a')


def generate_map(len, num):
    global map
    map = np.zeros((2 * N, 2 * N), dtype=int)
    l, r = N - (len - 1), N + (len - 1)
    if len % 2 == 0:
        l -= 1
        r += 1
    for i in range(l - 1, r + 1):
        map[i][l - 1], map[i][r + 1], map[l - 1][i], map[r + 1][i] = 1, 1, 1, 1
    for i in range(l - 1, r + 1, 2):
        for j in range(l - 1, r + 1, 2):
            map[i][j] = 1
    for i in range(num):
        if i % 100 == 0:
            print(i)
        x, y = random.randint(l, r), random.randint(l, r)
        while True:
            if x % 2 == y % 2 or map[x][y]:
                x, y = random.randint(l, r), random.randint(l, r)
                continue
            map[x][y] = 1
            _, dd = get_shortest_dis(l, l, r, r, map)
            if dd:
                break
            map[x][y] = 0
            x, y = random.randint(l, r), random.randint(l, r)
    return dd, l, r


# N-(len-1)..N+(len-1)

def paint_map(color):
    mystr = '11111' + ' ' + str(sizeOfMaze) + ' ' + '-1' + ' ' + str(color) + '\n'
    f.write(mystr)
    # c = ax0.pcolormesh(A, cmap=cMap)
    # # fig.savefig('figure.pdf')
    # plt.plot()
    # plt.pause(0.5)
    # eng = matlab.engine.start_matlab()
    # eng.map_paint(color, 2 * sizeOfMaze + 1, nargout=0)
    pass


def paint_square(x, y, color):
    xeff = x - N + sizeOfMaze
    yeff = y - N + sizeOfMaze
    mystr = '22222' + ' ' + str(xeff) + ' ' + str(yeff) + ' ' + str(color) + '\n'
    f.write(mystr)
    # print('x', x, 'y', y)
    # A[xeff][yeff] = color
    # c = ax0.pcolormesh(A, cmap=cMap)
    # # # fig.savefig('figure.pdf')
    # plt.plot()
    # plt.pause(0.5)
    # eng = matlab.engine.start_matlab()
    # eng.square_paint(xeff, yeff, color, nargout=0)
    pass


def paint_point(x, y, color):
    xeff = x - N + sizeOfMaze
    yeff = y - N + sizeOfMaze
    mystr = '33333' + ' ' + str(xeff) + ' ' + str(yeff) + ' ' + str(color) + '\n'
    f.write(mystr)
    # xeff = x - (N - sizeOfMaze)
    # yeff = y - (N - sizeOfMaze)
    # plt.scatter(xeff + 0.5, yeff + 0.5, c='green', s=200)
    # # fig.savefig('figure.pdf')
    # plt.plot()
    # plt.pause(0.5)
    # eng = matlab.engine.start_matlab()
    # eng.point_paint(xeff, yeff, color, nargout=0)
    pass


def left_obstacle():
    ppos = pos.left()
    return map[ppos.x][ppos.y]


def front_obstacle():
    ppos = pos.front()
    return map[ppos.x][ppos.y]


def right_obstacle():
    ppos = pos.right()
    return map[ppos.x][ppos.y]


def back_obstacle():
    ppos = pos.back()
    return map[ppos.x][ppos.y]


def go_back():
    global pos
    pos = pos.back().back()


def go_forward():
    global pos
    pos = pos.front().front()


def turn_left():
    global pos
    pos.dir = (3 if pos.dir == 0 else pos.dir - 1)


def turn_right():
    global pos
    pos.dir = (0 if pos.dir == 3 else pos.dir + 1)


def get_dict(XX, YY):
    global pos
    global N
    dict = {}
    dict['dis'], L, R = generate_map(XX, YY)
    dict['ans0'] = 0
    pos = status(L, L, 1)

    obs = np.zeros((N * 2, N * 2), dtype=int)
    vis = np.zeros((N * 2, N * 2), dtype=int)
    path = []

    def check_left(nw):
        t = nw.left()
        if obs[t.x][t.y] == -1:
            obs[t.x][t.y] = left_obstacle()
        paint_square(t.x, t.y, RED if obs[t.x][t.y] == 1 else WHITE)
        if obs[t.x][t.y] == 1:
            return 0
        t = t.front()
        if vis[t.x][t.y]:
            return 0
        vis[t.x][t.y] = 1
        turn_left()
        go_forward()
        paint_point(nw.x, nw.y, WHITE)
        paint_point(t.x, t.y, GREY)
        path.append(t)
        return 1

    def check_front(nw):
        t = nw.front()
        if obs[t.x][t.y] == -1:
            obs[t.x][t.y] = front_obstacle()
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
        t = nw.right()
        if obs[t.x][t.y] == -1:
            obs[t.x][t.y] = right_obstacle()
        paint_square(t.x, t.y, RED if obs[t.x][t.y] == 1 else WHITE)
        if obs[t.x][t.y] == 1:
            return 0
        t = t.front()
        if vis[t.x][t.y]:
            return 0
        vis[t.x][t.y] = 1
        turn_right()
        go_forward()
        paint_point(nw.x, nw.y, WHITE)
        paint_point(t.x, t.y, GREY)
        path.append(t)
        return 1

    paint_map(BLACK)
    paint_square(N, N, WHITE)
    paint_point(N, N, GREY)
    for i in range(N * 2):
        for j in range(N * 2):
            obs[i][j] = -1
    for i in range(0, N * 2, 2):
        for j in range(0, N * 2, 2):
            if N - sizeOfMaze <= i <= N + sizeOfMaze and  N - sizeOfMaze <= j <= N + sizeOfMaze:
                paint_square(i, j, RED)
            obs[i][j] = 1
    for i in range(1, N * 2, 2):
        for j in range(1, N * 2, 2):
            if N - sizeOfMaze <= i <= N + sizeOfMaze and N - sizeOfMaze <= j <= N + sizeOfMaze:
                paint_square(i, j, WHITE)
            obs[i][j] = 0
    vis[L][L] = 1
    path.append(status(L, L, 1))

    for i in range(L - 1, R + 2):
         print(map[i][L - 1:R + 2])

    start1 = time.time()
    while True:
        nw = path[-1]
        if nw.x == R and nw.y == R and not ('ans1' in dict.keys()):
            dict['ans1'] = dict['ans0']
        if not check_left(nw):
            if not check_front(nw):
                if not check_right(nw):
                    path.pop()
                    if not path:
                        break
                    t = path[-1]
                    nw = nw.back()
                    go_back()
                    if nw == t.left():
                        turn_right()
                    elif nw == t.right():
                        turn_left()
                    else:
                        assert nw == t.front()
                    paint_point(nw.x, nw.y, WHITE)
                    paint_point(t.x, t.y, GREY)
        dict['ans0'] += 1
    end1 = time.time()
    print('time1', end1 - start1)



    # now_status输入当前状态（变量种类为status），tx,ty为终点坐标（注意程序默认起点坐标为N,N）
    # 如果已经在终点了则不动，否则往终点按决策走一步，然后返回的是一个status
    def Floodfill_choice(now_status, tx, ty):
        if now_status.x == tx and now_status.y == ty:
            return now_status
        che_status = now_status.front()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = front_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        che_status = now_status.left()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = left_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        che_status = now_status.back()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = back_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        che_status = now_status.right()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = right_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        obss = obs.copy()
        for i in range(L - 1, R + 2):
            obss[L - 1][i], obss[R + 1][i], obss[i][L - 1], obss[i][R + 1] = 1, 1, 1, 1
        for i in range(0, N * 2):
            for j in range(0, N * 2):
                if obss[i][j] == -1:
                    obss[i][j] = 0
        d, _ = get_shortest_dis(now_status.x, now_status.y, tx, ty, obss)
        assert (d != -1)
        paint_point(now_status.x, now_status.y, WHITE)
        Tx, Ty = now_status.x + dx[d], now_status.y + dy[d]
        che_status = now_status.right()
        if che_status.x == Tx and che_status.y == Ty:
            che_status = che_status.front()
            paint_point(che_status.x, che_status.y, GREY)
            turn_right()
            go_forward()
        else:
            che_status = now_status.front()
            while che_status.x != Tx or che_status.y != Ty:
                turn_left()
                now_status.dir = (3 if now_status.dir == 0 else now_status.dir - 1)
                che_status = now_status.front()
            che_status = che_status.front()
            paint_point(che_status.x, che_status.y, GREY)
            go_forward()
        return che_status

    # 大体同上
    # 新增参数times与alpha。其中times表示随机次数，是正整数；alpha表示某个障碍存在的概率，为0到1之间的实数（最好在0.1~0.9之间）。
    def Monte_Carlo_choice(now_status, tx, ty, times, alpha):
        if now_status.x == tx and now_status.y == ty:
            return now_status
        che_status = now_status.front()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = front_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        che_status = now_status.left()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = left_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        che_status = now_status.back()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = back_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        che_status = now_status.right()
        if obs[che_status.x][che_status.y] == -1:
            obs[che_status.x][che_status.y] = right_obstacle()
        paint_square(che_status.x, che_status.y, RED if obs[che_status.x][che_status.y] == 1 else WHITE)
        vote = [0, 0, 0, 0]
        for time in range(times):
            lis = []
            obss = obs.copy()
            for i in range(L - 1, R + 2):
                obss[L - 1][i], obss[R + 1][i], obss[i][L - 1], obss[i][R + 1] = 1, 1, 1, 1
            for i in range(L - 1, R + 2):
                for j in range(L - 1, R + 2):
                    if obss[i][j] == -1:
                        lis.append([i, j])
                        obss[i][j] = 0
            # print(len(lis))
            random.shuffle(lis)
            for x, y in lis:
                if random.random() > alpha:
                    continue
                obss[x][y] = 1
                laa, _ = get_shortest_dis(now_status.x, now_status.y, tx, ty, obss)
                if laa == -1:
                    obss[x][y] = 0
            laa, _ = get_shortest_dis(now_status.x, now_status.y, tx, ty, obss)
            vote[laa] += 1
        d = 0
        for i in range(1, 4):
            if vote[i] > vote[d]:
                d = i
        paint_point(now_status.x, now_status.y, WHITE)
        Tx, Ty = now_status.x + dx[d], now_status.y + dy[d]
        che_status = now_status.right()
        if che_status.x == Tx and che_status.y == Ty:
            che_status = che_status.front()
            paint_point(che_status.x, che_status.y, GREY)
            turn_right()
            go_forward()
        else:
            che_status = now_status.front()
            while che_status.x != Tx or che_status.y != Ty:
                turn_left()
                now_status.dir = (3 if now_status.dir == 0 else now_status.dir - 1)
                che_status = now_status.front()
            che_status = che_status.front()
            paint_point(che_status.x, che_status.y, GREY)
            go_forward()
        return che_status

    for i in range(N * 2):
        for j in range(N * 2):
            obs[i][j] = -1
    for i in range(0, N * 2, 2):
        for j in range(0, N * 2, 2):
            # paint_square(i, j, RED)
            obs[i][j] = 1
    for i in range(1, N * 2, 2):
        for j in range(1, N * 2, 2):
            # paint_square(i, j, WHITE)
            obs[i][j] = 0

    start2 = time.time()
    pos = status(L, L, 1)
    nw = status(L, L, 1)
    dict['ans2'] = 0
    while True:
        tt = Floodfill_choice(nw, R, R)
        if nw == tt:
            break
        dict['ans2'] += 1
        nw = tt

    end2 = time.time()
    print('time2', end2 - start2)
    # print(dict)

    start3 = time.time()
    pos = status(L, L, 1)
    nw = status(L, L, 1)
    dict['ans3'] = 0
    while True:
        tt = Monte_Carlo_choice(nw, R, R, 10, 0.2)
        if nw == tt:
            break
        dict['ans3'] += 1
        nw = tt
    end3 = time.time()
    print('time3', end3 - start3)
    return dict


print(get_dict(sizeOfMaze, 60))
f.close()