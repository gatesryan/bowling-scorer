from .bowling_types import Roll, Frame, STRIKE_VALUE

def parse_frames(rolls: list[Roll]) -> list[Frame]:
    """Parse a roll sequence into up to 10 `Frame` objects."""
    frames = []

    i = 0

    while i < len(rolls) and len(frames) < 10:
        current_roll = get_roll(rolls, i)
        next_roll = get_roll(rolls, i + 1)

        if current_roll is None:
            break
        

        if is_strike(current_roll):
            frames.append(Frame("strike", current_roll, None, 2, i))
            i += 1
        elif next_roll is not None and is_spare(next_roll):
            frames.append(Frame("spare", current_roll, next_roll, 1, i))
            i += 2
        else:
            frames.append(Frame("open", current_roll, next_roll, 0, i))
            i += 2

    return frames

def validate_rolls(rolls: list[Roll]):
    """Validate roll values and basic ordering constraints."""
    i = 0
    prev_roll = None
    for roll in rolls:
        if not is_valid_roll(roll):
            raise ValueError("Rolls must be either an integer between 0 and 10, or a string representing a spare or strike.") 
        if (prev_roll is None or is_strike(prev_roll)) and is_spare(roll):
            raise ValueError("Invalid sequence of rolls")

        prev_roll = roll
        i += 1

def get_roll_value(roll: Roll | None, prev_roll: Roll | None=None) -> int:
    """Convert a roll token into its numeric pinfall value."""
    if isinstance(roll, int):
        return roll
    elif is_strike(roll):
        return STRIKE_VALUE
    elif is_spare(roll) and prev_roll is not None and isinstance(prev_roll, int):
        return STRIKE_VALUE - prev_roll
    else:
        raise ValueError("Must provide previous roll if current roll is a spare")

def get_bonus_roll_values(frame: Frame, rolls: list[Roll]) -> list[int] | None:
    """Return bonus roll values for spare/strike frames, or `None` if incomplete."""
    roll_values = []
    if frame.kind == "strike":
        i = frame.roll_start_index + 1
        while i < len(rolls) and i <= frame.roll_start_index + frame.bonus_rolls_needed:
            roll_values.append(get_roll_value(rolls[i], rolls[i-1]))
            i += 1
    elif frame.kind == "spare":
        i = frame.roll_start_index + frame.bonus_rolls_needed + 1
        while i < len(rolls) and i <= frame.roll_start_index + frame.bonus_rolls_needed + 1:
            roll_values.append(get_roll_value(rolls[i], rolls[i - 1]))
            i += 1

    return roll_values if len(roll_values) == frame.bonus_rolls_needed else None


def get_roll(rolls, idx) -> Roll | None:
    """Safely return the roll at `idx`, or `None` if out of bounds."""
    if idx < len(rolls):
        return rolls[idx]
    else:
        return None

def is_strike(roll: Roll | None) -> bool:
    """Return `True` when the roll token represents a strike."""
    return roll == "X"

def is_spare(roll: Roll | None) -> bool:
    """Return `True` when the roll token represents a spare."""
    return roll == "/"

def is_roll_number_valid(roll: Roll) -> bool:
    """Return `True` for integer rolls between 0 and `STRIKE_VALUE`."""
    return isinstance(roll, int) and 0 <= roll <= STRIKE_VALUE

def is_valid_roll(roll: Roll) -> bool:
    """Return `True` when the roll is a strike, spare, or valid numeric roll."""
    return is_strike(roll) or is_spare(roll) or is_roll_number_valid(roll)
