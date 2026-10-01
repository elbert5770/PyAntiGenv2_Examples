"""Run one project's simulation and write what it computes to CSV.

    python dump_simulation.py <project dir> <experiment key> <output dir> [n_rows]

With ``n_rows`` only that many evenly spaced rows (always including the first
and last) are written; the choice depends only on the number of rows, so two
runs with the same time grid write the same rows. Without it every row is
written.

The project's Model_run.py is imported (not executed as a script), its plot
function is replaced by one that writes every simulation result to
``<output dir>/<MODEL_NAME>__<label>.csv`` at full precision, and the project's
own ``setup_simulation`` is called. It therefore works unchanged for a project
written for PyAntiGen 1.x (``Engine.*``) and for 2.x (``pyantigen.engine.*``),
which is how the reference files in tests/reference were produced (from the 1.x
originals) and how they are checked (from this repository).
"""
import os
import re
import sys

import numpy as np
import pandas as pd


def safe_name(label):
    """A label as a file name ("IV Dose 36 mg/kg" -> "IV_Dose_36_mg_kg")."""
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(label)).strip("_")


def subsample(df, n_rows):
    """n_rows evenly spaced rows of df, first and last included."""
    if not n_rows or len(df) <= n_rows:
        return df
    idx = np.unique(np.linspace(0, len(df) - 1, int(n_rows)).astype(int))
    return df.iloc[idx]


def main(project_dir, key, out_dir, n_rows=None):
    project_dir = os.path.abspath(project_dir)
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    os.chdir(project_dir)
    sys.path.insert(0, project_dir)
    sys.argv = ["Model_run.py"]
    import Model_run as M

    cfg = dict(M.EXPERIMENT_dict[key])

    def dump(paths, results_dict):
        for label, item in results_dict.items():
            r = item["results"]
            df = pd.DataFrame(np.asarray(r), columns=list(r.colnames))
            subsample(df, int(n_rows) if n_rows else None).to_csv(
                os.path.join(out_dir, f"{M.MODEL_NAME}__{safe_name(label)}.csv"),
                index=False, float_format="%.17g")

    cfg["plot"] = dump
    M.update_antimony_model()
    M.setup_simulation({"run_steady_state_first": False, "Verbose": False,
                        "save_SBML?": False, "MODEL_NAME": M.MODEL_NAME,
                        "REPO_ROOT": M.REPO_ROOT}, cfg)


if __name__ == "__main__":
    main(*sys.argv[1:5])
