"""Whole184 first-pass source capture, explicitly separate from effect validation.

Detects the actual format of .source files, preserves tables/section context and
captures PDFs with page locators. Keyword matches are candidates, not eligibility
decisions or clinically interpreted effects. Nothing is approved for pooling.
"""
import csv,json,re,hashlib,collections,html
from pathlib import Path
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1];D=R/'data/extraction196';O=R.parents[1]/'outputs'
CLINICAL=re.compile(r'metabolic\s*syndrome|\bmet\s?s\b(?![- ]?IR\b)|waist|\bWC\b|abdominal\s*obesity|central\s*obesity|triglycer|\bTG\b|\bHDL\b|fasting\s*(?:blood\s*)?(?:glucose|glyc|sugar)|\bF(?:BG|PG|BS)\b|systolic|diastolic|\b[SD]BP\b|blood\s*pressure|hypertensi|glyca?emi',re.I)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(e):return ' '.join(' '.join(e.itertext()).split())
def detect(raw):
 if raw.lstrip().startswith(b'%PDF-'):return 'PDF'
 try:
  root=ET.fromstring(raw)
  if any(e.tag.split('}')[-1]=='article' for e in root.iter()):return 'XML'
 except ET.ParseError:pass
 if re.search(br'<(?:!doctype\s+html|html|body|article)\b',raw[:10000],re.I):return 'HTML'
 return 'Unknown'
