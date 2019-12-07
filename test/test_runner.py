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
TESTS = sorted(ROOT.glob("example*/example*_test.py"))

@pytest.fixture(params=TESTS)
def results_with_golden(request):
    path = request.param
    golden = path.parent.joinpath("results.json").resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix="test-runner-tests") as tmpdir:
        print(" ".join(map(str, [RUNNER, path.parent.name, path.parent, tmpdir])))
        subprocess.run([RUNNER, path.parent.name, path.parent, tmpdir], env={})
        results = Path(tmpdir).joinpath("results.json").resolve(strict=True)
        return json.loads(results.read_text()), json.loads(golden.read_text())

def test_f(results_with_golden):
    results, golden = results_with_golden
    assert results == golden

