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
from typing import List
from dataclasses import dataclass


@dataclass
class StrTriplet:
    left: str
    middle: str
    right: str
    changes: int


def highest_value_palindrome(string: str, max_changes: int) -> str:
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