class Blocks(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.blocks=[];self.active=None;self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
  if tag in ('p','h1','h2','h3','h4','h5','h6'):
   if self.active:self.flush()
   self.active=tag;self.parts=[]
 def handle_data(self,data):
  if self.active and not self.skip:self.parts.append(data)
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
  if tag==self.active:self.flush()
 def flush(self):
  text=' '.join(' '.join(self.parts).split())
  if text:self.blocks.append((self.active,text))
  self.active=None;self.parts=[]
def xml_capture(raw):
 root=ET.fromstring(raw)
 for e in root.iter():e.tag=e.tag.split('}')[-1]
 parent={c:p for p in root.iter() for c in p};passages=[];tables=[]
 for p in root.findall('.//body//p'):
  if p.find('.//table-wrap') is not None:continue
  titles=[];ancestor=parent.get(p);excluded=False
  while ancestor is not None:
   if ancestor.tag in ('ref-list','ref','table-wrap'):excluded=True;break
   if ancestor.tag=='sec':titles.append(clean(ancestor.find('title')) if ancestor.find('title') is not None else '')
   ancestor=parent.get(ancestor)
  path=' / '.join(reversed([t for t in titles if t]));text=clean(p)
  if not excluded and text and re.search(r'result|finding|method|material|statisti|particip|measure|interven|analysis|design',path,re.I):passages.append(dict(section=path,text=text))
 for i,t in enumerate(root.findall('.//table-wrap'),1):
  rows=[]
  for tr in t.findall('.//tr'):rows.append([dict(text=clean(c),rowspan=c.get('rowspan','1'),colspan=c.get('colspan','1')) for c in tr if c.tag in ('td','th')])
  tables.append(dict(table_id=t.get('id',str(i)),caption=' '.join(clean(e) for e in t.findall('./label')+t.findall('./caption')),footnotes=' '.join(clean(e) for e in t.findall('./table-wrap-foot')),rows=rows,graphics_only=not rows and t.find('.//graphic') is not None,page=''))
 return passages,tables
def html_capture(raw):
 text=raw.decode('utf-8',errors='replace');parser=Blocks();parser.feed(text);parser.flush();passages=[];section='Unclassified';references=False
 for tag,body in parser.blocks:
  if tag.startswith('h'):
   section=body
   if re.fullmatch(r'(?:\d+\.?\s*)?(?:references|bibliography)',section,re.I):references=True
  if tag=='p' and not references and re.search(r'result|finding|method|material|statisti|particip|measure|interven|analysis|design',section,re.I):passages.append(dict(section=section,text=body))
 tables=[]
 for i,m in enumerate(re.finditer(r'<table\b.*?</table>',text,re.S|re.I),1):
  if len(re.findall(r'<table\b',m[0],re.I))!=1:
   tables.append(dict(table_id='HTML'+str(i),caption='Nested HTML table requires manual parsing',footnotes='',rows=[],graphics_only=False,page=''));continue
  rows=[]
  for tr in re.findall(r'<tr\b.*?</tr>',m[0],re.S|re.I):
   cells=[]
   for c in re.finditer(r'<t[dh]\b([^>]*)>(.*?)</t[dh]>',tr,re.S|re.I):
    def span(name):
     a=re.search(name+r'\s*=\s*[\"\x27]?([0-9]+)',c[1],re.I);return a[1] if a else '1'
    cells.append(dict(text=' '.join(html.unescape(re.sub('<[^>]+>',' ',c[2])).split()),rowspan=span('rowspan'),colspan=span('colspan')))
   rows.append(cells)
  tables.append(dict(table_id='HTML'+str(i),caption='HTML table; first rows preserve headings',footnotes='',rows=rows,graphics_only=False,page=''))
 return passages,tables
def pdf_capture(p,rid):
 import pdfplumber
 from pypdf import PdfReader
 passages=[];tables=[];previous=D/'reports'/(rid+'.json')
 if previous.exists():
  cached=json.loads(previous.read_text(encoding='utf-8'))
  if cached.get('source_sha256')==sha(p) and cached.get('actual_format')=='PDF' and not cached.get('parse_error'):
   tables=cached['tables']
   for n,page in enumerate(PdfReader(p).pages,1):passages.append(dict(section=f'PDF page{n}; section/column order requires visual check',text=page.extract_text() or ''))
   return passages,tables
 with pdfplumber.open(p) as pdf:
  for n,page in enumerate(pdf.pages,1):
   for i,t in enumerate(page.extract_tables(),1):
    tables.append(dict(table_id=f'PDFp{n}t{i}',caption='Automatic PDF table capture; visual alignment unverified',footnotes='',rows=[[dict(text=' '.join((c or '').split()),rowspan='Unverified',colspan='Unverified') for c in row] for row in t],graphics_only=False,page=n))
 for n,page in enumerate(PdfReader(p).pages,1):passages.append(dict(section=f'PDF page{n}; section/column order requires visual check',text=page.extract_text() or ''))
 return passages,tables
def main():
 D.mkdir(exist_ok=True);(D/'reports').mkdir(exist_ok=True)
 with (R/'data/active_original_extraction_194.csv').open(encoding='utf-8-sig',newline='') as f:queue=list(csv.DictReader(f))
 assert len(queue)==len({x['record_id'] for x in queue})==184
 inventory=[];candidate_rows=[];failures=[]
 for r in queue:
  p=R/r['source_file'];assert sha(p)==r['source_sha256'];raw=p.read_bytes();kind=detect(raw);rid=r['record_id']
  try:
   if kind=='XML':passages,tables=xml_capture(raw)
   elif kind=='HTML':passages,tables=html_capture(raw)
   elif kind=='PDF':passages,tables=pdf_capture(p,rid)
   else:raise ValueError('Unknown actual format')
   error=''
  except Exception as e:
   passages=[];tables=[];error=type(e).__name__+': '+str(e);failures.append(dict(record_id=rid,error=error))
  findings=[x for x in passages if re.search(r'result|finding',x['section'],re.I) and CLINICAL.search(x['text'])]
  if kind=='PDF':findings=[x for x in passages if CLINICAL.search(x['text'])]
  nrows=0
  for t in tables:
   headers=t['rows'][:3];tablematch=bool(CLINICAL.search(t['caption']+' '+' '.join(c['text'] for row in headers for c in row)))
   for n,cells in enumerate(t['rows'],1):
    if not any(re.search(r'\d',c['text']) for c in cells):continue
    if not tablematch and not CLINICAL.search(' '.join(c['text'] for c in cells)):continue
    candidate_rows.append(dict(record_id=rid,table_id=t['table_id'],table_row=n,page=t['page'],caption=t['caption'],headers_json=json.dumps(headers,ensure_ascii=False),cells_json=json.dumps(cells,ensure_ascii=False),footnotes=t['footnotes'],source_file=r['source_file'],source_sha256=r['source_sha256'],capture_status='Machine-captured candidate row; clinical estimand/reference/denominator not validated',clinical_result_verified=False,independent_review='Outstanding'));nrows+=1
  packet=dict(record_id=rid,title=r['title'],source_file=r['source_file'],source_sha256=r['source_sha256'],actual_format=kind,prior_review_finding=r['review_finding'],prior_review_caution=r['review_caution'],review_evidence_file=r['review_evidence_file'],review_evidence_sha256=r['review_evidence_sha256'],original_sections=passages,clinical_result_passages=findings,tables=tables,parse_error=error,full_report_extraction_complete=False,clinical_results_verified=False,independent_review='Outstanding')
  target=D/'reports'/(rid+'.json');target.write_text(json.dumps(packet,indent=2,ensure_ascii=False),encoding='utf-8')
  inventory.append(dict(record_id=rid,title=r['title'],source_file=r['source_file'],source_sha256=r['source_sha256'],source_hash_verified=True,filename_extension=p.suffix,actual_format=kind,structured_table_count=len(tables),table_rows=sum(len(t['rows']) for t in tables),clinical_candidate_rows=nrows,clinical_result_passages=len(findings),graphics_only_tables=sum(t['graphics_only'] for t in tables),packet_file=str(target.relative_to(R)),packet_sha256=sha(target),parse_error=error,status='First-pass source capture only; detailed effect extraction/validation outstanding',extraction_complete=False,independent_review='Outstanding'))
 def write(p,rows,fields=None):
  with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else fields);w.writeheader();w.writerows(rows)
 for base in [R/'data',O]:
  write(base/'all184_source_capture_196.csv',inventory)
  write(base/'clinical_table_candidates_196.csv',candidate_rows,['record_id','table_id','table_row'])
 status=dict(queue_records=len(inventory),source_hashes_verified=len(inventory),actual_formats=dict(collections.Counter(x['actual_format'] for x in inventory)),source_suffix_xml_recovered=sum(x['filename_extension']=='.source' and x['actual_format']=='XML' for x in inventory),reports_with_candidate_rows=sum(bool(x['clinical_candidate_rows']) for x in inventory),clinical_candidate_rows=len(candidate_rows),reports_with_clinical_result_passages=sum(bool(x['clinical_result_passages']) for x in inventory),reports_with_graphics_only_tables=sum(bool(x['graphics_only_tables']) for x in inventory),parse_failures=failures,reports_without_candidate_rows=[x['record_id'] for x in inventory if not x['clinical_candidate_rows']],all184_capture_attempted=True,all184_fully_extracted=False,normalized_result_coverage_unchanged=159,independent_reviews_completed=0)
 (D/'status.json').write_text(json.dumps(status,indent=2),encoding='utf-8');print(json.dumps(status,indent=2))
if __name__=='__main__':main()
