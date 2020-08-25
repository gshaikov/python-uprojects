import random
import timeit
import time
import re
from pathlib import Path
from typing import Tuple

from solution import (
    highest_value_palindrome_suboptimal,
    highest_value_palindrome_optimal,
)


TEST_DIR = Path(__file__).parent

random.seed(13)


def benchmark(benched_function, number=None) -> Tuple[int, int]:
    timer = timeit.Timer(benched_function)
    if number is None:
        n_loops, time_taken = timer.autorange()
    else:
        n_loops, time_taken = timer.timeit(number=number)
    time_per_loop_ms = round(time_taken / n_loops * 1000, 6)
    print("Loops: {}, time per loop: {} ms".format(n_loops, time_per_loop_ms))
    return n_loops, time_per_loop_ms


def run(data_length):
    """
    *data_length* is n in O(n)

    Exmaple output:
        Loops: 500, time per loop: 0.470337 ms
    """
    big_number_str = str(random.randrange(data_length, data_length * 10))
    big_number_len = len(big_number_str)

    def benched_function():
        return highest_value_palindrome_optimal(big_number_str, big_number_len)

    benchmark(benched_function)


def run_bigfile():
    with (TEST_DIR / "big_test_case" / "bigfile.txt").open() as bigfile:
        input_number = bigfile.readline()
        input_number = re.search("[0-9]+", input_number).group(0)
    with (TEST_DIR / "big_test_case" / "bigfile_answer.txt").open() as bigfile:
        output_number = bigfile.readline()
        output_number = re.search("[0-9]+", output_number).group(0)
    start = time.perf_counter()
    result = highest_value_palindrome_optimal(input_number, 21724)
    end = time.perf_counter()
    assert result == output_number
    print("Length: {}, time: {}".format(len(input_number), end - start))
