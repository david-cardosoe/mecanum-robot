from robot_control.motor_commands import (
    wheel_speeds_to_all_motor_commands
)

result = wheel_speeds_to_all_motor_commands({'FL': 2.5, 'FR': -5.0, 'RL': 7.5, 'RR': 0.0}, 10)
print(result)
