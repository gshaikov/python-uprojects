test:
	PYTHONPATH=highest_value_palindrome python -m pytest highest_value_palindrome -vv

benchmark:
	PYTHONPATH=highest_value_palindrome python -c "from benchmarking import run; run($(n))"

benchmark_bigfile:
	PYTHONPATH=highest_value_palindrome python -c "from benchmarking import run_bigfile; run_bigfile()"
