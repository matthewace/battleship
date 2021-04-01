from typing import Iterable, Iterator, List, Optional, SupportsInt, Tuple, Union


ROW_NAMES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
COL_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

Coordinate = int
COORDINATES = [    
    A1, B1, C1, D1, E1, F1, G1, H1, I1, J1,
    A2, B2, C2, D2, E2, F2, G2, H2, I2, J2,
    A3, B3, C3, D3, E3, F3, G3, H3, I3, J3,
    A4, B4, C4, D4, E4, F4, G4, H4, I4, J4,
    A5, B5, C5, D5, E5, F5, G5, H5, I5, J5,
    A6, B6, C6, D6, E6, F6, G6, H6, I6, J6,
    A7, B7, C7, D7, E7, F7, G7, H7, I7, J7,
    A8, B8, C8, D8, E8, F8, G8, H8, I8, J8,
    A9, B9, C9, D9, E9, F9, G9, H9, I9, J9,
    AX, BX, CX, DX, EX, FX, GX, HX, IX, JX    
] = range(100)
COORDINATE_NAMES =  [c + r for r in ROW_NAMES for c in COL_NAMES]


def parse_coordinate(name: str) -> Coordinate:
    """Get coordinate value from name"""
    return COORDINATE_NAMES.index(name)

def coordinate_name(coordinate: Coordinate) -> str:
    """Get name of coordinate from tuple values"""
    return COORDINATE_NAMES[coordinate]

def coordinate_row(coordinate: Coordinate) -> int:
    """Get index of coordinate's row where ``0`` is row 1, ``9`` is row 10"""
    return int(coordinate / 10)

def coordinate_col(coordinate: Coordinate) -> int:
    """Get index of coordinate's column where ``0`` is column A."""
    return int(coordinate % 10)

def coordinate_mirror(coordinate: Coordinate) -> Coordinate:
    """Returns the index of the mirrored coordinate"""
    return 90 - 10 * coordinate_row(coordinate) + coordinate_col(coordinate)


COORDINATES_180 = [coordinate_mirror(c) for c in COORDINATES]


Bitboard = int
BB_EMPTY = 0
BB_ALL = 0x000f_ffff_ffff_ffff_ffff_ffff_ffff

BB_COORDINATES = [
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1, BB_I1, BB_J1,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2, BB_I2, BB_J2,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3, BB_I3, BB_J3,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4, BB_I4, BB_J4,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5, BB_I5, BB_J5,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6, BB_I6, BB_J6,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7, BB_I7, BB_J7,
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8, BB_I8, BB_J8,
    BB_A9, BB_B9, BB_C9, BB_D9, BB_E9, BB_F9, BB_G9, BB_H9, BB_I9, BB_J9,
    BB_AX, BB_BX, BB_CX, BB_DX, BB_EX, BB_FX, BB_GX, BB_HX, BB_IX, BB_JX
] = [1 << c for c in COORDINATES]

BB_COLS = [
    BB_COL_A,
    BB_COL_B,
    BB_COL_C,
    BB_COL_D,
    BB_COL_E,
    BB_COL_F,
    BB_COL_G,
    BB_COL_H,
    BB_COL_I,
    BB_COL_J,
] = [0x0401_0040_1004_0100_4010_0401 << i for i in range(10)]

BB_ROWS = [
    BB_ROW_1,
    BB_ROW_2,
    BB_ROW_3,
    BB_ROW_4,
    BB_ROW_5,
    BB_ROW_6,
    BB_ROW_7,
    BB_ROW_8,
    BB_ROW_9,
    BB_ROW_10,
] = [0x03ff << 10 * i for i in range(10)]

BB_PERIMETER = BB_ROW_1 | BB_ROW_10 | BB_COL_A | BB_COL_J
BB_SIDES = BB_COL_A | BB_COL_J
BB_TOP_BOTTOM = BB_ROW_1 | BB_ROW_10

def lsb(bb: Bitboard) -> int:
    """Returns least significant bit."""
    return (bb & -bb).bit_length() - 1

