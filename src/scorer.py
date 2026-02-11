from bowling_types import Roll, Frame
from helpers import validate_rolls, parse_frames, get_roll, get_roll_value, is_spare, get_bonus_roll_values

def score_game(rolls: list[Roll]) -> list[int | None]:
    validate_rolls(rolls)
    scores = []
    frames = parse_frames(rolls)

    for frame in frames:
        scores.append(score_frame(frame, rolls))

    return scores

def score_frame(frame: Frame, rolls: list[Roll]) -> int | None:
    if frame.kind == "open":
        return score_open_frame(frame)
    elif frame.kind == "spare":
        return score_spare_frame(frame, rolls)
    else:
        return score_strike_frame(frame, rolls)


def score_open_frame(frame: Frame) -> int | None:
    if isinstance(frame.first, int) and isinstance(frame.second, int):
        return frame.first + frame.second
    else:
        return None
    
def score_spare_frame(frame: Frame, rolls: list[Roll]) -> int | None:
    first_roll_val = get_roll_value(frame.first)
    second_roll_val = get_roll_value(frame.second, first_roll_val)

    bonus_roll_values = get_bonus_roll_values(frame, rolls)
    
    if bonus_roll_values is not None:
        return first_roll_val + second_roll_val + sum(bonus_roll_values)
    else:
        return None
    
def score_strike_frame(frame: Frame, rolls: list[Roll]) -> int | None:
    first_roll_val = get_roll_value(frame.first)
    bonus_roll_values = get_bonus_roll_values(frame, rolls)

    if bonus_roll_values is not None:
        return first_roll_val + sum(bonus_roll_values)
    else:
        return None


if __name__ == "__main__":
    print(score_game([4, 5, "X", 8, "/", 5, 3]))