import lgpio
from robot_control.motor_driver import MOTOR_CONFIG


PWM_FREQUENCY = 1000


def initialize_motor_gpio():

    chip = lgpio.gpiochip_open(0)

    try:

        # Claim all four enable pins, initally LOW
        # We do enable pins first to ensure no power is delivered
        for motor in MOTOR_CONFIG.values():
            lgpio.gpio_claim_output(chip, motor['enable'], 0)

        # Claim all eight direction pins, initially LOW
        for motor in MOTOR_CONFIG.values():
            lgpio.gpio_claim_output(chip, motor['in1'], 0)
            lgpio.gpio_claim_output(chip, motor['in2'], 0)

        # Return chip so other functions can use it
        return chip

    except Exception:
        lgpio.gpiochip_close(chip)
        raise


def apply_motor_commands(chip, motor_commands):

    try:

        # Disable PWM before changing direction pins
        for commands in motor_commands.values():

            lgpio.tx_pwm(
                chip,
                commands['enable_pin'],
                PWM_FREQUENCY,
                0,
            )

        # Set all direction pins
        for commands in motor_commands.values():

            lgpio.gpio_write(chip, commands['in1_pin'], commands['in1_state'])
            lgpio.gpio_write(chip, commands['in2_pin'], commands['in2_state'])

        # Apply new PWM to all four motors
        for commands in motor_commands.values():
            lgpio.tx_pwm(
                chip,
                commands['enable_pin'],
                PWM_FREQUENCY,
                commands['duty_cycle'],
            )

    except Exception:
        stop_all_motors(chip)
        raise


def stop_all_motors(chip):

    for motor in MOTOR_CONFIG.values():
        lgpio.tx_pwm(chip, motor['enable'], PWM_FREQUENCY, 0)

    for motor in MOTOR_CONFIG.values():
        lgpio.gpio_write(chip, motor['enable'], 0)

    for motor in MOTOR_CONFIG.values():
        lgpio.gpio_write(chip, motor['in1'], 0)
        lgpio.gpio_write(chip, motor['in2'], 0)


def cleanup_motor_gpio(chip):
    try:
        stop_all_motors(chip)
    finally:
        lgpio.gpiochip_close(chip)
