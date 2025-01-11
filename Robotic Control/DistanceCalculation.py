

def DistanceGet(speed, acceleration, time, targetspeed=-1):
    # unit is m. return delta position in one direction. unit m
    # current speed m/s. acceleration vector m/s2. time s. target speed m/s
    approAcceleration = max(acceleration[0], acceleration[1])
    if targetspeed == -1:
        distance = speed * time   # no acceleration
    else:
        timea = (targetspeed - speed) / approAcceleration
        if timea > time:  # time is not enough for acceleration
            distance = speed * time + approAcceleration * time ^ 2 / 2
        else:
            distance = speed * timea + approAcceleration * timea ^ 2 / 2 + targetspeed * (timea - time)
    return distance
