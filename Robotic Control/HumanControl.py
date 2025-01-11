from unifr_api_epuck import wrapper
import pygame
import time
import SensorRealValue
import classify

# REFLECT = 1000
# ip_addr = '192.168.6.11'
# robot = wrapper.get_robot(ip_addr)
# robot.init_sensors()
# robot.init_camera('C:\\Users\\19000\\PycharmProjects\\AIIRWIFI\\image')
# print(robot.get_battery_level())
# mycount = 0


def boardControl():
    text = ['Welcome to control our robot', 'A means turn left', 'D means turn right',
            'S means turn back', 'Z means stop', 'W means go ahead',
            'Good luck'
            ]
    pygame.init()
    bg_size = [600, 300]
    screen = pygame.display.set_mode(bg_size)
    background = pygame.image.load(r'C:\Users\19000\PycharmProjects\AIIRWIFI\car.jpeg')
    screen.blit(background, (0, 0))
    pygame.display.set_caption("keyControl")
    font = pygame.font.Font('freesansbold.ttf', 20)

    for i in range(len(text)):
        atext = font.render(text[i], True, (0, 0, 0))
        screen.blit(atext, (100, 50 + 30 * i))
    while True:
        # while大循环用于每次的按键输入，当for循环得到输入是右上角的X时就关闭程序，否则就输出音频
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                key = event.key
                # 下面这句就是找对应按键的音频
                if key == pygame.K_a:
                    # robot.go_on()
                    # print('turn left')
                    # # print(left_obstacle())
                    # turnleft()
                    # stop()
                    pass
                elif key == pygame.K_d:
                    # robot.go_on()
                    # print('turn right')
                    # # print(right_obstacle())
                    # turnright()
                    # stop()
                    pass
                elif key == pygame.K_z:
                    # print('stop')
                    # # stop()
                    # # prox = robot.get_prox()
                    # # for i in range(8):
                    # #     prox[i] = SensorRealValue.RealProxy(prox[i])
                    # # print(prox)
                    pass
                elif key == pygame.K_s:
                    # robot.go_on()
                    # print('turn back')
                    # # print(back_obstacle())
                    # turnback()
                    # stop()
                    pass
                elif key == pygame.K_w:
                    # robot.go_on()
                    # print('go ahead')
                    # # print(front_obstacle())
                    # goforward()
                    # stop()
                    pass
                elif key == pygame.K_q:
                    print('quit')
                    return
                else:
                    print('error taping')
                    # stop()
        pygame.display.update()


def goforward(velocity=4):
    leftSpeed = velocity
    rightSpeed = velocity
    robot.set_speed(leftSpeed, rightSpeed)
    robot.sleep(0.5)
    stop()


def goback(velocity=7):
    leftSpeed = -velocity
    rightSpeed = -velocity
    robot.set_speed(leftSpeed, rightSpeed)
    robot.sleep(1)


def turnback():
    turnleft()
    turnleft()


def turnright():
    start = time.time()
    degree = 25
    Rad = []
    Srad = 0
    Serr = 0
    V = 7
    kp = 1.5
    ki = 1
    kd = 0.1
    Rad.append(degree)
    while 1:
        Serr = 0
        leftSpeed = V
        rightSpeed = -V
        robot.set_speed(leftSpeed, rightSpeed)
        robot.sleep(0.01)
        z = robot.get_gyro_axes()[2] / 131
        z = abs(z)
        Srad = Srad + z * 0.01
        Rad.append(degree - Srad)

        if degree + 0.2 >= Srad >= degree - 0.2:
            print('Srad', Srad)
            break
        for i in Rad:
            Serr = Serr + i

        u = kp * (Rad[-1]) + ki * Serr / Rad.__sizeof__() + kd * (Rad[-1] - Rad[-2])

        V = min(u / 10, 7)
        print('Srad', Srad, 'u', u, 'v', V)

    stop()
    end = time.time()
    print('gap', end - start)


def turnleft():
    leftSpeed = -3
    rightSpeed = 3
    robot.set_speed(leftSpeed, rightSpeed)
    robot.sleep(0.77)
    stop()


def stop():
    robot.set_speed(0, 0)
    robot.sleep(0.1)


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


# for i in range(1):
#     front_obstacle()
boardControl()
# print('1')

# my_working_directory = 'C:\\Users\\Administrator\\PycharmProjects\\AIIRwifi\\images'
# robot.init_camera(my_working_directory)
# robot.sleep(1)
#
# while robot.go_on():
#     robot.live_camera() #call it in each step
# robot.init_camera()  # Enables the robot’s camera
# save_image_folder – input directory folder to save the images taken by the robot
# robot.disable_camera()
# robot.get_camera()  # Gets raw images from robot. [[red],[green],[blue]]
# robot.take_picture()  # take_picture(filename=None).


# robot.clean_up()

# if __name__ == '__main_':
#     classify.predict()
