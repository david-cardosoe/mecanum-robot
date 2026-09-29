import pytest
from robot_control.motor_driver import (
    all_motor_commands_to_gpio_outputs,
    direction_to_pin_states,
    motor_command_to_gpio_output,
    MOTOR_CONFIG
)


def test_forward_direction_to_pin_states():

    output = direction_to_pin_states('forward')

    assert output == (1, 0)


def test_reverse_direction_to_pin_states():

    output = direction_to_pin_states('reverse')

    assert output == (0, 1)


def test_stop_direction_to_pin_states():

    output = direction_to_pin_states('stop')

    assert output == (0, 0)


def test_forward_inverted_direction_to_pin_states():

    output = direction_to_pin_states('forward', inverted=True)

    assert output == (0, 1)


def test_reverse_inverted_direction_to_pin_states():

    output = direction_to_pin_states('reverse', inverted=True)

    assert output == (1, 0)


def test_invalid_direction_to_pin_states():

    with pytest.raises(ValueError):
        direction_to_pin_states('fod')


def test_forward_motor_commands_to_gpio_output():

    output = motor_command_to_gpio_output('FR', {'direction': 'forward', 'duty_cycle': 50.0})

    assert output['in1_pin'] == 5
    assert output['in1_state'] == 1
    assert output['in2_pin'] == 6
    assert output['in2_state'] == 0
    assert output['enable_pin'] == 16
    assert output['duty_cycle'] == 50.0


def test_stop_motor_commands_to_gpio_output():

    output = motor_command_to_gpio_output('FR', {'direction': 'stop', 'duty_cycle': 0.0})

    assert output['in1_pin'] == 5
    assert output['in1_state'] == 0
    assert output['in2_pin'] == 6
    assert output['in2_state'] == 0
    assert output['enable_pin'] == 16
    assert output['duty_cycle'] == 0.0


def test_inverted_motor_command_to_gpio_output(monkeypatch):

    monkeypatch.setitem(MOTOR_CONFIG['FR'], 'inverted', True)

    output = motor_command_to_gpio_output(
        'FR',
        {'direction': 'forward', 'duty_cycle': 50.0}
    )

    assert output['in1_state'] == 0
    assert output['in2_state'] == 1


def test_all_motor_commands_to_gpio_outputs():

    motor_commands = {
        'FL': {'direction': 'forward', 'duty_cycle': 50.0},
        'FR': {'direction': 'forward', 'duty_cycle': 50.0},
        'RL': {'direction': 'reverse', 'duty_cycle': 25.0},
        'RR': {'direction': 'stop', 'duty_cycle': 0.0}
    }

    output = all_motor_commands_to_gpio_outputs(motor_commands)

    expected = {
        'FL': {
            'in1_pin': 12,
            'in1_state': 1,
            'in2_pin': 13,
            'in2_state': 0,
            'enable_pin': 19,
            'duty_cycle': 50.0
        },
        'FR': {
            'in1_pin': 5,
            'in1_state': 1,
            'in2_pin': 6,
            'in2_state': 0,
            'enable_pin': 16,
            'duty_cycle': 50.0
        },
        'RL': {
            'in1_pin': 17,
            'in1_state': 0,
            'in2_pin': 18,
            'in2_state': 1,
            'enable_pin': 20,
            'duty_cycle': 25.0
        },
        'RR': {
            'in1_pin': 25,
            'in1_state': 0,
            'in2_pin': 23,
            'in2_state': 0,
            'enable_pin': 21,
            'duty_cycle': 0.0
        }
    }

    assert output == expected
