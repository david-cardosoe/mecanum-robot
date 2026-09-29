
MOTOR_CONFIG = {
    'FR': {
        'in1': 5,
        'in2': 6,
        'enable': 16,
        'inverted': False
    },
    'FL': {
        'in1': 12,
        'in2': 13,
        'enable': 19,
        'inverted': False
    },
    'RL': {
        'in1': 17,
        'in2': 18,
        'enable': 20,
        'inverted': False
    },
    'RR': {
        'in1': 25,
        'in2': 23,
        'enable': 21,
        'inverted': False
    }
}


def direction_to_pin_states(direction, inverted=False):

    if direction == 'forward':

        if inverted:
            return (0, 1)

        return (1, 0)
    elif direction == 'reverse':

        if inverted:
            return (1, 0)

        return (0, 1)
    elif direction == 'stop':
        return (0, 0)
    else:
        raise ValueError(f'Invalid Motor direction: {direction}')


def motor_command_to_gpio_output(wheel, motor_command):

    motor_data = MOTOR_CONFIG[wheel]

    direction_pin_states = direction_to_pin_states(
        motor_command['direction'],
        motor_data['inverted']
    )

    return {
        'in1_pin': motor_data['in1'],
        'in1_state': direction_pin_states[0],
        'in2_pin': motor_data['in2'],
        'in2_state': direction_pin_states[1],
        'enable_pin': motor_data['enable'],
        'duty_cycle': motor_command['duty_cycle']
    }


def all_motor_commands_to_gpio_outputs(motor_commands):

    gpio_outputs = {}

    for wheel, motor_command in motor_commands.items():

        command_to_gpio = motor_command_to_gpio_output(wheel, motor_command)

        gpio_outputs[wheel] = command_to_gpio

    return gpio_outputs
