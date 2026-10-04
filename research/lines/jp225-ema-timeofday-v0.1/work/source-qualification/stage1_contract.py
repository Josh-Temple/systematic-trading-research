"""Fixed acquisition contract; no market-performance calculation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

SYMBOL = 'JP225Cash'
START = 1732838400  # 2024-11-29 UTC request convention
DISCOVERY_START = 1735689600
HOLDOUT_START = 1767225600
# Last M1 open, not next year's first bar. copy_rates_range end is inclusive.
END = HOLDOUT_START - 60
M1_FIELDS = ('time','open','high','low','close','tick_volume','spread','real_volume')
TICK_FIELDS = ('time','bid','ask','last','volume','time_msc','flags','volume_real')
SYMBOL_FIELDS = ('name','digits','point','trade_tick_size','trade_contract_size',
                 'volume_min','volume_step','chart_mode')
PROBES = [
 ('P1_2025_01_TOKYO_OPEN','2025-01-15T23:35:00','2025-01-16T00:20:00'),
 ('P2_2025_04_TOKYO_CLOSE','2025-04-15T06:00:00','2025-04-15T07:00:00'),
 ('P3_2025_07_TOKYO_OPEN','2025-07-15T23:35:00','2025-07-16T00:20:00'),
 ('P4_2025_10_TOKYO_CLOSE','2025-10-15T06:00:00','2025-10-15T07:00:00')]

def utc(s):
    d = datetime.fromisoformat(s)
    if d.tzinfo is not None:
        return d.astimezone(timezone.utc)
    return d.replace(tzinfo=timezone.utc)

def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',',':'), allow_nan=False).encode()

def allowlist(obj, fields):
    d = obj._asdict() if obj is not None and hasattr(obj,'_asdict') else {}
    return {k:d.get(k) for k in fields}

def boundary_check(rows, tick=False):
    # Inspect timestamps before serializing any market field. Do not drop violations.
    for row in rows:
        t = int(row['time'])
        if not START <= t < HOLDOUT_START:
            raise ValueError('BOUNDARY_VIOLATION')
        if tick and (int(row['time_msc']) // 1000 != t):
            raise ValueError('TIMESTAMP_IDENTITY_VIOLATION')
