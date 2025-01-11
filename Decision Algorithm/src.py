import numpy as np

WHITE = 0
GREY = 1
RED = 2
BLACK = 3


def paint_map(color):
    pass


def paint_square(x, y, color):
    pass


def paint_point(x, y, color):
    pass


def left_obstacle():
    return 1


def front_obstacle():
    return 1


def right_obstacle():
    return 1


def back_obstacle():
    return 1


def go_back():
    pass


def go_forward():
    pass


def turn_left():
    pass


def turn_right():
    pass


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


N = 50 * 2 + 5
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
        paint_square(i, j, RED)
        obs[i][j] = 1
for i in range(1, N * 2, 2):
    for j in range(1, N * 2, 2):
        paint_square(i, j, WHITE)
        obs[i][j] = 0
vis[N][N] = 1
path.append(status(N, N, 1))
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
                if nw == t.left():
                    turn_right()
                elif nw == t.right():
                    turn_left()
                else:
                    assert nw == t.front()
                paint_point(nw.x, nw.y, WHITE)
                paint_point(t.x, t.y, GREY)


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
    return la[tx][ty]


# now_status输入当前状态（变量种类为status），nn为迷宫大小
# 如果已经在终点了则不动，否则往终点按决策走一步，然后返回的是一个status
def Floodfill_choice(now_status, nn):
    tx = N + (nn - 1) * 2
    ty = N + (nn - 1) * 2
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
    for i in range(0, N * 2):
        for j in range(0, N * 2):
            if obss[i][j] == -1:
                obss[i][j] = 0
    for i in range(N - 1, tx + 2):
        obss[N - 1][i], obss[tx + 1][i], obss[i][tx + 1], obss[i][N - 1] = 1, 1, 1, 1
    d = get_shortest_dis(now_status.x, now_status.y, tx, ty, obss)
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


import random


# 大体同上
# 新增参数times与alpha。其中times表示随机次数，是正整数；alpha表示某个障碍存在的概率，为0到1之间的实数（最好在0.1~0.9之间）。
def Monte_Carlo_choice(now_status, nn, times, alpha):
    tx = N + (nn - 1) * 2
    ty = N + (nn - 1) * 2
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
        for i in range(N - 1, tx + 2):
            obss[N - 1][i], obss[tx + 1][i], obss[i][tx + 1], obss[i][N - 1] = 1, 1, 1, 1
        for i in range(N - 1, tx + 2):
            for j in range(N - 1, ty + 2):
                if obss[i][j] == -1:
                    lis.append([i, j])
                    obss[i][j] = 0
        random.shuffle(lis)
        for x, y in lis:
            if random.random() > alpha:
                continue
            obss[x][y] = 1
            if get_shortest_dis(now_status.x, now_status.y, tx, ty, obss) == -1:
                obss[x][y] = 0
        vote[get_shortest_dis(now_status.x, now_status.y, tx, ty, obss)] += 1
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
