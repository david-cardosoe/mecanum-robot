from robot_control.motor_commands import (
    wheel_speeds_to_all_motor_commands
)
from robot_control.motor_driver import all_motor_commands_to_gpio_outputs

result = wheel_speeds_to_all_motor_commands({'FL': 2.5, 'FR': -5.0, 'RL': 7.5, 'RR': 0.0}, 10)
# print(result)

test_input = {
    'FL': {'direction': 'forward', 'duty_cycle': 50.0},
    'FR': {'direction': 'forward', 'duty_cycle': 50.0},
    'RL': {'direction': 'reverse', 'duty_cycle': 25.0},
    'RR': {'direction': 'stop', 'duty_cycle': 0.0}
}

print(all_motor_commands_to_gpio_outputs(test_input))