def scan_forward(bb: Bitboard) -> Iterator[Coordinate]:
    """Iterator of coordinates."""
    while bb:
        r = bb & -bb
        yield r.bit_length() - 1
        bb ^= r

def msb(bb: Bitboard) -> int:
    """Returns the most significant bit."""
    return bb.bit_length() - 1

def scan_reversed(bb: Bitboard) -> Iterator[Coordinate]:
    """Iterator of coordinates in reverse order."""
    while bb:
        r = bb.bit_length() - 1
        yield r
        bb ^= BB_COORDINATES[r]

def popcount(bb: Bitboard) -> int:
    """Returns number of `1`s in the Bitboard."""
    return bin(bb).count("1")

def flip_vertical(bb: Bitboard) -> Bitboard:
    """Flips the board vertically."""
    pass

def flip_horizontal(bb: Bitboard) -> Bitboard:
    """Flips the board horizontally."""
    pass

def flip_diagonal(bb: Bitboard) -> Bitboard:
    """Flips the board diagonally."""
    pass

def flip_anti_diagonal(bb: Bitboard) -> Bitboard:
    """Flips the board anti-diagonally."""
    pass


def shift_down(bb: Bitboard) -> Bitboard:
    """Shift all coordinates down one row."""
    return bb >> 10

def shift_2_down(bb: Bitboard) -> Bitboard:
    """Shift all coordinates down two rows."""
    return bb >> 20

def shift_up(bb: Bitboard) -> Bitboard:
    """Shift all coordinates up one row."""
    return (bb << 10) & BB_ALL

def shift_2_up(bb: Bitboard) -> Bitboard:
    """Shift all coordinates up two rows."""
    return (bb << 20) & BB_ALL

def shift_right(bb: Bitboard) -> Bitboard:
    """Shift all coordinates right one column."""
    pass

def shift_2_right(bb: Bitboard) -> Bitboard:
    """Shift all coordinates right two columns."""
    pass

def shift_left(bb: Bitboard) -> Bitboard:
    """Shift all coordinates left one column."""
    pass

def shift_2_left(bb: Bitboard) -> Bitboard:
    """Shift all coordinates left two columns."""
    pass

def shift_up_left(bb: Bitboard) -> Bitboard:
    """Shift all coordinates up one row and left one column."""
    pass

def shift_up_right(bb: Bitboard) -> Bitboard:
    """Shift all coordinates up one row and right one column."""
    pass

def shift_down_left(bb: Bitboard) -> Bitboard:
    """Shift all coordinates down one row and left one column."""
    pass

def shift_down_right(bb: Bitboard) -> Bitboard:
    """Shift all coordinates down one row and right one column."""
    pass


def _carry_rippler(mask):
    """Carry-Rippler iterater of mask subsets."""
    subset = gb.BB_EMPTY
    while True:
        yield subset
        subset = (subset - mask) & mask
        if not subset:
            break

def shared(a: Coordinate, b: Coordinate) -> Bitboard:
    """Tests if `a` and `b` are on the same row or column and returns the shared
    row or column.
    """
    if coordinate_col(a) == coordinate_col(b):
        return BB_COLS[coordinate_col(a)]
    elif coordinate_row(a) == coordinate_row(b):
        return BB_ROWS[coordinate_row(a)]
    else:
        return BB_EMPTY

def _rays() -> List[List[Bitboard]]:
    """Calculate all possible rays on the board.  Only rays on the same row or
    column are allowed; no diagonals.
    """
    rays = []
    for a, bb_a in enumerate(BB_COORDINATES):
        a_rays = []
        for b, bb_b in enumerate(BB_COORDINATES):
            ray = BB_EMPTY           
            for c in scan_forward(shared(a, b)):
                if min(a, b) <= c <= max(a, b):
                    ray |= BB_COORDINATES[c]
            a_rays.append(ray)
        rays.append(a_rays)
    return rays

BB_RAYS = _rays()

def ray(a: Coordinate, b: Coordinate) -> Bitboard:
    return BB_RAYS[a][b]

