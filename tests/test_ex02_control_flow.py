from exercises.ex02_control_flow import classify, first_primes, fizzbuzz, index_of_first_negative


def test_fizzbuzz_small():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_fizzbuzz_fifteen():
    result = fizzbuzz(15)
    assert result[14] == "FizzBuzz"
    assert result[2] == "Fizz"
    assert result[9] == "Buzz"
    assert len(result) == 15


def test_fizzbuzz_non_positive_is_empty():
    assert fizzbuzz(0) == []
    assert fizzbuzz(-3) == []


def test_classify_special_values():
    assert classify(None) == "nothing"
    assert classify(True) == "boolean"
    assert classify(False) == "boolean"
    assert classify(0) == "zero"


def test_classify_regular_values():
    assert classify(7) == "integer"
    assert classify(-7) == "integer"
    assert classify("hi") == "text"
    assert classify([1, 2]) == "sequence"
    assert classify((1, 2)) == "sequence"
    assert classify({"a": 1}) == "unknown"
    assert classify(3.14) == "unknown"


def test_first_primes():
    assert first_primes(5) == [2, 3, 5, 7, 11]
    assert first_primes(1) == [2]
    assert first_primes(0) == []
    assert first_primes(15)[-1] == 47


def test_index_of_first_negative_found():
    assert index_of_first_negative([3, 0, -2, -5]) == 2
    assert index_of_first_negative([-1]) == 0


def test_index_of_first_negative_not_found():
    assert index_of_first_negative([1, 2]) is None
    assert index_of_first_negative([]) is None
