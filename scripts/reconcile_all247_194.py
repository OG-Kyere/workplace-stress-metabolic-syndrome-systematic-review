"""Account for every record in the entire247 gap list without fake closure."""
import csv,json,hashlib,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R.parents[1]/'outputs';D=R/'data/reconciliation194';D.mkdir(exist_ok=True)
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
queuepath=O/'remaining_numeric_coverage_193.csv';queue=read(queuepath);q={x['record_id'] for x in queue};assert len(queue)==len(q)==247
reg={x['record_id']:x for x in read(R/'data/current_eligible_evidence_register.csv')};availability={x['record_id']:x for x in read(R/'data/current_source_availability_187.csv')}
priorfile=R/'data/remaining_pdf_components_095.csv';recovered=[]
for line,x in enumerate(read(priorfile),2):
 if x['record_id'] not in q:continue
 assert sha(R/x['original_file'])==x['original_sha256']
 recovered.append(dict(record_id=x['record_id'],source_ledger=str(priorfile.relative_to(R)),source_ledger_sha256=sha(priorfile),csv_line=line,original_file=x['original_file'],original_sha256=x['original_sha256'],outcome=x['outcome'],exposure=x['exposure'],contrast=x['contrast'],measure=x['measure'],estimate=x['estimate'],ci_lower=x['ci_lower'],ci_upper=x['ci_upper'],p_value=x['p_value'],reported_group_values=x['reported_group_values'],denominator_context=x['denominator_context'],source_locator=x['source_locator'],caution=x['caution'],source_integrity_flags=x['source_integrity_flags'],raw_original_row_json=json.dumps(x,ensure_ascii=False),recovery_status='Previously extracted row recovered from omitted ledger; not a new extraction or independent verification',quantitative_synthesis_approved=False))
assert len(recovered)==40 and len({x['record_id'] for x in recovered})==9
narrativefile=R/'data/all62_specified_findings_109.csv';narrative=[]
for line,x in enumerate(read(narrativefile),2):
 if x['record_id'] not in q:continue
 assert sha(R/x['original_file'])==x['original_sha256']
 narrative.append(dict(**x,source_ledger=str(narrativefile.relative_to(R)),source_ledger_sha256=sha(narrativefile),csv_line=line,recovery_status='Existing narrative only; not converted to verified normalized effect',normalization_complete=False))
assert len(narrative)==46
numeric={x['record_id'] for x in recovered};new={x['record_id'] for x in read(R/'data/source_read_clinical_results_195.csv')};notes={x['record_id'] for x in narrative};assert new<=q and not new&numeric and new<=notes
rows=[];reviewchecks=collections.Counter()
for rid in sorted(q):
 a=availability[rid];r=reg[rid];archived=a['status'].startswith('Archived article source')
 assert sha(R/a['source_file'])==a['source_sha256']
 if r['review_evidence_file'] and r['review_evidence_sha256']:
  check='Hash verified' if (R/r['review_evidence_file']).exists() and sha(R/r['review_evidence_file'])==r['review_evidence_sha256'] else 'Review pointer/hash mismatch; investigate'
 else:check='No review pointer/hash supplied'
 reviewchecks[check]+=1
 if rid in new:state='New specified original-table findings195';action='Finish endpoint/model/denominator fields and independent verification'
 elif rid in numeric:state='Existing specified findings recovered194';action='Reconcile existing model/denominator/holds; original PDF visual verification if outstanding'
 elif not archived:state='Original-source work deferred';action='Retain uncertainty and retrieval history; no further retries requested; not a full-text eligibility exclusion'
 elif rid in notes:state='Prior narrative findings only';action='Verify original endpoints and normalize findings; narrative is not completed numeric extraction'
 else:state='Available original; detailed extraction outstanding';action='Extract eligible clinical contrasts from complete original; review notes alone do not close gap'
 rows.append(dict(record_id=rid,title=r['title'],provisional_study_id=r['provisional_study_id'],disposition=state,next_action=action,source_status=a['status'],source_file=a['source_file'],source_sha256=a['source_sha256'],source_bytes_hash_verified=True,review_finding=r['effect_estimate_or_note'],review_caution=r['appraisal_caution'],review_evidence_file=r['review_evidence_file'],review_evidence_sha256=r['review_evidence_sha256'],review_pointer_check=check,extraction_complete=False,independent_verification='Outstanding'))
counts=dict(collections.Counter(x['disposition'] for x in rows));assert sum(counts.values())==247 and counts['Original-source work deferred']==45
allold=[]
for name in ['current_numeric_extraction_audit_188.csv','source_read_clinical_results_191.csv','source_read_clinical_results_192.csv','source_read_clinical_results_193.csv']:allold+=read(R/'data'/name)
covered={x['record_id'] for x in allold}|numeric|new;assert len(covered)==159
for base in [R/'data',O]:
 write(base/'all247_reconciliation_194.csv',rows);write(base/'recovered_existing_results_194.csv',recovered);write(base/'recovered_narrative_findings_194.csv',narrative)
 write(base/'deferred_original_source_records_194.csv',[x for x in rows if x['disposition']=='Original-source work deferred'])
 write(base/'active_original_extraction_194.csv',[x for x in rows if x['disposition'] in ['Prior narrative findings only','Available original; detailed extraction outstanding']])
status=dict(queue_records=len(q),queue_file_sha256=sha(queuepath),disposition_counts=counts,prior_numeric_rows_recovered=40,prior_numeric_reports_recovered=9,prior_narrative_reports_recovered=46,new_specified_results_rows=125,new_specified_reports=9,reports_with_specified_rows_in_expanded_ledgers=len(covered),reports_without_specified_rows_in_these_ledgers=len(reg)-len(covered),active_originals_without_specified_rows=counts['Prior narrative findings only']+counts['Available original; detailed extraction outstanding'],original_source_gaps_deferred=45,queue_source_hashes_verified=247,queue_archived_originals_hash_verified=202,review_pointer_checks=dict(reviewchecks),all247_fully_extracted=False,independent_reviews_completed=0)
(D/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
