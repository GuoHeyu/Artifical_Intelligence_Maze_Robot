from unifr_api_epuck import wrapper

ip_addr = '192.168.43.125'
robot = wrapper.get_robot(ip_addr)

robot.go_on()  # Sends and receives commands between computer and robot. True (if no problem occurs)
robot.sleep(0)  # Pause the execution during duration seconds

robot.get_battery_level()  # Gets robot’s battery level.

robot.set_speed(0, 0)  # Sets the speed of the robot’s motors. int -7 to 7
robot.get_speed()  # Gets speed of the motors [left_wheel, right_wheel] [int, int]
robot.get_motors_steps()  # Gets number of steps of the wheels.[left_wheel, right_wheel].[int,int]

robot.enable_led(0)  # Turns ON led at led_position. int 0 to 7.
# Only LEDs at position 1,3,5 and 7 are RGB
# red,green,blue – int - between 0 (low) and 100 (high)
robot.disable_led(0)  # Turns OFF led at led_position. int - (value between 0 and 7)
robot.enable_all_led()
robot.disable_all_led()
robot.enable_body_led()
robot.disable_body_led()
robot.enable_front_led()
robot.disable_front_led()

robot.init_sensors()
robot.disable_sensors()

robot.get_prox()  # Gets the robot’s proximity sensor raw values
# IR proximity: between 0 (no objects detected) and 4095 (object near the sensor)
# int array - (length 8)

robot.init_tof()  # Initiates Time Of Flight sensor
robot.get_tof()  # Gets the Time Of Flight value. values in millimetres. int
robot.disable_tof()

robot.get_acceleration()  # Gets the magnitude of the acceleration vector
# acceleration magnitude, between 0.0 and about 2600.0 (~3.46 g)
# Returns value of the accelerometer. int
robot.get_roll()  # Gets roll degree reading.
# Orientation between 0.0 and 360.0 degrees. float
robot.get_pitch()  # Gets pitch angle reading.
# Inclination between 0.0 and 90.0 degrees (when tilted in any direction). float

robot.init_camera()  # Enables the robot’s camera
# save_image_folder – input directory folder to save the images taken by the robot
robot.disable_camera()
robot.get_camera()  # Gets raw images from robot. [[red],[green],[blue]]
robot.take_picture()  # take_picture(filename=None).
