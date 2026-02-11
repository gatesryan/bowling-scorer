from dataclasses import dataclass
from typing import Literal

type Roll = int | Literal["/", "X"]
type FrameKind = Literal["open", "spare", "strike"]

STRIKE_VALUE = 10

@dataclass(frozen=True)
class Frame:
    """Represents one parsed frame and the bonus information needed to score it."""
    kind: FrameKind
    first: Roll
    second: Roll | None
    bonus_rolls_needed: int
    roll_start_index: int
