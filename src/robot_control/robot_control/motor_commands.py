
def wheel_speed_to_motor_command(wheel_speed, max_speed):

    if max_speed <= 0:
        raise ValueError('max_speed must be greater than 0')

    if wheel_speed == 0:
        return {
            'direction': 'stop',
            'duty_cycle': 0.0
        }

    if wheel_speed > 0:
        direction = 'forward'
    else:
        direction = 'reverse'

    duty_cycle = (abs(wheel_speed) / max_speed) * 100
    duty_cycle = min(duty_cycle, 100.0)

    return {
        'direction': direction,
        'duty_cycle': duty_cycle
    }


def wheel_speeds_to_all_motor_commands(wheel_speeds, max_speed):

    all_motor_commands = {}

    for key, value in wheel_speeds.items():

        motor_command = wheel_speed_to_motor_command(value, max_speed)

        all_motor_commands[key] = motor_command

    return all_motor_commands


def create_stop_motor_commands():

    return {
        'FL': {'direction': 'stop', 'duty_cycle': 0.0},
        'FR': {'direction': 'stop', 'duty_cycle': 0.0},
        'RL': {'direction': 'stop', 'duty_cycle': 0.0},
        'RR': {'direction': 'stop', 'duty_cycle': 0.0}
    }
