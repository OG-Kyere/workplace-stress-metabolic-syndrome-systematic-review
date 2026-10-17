"""Export the current eligible-report set without replacing incomplete extraction with invented data."""
import csv,hashlib,json,re,html,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parents[1]/'outputs'
def read(p):
 with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 log=read('data/screening_log.csv');eligible=[x for x in log if not x['duplicate_of'] and x['full_text_decision']=='Include']
 batches={}
 for p in sorted((ROOT/'data/full_text_review_batches').glob('*.json')):
  for x in json.loads(p.read_text(encoding='utf-8'))['records']:batches[x['record_id']]=(p,x)
 master=read('data/master_study_characteristics_findings.csv');cross=read('data/study_reconciliation_2026-10-10.csv')
 old={x['record_id']:master[i] for i,x in enumerate(cross[:len(master)])}
 xml={}
 for p in sorted((ROOT/'data/search_2026-10-10').glob('pubmed_*.xml')):
  for a in ET.parse(p).getroot().findall('PubmedArticle'):
   xml[a.findtext('MedlineCitation/PMID')]=a
 additions={x['record_id']:x for x in json.loads((ROOT/'data/provisional_effect_additions_048.json').read_text(encoding='utf-8'))}
 direct_pointer_path=ROOT/'data/direct_original_evidence_pointers_092.json'
 direct_pointers={z['record_id']:z for z in json.loads(direct_pointer_path.read_text(encoding='utf-8'))} if direct_pointer_path.exists() else {}
 quantitative_hold_path=ROOT/'data/current_quantitative_hold_register_092.csv'
 quantitative_holds=read('data/current_quantitative_hold_register_092.csv') if quantitative_hold_path.exists() else []
 scope_path=ROOT/'data/scope_companion_adjudication_111.csv'
 scopes={z['record_id']:z for z in read('data/scope_companion_adjudication_111.csv')} if scope_path.exists() else {}
 completion_path=ROOT/'data/completion106_comparison_audit_181.csv'
 completion={z['record_id']:z for z in read('data/completion106_comparison_audit_181.csv')} if completion_path.exists() else {}
 primary_metadata={}
 for folder in ['data/supplementary_search_143/metadata','data/supplementary_search_141/metadata','data/completion181/citation_search/metadata']:
  for p in (ROOT/folder).glob('*.json'):
   if 'provenance' in p.name or p.name=='manifest.json':continue
   content=json.loads(p.read_text(encoding='utf-8'))
   for z in content.get('resultList',{}).get('result',[]):
    if z.get('source')=='MED':primary_metadata[z['id']]=z
 correction_path=ROOT/'data/current_source_corrections_194.json'
 source_corrections=json.loads(correction_path.read_text(encoding='utf-8')) if correction_path.exists() else {}
 evidence=[];supp=[];ris=[];risids=[];reference_metadata=[]
 for x in eligible:
  rid=x['record_id'];batch,item=batches.get(rid,(None,{}));m=old.get(rid,{})
  e=dict(record_id=rid,provisional_study_id=x['final_study_id'],companion_report_of=x['companion_report_of'],title=x['title'],first_author=x['first_author'],year=x['year'],doi_or_pmid=x['doi_or_pmid'],eligibility_evidence=item.get('evidence') or x['notes'],effect_estimate_or_note=item.get('effect') or m.get('key_effect_estimate','Not yet extracted'),appraisal_caution=item.get('appraisal') or m.get('main_caution','Not yet independently appraised'),source_url=item.get('source_url',''),source_locator=item.get('locator','See archived retrieval note'),review_evidence_file=str(batch.relative_to(ROOT)) if batch else 'See screening notes: archived original XML',review_evidence_sha256=hashlib.sha256(batch.read_bytes()).hexdigest() if batch else '',structured_extraction_status='Historical extraction requires final verification' if m else 'Partial review-note extraction; detailed extraction outstanding',independent_appraisal_status='Outstanding',membership_status='Provisional first-review eligibility; not frozen')
  if rid in additions:
   z=additions[rid];source=ROOT/z['source'];assert source.exists()
   e.update(effect_estimate_or_note=z['effect'],appraisal_caution=z['appraisal'],source_locator=z['locator'],review_evidence_file=z['source'],review_evidence_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
  correction_path=ROOT/'data/effect_corrections_064.json'
  pretrend_correction=ROOT/'data/appraisal_correction_059.json'
  if rid=='PM03843' and pretrend_correction.exists():
   corrected=json.loads(pretrend_correction.read_text(encoding='utf-8'));corrected_source=ROOT/corrected['source'];assert hashlib.sha256(corrected_source.read_bytes()).hexdigest()==corrected['source_sha256']
   e.update(appraisal_caution=corrected['correction']+' Supporting supplement still unverified; voluntary uptake and excluded follow-up remain concerns.',source_locator=corrected['locator'],review_evidence_file=str(pretrend_correction.relative_to(ROOT)),review_evidence_sha256=hashlib.sha256(pretrend_correction.read_bytes()).hexdigest())
  if correction_path.exists():
   for correction in json.loads(correction_path.read_text(encoding='utf-8')):
    if correction['record_id']==rid:
     corrected_source=ROOT/correction['source'];assert hashlib.sha256(corrected_source.read_bytes()).hexdigest()==correction['sha256']
     e.update(effect_estimate_or_note=correction['effect'],appraisal_caution=correction['caution'])
  if rid in direct_pointers:
   z=direct_pointers[rid];p=ROOT/z['source'];assert hashlib.sha256(p.read_bytes()).hexdigest()==z['sha256']
   e.update(review_evidence_file=z['source'],review_evidence_sha256=z['sha256'],source_locator=z['locator'])
  for correction_name in ['extraction_corrections_096.json','remaining_extraction_corrections_098.json','adjudicated_extraction_corrections_139.json']:
   source_corrections_path=ROOT/'data'/correction_name
   if source_corrections_path.exists():
    for z in json.loads(source_corrections_path.read_text(encoding='utf-8')):
     if z['record_id']==rid:
      assert hashlib.sha256((ROOT/z['source']).read_bytes()).hexdigest()==z['source_sha256']
      e.update(effect_estimate_or_note=z['effect'],source_locator=z['locator'])
      e['appraisal_caution']+=' '+z['append_caution']+' Correction provenance: data/'+correction_name+'.'
  report_holds=[z for z in quantitative_holds if z['record_id']==rid]
  if report_holds:
   for z in report_holds:
    assert hashlib.sha256((ROOT/z['source_file']).read_bytes()).hexdigest()==z['source_sha256']
    assert hashlib.sha256((ROOT/z['ledger_file']).read_bytes()).hexdigest()==z['ledger_sha256']
   e['appraisal_caution']+=' Quantitative integrity holds: '+str(len(report_holds))+' outcome/report entries in data/current_quantitative_hold_register_092.csv; apply each stated scope, preserve eligibility, and resolve before quantitative synthesis.'
  if rid in scopes and scopes[rid]['step1_status'].startswith(('Eligible secondary','Eligible component','Eligible worker')):
   z=scopes[rid];source=ROOT/z['original_file'];assert hashlib.sha256(source.read_bytes()).hexdigest()==z['original_sha256']
   e['effect_estimate_or_note']='Qualifying comparison identified in original: '+z['evidence']
   e['appraisal_caution']+=' Scope adjudication111: '+z['synthesis_action']+'; complete numeric extraction and independent appraisal outstanding.'
   e['source_locator']=z['evidence'];e['review_evidence_file']=z['original_file'];e['review_evidence_sha256']=z['original_sha256']
  scope_integrity_path=ROOT/'data/scope_integrity_cautions_117.json'
  if scope_integrity_path.exists():
   for z in json.loads(scope_integrity_path.read_text(encoding='utf-8')):
    if z['record_id']==rid:
     assert hashlib.sha256((ROOT/z['source']).read_bytes()).hexdigest()==z['source_sha256']
     e['appraisal_caution']+=' Source-verified scope safeguards117: '+z['append_caution']
  ontario_path=ROOT/'data/ontario_source_comparison_121.json'
  if ontario_path.exists():
   for z in json.loads(ontario_path.read_text(encoding='utf-8'))['reports']:
    if z['record_id']==rid:
     e['appraisal_caution']+=' Author-manuscript comparison121: '+z['append_caution']+' Source: '+z['source_url']+'; '+z['locator']+'. PDF bytes not archived.'
  recovered_inspection=ROOT/'data/retrieved12_source_inspection_129.json'
  if recovered_inspection.exists():
   for z in json.loads(recovered_inspection.read_text(encoding='utf-8')):
    if z['record_id']==rid:
     assert hashlib.sha256((ROOT/z['source']).read_bytes()).hexdigest()==z['sha256']
     e['appraisal_caution']+=' Recovered original129: '+z['caution']+' Full numeric extraction and independent review not certified.'
  for inspection_name in ['alternative12_inspection_133.json','web18_inspection_135.json','final_source_inspection_137.json']:
   inspection_path=ROOT/'data'/inspection_name
   if inspection_path.exists():
    for z in json.loads(inspection_path.read_text(encoding='utf-8')):
     if z['record_id']==rid:
      assert hashlib.sha256((ROOT/z['evidence_file']).read_bytes()).hexdigest()==z['evidence_sha256']
      e['appraisal_caution']+=' Source review '+inspection_name+': '+z['summary']+' '+z['source_type']+'. Full extraction and independent review not certified.'
      e.update(review_evidence_file=z['evidence_file'],review_evidence_sha256=z['evidence_sha256'],source_url=z['source_url'],source_locator=z['locator'])
  residual_path=ROOT/'data/residual_scope_review_138.csv'
  if residual_path.exists():
   for z in read('data/residual_scope_review_138.csv'):
    if z['record_id']==rid:
     assert hashlib.sha256((ROOT/z['source_file']).read_bytes()).hexdigest()==z['source_sha256']
     e['appraisal_caution']+=' Residual-group review138: '+z['evidence']+' '+z['synthesis_action']+' Status: '+z['status']+'.'
  if rid=='PM03936' and (ROOT/'data/study_family_adjudication_138.json').exists():
   z=json.loads((ROOT/'data/study_family_adjudication_138.json').read_text())
   for s in z['sources']:assert hashlib.sha256((ROOT/s['evidence_file']).read_bytes()).hexdigest()==s['evidence_sha256']
   e['appraisal_caution']+=' Confirmed nested companion of PM04489;145is a subset of418,not an independent workforce. Dietary-exposure scope still unresolved.'
  if rid in completion:
   z=completion[rid]
   assert hashlib.sha256((ROOT/z['source_file']).read_bytes()).hexdigest()==z['source_sha256']
   e['appraisal_caution']=re.sub(r'possible US baseline companion\s*FC143-01659 not yet verified\.?','US baseline companion FC143-01659 verified in the same trial family179.',e['appraisal_caution'],flags=re.I)
   e['appraisal_caution']+=' Comparison-specific provisional appraisal181 ('+z['design']+'): '+z['specific_caution']+' Unclear item answers remain; no final quality rating or independent review is certified.'
  if rid in source_corrections:
   correction=source_corrections[rid]
   assert hashlib.sha256((ROOT/correction['source_file']).read_bytes()).hexdigest()==correction['source_sha256']
   assert set(correction['fields'])<=set(['eligibility_evidence','effect_estimate_or_note','appraisal_caution'])
   e.update(correction['fields']);e['source_locator']+='; source correction194: '+correction['source_locator']
   e['appraisal_caution']+=' Source correction provenance: data/current_source_corrections_194.json; source_sha256='+correction['source_sha256']
  evidence.append(e);supp.append({k:e[k] for k in ['record_id','provisional_study_id','companion_report_of','title','year','doi_or_pmid','eligibility_evidence','effect_estimate_or_note','appraisal_caution','structured_extraction_status','membership_status']})
  pm=re.search(r'PMID:(\d+)',x['doi_or_pmid']);a=xml.get(pm.group(1)) if pm else None
  lines=['TY  - JOUR','ID  - '+rid,'TI  - '+x['title'],'PY  - '+x['year']]
  if a is not None:
   for author in a.findall('MedlineCitation/Article/AuthorList/Author'):
    name=author.findtext('CollectiveName') or ', '.join(z for z in [author.findtext('LastName'),author.findtext('ForeName') or author.findtext('Initials')] if z)
    if name:lines.append('AU  - '+name)
   article=a.find('MedlineCitation/Article')
   for tag,value in [('JO',article.findtext('Journal/Title')),('VL',article.findtext('Journal/JournalIssue/Volume')),('IS',article.findtext('Journal/JournalIssue/Issue')),('SP',article.findtext('Pagination/StartPage') or article.findtext('Pagination/MedlinePgn'))]:
    if value:lines.append(tag+'  - '+value)
  elif pm and pm.group(1) in primary_metadata:
   z=primary_metadata[pm.group(1)]
   for author in z.get('authorList',{}).get('author',[]):
    name=', '.join(v for v in [author.get('lastName'),author.get('firstName') or author.get('initials')] if v) or author.get('fullName','')
    if name:lines.append('AU  - '+name)
   ji=z.get('journalInfo',{})
   for tag,value in [('JO',ji.get('journal',{}).get('title')),('VL',ji.get('volume')),('IS',ji.get('issue')),('SP',z.get('pageInfo'))]:
    if value:lines.append(tag+'  - '+value)
   if not any(v.startswith('AU  - ') for v in lines):lines.extend(['AU  - '+x['first_author'],'N1  - Full author metadata requires verification; first author only.'])
  elif (ROOT/'data/completion181/reference_recovery'/(rid+'_provenance.json')).exists():
   recovered=json.loads((ROOT/'data/completion181/reference_recovery'/(rid+'_provenance.json')).read_text())
   assert 'metadata' in recovered and hashlib.sha256((ROOT/recovered['source_file']).read_bytes()).hexdigest()==recovered['source_sha256']
   z=recovered['metadata'];doi_identity=z['DOI'].lower() in x['doi_or_pmid'].lower()
   context=ROOT/'data/completion181/sources106'/(rid+'.json')
   if not doi_identity and context.exists():doi_identity=z['DOI'].lower() in json.loads(context.read_text())['body'].lower()
   assert doi_identity,rid
   for author in z.get('author',[]):
    name=', '.join(v for v in [author.get('family'),author.get('given')] if v)
    if name:lines.append('AU  - '+name)
   for tag,value in [('JO','; '.join(z.get('container-title',[]))),('VL',z.get('volume')),('IS',z.get('issue')),('SP',z.get('page') or z.get('article-number'))]:
    if value:lines.append(tag+'  - '+html.unescape(value))
   if not re.search(r'10\.\d{4,9}/',x['doi_or_pmid']):lines.append('DO  - '+z['DOI'])
  else:
   lines.extend(['AU  - '+x['first_author'],'N1  - Full bibliographic metadata requires verification; first author only.'])
  doi=re.search(r'doi:(10\.[^;]+)',x['doi_or_pmid'],re.I)
  if doi:lines.append('DO  - '+doi.group(1))
  elif x['doi_or_pmid'].startswith('10.'):lines.append('DO  - '+x['doi_or_pmid'])
  if pm:lines.append('AN  - PMID:'+pm.group(1))
  lines.extend(['N1  - Provisional eligible report; study family '+x['final_study_id']+'; do not pool overlapping companion outcomes without adjudication.','ER  - ',''])
  ris.append('\n'.join(lines));risids.append(rid)
  reference_metadata.append(dict(record_id=rid,primary_index_bibliographic_metadata=bool(a is not None or (pm and pm.group(1) in primary_metadata)),registry_bibliographic_metadata=(ROOT/'data/completion181/reference_recovery'/(rid+'_provenance.json')).exists(),journal_present=any(v.startswith('JO  - ') for v in lines),author_metadata_partial=any('first author only' in v.lower() for v in lines)))
 write(ROOT/'data/current_eligible_evidence_register.csv',evidence);write(ROOT/'data/current_eligible_supplement_register.csv',supp)
 (ROOT/'data/current_eligible_references.ris').write_text('\n'.join(ris),encoding='utf-8')
 target={x['record_id'] for x in eligible};assert len(target)==len(eligible)
 assert {x['record_id'] for x in evidence}=={x['record_id'] for x in supp}==set(risids)==target
 with (ROOT/'data/current_eligible_evidence_register.csv').open(encoding='utf-8-sig',newline='') as f:assert len(list(csv.DictReader(f)))==len(target)
 audit=dict(provisional_included_reports=len(target),evidence_register_reports=len(evidence),supplement_register_reports=len(supp),reference_records=len(risids),record_sets_identical=True,final_extraction_complete=False,independent_appraisal_complete=False,final_research_audit_complete=False,historical_pool_excluded=[x['record_id'] for x in cross if x['in_master']=='Yes' and x['screening_full_text_decision']=='Exclude'],eligible_without_batch_effect_note=[x['record_id'] for x in evidence if x['effect_estimate_or_note']=='Not yet extracted'])
 (ROOT/'data/current_register_alignment_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
 write(ROOT/'data/current_reference_metadata_coverage.csv',reference_metadata)
 for p in ['current_eligible_evidence_register.csv','current_eligible_supplement_register.csv','current_eligible_references.ris','current_register_alignment_audit.json']:(OUT/p).write_bytes((ROOT/'data'/p).read_bytes())
 status=ROOT/'data/search_2026-10-10/completion_status.json';s=json.loads(status.read_text());s.update(title_abstract_screening_complete=all(x['title_abstract_decision'] in ['Include','Exclude'] for x in log if not x['duplicate_of']),full_text_screening_complete=all(x['full_text_retrieved']=='No' or x['full_text_decision'] in ['Include','Exclude'] for x in log if not x['duplicate_of'] and x['title_abstract_decision']=='Include'));status.write_text(json.dumps(s,indent=2),encoding='utf-8')
 print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
