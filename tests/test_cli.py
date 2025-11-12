"""
Integration tests for CLI module.
"""
import pytest
from click.testing import CliRunner
from src.cli import cli


@pytest.fixture
def runner():
    """Fixture to create a CliRunner instance."""
    return CliRunner()


def test_cli_clean_remove_missing(runner):
    """Test CLI clean remove-missing command."""
    result = runner.invoke(cli, ['clean', 'remove-missing', '1', '2', 'None', '3'])
    assert result.exit_code == 0
    assert '1' in result.output


def test_cli_clean_fill_missing(runner):
    """Test CLI clean fill-missing command."""
    result = runner.invoke(cli, ['clean', 'fill-missing', '1', 'None', '2', '--fill-value', '0'])
    assert result.exit_code == 0


def test_cli_numeric_normalize(runner):
    """Test CLI numeric normalize command."""
    result = runner.invoke(cli, ['numeric', 'normalize', '1', '2', '3', '4', '5'])
    assert result.exit_code == 0
    assert '0.0' in result.output
    assert '1.0' in result.output


def test_cli_numeric_normalize_with_options(runner):
    """Test CLI numeric normalize with custom range."""
    result = runner.invoke(cli, ['numeric', 'normalize', '1', '2', '3', '--min', '-1', '--max', '1'])
    assert result.exit_code == 0


def test_cli_numeric_standardize(runner):
    """Test CLI numeric standardize command."""
    result = runner.invoke(cli, ['numeric', 'standardize', '1', '2', '3', '4', '5'])
    assert result.exit_code == 0


def test_cli_numeric_clip(runner):
    """Test CLI numeric clip command."""
    result = runner.invoke(cli, ['numeric', 'clip',  '--min', '0', '--max', '2', '--',  '-1', '0', '1', '2', '3'])
    assert result.exit_code == 0


def test_cli_numeric_to_int(runner):
    """Test CLI numeric to-int command."""
    result = runner.invoke(cli, ['numeric', 'to-int', '1', '2.5', '3', 'abc'])
    assert result.exit_code == 0
    assert '1' in result.output
    assert '2' in result.output


def test_cli_numeric_log(runner):
    """Test CLI numeric log command."""
    result = runner.invoke(cli, ['numeric', 'log', '1', '2', '3'])
    assert result.exit_code == 0


def test_cli_text_tokenize(runner):
    """Test CLI text tokenize command."""
    result = runner.invoke(cli, ['text', 'tokenize', 'Hello, World!'])
    assert result.exit_code == 0
    assert 'hello' in result.output
    assert 'world' in result.output


def test_cli_text_remove_punctuation(runner):
    """Test CLI text remove-punctuation command."""
    result = runner.invoke(cli, ['text', 'remove-punctuation', 'Hello, World!'])
    assert result.exit_code == 0
    assert 'Hello World' in result.output


def test_cli_text_remove_stopwords(runner):
    """Test CLI text remove-stopwords command."""
    result = runner.invoke(cli, ['text', 'remove-stopwords', 'this is a test', 
                                  '--stopwords', 'this', '--stopwords', 'is'])
    assert result.exit_code == 0
    assert 'test' in result.output


def test_cli_struct_shuffle(runner):
    """Test CLI struct shuffle command."""
    result = runner.invoke(cli, ['struct', 'shuffle', '1', '2', '3', '4', '5', '--seed', '42'])
    assert result.exit_code == 0


def test_cli_struct_shuffle_reproducibility(runner):
    """Test CLI struct shuffle reproducibility with seed."""
    result1 = runner.invoke(cli, ['struct', 'shuffle', '1', '2', '3', '--seed', '42'])
    result2 = runner.invoke(cli, ['struct', 'shuffle', '1', '2', '3', '--seed', '42'])
    assert result1.output == result2.output


def test_cli_struct_flatten(runner):
    """Test CLI struct flatten command."""
    result = runner.invoke(cli, ['struct', 'flatten', '1,2,3', '4,5,6'])
    assert result.exit_code == 0
    assert '1' in result.output


def test_cli_struct_unique(runner):
    """Test CLI struct unique command."""
    result = runner.invoke(cli, ['struct', 'unique', '1', '2', '2', '3', '3', '3'])
    assert result.exit_code == 0
    assert '1' in result.output
    assert '2' in result.output
    assert '3' in result.output