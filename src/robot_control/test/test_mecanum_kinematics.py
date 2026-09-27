import pytest
from robot_control.mecanum_kinematics import (
    apply_deadband,
    calculate_wheel_speeds,
    normalize_wheel_speeds
)


def test_forward():

    speeds = calculate_wheel_speeds(0.3, 0, 0)
    assert speeds['FL'] == pytest.approx(9.09, abs=0.01)
    assert speeds['FR'] == pytest.approx(9.09, abs=0.01)
    assert speeds['RL'] == pytest.approx(9.09, abs=0.01)
    assert speeds['RR'] == pytest.approx(9.09, abs=0.01)


def test_left():

    speeds = calculate_wheel_speeds(0.0, 0.3, 0)
    assert speeds['FL'] == pytest.approx(-9.09, abs=0.01)
    assert speeds['FR'] == pytest.approx(9.09, abs=0.01)
    assert speeds['RL'] == pytest.approx(9.09, abs=0.01)
    assert speeds['RR'] == pytest.approx(-9.09, abs=0.01)


def test_ccw_rotation():

    speeds = calculate_wheel_speeds(0.0, 0.0, 0.3)
    assert speeds['FL'] == pytest.approx(-1.152, abs=0.01)
    assert speeds['FR'] == pytest.approx(1.152, abs=0.01)
    assert speeds['RL'] == pytest.approx(-1.152, abs=0.01)
    assert speeds['RR'] == pytest.approx(1.152, abs=0.01)


def test_diag_forward_left():

    speeds = calculate_wheel_speeds(0.3, 0.3, 0)
    assert speeds['FL'] == pytest.approx(0, abs=0.01)
    assert speeds['FR'] == pytest.approx(18.18, abs=0.01)
    assert speeds['RL'] == pytest.approx(18.18, abs=0.01)
    assert speeds['RR'] == pytest.approx(0, abs=0.01)


def test_normalize_when_over_limit():
    speeds = {
        'FL': -4.0,
        'FR': 8.0,
        'RL': -12.0,
        'RR': 6.0
    }

    result = normalize_wheel_speeds(speeds, 6.0)

    assert result['FL'] == pytest.approx(-2.0)
    assert result['FR'] == pytest.approx(4.0)
    assert result['RL'] == pytest.approx(-6.0)
    assert result['RR'] == pytest.approx(3.0)


def test_normalize_when_under_limit():
    speeds = {
        'FL': 2.0,
        'FR': 4.0,
        'RL': -5.0,
        'RR': 3.0,
    }

    result = normalize_wheel_speeds(speeds, 6.0)

    assert result == speeds


def test_normalize_all_zero():
    speeds = {
        'FL': 0.0,
        'FR': 0.0,
        'RL': 0.0,
        'RR': 0.0,
    }

    result = normalize_wheel_speeds(speeds, 6.0)

    assert result == speeds


def test_apply_deadband():

    assert apply_deadband(0.01, 0.02) == 0.0
    assert apply_deadband(0.3, 0.02) == 0.3
    assert apply_deadband(0, 0.02) == 0.0
    assert apply_deadband(-0.01, 0.02) == 0.0
