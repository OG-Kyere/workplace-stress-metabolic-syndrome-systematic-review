"""Validate and export the entire184 source-capture pass with explicit limits."""
import csv,json,hashlib,zipfile,collections,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R.parents[1]/'outputs';D=R/'data/extraction196'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
q=read(R/'data/active_original_extraction_194.csv');rows=read(R/'data/all184_source_capture_196.csv');status=json.loads((D/'status.json').read_text());pdf=read(R/'data/source_read_pdf_results_198.csv')
assert len(rows)==184 and {x['record_id'] for x in rows}=={x['record_id'] for x in q}
assert not status['parse_failures']
files=[]
for x in rows:
 assert sha(R/x['source_file'])==x['source_sha256'] and sha(R/x['packet_file'])==x['packet_sha256']
 packet=json.loads((R/x['packet_file']).read_text(encoding='utf-8'));assert packet['record_id']==x['record_id'] and not packet['clinical_results_verified']
 files.append(R/x['packet_file'])
for x in pdf:assert sha(R/x['original_file'])==x['original_sha256'] and sha(R/x['visual_check_image'])==x['visual_check_image_sha256']
typed={x['record_id'] for x in pdf};n=[]
for x in rows:
 r=dict(x)
 r['current_status']='Specified PDF findings visually checked198; full extraction incomplete' if x['record_id'] in typed else ('Machine candidate tables captured; clinical validation outstanding' if int(x['clinical_candidate_rows']) else 'No machine candidate table rows; narrative/figure/manual review required')
 r['machine_candidate_rows_are_verified_effects']=False;n.append(r)
for base in [R/'data',O]:
 with (base/'all184_current_status_199.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(n[0]));w.writeheader();w.writerows(n)
summary=dict(all184_source_capture_complete=True,all184_clinical_extraction_complete=False,reports=184,source_and_packet_hashes_verified=184,format_counts=status['actual_formats'],actual_xml_in_source_files=37,candidate_rows=status['clinical_candidate_rows'],reports_with_machine_candidate_rows=status['reports_with_candidate_rows'],parse_failures=0,current_status_counts=dict(collections.Counter(x['current_status'] for x in n)),new_visually_checked_pdf_rows=33,new_visually_checked_pdf_reports=3,overall_specified_report_coverage=162,available_originals_without_specified_rows=181,deferred_original_source_gaps=45,independent_reviews_completed=0)
(D/'current_status_199.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
report='''# All184 source-capture pass

All184 available originals were processed together, with source and packet hashes checked and no parsing failures. This is a first-pass source capture, not completed clinical extraction or independent verification.

Actual formats:162XML,10HTML,12PDF. Thirty-seven `.source` files contain XML; they had been incorrectly routed to manual capture by filename suffix. The full343-original format audit finds267XML,36HTML,40PDF; its62XML `.source` files explain the earlier inflated PDF/other category.

The pass captured5,521 clinical-keyword candidate table rows across165 reports, alongside original methods/results passages, captions, headers, footnotes, row/column spans and exact source hashes. Candidates include baseline descriptions and rows whose exposure/model/endpoint cannot yet be interpreted. They are not5,521 verified effects and are not added to the normalized result count. PDF pages may include references or columns requiring visual separation. Graphics-only tables and absent candidate matches remain explicit.

Three PDF originals were visually inspected at their clinical tables and contributed33 specified results:Viester12,Geaney9,Rusali12. Two of those papers had no automatically captured table rows. Of the184 reports,3 now have those specified PDF findings,164 have machine table candidates only, and17 have no machine candidate rows and need narrative/figure/manual work. These statuses do not certify full extraction for any report.

Overall specified-result coverage is162reports. Of388 provisional reports,181available originals still lack specified rows in these ledgers and45original-source gaps remain deferred. Reports with some rows still require full endpoint/model/denominator and companion verification. Independent reviews completed:zero. Eligibility decisions, screening counts and PRISMA freeze have not been changed.

The local ZIP contains184 report packets, the whole-set index, candidate table rows, source-format audit, three visually checked PDF-result rows, source images for those checks, the capture/validation scripts and a hash manifest. Original article files remain in the research workspace; the packet source paths/hashes identify them. Primary passages are source captures rather than independently reviewed findings. Read this status alongside the manuscript; do not treat the archive as a finished research freeze.
'''
(R/'docs/all184_source_pass_199.md').write_text(report,encoding='utf-8');(O/'all184_progress.md').write_text(report,encoding='utf-8')
extras=['data/all184_source_capture_196.csv','data/all184_current_status_199.csv','data/clinical_table_candidates_196.csv','data/original_source_formats_197.csv','data/source_read_pdf_results_198.csv','data/extraction196/status.json','data/extraction196/current_status_199.json','data/extraction196/source_format_audit_197.json','data/extraction198/status.json','docs/all184_source_pass_199.md','scripts/capture_all184_196.py','scripts/test_source_capture196.py','scripts/audit_source_formats197.py','scripts/extract_pdf_results198.py','scripts/package_all184_199.py']
files+=[R/x for x in extras];files.append(R/'manuscript/current_working_manuscript.md');files+=list((D/'pdf_visual_checks').glob('*.png'))
manifest={str(p.relative_to(R)):sha(p) for p in files};(O/'all184_file_hashes.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
archive=O/'all184-source-extraction-pass.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,str(p.relative_to(R)))
 z.write(O/'all184_file_hashes.json','file_hashes.json')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None and len([x for x in z.namelist() if x.startswith('data/extraction196/reports/')])==184
print(json.dumps(dict(**summary,archive=str(archive),archive_bytes=archive.stat().st_size),indent=2))
