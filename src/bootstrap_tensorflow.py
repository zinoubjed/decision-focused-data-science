"""Windows fallback: install official wheel runtime, omit C++ custom-op headers.
Does not alter registry or system Python. Requires the workspace-local venv.
"""
import sys,sysconfig,pathlib,zipfile,hashlib,json,os
ROOT=pathlib.Path(__file__).resolve().parents[1];WORK=pathlib.Path(os.environ.get('DFDS_WORK_DIR',str(ROOT/'.runtime'))).resolve()
def main():
 target=pathlib.Path(sysconfig.get_path('purelib')).resolve()
 if not target.is_relative_to(WORK.resolve()):raise SystemExit('Use the workspace-local runtime interpreter; refusing system-site mutation')
 wheel=next((WORK/'wheels').glob('tensorflow-2.21.0-cp313-cp313-win_amd64.whl'));written=0;omitted=0
 with zipfile.ZipFile(wheel) as z:
  assert z.testzip() is None
  for item in z.infolist():
   if item.filename.startswith('tensorflow/include/'):
    omitted+=1;continue
   dest=(target/item.filename).resolve()
   if not dest.is_relative_to(target):raise ValueError('Unsafe wheel path')
   path='\\\\?\\'+str(dest) if os.name=='nt' else str(dest)
   if item.is_dir():os.makedirs(path,exist_ok=True);continue
   os.makedirs(os.path.dirname(path),exist_ok=True)
   with open(path,'wb') as f:f.write(z.read(item))
   written+=1
 rec={'wheel':wheel.name,'sha256':hashlib.file_digest(wheel.open('rb'),'sha256').hexdigest(),'runtime_files_written':written,'cpp_header_members_omitted':omitted,'reason':'Native Windows MAX_PATH during normal pip install; C++ custom-op headers not needed by CPU Keras benchmark. Official Python runtime and libraries retained.','limitation':'Custom C++ op compilation not supported by this reduced installation.'}
 (ROOT/'reports/tensorflow_bootstrap.json').write_text(json.dumps(rec,indent=2));print(rec,flush=True)
if __name__=='__main__':main()
