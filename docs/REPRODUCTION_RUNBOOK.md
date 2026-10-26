# Reproduction — tested Windows x64 CPU workflow

Run from the **portfolio root**. Runtime assets now default to `.runtime/` within that root. `DFDS_WORK_DIR` may explicitly point to an existing verified asset directory; no parent-of-chat-directory path is assumed. Data remains under ignored data/.

## Core environment and frozen inputs

```powershell
python -m venv .venv-core
.venv-core/Scripts/python -m pip install -r requirements-core.txt
.venv-core/Scripts/python src/download.py
```

Acquisition creates missing directories, uses the preserved 21-export catalog and checks all 24 archives against frozen audit SHA-256 values and ZIP CRC. Existing files are not overwritten. A changed source/Kaggle file fails validation rather than becoming a silent dataset substitution. If the approved ZIPs are already present, this command verifies them without source-site requests. Initial audit evidence is not rewritten.

## LAB environment without Windows registry changes

```powershell
python -m venv .runtime/runtime
.runtime/runtime/Scripts/python -m pip install -r requirements-lab-base.txt
.runtime/runtime/Scripts/python -m pip download --no-deps --dest .runtime/wheels tensorflow==2.21.0
.runtime/runtime/Scripts/python src/bootstrap_tensorflow.py
.runtime/runtime/Scripts/python src/fetch_runtime_assets.py
```

The LAB base file pins the actually installed environment excluding TensorFlow, so a MAX_PATH error cannot interrupt unrelated package installation. The workspace-only fallback extracts the official TensorFlow Python runtime/libraries and metadata, omitting only custom-C++-operator headers. It does not modify system Python or the registry. Custom C++ operator compilation is unsupported. Use an ordinary working TensorFlow installation instead when available. Wheel hash/omission counts are recorded.

The asset fetcher uses manifest-pinned FLAN-T5-small files, portable Temurin Java 17 and the GlobalMentor pure-Java filesystem adapter. All files are SHA-256 verified. `--offline` verifies existing assets. No model endpoint or remote code is used. The pinned Java runtime is Windows x64; other operating systems need their own Java/runtime setup and are not claimed tested here.

## Full computation followed by tests

```powershell
.venv-core/Scripts/python src/run_pipeline.py --core-python .venv-core/Scripts/python.exe --lab-python .runtime/runtime/Scripts/python.exe --assets .runtime --include-download-check
.venv-core/Scripts/python -m unittest discover -s tests -v
```

The runner actually executes the four projects, supplemental population/relational reviews, numeric HTTP smoke, RAG, Spark/Parquet, TensorFlow and local CFPB LLM diagnostic. It sets the Java and Spark-worker paths, separates the two Python environments, retains command logs and stops on nonzero exit. It does not install software, publish, provision cloud or claim a Docker run.

Full artifact tests require LAB outputs, including local Parquet; they are **not a first-step core-only test**. Before full computation, use the smaller code/API suite:

```powershell
.venv-core/Scripts/python -m unittest tests.test_production tests.test_api_ci -v
```

Data audits need not be repeated. Metro reuses the included public audit-prepared medians and checks raw timestamp coverage; original preparation code remains available in audit.py. The review archive includes approved public aggregates/derived evidence, but no raw data or private complaint/model files. CFPB cache provenance checks source and cache SHA-256 and the sampling rule. A fresh tree reconstructs the sample from raw ZIPs. Text, IDs, vocabulary and fitted models remain in ignored data/processed.

## Editorial output and concrete notebooks

```powershell
.venv-core/Scripts/python -m pip install -r requirements-editorial.txt
.venv-core/Scripts/python src/render_results.py
.venv-core/Scripts/python src/build_portfolio.py --reviewed
.venv-core/Scripts/python src/prepare_publication.py --execute-notebooks
.venv-core/Scripts/python src/package_release.py
```

The seven companion notebooks execute result-reading/visualization cells, not training or hosted Kaggle computation. Their metadata records metrics/figure hashes; changed assets invalidate preserved kernel output. Channel packages contain actual reviewable text, not a prompt to write it later. No external URL, upload or approval is invented.

## Compatibility and numerical limits

Tested Python is 3.13.1. Core uses pandas 2.2.3/NumPy 2.5.4; LAB uses pandas 3.1.0. Each result records versions and the full LAB freeze is retained. Spark warns about incomplete pandas-3 support; actual Parquet/conversion parity passes at 1e-10. Date arithmetic may emit pandas/NumPy warnings. Seeded TensorFlow/Torch CPU runs are not guaranteed bit-identical across hardware. No production-cluster or broad cross-platform reproducibility claim is made.

Windows asyncio, Jupyter and Spark need localhost sockets, which required loopback-capable execution permission in this managed sandbox. This is not public exposure. Model loading is offline/local-files-only and complaint prompts do not leave the machine.

## Docker, remote CI and stop/rollback

Docker Desktop, WSL and the engine are now installed and locally verified. The following commands are an alternative manual run; the actual repeatable smoke/stop procedure and evidence are described in the final Docker execution section below:

```powershell
docker build -t decision-api:review .
docker run --rm --name decision-api -p 127.0.0.1:8000:8000 decision-api:review
```

GitHub Actions is prepared configuration, not a recorded remote run. Public/cloud service and associated costs require explicit approval. No key is needed for the local demonstration. Stop manual uvicorn with Ctrl+C; stop only the named container with `docker stop decision-api`, and keep the previous reviewed image tag for rollback. No shared data/volumes/services are deleted and no cost-bearing resource has been provisioned.


## Existing Telco reproduction (23 October 2026)

See projects/PRJ1_telco/docs/HARMONISATION.md and results/audit.json. The existing public pinned repository was reproduced separately in a fresh Python 3.10.21 environment using its own original lock, not the portfolio Python 3.13 runtime. Its original analysis, three tests, nine notebook cells and five aggregate CSVs were checked. Original source/raw/private Notion snapshots are excluded from this package; retrieve the pinned repository to reproduce. No change to model choice or conclusions.


## Actual Docker execution — 23 October 2026

Docker Desktop 4.96.3 / engine 29.9.2 / WSL 3.0.3 installed and verified after authorised prerequisites and manual Windows restart. From portfolio root: docker build -t dfds-lab4:review . ; python src/verify_container.py (execute as separate commands). DFDS_DOCKER may supply the CLI path. The script binds only 127.0.0.1:18765, uses synthetic numbers, checks health/forecast/five invalid inputs, actual healthcheck, non-root UID and stops the named container. Inspect/remove only its stopped dfds-lab4-review container before repeating. Proof and image/base digests: projects/LAB4_delivery/results/container_smoke.json; build/run text alongside. Direct dependencies pinned; transitive versions can vary in a future rebuild. No remote CI/cloud claim.
