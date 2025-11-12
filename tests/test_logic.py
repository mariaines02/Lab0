"""
Unit tests for preprocessing module.
"""
import math
import pytest
from src.preprocessing import (
    remove_missing, fill_missing, remove_duplicates,
    normalize, standardize, clip_values, convert_to_int,
    log_transform, tokenize_text, remove_punctuation,
    remove_stopwords, flatten_list, shuffle_list
)


@pytest.fixture
def sample_numbers():
    """Fixture providing a sample list of numbers for testing."""
    return [1.0, 2.0, 3.0, 4.0, 5.0]


@pytest.fixture
def sample_mixed_list():
    """Fixture providing a list with missing values."""
    return [1, None, 2, '', 3, float('nan'), 4]


def test_remove_missing(sample_mixed_list):
    """Test removal of missing values."""
    result = remove_missing(sample_mixed_list)
    assert len(result) == 4
    assert result == [1, 2, 3, 4]


@pytest.mark.parametrize("values,fill_value,expected", [
    ([1, None, 2, '', 3], 0, [1, 0, 2, 0, 3]),
    ([1, None, 2], -1, [1, -1, 2]),
    (['a', None, 'b'], 'x', ['a', 'x', 'b']),
])
def test_fill_missing_parametrize(values, fill_value, expected):
    """Test filling missing values with parametrize."""
    result = fill_missing(values, fill_value)
    assert result == expected


def test_fill_missing_with_nan():
    """Test filling missing values including NaN."""
    values = [1, float('nan'), 2]
    result = fill_missing(values, 0)
    assert result == [1, 0, 2]


@pytest.mark.parametrize("values,expected", [
    ([1, 2, 2, 3, 3, 3], [1, 2, 3]),
    (['a', 'b', 'a', 'c'], ['a', 'b', 'c']),
    ([1, 1, 1, 1], [1]),
])
def test_remove_duplicates_parametrize(values, expected):
    """Test removal of duplicates with parametrize."""
    result = remove_duplicates(values)
    assert result == expected


def test_normalize(sample_numbers):
    """Test normalization with default range."""
    result = normalize(sample_numbers)
    assert result[0] == 0.0
    assert result[-1] == 1.0
    assert all(0.0 <= x <= 1.0 for x in result)


@pytest.mark.parametrize("values,new_min,new_max,expected_min,expected_max", [
    ([1.0, 2.0, 3.0, 4.0, 5.0], 0.0, 1.0, 0.0, 1.0),
    ([1.0, 2.0, 3.0, 4.0, 5.0], -1.0, 1.0, -1.0, 1.0),
    ([10.0, 20.0, 30.0], 0.0, 10.0, 0.0, 10.0),
])
def test_normalize_parametrize(values, new_min, new_max, expected_min, expected_max):
    """Test normalization with different ranges."""
    result = normalize(values, new_min, new_max)
    assert abs(result[0] - expected_min) < 1e-10
    assert abs(result[-1] - expected_max) < 1e-10


def test_normalize_empty():
    """Test normalization with empty list."""
    result = normalize([])
    assert result == []


def test_standardize(sample_numbers):
    """Test standardization."""
    result = standardize(sample_numbers)
    mean = sum(result) / len(result)
    assert abs(mean) < 1e-10


def test_standardize_constant():
    """Test standardization with constant values."""
    result = standardize([5.0, 5.0, 5.0])
    assert all(x == 0.0 for x in result)


def test_clip_values():
    """Test clipping values."""
    values = [-1.0, 0.0, 0.5, 1.0, 2.0]
    result = clip_values(values, 0.0, 1.0)
    assert result == [0.0, 0.0, 0.5, 1.0, 1.0]


@pytest.mark.parametrize("values,expected", [
    (['1', '2', '3'], [1, 2, 3]),
    (['1.5', '2.7', '3.9'], [1, 2, 3]),
    (['1', 'abc', '2', 'def', '3'], [1, 2, 3]),
    (['abc', 'def'], []),
])
def test_convert_to_int_parametrize(values, expected):
    """Test conversion to integers with parametrize."""
    result = convert_to_int(values)
    assert result == expected


def test_log_transform():
    """Test logarithmic transformation."""
    values = [1.0, math.e, math.e**2]
    result = log_transform(values)
    assert abs(result[0] - 0.0) < 1e-10
    assert abs(result[1] - 1.0) < 1e-10
    assert abs(result[2] - 2.0) < 1e-10


def test_log_transform_negative():
    """Test log transform excludes negative values."""
    values = [-1.0, 0.0, 1.0, 2.0]
    result = log_transform(values)
    assert len(result) == 2


def test_tokenize_text():
    """Test text tokenization."""
    text = "Hello, World! This is a TEST."
    result = tokenize_text(text)
    assert result == "hello world this is a test"


def test_remove_punctuation():
    """Test punctuation removal."""
    text = "Hello, World! How are you?"
    result = remove_punctuation(text)
    assert result == "Hello World How are you"


def test_remove_stopwords():
    """Test stop words removal."""
    text = "this is a test"
    stop_words = ['this', 'is', 'a']
    result = remove_stopwords(text, stop_words)
    assert result == "test"


def test_flatten_list():
    """Test list flattening."""
    nested = [[1, 2], [3, 4], [5]]
    result = flatten_list(nested)
    assert result == [1, 2, 3, 4, 5]


def test_shuffle_list_with_seed():
    """Test shuffle with seed for reproducibility."""
    values = [1, 2, 3, 4, 5]
    result1 = shuffle_list(values, seed=42)
    result2 = shuffle_list(values, seed=42)
    assert result1 == result2
    assert set(result1) == set(values)


def test_shuffle_list_without_seed():
    """Test shuffle without seed."""
    values = [1, 2, 3, 4, 5]
    result = shuffle_list(values)
    assert set(result) == set(values)
    assert len(result) == len(values)