def between(a: Coordinate, b: Coordinate) -> Bitboard:
    bb = BB_RAYS[a][b] & ((BB_ALL << a) ^ (BB_ALL << b))
    return bb & (bb - 1)


IntoCoordinateSet = Union[SupportsInt, Iterable[Coordinate]]

class CoordinateSet:
    """A set of coordinates.
    
    >>> import bitboard
    >>>
    >>> coords = bitboard.CoordinateSet([bitboard.F3, bitboard.G4])
    >>> coords
    CoordinateSet(0x0000_0000_0000_0000_0010_0200_0000)

    >>> coords = bitboard.CoordinateSet(bitboard.BB_C7 | bitboard.BB_ROW_3)
    >>> coords
    CoordinateSet(0x0000_0000_0000_4000_0000_3ff0_0000)

    >>> print(coords)
    . . . . . . . . . .
    . . . . . . . . . .
    . . . . . . . . . .
    . . 1 . . . . . . .
    . . . . . . . . . .
    . . . . . . . . . .
    . . . . . . . . . .
    1 1 1 1 1 1 1 1 1 1
    . . . . . . . . . .
    . . . . . . . . . .

    >>> len(coords)
    11

    >>> bitboard.H3 in coords
    True

    >>> for coord in coords:
    ...     print(coord)
    ... 
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    62

    >>> list(coords)
    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 62]

    >>> int(coords)
    4611686019500081152
    """
    def __init__(self, coordinates: list) -> None:
        try:
            self.mask = coordinates & BB_ALL
            return
        except:
            self.mask = 0

        for coordinate in coordinates:
            self.add(coordinate)

    def __contains__(self, coordinate: Coordinate) -> bool:
        return bool(self.mask & BB_COORDINATES[coordinate])

    def __iter__(self) -> Iterator[Coordinate]:
        return scan_forward(self.mask)

    def __reversed__(self) -> Iterator[Coordinate]:
        return scan_reversed(self.mask)

    def __len__(self) -> int:
        return popcount(self.mask)

    def union(self, other: IntoCoordinateSet):
        return self | other

    def __or__(self, other: IntoCoordinateSet):
        try:
            other.mask |= self.mask
        except:
            other = CoordinateSet(other)
            other.mask |= self.mask
        return other
    
    def intersection(self, other: IntoCoordinateSet):
        return self & other
    
    def __and__(self, other: IntoCoordinateSet):
        try:
            other.mask &= self.mask
        except:
            other = CoordinateSet(other)
            other.mask &= self.mask
        return other
    
    def difference(self, other: IntoCoordinateSet):
        return self - other
    
    def __sub__(self, other: IntoCoordinateSet):
        try:
            other.mask = self.mask & ~other.mask
        except:
            other = CoordinateSet(other)
            other.mask = self.mask & ~other.mask
        return other

    def symmetric_difference(self, other: IntoCoordinateSet):
        return self ^ other

    def __xor__(self, other: IntoCoordinateSet):
        try:
            other.mask ^= self.mask
        except:
            other = CoordinateSet(other)
            other.mask ^= self.mask
        return other

    def copy(self):
        return CoordinateSet(self.mask)


    def update(self, *others: IntoCoordinateSet) -> None:
        for other in others:
            self |= other

    def __ior__(self, other: IntoCoordinateSet):
        try:
            self.mask |= other.mask
        except:
            self.mask |= CoordinateSet(other).mask
        return self

    def intersection_update(self, *others: IntoCoordinateSet) -> None:
        for other in others:
            self &= others

    def __iand__(self, other: IntoCoordinateSet):
        try:
            self.mask &= other.mask
        except:
            self.mask &= CoordinateSet(other).mask
        return self

    def difference_update(self, other: IntoCoordinateSet) -> None:
        self -= other

    def __isub__(self, other: IntoCoordinateSet):
        try:
            self.mask &= ~other.mask
        except:
            self.mask &= ~CoordinateSet(other).mask
        return self

    def symmetric_difference_update(self, other: IntoCoordinateSet) -> None:
        self ^= other

    def __ixor__(self, other: IntoCoordinateSet):
        try:
            self.mask ^= other.mask
        except:
            self.mask ^= CoordinateSet(other).mask


    def add(self, coordinate: Coordinate) -> None:
        """Add a coordinate to the set."""
        self.mask |= BB_COORDINATES[coordinate]

    def discard(self, coordinate: Coordinate) -> None:
        """Removes coordinate from the set."""
        self.mask &= ~BB_COORDINATES[coordinate]
    
    def remove(self, coordinate: Coordinate) -> None:
        """Remove a coordinate from the set.

        raises `KeyError` if provided coordinate is not in set.
        """
        mask = BB_COORDINATES[coordinate]
        if self.mask & mask:
            self.mask ^= mask
        else:
            raise KeyError(coordinate)

    def pop(self) -> Coordinate:
        """Remove and return the least significant bit from set.

        raises `KeyError` if set is empty.
        """
        if not self.mask:
            raise KeyError("pop from empty CoordinateSet")

        coordinate = lsb(self.mask)
        self.mask &= (self.mask - 1)
        return coordinate

    def clear(self) -> None:
        """Removes all coordinates from set."""
        self.mask = BB_EMPTY


    def carry_rippler(self) -> Iterator[Bitboard]:
        """Iterator over subsets of this set."""
        return _carry_rippler(self.mask)

    def tolist(self) -> List[bool]:
        """Convert set to a list of 100 boolean values."""
        bool_list = [False] * 100
        for coordinate in self:
            bool_list[coordinate] = True
        return bool_list

    def __bool__(self) -> bool:
        """Return True if any coordinates found in set."""
        return bool(self.mask)

    def __eq__(self, other: object) -> bool:
        try:
            return self.mask == CoordinateSet(other).mask
        except (TypeError, ValueError):
            return NotImplemented

    def __lshift__(self, shift: int):
        return CoordinateSet((self.mask << shift) & BB_ALL)

    def __rshift__(self, shift: int):
        return CoordinateSet((self.mask >> shift) & BB_ALL)

    def __ilshift__(self, shift: int):
        self.mask = (self.mask << shift) & BB_ALL
        return self

    def __irshift__(self, shift: int):
        self.mask = (self.mask >> shift) & BB_ALL
        return self

    def __invert__(self):
        return CoordinateSet(~self.mask & BB_ALL)

    def __int__(self) -> int:
        return self.mask

    def __index__(self) -> int:
        return self.mask

    def __repr__(self) -> str:
        return f'CoordinateSet({self.mask:#036_x})'

    def __str__(self) -> str:
        out = ''

        for coord in COORDINATES_180:
            mask = BB_COORDINATES[coord]
            out += '1' if self.mask & mask else '.'

            if not mask & BB_COL_J:
                out += ' '
            elif coord != J1:
                out += '\n'

        return out

    @classmethod
    def ray(cls, a: Coordinate, b: Coordinate):
        """All coordinates on a row or column between and including the two
        input value coordinates (if they are aligned).

        >>> import bitboard
        >>> print(bitboard.CoordinateSet.ray(bitboard.C4, bitboard.F4))
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . 1 1 1 1 . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        """
        return cls(ray(a, b))

    @classmethod
    def between(cls, a: Coordinate, b: Coordinate):
        """All coordinates on a row or column between but excluding the two 
        input value coordinates (if they are aligned).

        >>> import bitboard
        >>> print(bitboard.CoordinateSet.between(bitboard.C4, bitboard.F4))
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . 1 1 . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        . . . . . . . . . .
        """
        return cls(between(a, b))

    @classmethod
    def from_coordinate(cls, coordinate: Coordinate):
        """Creates a <class `bitboard.CoordinateSet`> from a single coordinate.

        >>> import bitboard
        >>> bitboard.CoordinateSet.from_coordinate(bitboard.H4) == bitboard.BB_H4
        True
        """
        return cls(BB_COORDINATES[coordinate])
