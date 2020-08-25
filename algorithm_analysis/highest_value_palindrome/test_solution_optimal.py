import pytest

from solution import (
    StrTriplet,
    palindromify_triplet,
    maximise_triplet,
    highest_value_palindrome_optimal,
)


class Test_palindromify_triplet:
    def test_0(self):
        triplet = StrTriplet(left="", middle="0", right="", changes=1)
        pali_triplet, changes_map = palindromify_triplet(triplet)
        expected_triplet = StrTriplet(left="", middle="0", right="", changes=1)
        expected_map = [0]
        assert pali_triplet == expected_triplet
        assert changes_map == expected_map

    def test_00(self):
        triplet = StrTriplet(left="", middle="00", right="", changes=1)
        pali_triplet, changes_map = palindromify_triplet(triplet)
        expected_triplet = StrTriplet(left="0", middle="", right="0", changes=1)
        expected_map = [0]
        assert pali_triplet == expected_triplet
        assert changes_map == expected_map

    def test_01(self):
        triplet = StrTriplet(left="", middle="01", right="", changes=1)
        pali_triplet, changes_map = palindromify_triplet(triplet)
        expected_triplet = StrTriplet(left="1", middle="", right="1", changes=0)
        expected_map = [1]
        assert pali_triplet == expected_triplet
        assert changes_map == expected_map

    def test_001(self):
        triplet = StrTriplet(left="", middle="001", right="", changes=1)
        pali_triplet, changes_map = palindromify_triplet(triplet)
        expected_triplet = StrTriplet(left="1", middle="0", right="1", changes=0)
        expected_map = [1, 0]
        assert pali_triplet == expected_triplet
        assert changes_map == expected_map


class Test_maximise_triplet:
    def test_0_1_0(self):
        triplet = StrTriplet(left="", middle="0", right="", changes=1)
        changes_map = [0]
        max_triplet = maximise_triplet(triplet, changes_map)
        expected = StrTriplet(left="", middle="9", right="", changes=0)
        assert max_triplet == expected

    def test_0_0_0(self):
        triplet = StrTriplet(left="", middle="0", right="", changes=0)
        changes_map = [0]
        max_triplet = maximise_triplet(triplet, changes_map)
        expected = StrTriplet(left="", middle="0", right="", changes=0)
        assert max_triplet == expected

    def test_00_1_0(self):
        triplet = StrTriplet(left="", middle="00", right="", changes=1)
        changes_map = [0]
        max_triplet = maximise_triplet(triplet, changes_map)
        expected = StrTriplet(left="0", middle="", right="0", changes=1)
        assert max_triplet == expected

    def test_00_1_1(self):
        triplet = StrTriplet(left="", middle="00", right="", changes=1)
        changes_map = [1]
        max_triplet = maximise_triplet(triplet, changes_map)
        expected = StrTriplet(left="9", middle="", right="9", changes=0)
        assert max_triplet == expected

    def test_000000_5_000(self):
        triplet = StrTriplet(left="", middle="000000", right="", changes=5)
        changes_map = [0, 0, 0]
        max_triplet = maximise_triplet(triplet, changes_map)
        expected = StrTriplet(left="990", middle="", right="099", changes=1)
        assert max_triplet == expected

    def test_000000_5_001(self):
        triplet = StrTriplet(left="", middle="000000", right="", changes=5)
        changes_map = [0, 0, 1]
        max_triplet = maximise_triplet(triplet, changes_map)
        expected = StrTriplet(left="999", middle="", right="999", changes=0)
        assert max_triplet == expected

    def test_000000_6_000(self):
        triplet = StrTriplet(left="", middle="000000", right="", changes=6)
        changes_map = [0, 0, 0]
        max_triplet = maximise_triplet(triplet, changes_map)
        expected = StrTriplet(left="999", middle="", right="999", changes=0)
        assert max_triplet == expected


class Test_highest_value_palindrome_optimal:
    def test_9389_0(self):
        assert highest_value_palindrome_optimal("9389", 0) == "-1"

    def test_9389_1(self):
        assert highest_value_palindrome_optimal("9389", 1) == "9889"

    def test_9389_2(self):
        assert highest_value_palindrome_optimal("9389", 2) == "9999"

    def test_9389_3(self):
        assert highest_value_palindrome_optimal("9389", 3) == "9999"

    def test_0011_1(self):
        assert highest_value_palindrome_optimal("0011", 1) == "-1"
