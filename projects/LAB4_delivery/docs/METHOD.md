# Delivery contract, controls and outstanding checks

Numeric API accepts 52–260 weekly nonnegative finite sales values <=1e10. They must be complete chronological weeks, a client-side data contract that cannot be inferred from an unlabelled numeric array. Endpoint /forecast returns the annual seasonal naive value at index -52, one-week horizon. No complaint text, customer IDs, keys or trained private vocabulary enter the API/image.

Validation rejects short/long arrays, negatives, nonfinite values and nonnumeric text. Health and forecast requests are exercised by actual ASGI tests; generated request IDs and timing logs contain method/path/status, no request body. No authentication, public service hardening or production traffic claim is made.

Dockerfile pins direct API dependencies, uses a non-root user and a health check. The restricted build context includes only the API module (about 2 KB), excluding all datasets. Actual Docker Desktop 4.96.3 / engine 29.9.2 / WSL 3.0.3 image build/run is verified on 23 October 2026. Image and base-image digests, versions, healthcheck, non-root UID 1000 and loopback port binding are recorded in results/container_smoke.json. Health and forecast return 200; short, negative, excessive, null and NaN inputs return 422; forecast on synthetic 1..104 is 53. Container stops with exit 0.

The first container test exposed a NaN error-response serialization failure (500). The local API now returns safe validation details without submitted values, with a regression test for NaN, both infinities and overflow 1e999. The corrected image passed actual HTTP tests.

GitHub Actions configuration has not run remotely. No cloud service, public endpoint or operational benefit is claimed. Base image and resolved dependency versions are recorded for this build; the Dockerfile pins direct packages only, so a later rebuild may resolve different transitive dependencies. Use the recorded image digest/environment for this exact evidence; a fully locked image supply chain is outside this demonstration.

Reproduce from portfolio root: `docker build -t dfds-lab4:review .` then `python src/verify_container.py`. Docker must be in PATH or DFDS_DOCKER must identify its executable. The script uses only synthetic numeric fixtures and stops its named container in finally. It leaves the stopped test container available for inspection; before rerunning, inspect and remove only that stopped named test container (`docker rm dfds-lab4-review`). Do not stop unrelated containers. Remote publication/cloud requires separate approval.
