# Local harmonisation — no external changes



PRJ1 is now linked to the existing repository and reproduced evidence in the overall portfolio. The prior access blocker is resolved. Existing professional positioning, dataset counts, leakage-safe preprocessing, training-CV choice, held-out outcomes and conditional recommendation are preserved. No duplicate Telco reconstruction is introduced.



Optional future source patch: normalise notebook cell IDs with nbformat (current notebook executes with a MissingIDFieldWarning); derive the dashboard’s frozen test denominators from summary.json if making the dashboard reusable; choose an explicit root code licence as repository owner. These are proposals only, not applied to GitHub/Notion. The current frozen denominator 1409/374 is correct.



Reproduction: verified public commit archive → separate copy → Python 3.10 venv → pip install -r requirements-lock.txt → python src/analysis.py → python -m unittest discover -s tests -v → python scripts/build_dashboard_data.py → python scripts/execute_notebook.py. Data download checks its pinned IBM SHA-256. Comparisons use full summary equality, CSV tolerance 1e-12 and dashboard text equality (line endings normalised).



Two existing private Notion pages were read and found consistent with reproduced aggregate results. Their private URLs are omitted. Neither was edited.

