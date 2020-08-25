import pytest

from solution import (
    StrTriplet,
    is_palindrome,
    split_string,
    highest_value_palindrome_suboptimal,
)


class Test_is_palindrome:
    @pytest.mark.parametrize("string", ["", "a", "aa", "aba", "abba"])
    def test_true(self, string):
        assert is_palindrome(string)

    @pytest.mark.parametrize("string", ["ab", "bba", "abaa"])
    def test_false(self, string):
        assert not is_palindrome(string)


class Test_split_string:
    def test_1_99_1_(self):
        triplet = StrTriplet(left="1", middle="99", right="1", changes=3)
        to_do = split_string(triplet)
        assert to_do == [StrTriplet(left="19", middle="", right="91", changes=3)]

    def test_1_29_1_(self):
        triplet = StrTriplet(left="1", middle="29", right="1", changes=3)
        to_do = split_string(triplet)
        assert to_do == [StrTriplet(left="19", middle="", right="91", changes=2)]

    def test_1_28_1_(self):
        triplet = StrTriplet(left="1", middle="28", right="1", changes=3)
        to_do = split_string(triplet)
        assert to_do == [
            StrTriplet(left="18", middle="", right="81", changes=2),
            StrTriplet(left="19", middle="", right="91", changes=1),
        ]

    def test_1_82_1_(self):
        triplet = StrTriplet(left="1", middle="82", right="1", changes=3)
        to_do = split_string(triplet)
        assert to_do == [
            StrTriplet(left="18", middle="", right="81", changes=2),
            StrTriplet(left="19", middle="", right="91", changes=1),
        ]


class Test_highest_value_palindrome_suboptimal:
    def test_9389_0(self):
        assert highest_value_palindrome_suboptimal("9389", 0) == "-1"

    def test_9389_1(self):
        assert highest_value_palindrome_suboptimal("9389", 1) == "9889"

    def test_9389_2(self):
        assert highest_value_palindrome_suboptimal("9389", 2) == "9999"

    def test_9389_3(self):
        assert highest_value_palindrome_suboptimal("9389", 3) == "9999"

    def test_0011_1(self):
        assert highest_value_palindrome_suboptimal("0011", 1) == "-1"
