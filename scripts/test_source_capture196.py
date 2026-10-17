"""Synthetic parser fixtures only; no invented research records."""
import unittest
from capture_all184_196 import detect,xml_capture,html_capture,CLINICAL
class SourceCaptureTests(unittest.TestCase):
 def test_xml_without_xml_extension(self):
  raw=b'<!DOCTYPE article><article><body><sec><title>Results</title><p>Marker text.</p></sec></body></article>'
  self.assertEqual(detect(raw),'XML')
 def test_html_and_pdf(self):
  self.assertEqual(detect(b'<!DOCTYPE html><html><body><p>x</p></body></html>'),'HTML')
  self.assertEqual(detect(b'%PDF-1.7\nx'),'PDF')
 def test_actual_row_spans_preserved(self):
  raw=b'<article><body><table-wrap id="t"><table><tr><th colspan="2">Heading</th></tr><tr><td rowspan="2">Label</td><td>value</td></tr></table></table-wrap></body></article>'
  _,tables=xml_capture(raw)
  self.assertEqual(tables[0]['rows'][0][0]['colspan'],'2')
  self.assertEqual(tables[0]['rows'][1][0]['rowspan'],'2')
 def test_html_reference_sections_not_results(self):
  p,t=html_capture(b'<html><body><h2>Results</h2><p>Original result.</p><h2>References</h2><p>Cited material.</p></body></html>')
  self.assertEqual([x['text'] for x in p],['Original result.'])
 def test_component_abbreviations_and_surrogate_boundary(self):
  for x in ['SBP','DBP','WC','FBS','FBG','FPG','TG','HDL','MetS']:self.assertTrue(CLINICAL.search(x),x)
  self.assertFalse(CLINICAL.search('METS-IR'))
if __name__=='__main__':unittest.main()
