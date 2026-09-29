import time
import lgpio

IN1 = 5
IN2 = 6
ENABLE = 16

IN3 = 12
IN4 = 13
ENABLE_FL = 19

PWM_FREQUENCY = 1000
DUTY_CYCLE = 60

chip = lgpio.gpiochip_open(0)

try:
    # Start in a known safe state
    lgpio.gpio_claim_output(chip, IN1, 0)
    lgpio.gpio_claim_output(chip, IN2, 0)
    lgpio.gpio_claim_output(chip, ENABLE, 0)

    lgpio.gpio_claim_output(chip, IN3, 0)
    lgpio.gpio_claim_output(chip, IN4, 0)
    lgpio.gpio_claim_output(chip, ENABLE_FL, 0)

    print('Safe state ready: motor stopped.')
    input('Connect Driver 1 motor battery, then press Enter...')

    # Choose one direction
    lgpio.gpio_write(chip, IN1, 1)
    lgpio.gpio_write(chip, IN2, 0)
    lgpio.gpio_write(chip, IN3, 1)
    lgpio.gpio_write(chip, IN4, 0)

    print('Running FR and FL motor at 25% PWM for 0.5 seconds...')
    lgpio.tx_pwm(chip, ENABLE, PWM_FREQUENCY, DUTY_CYCLE)
    lgpio.tx_pwm(chip, ENABLE_FL, PWM_FREQUENCY, DUTY_CYCLE)

    time.sleep(2)

finally:
    # Always stop the motor
    lgpio.tx_pwm(chip, ENABLE, 0, 0)
    lgpio.gpio_write(chip, ENABLE, 0)
    lgpio.gpio_write(chip, IN1, 0)
    lgpio.gpio_write(chip, IN2, 0)

    lgpio.tx_pwm(chip, ENABLE_FL, 0, 0)
    lgpio.gpio_write(chip, ENABLE_FL, 0)
    lgpio.gpio_write(chip, IN3, 0)
    lgpio.gpio_write(chip, IN4, 0)

    lgpio.gpiochip_close(chip)

    print('Motor stopped and GPIO released.')