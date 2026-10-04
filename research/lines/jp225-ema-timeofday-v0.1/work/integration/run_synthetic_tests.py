"""All JP225 synthetic tests, without any network, MT5 package, or market source."""
import sys,unittest,hashlib,json,platform
from pathlib import Path
ROOT=Path(__file__).parents[1]
paths=[ROOT/'implementation',ROOT/'source-qualification']
for p in paths:sys.path.insert(0,str(p))
suite=unittest.TestSuite()
for p in paths:suite.addTests(unittest.TestLoader().discover(str(p),pattern='test_*.py'))
r=unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'python':platform.python_version(),'tests':r.testsRun,'success':r.wasSuccessful(),
    'market_data_accessed':False,'files_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(ROOT.rglob('*.py')) if 'proxy' not in str(p)}},indent=2))
raise SystemExit(0 if r.wasSuccessful() else 1)
