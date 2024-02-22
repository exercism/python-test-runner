"""
Run tests on the test runner itself.
"""
import json
import subprocess
import tempfile
from pathlib import Path

import pytest

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
    with tempfile.TemporaryDirectory(prefix="test-runner-tests", dir=ROOT) as tmp_dir:
        rc = subprocess.run(
            [RUNNER, exercise_name, exercise_dir, tmp_dir] + args, env={}
        ).returncode
        results = Path(tmp_dir).joinpath("results.json").resolve(strict=True)
        return json.loads(results.read_text()), json.loads(golden_path.read_text()), rc


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
    results, golden, rc = run_in_subprocess(*test_with_golden)
       
    # Ensure 'results' and 'golden' have the same structure, and 'duration' is present
    assert len(results['tests']) == len(golden['tests']), "Number of tests must match"
    for result_test, golden_test in zip(results['tests'], golden['tests']):
        assert 'duration' in result_test, "Duration key must be present"
        # Remove or ignore 'duration' for comparison
        result_test.pop('duration')
        golden_test.pop('duration', None)  # Remove duration from golden if present
    
    # Compare results and golden, ignoring duration
    assert results == golden, "Results must match the golden file, ignoring duration"
    
    assert rc == 0, f"Return code must be 0 even when errors occur: got {rc}"

# the below are the --tb=STYLE options for traceback styling, see pytest -h
@pytest.fixture(params="auto/long/short/line/native/no".split("/"))
def style(request):
    """
    Path to a style's test and its golden file. We want to verify that passing neither
    a single "--tb=STYLE" or a split "--tb STYLE" effect the result.json.
    """
    return request.param


def test_style_matches_golden_file(test_with_golden, style):
    """
    Test that --tb=STYLE arguments don't change the results.json contents.
    """
    results, golden, rc = run_in_subprocess(*test_with_golden, args=[f"--tb={style}"])
    # Ensure 'results' and 'golden' have the same structure, and 'duration' is present
    assert len(results['tests']) == len(golden['tests']), "Number of tests must match"
    for result_test, golden_test in zip(results['tests'], golden['tests']):
        assert 'duration' in result_test, "Duration key must be present"
        # Remove or ignore 'duration' for comparison
        result_test.pop('duration')
        golden_test.pop('duration', None)  # Remove duration from golden if present
    
    # Compare results and golden, ignoring duration
    assert results == golden, "Results must match the golden file, ignoring duration"
    
    assert rc == 0, f"Return code must be 0 even when errors occur: got {rc}"
