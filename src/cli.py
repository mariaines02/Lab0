"""
Command Line Interface for data preprocessing functions.
"""

import click
from src.preprocessing import (
    remove_missing,
    fill_missing,
    remove_duplicates,
    normalize,
    standardize,
    clip_values,
    convert_to_int,
    log_transform,
    tokenize_text,
    remove_punctuation,
    remove_stopwords,
    flatten_list,
    shuffle_list,
)


@click.group()
def cli():
    """Data preprocessing CLI tool."""


@cli.group()
def clean():
    """Commands for data cleaning operations."""


@cli.group()
def numeric():
    """Commands for numerical data operations."""


@cli.group()
def text():
    """Commands for text processing operations."""


@cli.group()
def struct():
    """Commands for data structure operations."""


@clean.command("remove-missing")
@click.argument("values", nargs=-1)
def cmd_remove_missing(values):
    """
    Remove missing values from a list.

    Example: cli clean remove-missing 1 2 None '' 3
    """
    converted = [None if v == "None" else ("" if v == "''" else v) for v in values]
    result = remove_missing(converted)
    click.echo(result)


@clean.command("fill-missing")
@click.argument("values", nargs=-1)
@click.option("--fill-value", default="0", help="Value to fill missing values with")
def cmd_fill_missing(values, fill_value):
    """
    Fill missing values with a specified value.

    Example: cli clean fill-missing 1 2 None '' 3 --fill-value 0
    """
    converted = [None if v == "None" else ("" if v == "''" else v) for v in values]
    result = fill_missing(converted, fill_value)
    click.echo(result)


@numeric.command("normalize")
@click.argument("values", nargs=-1, type=float)
@click.option("--min", "new_min", default=0.0, help="New minimum value")
@click.option("--max", "new_max", default=1.0, help="New maximum value")
def cmd_normalize(values, new_min, new_max):
    """
    Normalize numerical values using min-max scaling.

    Example: cli numeric normalize 1 2 3 4 5 --min 0 --max 1
    """
    result = normalize(list(values), new_min, new_max)
    click.echo(result)


@numeric.command("standardize")
@click.argument("values", nargs=-1, type=float)
def cmd_standardize(values):
    """
    Standardize numerical values using z-score method.

    Example: cli numeric standardize 1 2 3 4 5
    """
    result = standardize(list(values))
    click.echo(result)


@numeric.command("clip")
@click.option("--min", "min_val", default=0.0, help="Minimum value to clip")
@click.option("--max", "max_val", default=1.0, help="Maximum value to clip")
@click.argument("values", nargs=-1, type=float)
def cmd_clip(min_val, max_val, values):
    """
    Clip numerical values to a specified range.

    Example: cli numeric clip --min 0 --max 2 -- -1 0 1 2 3
    """
    result = clip_values(list(values), min_val, max_val)
    click.echo(result)


@numeric.command("to-int")
@click.argument("values", nargs=-1)
def cmd_to_int(values):
    """
    Convert string values to integers.

    Example: cli numeric to-int 1 2.5 3 abc 4
    """
    result = convert_to_int(list(values))
    click.echo(result)


@numeric.command("log")
@click.argument("values", nargs=-1, type=float)
def cmd_log(values):
    """
    Transform values to logarithmic scale.

    Example: cli numeric log 1 2 3 4 5
    """
    result = log_transform(list(values))
    click.echo(result)


@text.command("tokenize")
@click.argument("text")
def cmd_tokenize(text):
    """
    Tokenize text into words.

    Example: cli text tokenize "Hello, World! This is a TEST."
    """
    result = tokenize_text(text)
    click.echo(result)


@text.command("remove-punctuation")
@click.argument("text")
def cmd_remove_punctuation(text):
    """
    Remove punctuation from text.

    Example: cli text remove-punctuation "Hello, World!"
    """
    result = remove_punctuation(text)
    click.echo(result)


@text.command("remove-stopwords")
@click.argument("text")
@click.option("--stopwords", multiple=True, help="Stop words to remove")
def cmd_remove_stopwords(text, stopwords):
    """
    Remove stop words from text.

    Example: cli text remove-stopwords "this is a test" --stopwords this --stopwords is
    """
    result = remove_stopwords(text, list(stopwords))
    click.echo(result)


@struct.command("shuffle")
@click.argument("values", nargs=-1)
@click.option("--seed", default=None, type=int, help="Seed for reproducibility")
def cmd_shuffle(values, seed):
    """
    Randomly shuffle a list of values.

    Example: cli struct shuffle 1 2 3 4 5 --seed 42
    """
    result = shuffle_list(list(values), seed)
    click.echo(result)


@struct.command("flatten")
@click.argument("lists", nargs=-1)
def cmd_flatten(lists):
    """
    Flatten a list of lists.

    Example: cli struct flatten 1,2,3 4,5,6
    """
    nested = [item.split(",") for item in lists]
    result = flatten_list(nested)
    click.echo(result)


@struct.command("unique")
@click.argument("values", nargs=-1)
def cmd_unique(values):
    """
    Get unique values from a list.

    Example: cli struct unique 1 2 2 3 3 3 4
    """
    result = remove_duplicates(list(values))
    click.echo(result)


if __name__ == "__main__":
    cli()
