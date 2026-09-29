import lgpio

DIRECTION_PINS = [5, 6, 12, 13, 17, 18, 25, 23]
ENABLE_PINS = [16, 19, 20, 21]

chip = lgpio.gpiochip_open(0)

for pin in DIRECTION_PINS:
    lgpio.gpio_claim_output(chip, pin, 0)

for pin in ENABLE_PINS:
    lgpio.gpio_claim_output(chip, pin, 0)

print('All motor control pins set LOW.')
input('Press Enter to release GPIO...')

lgpio.gpiochip_close(chip)