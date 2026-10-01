# PyAntiGen 2 examples

Three published amyloid-beta / antibody models, built and simulated with
[PyAntiGen 2](https://github.com/elbert5770/PyAntiGen):

| Project | Model | What it simulates |
| --- | --- | --- |
| `Projects/Elbert_2022_PyAntiGen_v4` | Elbert 2022 | Abeta production and clearance in the CNS, with a stable-isotope labelling (SILK) experiment |
| `Projects/Bloomingdale_2021_PyAntiGen_v4` | Bloomingdale 2021 | Antibody pharmacokinetics (IV dose, 36 mg/kg) |
| `Projects/Lin_2022_PyAntiGen_v4` | Lin 2022 | Antibody binding and clearance of Abeta, including plaque |
| `Projects/Example` | (toy model) | The two-step A -> B -> C example that `pyantigen-create` generates, with optimization and identifiability demos |

These replace the separate `Elbert_2022_PyAntiGen_v4`, `Bloomingdale_2021_PyAntiGen_v4`
and `Lin_2022_PyAntiGen_v4` repositories, which ran on PyAntiGen 1.x with a copy of
the Engine in every project. Here there is one Engine, `pyantigen.engine`, from
the installed package. The model code is unchanged apart from the import paths;
see [Relationship to the 1.x repositories](#relationship-to-the-1x-repositories).

## Setup

You need **Python 3.11 or newer**. Keep one virtual environment for this
repository, inside it (`.venv/` is git-ignored). The full environment is about
0.9 GB.

### uv (recommended)

[uv](https://docs.astral.sh/uv/) installs from a shared cache, so extra
environments cost little disk space.

```bash
git clone https://github.com/elbert5770/PyAntiGenv2_Examples.git
cd PyAntiGenv2_Examples
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt     # Windows: .venv\Scripts\python
```

### venv and pip

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt              # Windows: .venv\Scripts\python
```

### conda

```bash
conda create -n pyantigen-examples python=3.12
conda activate pyantigen-examples
pip install -r requirements.txt
```

`requirements.txt` pins the versions the results below were verified with. If
you would rather use newer ones, `pip install pyantigen` alone installs the
current stack, and `python -m pytest tests` tells you whether the three models
still reproduce.

Check the installation:

```bash
.venv/bin/python -c "import pyantigen, pyantigen.engine; print(pyantigen.__version__)"
```

If a project stops with "PyAntiGen 2 ... is not installed", the wrong
environment is active. In VS Code or Cursor, select the `.venv` interpreter
(**Python: Select Interpreter**) and open this folder as the workspace.

## Running

Run from a project folder, with the environment's Python. Each project's
`MODEL_NAME` is its folder name, and `antimony_models/`, `generated/` and
`results/` are shared at the repository root, one sub-folder per model.

```bash
cd Projects/Elbert_2022_PyAntiGen_v4
python Model_run.py --simulate Elbert_2022       # figures to results/Elbert_2022_PyAntiGen_v4/

cd ../Bloomingdale_2021_PyAntiGen_v4
python Model_run.py --simulate Bloomingdale

cd ../Lin_2022_PyAntiGen_v4
python Model_run.py --simulate Lin
```

`Model_run.py` regenerates the Antimony model first (`Model_generate.py` does
only that). Reactions and rules are written to `antimony_models/<Model>/`;
parameters, initial conditions, manual rules and events live there too and are
yours to edit. The complete generated set is also written to `generated/<Model>/`.

`Projects/Example` has the optimization demos (`python Model_run.py --optimize
Example1` ... `Example5`) described in the
[PyAntiGen README](https://github.com/elbert5770/PyAntiGen#readme).

None of the three models defines an optimization. To fit one, add an
`Optimization` to its `Modules/Optimizer_settings.py`, following
`Projects/Example`.

## Tests

```bash
python -m pytest tests
```

`tests/test_matches_pyantigen_1x.py` runs each model here and compares the whole
time course with `tests/reference/`, which is what the same model produced on
PyAntiGen 1.x. It works on a temporary copy, so the repository is not modified.
`tools/dump_simulation.py` is the script that wrote both sides.

## Relationship to the 1.x repositories

Moving a project to PyAntiGen 2 changed:

* `from framework.<module> import ...` is now `from pyantigen.generate.<module> import ...`.
* `from Engine.<module> import ...` is now `from pyantigen.engine.<module> import ...`,
  and the `Engine/` folders are gone.
* `Model_run.py` passes `REPO_ROOT` to the Engine, and `AntiGen_paths.py` is the
  2.x version, which refuses to run without `pyantigen.engine` or with a local
  `Engine/` folder.
* The regenerated Antimony writes constant compartment volumes as
  `compartment X := V_X` where 1.x wrote `compartment X = V_X`. This has no effect on
  the results.

The simulations were compared at full precision, on identical dependency
versions: Elbert 2022 and Bloomingdale 2021 agree to floating-point round-off
(identical in the full comparison; later runs differ in the 14th digit at most).
Lin 2022 agrees to a relative difference of about 1e-8 (largest 5.5e-8, against a
solver tolerance of 1e-6): the generated model is identical, but the 2.x Engine floors the
per-species absolute tolerances and clamps numerical dust, which nudges the
adaptive integrator for a model whose species span twenty orders of magnitude.

## License

MIT; see [LICENSE](LICENSE).
