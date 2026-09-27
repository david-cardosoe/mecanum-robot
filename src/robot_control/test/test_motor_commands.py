from robot_control.motor_commands import (
    create_stop_motor_commands,
    wheel_speed_to_motor_command,
    wheel_speeds_to_all_motor_commands
)


def test_forward_motor_command():
    result = wheel_speed_to_motor_command(5.0, 10.0)

    assert result['direction'] == 'forward'
    assert result['duty_cycle'] == 50.0


def test_reverse_motor_command():
    result = wheel_speed_to_motor_command(-7.5, 10.0)

    assert result['direction'] == 'reverse'
    assert result['duty_cycle'] == 75.0


def test_stop_motor_command():
    result = wheel_speed_to_motor_command(0.0, 10.0)

    assert result['direction'] == 'stop'
    assert result['duty_cycle'] == 0.0


def test_max_motor_command():
    result = wheel_speed_to_motor_command(10.0, 10.0)

    assert result['direction'] == 'forward'
    assert result['duty_cycle'] == 100.0


def test_over_max_motor_command():
    result = wheel_speed_to_motor_command(15.0, 10.0)

    assert result['direction'] == 'forward'
    assert result['duty_cycle'] == 100.0


def test_all_motor_commands():

    result = wheel_speeds_to_all_motor_commands({'FL': 2.5, 'FR': -5.0, 'RL': 7.5, 'RR': 0.0}, 10)

    assert result['FL']['direction'] == 'forward'
    assert result['FL']['duty_cycle'] == 25.0
    assert result['FR']['direction'] == 'reverse'
    assert result['FR']['duty_cycle'] == 50.0
    assert result['RL']['direction'] == 'forward'
    assert result['RL']['duty_cycle'] == 75.0
    assert result['RR']['direction'] == 'stop'
    assert result['RR']['duty_cycle'] == 0.0


def test_stop_all_motor_commands():

    result = create_stop_motor_commands()

    assert result['FL']['direction'] == 'stop'
    assert result['FL']['duty_cycle'] == 0.0
    assert result['FR']['direction'] == 'stop'
    assert result['FR']['duty_cycle'] == 0.0
    assert result['RL']['direction'] == 'stop'
    assert result['RL']['duty_cycle'] == 0.0
    assert result['RR']['direction'] == 'stop'
    assert result['RR']['duty_cycle'] == 0.0
