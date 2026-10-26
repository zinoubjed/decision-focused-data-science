"""Write concrete channel drafts and companion evidence notebooks; never publish."""
import json,pathlib,argparse,hashlib
from common import ROOT
from build_portfolio import CONFIG,load,evidence
HOOKS={
 'PRJ2':'The cleaning rule changed the forecasting result more than a more complex model did.',
 'PRJ3':'A delivery KPI is only useful when its denominator survives the joins.',
 'PRJ4':'A confident suggestion can still be wrong for the people in a rare category.',
 'PRJ5':'Detecting a reported fault is different from predicting it before it starts.',
 'LAB1':'A source citation can accompany an irrelevant answer.',
 'LAB2':'The engineering result to verify first is agreement with an independent calculation.',
 'LAB3':'Training a neural network does not oblige us to retain it.',
 'LAB4':'A working local API and a tested container are separate pieces of evidence.'}
CLIENT={
 'PRJ2':('Observed-sales planning analysis','A cleaned weekly series, time-based baseline comparison, error report and clearly labelled planning scenarios.','Inventory optimisation, profit claims and unobserved demand estimation are outside scope.'),
 'PRJ3':('SQL reporting methodology','An agreed analytical grain, controlled joins, denominator definitions, data-quality checks and an investigation handoff.','Method-only presentation: no Olist-derived data, numbers, charts or screenshots in a commercial offer.'),
 'PRJ4':('Local text-category prototype methodology','A label dictionary, temporal evaluation, class-specific error report and abstention/review design.','No legal assessment, institutional routing guarantee, raw-text publication or external processing of sensitive text.'),
 'PRJ5':('Sensor alert review methodology','Timestamp and coverage checks, alert-episode definitions, exposure reporting and a documented event comparison.','No safety decision, automated shutdown or measured downtime-reduction claim.'),
 'LAB1':('Document-question-answering evaluation','An authorised corpus, reproducible retrieval/generation evaluation, source references and a failure report.','No unattended-answer guarantee; private documents require an agreed local-processing and privacy boundary.'),
 'LAB2':('Reproducible data transformation','Typed ingestion, SQL transformations, quality checks, Parquet outputs and reconciliation against an independent calculation.','Resource/volume limits must be agreed. A local demonstration is not evidence of production-cluster operation.'),
 'LAB3':('Classical-versus-neural benchmark','A fixed evaluation protocol, baseline, training histories and a performance/complexity comparison.','No promise that deep learning improves a given dataset; model selection requires validation evidence.'),
 'LAB4':('Local numeric API handoff','A bounded input contract, validation tests, request tracing and execution/stop instructions.','Local image build/run, healthcheck, HTTP validation and stop are verified; remote CI and cloud deployment remain outside the executed evidence.')}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--execute-notebooks',action='store_true');args=ap.parse_args()
 import nbformat
 execution=[]
 for folder,(id,title,script,license,decision) in CONFIG.items():
  p=ROOT/'projects'/folder;m=load(p/'results/metrics.json');summary,limits=evidence(folder,m);hook=HOOKS[id];service,deliverable,exclusion=CLIENT[id]
  if id=='LAB1':
   score=load(p/'results/scoring_v2.json');summary=f"On 20 fixed diagnostic questions, explicit rubric v2 scores no-RAG at {score['baseline_accuracy']:.0%}, raw RAG at {score['raw_rag_accuracy']:.0%} and guarded RAG at {score['guarded_accuracy']:.0%}. Among 16 non-abstained responses, 14 are correct; three of four unanswerable questions are refused. This is a post-run scoring clarification, not a blind new test."
  if id=='PRJ4':
   summary+=' The subgroup review reinforces the recommendation: human verification is required; aggregate accepted accuracy is not a per-class routing guarantee.'
  badge=('Local container verified; remote CI/cloud not executed' if load(p/'results/container_smoke.json') else 'BLOCKED on container verification') if id=='LAB4' else 'Local study executed; external publication not performed'
  body=f'''# Concrete publication copy — {id}

Status: {badge}. All texts below are drafts requiring approval of the exact content and platform. They do not assert personal independent execution or real client experience.

## GitHub repository description

**{title}** — {decision} Includes executable code, measured evaluation, tests and explicit limits. AI-assisted portfolio study; data and private model artifacts excluded.

Suggested repository slug: `{folder.lower().replace('_','-')}`. Ready local assets: `README.md`, `docs/METHOD.md`, `results/`, `figures/`, shared `../../src/{script}`, tests and dependency files. Use the monorepo layout unless the shared imports are packaged into each standalone repository. No remote repository or public link exists yet.

## Notion case-study copy

### {hook}

**Decision.** {decision}

**Evidence.** {summary}

**Interpretation.** {limits}

**Handoff.** Review the source, tests and population boundaries before using this as a business result. This is a portfolio study and local technical demonstration, not a client deployment. Personal autonomous proficiency remains unverified. Source and rights: {license}.

## Personal portfolio card

**{title}**

{hook} {summary}

Read the local case study and reproducible evidence. External URL: not created; use the approved repository/case-study URL only after publication.

## LinkedIn post copy

{hook}

{summary}

The boundary I would keep visible: {limits}

This AI-assisted portfolio study is a demonstration of an evaluation workflow, not a client outcome, industrial deployment or proof of independently verified personal mastery.

## Kaggle preparation

{('Not applicable to this API lifecycle demonstration. No forced notebook or Kaggle execution claim.' if id=='LAB4' else 'Companion notebook: ../evidence_companion.ipynb. It is a locally executed evidence-reading and visualization notebook, not a claim of full recomputation on Kaggle. It contains measured aggregates and figures, no raw complaints or private model vocabulary. Full computation commands are in the notebook and reproduction guide. A Kaggle run has not occurred. Dataset permissions and approved public assets must be checked before upload.')}

## Upwork portfolio-item copy — method presentation, not an active offer

**{service}**

Problem framing: {decision}

Illustrative deliverable: {deliverable}

Boundary: {exclusion}

This describes a portfolio workflow. No client engagement, availability, price, guarantee or service acceptance is asserted. The owner must confirm the service and personal delivery capacity before commercial use.

## Fiverr description copy — review draft, not a created gig

**{service}: a clearly scoped analytical handoff**

Proposed output, subject to personal acceptance: {deliverable} Agree input fields, volume, permitted processing, output format and review criteria before starting. {exclusion} This draft does not authorise a sale or claim previously delivered client work.

## Visual and link assets

Case study: `../README.md`. Method: `METHOD.md`. Measured evidence: `../results/metrics.json`. Relevant visual files are listed in the local case folder; do not invent a public URL. Always include the project-specific denominator, split or exposure caption. {'For any commercial presentation, use only original SQL-method text; omit Olist-derived figures and results. Noncommercial sharing must retain attribution and applicable ShareAlike terms.' if id=='PRJ3' else 'No raw datasets, private text, fitted vocabulary or local weights are release assets.'}

## Approval record

Platform, exact approved text, approved attachments, final public URL and publication date: **not approved / not published**. The draft itself is the concrete review object. Do not send messages, applications or offers from this file without explicit authorisation.
'''
  (p/'docs/PUBLICATION_KIT.md').write_text(body,encoding='utf-8')
  if id=='LAB4':continue
  nb=nbformat.v4.new_notebook();figure=next(iter((p/'figures').glob('*.png')),None) if (p/'figures').exists() else None
  setup=f"from pathlib import Path\nimport json\nROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'src/common.py').exists())\nCASE = ROOT / 'projects/{folder}'\nmetrics = json.loads((CASE / 'results/metrics.json').read_text(encoding='utf-8'))\nprint(json.dumps(metrics, indent=2))"
  cells=[nbformat.v4.new_markdown_cell(f'# {title}\n\nLocally executed companion evidence notebook. It reads measured outputs; it does not rerun training or claim execution on Kaggle.\n\n{license}. AI-assisted portfolio study; no independently verified personal-skill claim.\n\n{decision}'),nbformat.v4.new_code_cell(setup)]
  supplements=[n for n in ['scoring_v2.json','decision_population.json','selective_by_actual_class.json','relational_review.json','sql_check.json'] if (p/'results'/n).exists()]
  if supplements:cells.append(nbformat.v4.new_code_cell(f"for name in {supplements!r}:\n    print(name)\n    print(json.dumps(json.loads((CASE / 'results' / name).read_text(encoding='utf-8')), indent=2))"))
  if figure:cells.append(nbformat.v4.new_code_cell(f"from IPython.display import Image, display\ndisplay(Image(filename=str(CASE / 'figures/{figure.name}')))"))
  cells.append(nbformat.v4.new_markdown_cell(f'## Interpretation and full recomputation\n\n{summary}\n\n{limits}\n\nFrom the portfolio root, use the environment and authorised inputs in `docs/REPRODUCIBILITY.md`, then execute `python src/{script}`. Do not rerun the data audits merely to read these results. A standalone Kaggle environment requires adapting input mounting and installing the documented dependencies; no hosted execution is claimed.'))
  nb['cells']=cells;nb.metadata['kernelspec']={'name':'python3','display_name':'Python 3','language':'python'};nb.metadata['language_info']={'name':'python','version':'3.13'}
  path=p/'evidence_companion.ipynb'
  nb.metadata['evidence_metrics_sha256']=hashlib.sha256((p/'results/metrics.json').read_bytes()).hexdigest()
  nb.metadata['evidence_figure_sha256']=hashlib.sha256(figure.read_bytes()).hexdigest() if figure else None
  nb.metadata['preparation_version']=2
  nb.metadata['supplement_sha256']={n:hashlib.sha256((p/'results'/n).read_bytes()).hexdigest() for n in supplements}
  if path.exists() and not args.execute_notebooks:
   previous=nbformat.read(path,as_version=4)
   if previous.metadata.get('preparation_version')==2 and previous.metadata.get('evidence_metrics_sha256')==nb.metadata['evidence_metrics_sha256'] and previous.metadata.get('evidence_figure_sha256')==nb.metadata['evidence_figure_sha256'] and previous.metadata.get('supplement_sha256')==nb.metadata['supplement_sha256']:continue
  if args.execute_notebooks:
   from nbclient import NotebookClient
   NotebookClient(nb,timeout=60,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute();execution.append({'project':id,'notebook':str(path.relative_to(ROOT)),'executed_code_cells':sum(c.cell_type=='code' for c in nb.cells),'errors':sum(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.get('outputs',[])),'scope':'read and display executed pipeline evidence; not training or Kaggle execution'})
  nbformat.write(nb,path)
 if args.execute_notebooks:(ROOT/'reports/companion_notebook_execution.json').write_text(json.dumps(execution,indent=2),encoding='utf-8')
 print('Concrete channel copy and seven companion notebooks prepared',flush=True)
if __name__=='__main__':main()
