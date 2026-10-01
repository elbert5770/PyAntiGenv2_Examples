"""The ported projects must reproduce what they computed on PyAntiGen 1.x.

``tests/reference/*.csv`` are 200 evenly spaced rows (first and last included)
of the full simulation each project produced as it stood in its ``*_PyAntiGen_v4``
repository, with that repository's own copy of the 1.x Engine, on the same
dependency versions as requirements.txt. Each test runs the project here, on
PyAntiGen 2, and compares row for row.

Elbert 2022 and Bloomingdale 2021 agree exactly. Lin 2022 agrees to about 1e-8
relative: the generated model is identical, but the 2.x Engine floors the
per-species absolute tolerances and clamps numerical dust, which changes the
adaptive integrator's step choices slightly for a model whose species span
twenty orders of magnitude. The tolerances below are far looser than that
(1e-6 relative, the solver's own setting) and far tighter than any change to
the model itself would produce.

The projects regenerate their Antimony files when they run, so each test works
on a temporary copy of the repository and leaves the working tree alone.
"""
import os
import shutil
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_ROWS = 200

# project folder, experiment key, results file written by tools/dump_simulation.py
CASES = [
    ("Elbert_2022_PyAntiGen_v4", "Elbert_2022", "Elbert_2022_PyAntiGen_v4__SILK.csv"),
    ("Bloomingdale_2021_PyAntiGen_v4", "Bloomingdale",
     "Bloomingdale_2021_PyAntiGen_v4__IV_Dose_36_mg_kg.csv"),
    ("Lin_2022_PyAntiGen_v4", "Lin", "Lin_2022_PyAntiGen_v4__Experiment_1.csv"),
]


def _scratch_copy(dst):
    """The parts of the repository a project reads and writes, without .git/results."""
    for name in ("Projects", "antimony_models", "antimony_modules", "data",
                 "pyantigen_settings.json"):
        src = os.path.join(REPO, name)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(dst, name),
                            ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy(src, dst)
    os.makedirs(os.path.join(dst, "generated"), exist_ok=True)
    os.makedirs(os.path.join(dst, "results"), exist_ok=True)


@pytest.mark.parametrize("project,key,csv", CASES, ids=[c[0] for c in CASES])
def test_simulation_matches_1x(project, key, csv, tmp_path):
    work = tmp_path / "repo"
    work.mkdir()
    _scratch_copy(str(work))
    out = tmp_path / "out"
    env = dict(os.environ, MPLBACKEND="Agg")
    proc = subprocess.run(
        [sys.executable, os.path.join(REPO, "tools", "dump_simulation.py"),
         str(work / "Projects" / project), key, str(out), str(N_ROWS)],
        capture_output=True, text=True, env=env, timeout=1800)
    assert proc.returncode == 0, proc.stdout[-2000:] + proc.stderr[-2000:]

    ref = pd.read_csv(os.path.join(REPO, "tests", "reference", csv))
    new = pd.read_csv(out / csv)
    assert list(new.columns) == list(ref.columns)
    assert new.shape == ref.shape
    a, b = ref.to_numpy(float), new.to_numpy(float)
    # a column's own scale sets the floor, so a species near zero is not held
    # to a relative tolerance it cannot meet
    atol = 1e-8 * np.abs(a).max(axis=0)
    excess = np.abs(b - a) - (atol + 1e-6 * np.abs(a))
    if (excess > 0).any():
        row, col = np.unravel_index(np.argmax(excess), excess.shape)
        pytest.fail(f"{(excess > 0).sum()} value(s) differ from the 1.x reference; "
                    f"worst: {ref.columns[col]} at row {row}, 1.x {a[row, col]!r} "
                    f"vs {b[row, col]!r}")
