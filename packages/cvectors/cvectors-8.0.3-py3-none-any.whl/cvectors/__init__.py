"""A package for using complex numbers as 2D vectors."""
from __future__ import annotations

import cmath
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Literal, overload, TypeVar

__all__ = ["Vector", "angle"]


def angle(angle: float, /, unit: str) -> float:
    """Convert an angle to radians."""
    unit = unit.casefold()
    if unit in {"d", "deg", "degrees", "degree", "°"}:
        return angle * cmath.tau / 360
    if unit in {"r", "rad", "radian", "radians"}:
        return angle
    if unit in {"g", "grad", "gradians", "gradian", "gons", "gon", "grades", "grade"}:
        return angle * cmath.tau / 400
    if unit in {"mins", "min", "minutes", "minute", "'", "′"}:
        return angle * cmath.tau / 21600
    if unit in {"secs", "sec", "seconds", "second", '"', "″"}:
        return angle * cmath.tau / 1296000
    if unit in {"turn", "turns"}:
        return angle * cmath.tau
    raise ValueError(f"invalid angle unit: '{unit}'")


def _iterable_to_complex(obj: Iterable[float], /) -> complex:
    """Convert an iterable to an (x, y) tuple."""
    try:
        iterable = iter(obj)
    except TypeError:
        raise TypeError(
            "single argument Vector must be Vector, complex or iterable"
        ) from None
    try:
        x = next(iterable)
        y = next(iterable)
    except StopIteration:
        raise ValueError("iterable is too short to create Vector") from None
    try:
        next(iterable)
        raise ValueError("iterable is too long to create Vector")
    except StopIteration:
        return complex(x, y)


TVector = TypeVar("TVector", bound="Vector")


@dataclass(frozen=True, init=False, repr=False)
class Vector:
    """A two-dimensional vector."""

    __slots__ = ("_complex",)
    _complex: complex

    @overload
    def __init__(self, /, x: complex | Iterable[float]) -> None:
        ...

    @overload
    def __init__(self, /, x: float, y: float) -> None:
        ...

    def __init__(self, /, x, y=None):
        """Create a Vector from a single argument or x, y pair."""
        if y is None:
            if isinstance(x, complex):
                object.__setattr__(self, "_complex", x)
            elif isinstance(x, str):
                raise TypeError("cannot create Vector from string")
            else:
                object.__setattr__(self, "_complex", _iterable_to_complex(x))
        else:
            # Create Vector from x and y
            try:
                object.__setattr__(self, "_complex", complex(x, y))
            except TypeError:
                raise TypeError(
                    "x and y values must be numeric to create Vector"
                ) from None

    @classmethod
    def from_polar(cls: type[TVector], r: float, theta: float) -> TVector:
        """Create a Vector from polar coordinates."""
        return cls(cmath.rect(r, theta))

    def dot(self, other: Vector, /) -> float:
        """Return the dot product of self and other."""
        return (
            self._complex.real * other._complex.real
            + self._complex.imag * other._complex.imag
        )

    def perp_dot(self, other: Vector, /) -> float:
        """
        Return the perp dot product of self and other.

        This is the signed area of the parallelogram they define. It is
        also one of the 'cross products' that can be defined on 2D
        vectors.
        """
        return (
            self._complex.real * other._complex.imag
            - self._complex.imag * other._complex.real
        )

    def perp(self, /) -> Vector:
        """
        Return the Vector, rotated anticlockwise by pi / 2.

        This is one of the 'cross products' that can be defined on 2D
        vectors. Use -Vector.perp() for a clockwise rotation.
        """
        return Vector(self._complex * 1j)

    def rotate(self, /, angle: float) -> Vector:
        """
        Return a self, rotated by angle anticlockwise.

        Use negative angles for a clockwise rotation.
        """
        return Vector(self._complex * cmath.rect(1, angle))

    def hat(self, /) -> Vector:
        """Return a Vector with the same direction, but unit length."""
        return Vector(self._complex / abs(self._complex))

    def rec(self, /) -> tuple[float, float]:
        """Get the vector as (x, y)."""
        return (self._complex.real, self._complex.imag)

    def pol(self, /) -> tuple[float, float]:
        """Get the vector as (r, theta)."""
        return cmath.polar(self._complex)

    @overload
    def round(self, /, ndigits: None = ...) -> tuple[int, int]:
        ...

    @overload
    def round(self, /, ndigits: int) -> tuple[float, float]:
        ...

    def round(self, /, ndigits=None):
        """Get the vector with both components rounded, as a tuple."""
        return (round(self._complex.real, ndigits), round(self._complex.imag, ndigits))

    def __str__(self, /) -> str:
        return f"({self._complex.real} {self._complex.imag})"

    def __repr__(self, /) -> str:
        return (
            f"{self.__class__.__qualname__}({self._complex.real}, {self._complex.imag})"
        )

    def __len__(self, /) -> Literal[2]:
        return 2

    def __getitem__(self, key: int, /) -> float:
        return self.rec()[key]

    def __iter__(self, /) -> Iterator[float]:
        yield self._complex.real
        yield self._complex.imag

    def __reversed__(self, /) -> Iterator[float]:
        yield self._complex.imag
        yield self._complex.real

    def __neg__(self, /) -> Vector:
        return Vector(-self._complex)

    def __add__(self, other: Vector, /) -> Vector:
        return Vector(self._complex + other._complex)

    def __sub__(self, other: Vector, /) -> Vector:
        return Vector(self._complex - other._complex)

    def __mul__(self, value: float, /) -> Vector:
        return Vector(self._complex * value)

    def __truediv__(self, value: float, /) -> Vector:
        return Vector(self._complex / value)

    __rmul__ = __mul__

    def __abs__(self, /) -> float:
        return abs(self._complex)

    @property
    def x(self) -> float:
        """The horizontal component of the vector."""
        return self._complex.real

    @property
    def y(self) -> float:
        """The vertical component of the vector."""
        return self._complex.imag

    @property
    def r(self) -> float:
        """The radius of the vector."""
        return abs(self._complex)

    @property
    def theta(self) -> float:
        """
        The angle of the vector, anticlockwise from the horizontal.

        Negative values are clockwise. Returns values in the range
        [-pi, pi]. See documentation of cmath.phase for details.
        """
        return cmath.phase(self._complex)
