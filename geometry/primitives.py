from dataclasses import dataclass
from typing import Union, Tuple

Point = Tuple[float, float]


@dataclass
class Line:
    start: Point
    end: Point


@dataclass
class Arc:
    center: Point
    radius: float
    start_angle: float  # degrees
    end_angle: float  # degrees
    clockwise: bool = False


@dataclass
class QuadraticBezier:
    start: Point
    control: Point
    end: Point
