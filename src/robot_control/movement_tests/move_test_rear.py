import time
import lgpio

IN1 = 25
IN2 = 23
ENABLE = 21

PWM_FREQUENCY = 1000
DUTY_CYCLE = 60

chip = lgpio.gpiochip_open(0)

try:
    # Start in a known safe state
    lgpio.gpio_claim_output(chip, IN1, 0)
    lgpio.gpio_claim_output(chip, IN2, 0)
    lgpio.gpio_claim_output(chip, ENABLE, 0)

    print('Safe state ready: motor stopped.')
    input('Connect Driver 1 motor battery, then press Enter...')

    # Choose one direction
    lgpio.gpio_write(chip, IN1, 0)
    lgpio.gpio_write(chip, IN2, 1)

    print('Running FR and FL motor at 25% PWM for 0.5 seconds...')
    lgpio.tx_pwm(chip, ENABLE, PWM_FREQUENCY, DUTY_CYCLE)

    time.sleep(2)

finally:
    # Always stop the motor
    lgpio.tx_pwm(chip, ENABLE, 0, 0)
    lgpio.gpio_write(chip, ENABLE, 0)
    lgpio.gpio_write(chip, IN1, 0)
    lgpio.gpio_write(chip, IN2, 0)

    lgpio.gpiochip_close(chip)

    print('Motor stopped and GPIO released.')