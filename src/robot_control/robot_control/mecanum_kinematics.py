# Wheel kinematics equations based off robot dimensions

# Measurements in Meters
WHEEL_RADIUS = 0.033
HALF_LENGTH = 0.06675
HALF_WIDTH = 0.06


def calculate_wheel_speeds(vx, vy, wz):
    # Calculations will result in rad/s
    front_left = (vx - vy - ((HALF_LENGTH + HALF_WIDTH) * wz)) / WHEEL_RADIUS
    front_right = (vx + vy + ((HALF_LENGTH + HALF_WIDTH) * wz)) / WHEEL_RADIUS
    rear_left = (vx + vy - ((HALF_LENGTH + HALF_WIDTH) * wz)) / WHEEL_RADIUS
    rear_right = (vx - vy + ((HALF_LENGTH + HALF_WIDTH) * wz)) / WHEEL_RADIUS

    return {
        'FL': front_left,
        'FR': front_right,
        'RL': rear_left,
        'RR': rear_right
    }


def normalize_wheel_speeds(wheel_speeds, max_speed):

    absolute_largest_speed = abs(max(wheel_speeds.values(), key=abs))

    if absolute_largest_speed <= max_speed:
        return wheel_speeds

    scale = max_speed / absolute_largest_speed

    scaled_speeds = {key: value * scale for key, value in wheel_speeds.items()}

    return scaled_speeds


def apply_deadband(value, threshold):

    if abs(value) < threshold:
        return 0.0
    else:
        return value
