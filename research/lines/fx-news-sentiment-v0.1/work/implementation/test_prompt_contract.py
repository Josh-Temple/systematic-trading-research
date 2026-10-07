import json
import unittest
from prompt_contract import parse_output, validate_batch

class PromptContractTest(unittest.TestCase):
    def row(self):
        return dict(record_id='synthetic-1', EUR='APPRECIATION', JPY='NOT_MENTIONED', reason_code_EUR='POLICY', reason_code_JPY='NONE')
    def test_valid(self):
        self.assertEqual(parse_output(json.dumps(self.row()), 'synthetic-1'), self.row())
    def test_missing_extra_identity_enum_reason(self):
        for key,value in [('extra','x'),('record_id','wrong'),('EUR','BULLISH'),('reason_code_JPY','POLICY'),('reason_code_EUR','BAD'),('JPY',None)]:
            row=self.row(); row[key]=value
            with self.subTest(key=key), self.assertRaises(ValueError):
                parse_output(json.dumps(row),'synthetic-1')
        row=self.row(); del row['JPY']
        with self.assertRaises(ValueError): parse_output(json.dumps(row),'synthetic-1')
    def test_duplicate_keys(self):
        raw=json.dumps(self.row()).replace('"EUR": "APPRECIATION"','"EUR": "APPRECIATION", "EUR": "DEPRECIATION"')
        with self.assertRaises(ValueError): parse_output(raw,'synthetic-1')
    def test_markdown_and_array_rejected(self):
        for raw in ['```json\n'+json.dumps(self.row())+'\n```',json.dumps([self.row()])]:
            with self.assertRaises(ValueError): parse_output(raw,'synthetic-1')
    def test_missing_and_duplicate_batch(self):
        with self.assertRaises(ValueError): validate_batch([],['synthetic-1'])
        with self.assertRaises(ValueError): validate_batch([json.dumps(self.row())]*2,['synthetic-1']*2)
