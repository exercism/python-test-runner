"""
Run tests on the test runner itself.
"""
import json
import subprocess
import tempfile
from pathlib import Path

import pytest

from runner import run_tests

ROOT = Path(__file__).parent
RUNNER = ROOT.joinpath("..", "bin", "run.sh").resolve(strict=True)

STYLE_TEST = ROOT.joinpath("traceback-styles/traceback_styles_test.py")
TESTS = sorted(ROOT.glob("example*/example*_test.py"))


def run_in_subprocess(test_path, golden_path, args=None):
    """
    Run given tests against the given golden file.
    """
    exercise_dir = test_path.parent
    exercise_name = exercise_dir.name
    args = ["--color=no"] + (args or [])
    with tempfile.TemporaryDirectory(prefix="test-runner-tests") as tmp_dir:
        subprocess.run([RUNNER, exercise_name, exercise_dir, tmp_dir] + args, env={}, shell=True)
        results = Path(tmp_dir).joinpath("results.json").resolve(strict=True)
        return json.loads(results.read_text()), json.loads(golden_path.read_text())


@pytest.fixture(params=TESTS)
def test_with_golden(request):
    """
    Path to a test and its golden file.
    """
    path = request.param
    golden = path.parent.joinpath("results.json").resolve(strict=True)
    return path, golden


def test_results_matches_golden_file(test_with_golden):
    """
    Test that the results of a run matches the golden file.
    """
    results, golden = run_in_subprocess(*test_with_golden)
    assert results == golden


# the below are the --tb=STYLE options for traceback styling, see pytest -h
@pytest.fixture(params="long/short/line/native/no".split("/"))
def style_test_and_golden(request):
    """
    Path to a style's test and its golden file.
    """
    style = request.param
    golden = STYLE_TEST.parent.joinpath(f"results.{style}.json").resolve(strict=True)
    return style, STYLE_TEST, golden


def test_style_matches_golden_file(style_test_and_golden):
    """
    Test the various traceback styles generate correctly.
    """
    style, test_file, golden_file = style_test_and_golden
    results, golden = run_in_subprocess(test_file, golden_file, args=[f"--tb={style}"])
    assert results == golden