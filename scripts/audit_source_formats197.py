"""Correct format assumptions using actual bytes for all343 original archives."""
import csv,json,hashlib,collections
from pathlib import Path
from capture_all184_196 import detect
R=Path(__file__).resolve().parents[1];out=[]
with (R/'data/current_source_availability_187.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
for r in rows:
 if not r['status'].startswith('Archived article source'):continue
 p=R/r['source_file'];raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==r['source_sha256']
 kind=detect(raw);out.append(dict(record_id=r['record_id'],source_file=r['source_file'],source_sha256=r['source_sha256'],filename_extension=p.suffix,actual_format=kind,format_verified_from_bytes=kind!='Unknown',clinical_extraction_complete=False))
assert len(out)==343
with (R/'data/original_source_formats_197.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
status=dict(original_reports=len(out),actual_formats=dict(collections.Counter(r['actual_format'] for r in out)),xml_source_suffix=sum(r['filename_extension']=='.source' and r['actual_format']=='XML' for r in out),normalized_result_coverage_changed=False)
(R/'data/extraction196/source_format_audit_197.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
