import cmath


def RealMotorSpeed(MotorSpeed):

    pass


def RealProxy(proxy):  # centimeter. approximation. range 0.2-4.5cm. 0 means small. 5 means large
    if proxy > 3790:
        return 0
    elif 3790 >= proxy > 3697:  # 0.2-0.3cm
        slope = (0.3 - 0.2) / (3697 - 3790)
        value = slope * (proxy - 3790) + 0.2
        return value
    elif 3697 >= proxy > 2637:  # 0.3-0.5cm
        slope = (0.5 - 0.3) / (2637 - 3697)
        value = slope * (proxy - 3697) + 0.3
        return value
    elif 2637 >= proxy > 1554:  # 0.5-0.7cm
        slope = (0.7 - 0.5) / (1554 - 2637)
        value = slope * (proxy - 2637) + 0.5
        return value
    elif 1554 >= proxy > 600:  # 0.7-1cm
        slope = (1 - 0.7) / (600 - 1554)
        value = slope * (proxy - 1554) + 0.7
        return value
    elif 600 >= proxy > 377:  # 1-1.5cm
        slope = (1.5 - 1) / (377 - 600)
        value = slope * (proxy - 600) + 1
        return value
    elif 377 >= proxy > 195:  # 1.5-2cm
        slope = (2 - 1.5) / (195 - 377)
        value = slope * (proxy - 377) + 1.5
        return value
    elif 195 >= proxy > 128:  # 2-2.5cm
        slope = (2.5 - 2) / (128 - 195)
        value = slope * (proxy - 195) + 2
        return value
    elif 128 >= proxy > 91:  # 2.5-3cm
        slope = (3 - 2.5) / (91 - 128)
        value = slope * (proxy - 128) + 2.5
        return value
    elif 91 >= proxy > 61:  # 3-3.5cm
        slope = (3.5 - 3) / (61 - 91)
        value = slope * (proxy - 91) + 3
        return value
    elif 61 >= proxy > 45:  # 3.5-4cm
        slope = (4 - 3.5) / (45 - 61)
        value = slope * (proxy - 61) + 3.5
        return value
    elif 45 >= proxy > 36:  # 4-4.5cm
        slope = (4.5 - 4) / (36 - 45)
        value = slope * (proxy - 45) + 4
        return value
    else:
        return 5


def RealTof(tof):  # give real value of sensor right before. cm
    return tof / 10.0


def RealAcceleration(acceleration, roll, pitch):  # give magnitude in x, y, z. unit is g
    stand_acceleration = acceleration * 3.46 / 2600
    realValue = [x for x in range(3)]
    realValue[2] = stand_acceleration * cmath.cos(pitch)
    realValue[1] = stand_acceleration * cmath.sin(pitch) * cmath.sin(roll)
    realValue[0] = stand_acceleration * cmath.sin(pitch) * cmath.cos(roll)
    return realValue
