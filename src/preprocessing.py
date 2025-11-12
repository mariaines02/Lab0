"""
Data preprocessing module with various data transformation functions.
"""

import math
import random
import re
from typing import List, Any, Union


def remove_missing(values: List[Any]) -> List[Any]:
    """
    Remove missing values from a list.

    Args:
        values: List containing values and missing values (None, '', nan)

    Returns:
        List with missing values removed
    """
    result = []
    for val in values:
        if val is None or val == "":
            continue
        # Check for nan
        if isinstance(val, float) and math.isnan(val):
            continue
        result.append(val)
    return result


def fill_missing(values: List[Any], fill_value: Any = 0) -> List[Any]:
    """
    Fill missing values with a specified value.

    Args:
        values: List containing values and missing values
        fill_value: Value to replace missing values with (default: 0)

    Returns:
        List with missing values replaced
    """
    result = []
    for val in values:
        if val is None or val == "":
            result.append(fill_value)
        elif isinstance(val, float) and math.isnan(val):
            result.append(fill_value)
        else:
            result.append(val)
    return result


def remove_duplicates(values: List[Any]) -> List[Any]:
    """
    Remove duplicate values from a list while preserving order.

    Args:
        values: List of values

    Returns:
        List of unique values
    """
    seen = set()
    result = []
    for val in values:
        if val not in seen:
            seen.add(val)
            result.append(val)
    return result


def normalize(
    values: List[float], new_min: float = 0.0, new_max: float = 1.0
) -> List[float]:
    """
    Normalize numerical values using min-max scaling.

    Args:
        values: List of numerical values
        new_min: New minimum value (default: 0.0)
        new_max: New maximum value (default: 1.0)

    Returns:
        List of normalized values
    """
    if not values:
        return []

    old_min = min(values)
    old_max = max(values)

    if old_min == old_max:
        return [new_min] * len(values)

    result = []
    for val in values:
        normalized = ((val - old_min) / (old_max - old_min)) * (
            new_max - new_min
        ) + new_min
        result.append(normalized)
    return result


def standardize(values: List[float]) -> List[float]:
    """
    Standardize numerical values using z-score method.

    Args:
        values: List of numerical values

    Returns:
        List of standardized values
    """
    if not values:
        return []

    mean_val = sum(values) / len(values)
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return [0.0] * len(values)

    return [(val - mean_val) / std_dev for val in values]


def clip_values(values: List[float], min_val: float, max_val: float) -> List[float]:
    """
    Clip numerical values to a specified range.

    Args:
        values: List of numerical values
        min_val: Minimum value to clip
        max_val: Maximum value to clip

    Returns:
        List of clipped values
    """
    result = []
    for val in values:
        if val < min_val:
            result.append(min_val)
        elif val > max_val:
            result.append(max_val)
        else:
            result.append(val)
    return result


def convert_to_int(values: List[str]) -> List[int]:
    """
    Convert string values to integers, excluding non-numerical values.

    Args:
        values: List of strings

    Returns:
        List of integers (non-numerical values excluded)
    """
    result = []
    for val in values:
        try:
            result.append(int(float(val)))
        except (ValueError, TypeError):
            continue
    return result


def log_transform(values: List[float]) -> List[float]:
    """
    Transform values to logarithmic scale.

    Args:
        values: List of numerical values

    Returns:
        List of log-transformed values (only positive numbers)
    """
    result = []
    for val in values:
        if val > 0:
            result.append(math.log(val))
    return result


def tokenize_text(text: str) -> str:
    """
    Tokenize text into words, keeping only alphanumeric characters and lowercasing.

    Args:
        text: Text to be processed

    Returns:
        Processed text with tokens separated by spaces
    """
    tokens = re.findall(r"\w+", text.lower())
    return " ".join(tokens)


def remove_punctuation(text: str) -> str:
    """
    Remove punctuation from text, keeping only alphanumeric characters and spaces.

    Args:
        text: Text to be processed

    Returns:
        Processed text
    """
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def remove_stopwords(text: str, stop_words: List[str]) -> str:
    """
    Remove stop words from text.

    Args:
        text: Text to be processed (should be lowercased)
        stop_words: List of stop words to remove

    Returns:
        Processed text with stop words removed
    """
    words = text.lower().split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Flatten a list of lists.

    Args:
        nested_list: A list of lists

    Returns:
        A flattened list
    """
    result = []
    for sublist in nested_list:
        result.extend(sublist)
    return result


def shuffle_list(values: List[Any], seed: Union[int, None] = None) -> List[Any]:
    """
    Randomly shuffle a list of values.

    Args:
        values: List of values
        seed: Seed for reproducibility (default: None)

    Returns:
        Shuffled list
    """
    result = values.copy()
    if seed is not None:
        random.seed(seed)
    random.shuffle(result)
    return result
