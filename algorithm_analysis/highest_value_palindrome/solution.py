"""
Palindromes are strings that read the same from the left or right, for example madam or
0110.

You will be given a string representation of a number and a maximum number of changes
you can make.
Alter the string, one digit at a time, to create the string representation of the
largest number possible given the limit to the number of changes.
The length of the string may not be altered, so you must consider 0's left of all
higher digits in your tests. For example 0110 is valid, 0011 is not.

Given a string representing the starting number and a maximum number of changes allowed,
create the largest palindromic string of digits possible or the string -1 if it's
impossible to create a palindrome under the contstraints.
"""
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class StrTriplet:
    left: str
    middle: str
    right: str
    changes: int


# optimal solution


def highest_value_palindrome_optimal(string: str, max_changes: int) -> str:
    orig_triplet = StrTriplet(left="", middle=string, right="", changes=max_changes)
    pali_triplet, changes_map = palindromify_triplet(orig_triplet)
    if pali_triplet is None:
        return "-1"
    return triplet_to_string(maximise_triplet(reset_triplet(pali_triplet), changes_map))


def palindromify_triplet(triplet: StrTriplet) -> Tuple[Optional[StrTriplet], List[int]]:
    changes_map = []
    pali_triplet = triplet
    for _ in range(len(pali_triplet.middle) + 1):
        if pali_triplet.changes < 0:
            return None, changes_map
        if len(pali_triplet.middle) == 0:
            return pali_triplet, changes_map
        if len(pali_triplet.middle) == 1:
            changes_map.append(0)
            return pali_triplet, changes_map
        # at least 2 chars in `middle` and `changes` is at least 0
        pali_triplet, changes_made = palindromify_one_pair(pali_triplet)
        changes_map.append(changes_made)
        continue
    raise ValueError()


def palindromify_one_pair(triplet: StrTriplet) -> Tuple[StrTriplet, int]:
    left_char, middle, right_char = (
        triplet.middle[0],
        triplet.middle[1:-1],
        triplet.middle[-1],
    )
    if left_char == right_char:
        return (
            StrTriplet(
                left=triplet.left + left_char,
                middle=middle,
                right=right_char + triplet.right,
                changes=triplet.changes,
            ),
            0,
        )
    new_char = left_char if left_char > right_char else right_char
    return (
        StrTriplet(
            left=triplet.left + new_char,
            middle=middle,
            right=new_char + triplet.right,
            changes=triplet.changes - 1,
        ),
        1,
    )


def reset_triplet(triplet: StrTriplet) -> StrTriplet:
    return StrTriplet(
        left="",
        middle=triplet.left + triplet.middle + triplet.right,
        right="",
        changes=triplet.changes,
    )


def maximise_triplet(triplet: StrTriplet, changes_map: List[int]) -> StrTriplet:
    max_triplet = triplet
    for changes_made in changes_map:
        if max_triplet.changes < 0:
            raise ValueError()
        if len(max_triplet.middle) == 0 or max_triplet.changes == 0:
            return max_triplet
        if len(max_triplet.middle) == 1 and triplet.changes + changes_made >= 1:
            return StrTriplet(
                left=max_triplet.left,
                middle="9",
                right=max_triplet.right,
                changes=triplet.changes + changes_made - 1,
            )
        # at least 2 chars in `middle` and `changes` is at least 1
        max_triplet = maximise_one_pair(max_triplet, changes_made)
        continue
    return max_triplet


def maximise_one_pair(triplet: StrTriplet, changes_made: int) -> StrTriplet:
    """
    Invariants:
        - triplet strings form a palindrome
        - triplet.changes >= 1
    """
    left_char, middle, right_char = (
        triplet.middle[0],
        triplet.middle[1:-1],
        triplet.middle[-1],
    )
    if triplet.changes + changes_made == 1 or left_char == right_char == "9":
        return StrTriplet(
            left=triplet.left + left_char,
            middle=middle,
            right=right_char + triplet.right,
            changes=triplet.changes,
        )
    return StrTriplet(
        left=triplet.left + "9",
        middle=middle,
        right="9" + triplet.right,
        changes=triplet.changes + changes_made - 2,
    )


def triplet_to_string(triplet: StrTriplet) -> str:
    return triplet.left + triplet.middle + triplet.right


# suboptimal solution


def highest_value_palindrome_suboptimal(string: str, max_changes: int) -> str:
    """
    Main function of the solution

    :param string: a string representation of an integer
    :param max_changes: an integer that represents the maximum number of changes allowed
    """
    return process_str_triplet(
        StrTriplet(left="", middle=string, right="", changes=max_changes)
    )


def process_str_triplet(triplet: StrTriplet) -> str:
    to_do = [triplet]
    while len(to_do):
        triplet = to_do.pop()
        if triplet.changes < 0:
            continue
        if triplet.changes == 0:
            if is_palindrome(triplet.middle):
                return triplet.left + triplet.middle + triplet.right
            continue
        if len(triplet.middle) == 0:
            return triplet.left + triplet.right
        if len(triplet.middle) == 1:
            return triplet.left + "9" + triplet.right
        if len(triplet.middle) >= 2:
            to_do.extend(split_string(triplet))
            continue
        raise ValueError()
    return "-1"


def split_string(triplet: StrTriplet) -> List[StrTriplet]:
    """
    Depth-first search

    Invariant: triplet.middle has at least 2 elements

    Append the move with the most changes (2) to the top of the stack,
    followed by the move with 1 change, and finally no changes.
    If popped from the top, this algorithm will be the fastest to exhaust
    all moves (greedy).
    """
    to_do = []
    left_char, middle, right_char = (
        triplet.middle[0],
        triplet.middle[1:-1],
        triplet.middle[-1],
    )
    if left_char == right_char:
        to_do.append(
            StrTriplet(
                left=triplet.left + left_char,
                middle=middle,
                right=right_char + triplet.right,
                changes=triplet.changes,
            )
        )
    if left_char != right_char:
        new_char = left_char if left_char > right_char else right_char
        to_do.append(
            StrTriplet(
                left=triplet.left + new_char,
                middle=middle,
                right=new_char + triplet.right,
                changes=triplet.changes - 1,
            )
        )
    if left_char != "9" and right_char != "9":
        to_do.append(
            StrTriplet(
                left=triplet.left + "9",
                middle=middle,
                right="9" + triplet.right,
                changes=triplet.changes - 2,
            )
        )
    return to_do


def is_palindrome(string: str) -> bool:
    half = int(len(string) // 2)
    for idx, (a, b) in enumerate(zip(string, reversed(string))):
        if idx == half:
            return True
        if a != b:
            return False
    return True
