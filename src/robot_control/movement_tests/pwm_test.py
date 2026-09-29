import time
import lgpio

ENABLE_PIN = 16
PWM_FREQUENCY = 1000

chip = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(chip, ENABLE_PIN, 0)

print('PWM 0%')
lgpio.tx_pwm(chip, ENABLE_PIN, PWM_FREQUENCY, 0)
time.sleep(1)

print('PWM 25%')
lgpio.tx_pwm(chip, ENABLE_PIN, PWM_FREQUENCY, 25)
time.sleep(2)

print('PWM 50%')
lgpio.tx_pwm(chip, ENABLE_PIN, PWM_FREQUENCY, 50)
time.sleep(2)

print('PWM stopped')
lgpio.tx_pwm(chip, ENABLE_PIN, 0, 0)

lgpio.gpiochip_close(chip)