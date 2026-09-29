import time
import lgpio

GPIO_PIN = 5

chip = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(chip, GPIO_PIN, 0)

print('GPIO 5 LOW')
time.sleep(1)

lgpio.gpio_write(chip, GPIO_PIN, 1)
print('GPIO 5 HIGH')
time.sleep(1)

lgpio.gpio_write(chip, GPIO_PIN, 0)
print('GPIO 5 LOW')

lgpio.gpiochip_close(chip)
