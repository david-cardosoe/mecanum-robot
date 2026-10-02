from unittest.mock import call, patch
from robot_control.l298n_gpio import(
    initialize_motor_gpio,
    apply_motor_commands,
    stop_all_motors,
    cleanup_motor_gpio
)


from unittest.mock import call, patch

from robot_control.l298n_gpio import initialize_motor_gpio


@patch('robot_control.l298n_gpio.lgpio')
def test_initialize_motor_gpio(mock_lgpio):

    # Initialize using the mocked GPIO library.
    chip = initialize_motor_gpio()

    # Verify that the GPIO controller was opened.
    mock_lgpio.gpiochip_open.assert_called_once_with(0)

    # Verify that the function returns the opened handle.
    assert chip is mock_lgpio.gpiochip_open.return_value

    # All enable pins first, followed by direction pins.
    expected_calls = [
        call(chip, 16, 0),
        call(chip, 19, 0),
        call(chip, 20, 0),
        call(chip, 21, 0),

        call(chip, 5, 0),
        call(chip, 6, 0),
        call(chip, 12, 0),
        call(chip, 13, 0),
        call(chip, 17, 0),
        call(chip, 18, 0),
        call(chip, 25, 0),
        call(chip, 23, 0),
    ]

    assert mock_lgpio.gpio_claim_output.call_args_list == expected_calls


@patch('robot_control.l298n_gpio.lgpio')
def test_apply_motor_commands(mock_lgpio):
    chip = 123  # Fake GPIO controller handle

    commands = {
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
        }
    }

    apply_motor_commands(chip, commands)

    expected_calls = [
        # Disable PWM on both motors
        call.tx_pwm(chip, 16, 1000, 0),
        call.tx_pwm(chip, 20, 1000, 0),

        # Set direction pins
        call.gpio_write(chip, 5, 1),
        call.gpio_write(chip, 6, 0),
        call.gpio_write(chip, 17, 0),
        call.gpio_write(chip, 18, 1),

        # Apply new PWM
        call.tx_pwm(chip, 16, 1000, 50.0),
        call.tx_pwm(chip, 20, 1000, 25.0)
    ]

    assert mock_lgpio.mock_calls == expected_calls


@patch('robot_control.l298n_gpio.lgpio')
def test_stop_all_motors(mock_lgpio):
    chip = 123

    stop_all_motors(chip)

    # Add assertions here.
    expected_calls = [
        call.tx_pwm(chip, 16, 1000, 0),
        call.tx_pwm(chip, 19, 1000, 0),
        call.tx_pwm(chip, 20, 1000, 0),
        call.tx_pwm(chip, 21, 1000, 0),

        call.gpio_write(chip, 16, 0),
        call.gpio_write(chip, 19, 0),
        call.gpio_write(chip, 20, 0),
        call.gpio_write(chip, 21, 0),

        call.gpio_write(chip, 5, 0),
        call.gpio_write(chip, 6, 0),

        call.gpio_write(chip, 12, 0),
        call.gpio_write(chip, 13, 0),

        call.gpio_write(chip, 17, 0),
        call.gpio_write(chip, 18, 0),

        call.gpio_write(chip, 25, 0),
        call.gpio_write(chip, 23, 0)  
    ]

    assert mock_lgpio.mock_calls == expected_calls


@patch('robot_control.l298n_gpio.lgpio')
def test_cleanup_motor_gpio(mock_lgpio):
    chip = 123

    cleanup_motor_gpio(chip)

    # Check that the final GPIO operation closes the controller.
    assert mock_lgpio.mock_calls[-1] == call.gpiochip_close(chip)

    # Check the total number of operations.
    assert len(mock_lgpio.mock_calls) == 17


import pytest
from unittest.mock import call, patch


@patch('robot_control.l298n_gpio.lgpio')
def test_apply_motor_commands_stops_on_failure(mock_lgpio):
    chip = 123

    commands = {
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
        }
    }

    mock_lgpio.tx_pwm.side_effect = [
        None,  # Disable FR PWM
        None,  # Disable RL PWM
        None,  # Apply FR PWM
        RuntimeError('Simulated PWM failure'),  # RL fails

        # Allow all four emergency stop calls to succeed
        None,
        None,
        None,
        None
    ]

    with pytest.raises(RuntimeError, match='Simulated PWM failure'):
        apply_motor_commands(chip, commands)

    # All four motors should receive a stop command.
    expected_stop_calls = [
        call(chip, 16, 1000, 0),
        call(chip, 19, 1000, 0),
        call(chip, 20, 1000, 0),
        call(chip, 21, 1000, 0)
    ]

    assert mock_lgpio.tx_pwm.call_args_list[-4:] == expected_stop_calls

    # Stop, but leave the controller open.
    mock_lgpio.gpiochip_close.assert_not_called()


@patch('robot_control.l298n_gpio.lgpio')
def test_initialize_motor_gpio_failure(mock_lgpio):
    chip = 123
    mock_lgpio.gpiochip_open.return_value = chip

    # The four enable pins succeed.
    # Claiming the fifth pin raises an error.
    mock_lgpio.gpio_claim_output.side_effect = [
        None,
        None,
        None,
        None,
        RuntimeError('GPIO pin unavailable')
    ]

    with pytest.raises(RuntimeError, match='GPIO pin unavailable'):
        initialize_motor_gpio()

    expected_calls = [
        call(chip, 16, 0),
        call(chip, 19, 0),
        call(chip, 20, 0),
        call(chip, 21, 0),
        call(chip, 5, 0)  # Simulated failure occurs here.
    ]

    assert mock_lgpio.gpio_claim_output.call_args_list == expected_calls

    # Initialization must release the controller.
    mock_lgpio.gpiochip_close.assert_called_once_with(chip)
