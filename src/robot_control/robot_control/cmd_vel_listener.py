from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from robot_control.mecanum_kinematics import (
    apply_deadband,
    calculate_wheel_speeds,
    normalize_wheel_speeds
)
from robot_control.motor_commands import (
    create_stop_motor_commands,
    wheel_speeds_to_all_motor_commands
)

MAX_WHEEL_SPEED = 10.0
LINEAR_DEADBAND = 0.02
ANGULAR_DEADBAND = 0.05


class CmdVelListener(Node):

    def __init__(self):
        super().__init__('cmd_vel_listener')

        self.last_cmd_time = None
        self.command_timeout = 0.5
        self.watchdog_timer = self.create_timer(0.1, self.watchdog_callback)
        self.watchdog_triggered = False

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.get_logger().info('cmd_vel listener started')

    def watchdog_callback(self):

        if self.last_cmd_time is None:
            return

        if self.watchdog_triggered:
            return

        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.last_cmd_time).nanoseconds / 1e9

        if elapsed_time > self.command_timeout:

            self.watchdog_triggered = True

            stop_motor_commands = create_stop_motor_commands()

            self.get_logger().info(
                'Watchdog triggered, elapsed time since last command exceeded. \n'
                f'{stop_motor_commands}'
            )

    def cmd_vel_callback(self, msg):

        self.last_cmd_time = self.get_clock().now()
        self.watchdog_triggered = False

        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z

        vx = apply_deadband(vx, LINEAR_DEADBAND)
        vy = apply_deadband(vy, LINEAR_DEADBAND)
        wz = apply_deadband(wz, ANGULAR_DEADBAND)

        self.get_logger().info(
            f'Message: {msg}'
        )

        wheel_speeds = calculate_wheel_speeds(vx, vy, wz)
        normalized_all_wheel_speeds = normalize_wheel_speeds(
            wheel_speeds,
            MAX_WHEEL_SPEED
        )
        motor_commands = wheel_speeds_to_all_motor_commands(
            normalized_all_wheel_speeds,
            MAX_WHEEL_SPEED
        )

        self.get_logger().info(
            f'Forward: {vx:.2f} m/s | '
            f'Sideways: {vy:.2f} m/s | '
            f'Rotation: {wz:.2f} rad/s'
        )

        self.get_logger().info(
            f"FL -> {motor_commands['FL']['direction']}, "
            f"{motor_commands['FL']['duty_cycle']:.2f}% \n"
            f"FR -> {motor_commands['FR']['direction']}, "
            f"{motor_commands['FR']['duty_cycle']:.2f}% \n"
            f"RL -> {motor_commands['RL']['direction']}, "
            f"{motor_commands['RL']['duty_cycle']:.2f}% \n"
            f"RR -> {motor_commands['RR']['direction']}, "
            f"{motor_commands['RR']['duty_cycle']:.2f}% \n"
        )


def main(args=None):
    rclpy.init(args=args)

    node = CmdVelListener()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
