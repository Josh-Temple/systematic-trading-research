from datetime import datetime, timedelta


def trailing_return(values, end, lookback):
    return values[end] / values[end - lookback] - 1.0


def test_prefix_invariance():
    values = [100.0, 102.0, 99.0, 104.0, 107.0, 90.0, 150.0]
    lookback = 2
    for end in range(lookback, 5):
        full = trailing_return(values, end, lookback)
        prefix = trailing_return(values[: end + 1], end, lookback)
        assert full == prefix
    altered = values[:5] + [-1000.0, 0.01]
    for end in range(lookback, 5):
        assert trailing_return(values, end, lookback) == trailing_return(altered, end, lookback)


def test_pair_extreme_identity():
    scores = {"AUD": 0.04, "CAD": -0.02, "EUR": 0.01, "JPY": -0.05}
    long_ccy = max(scores, key=scores.get)
    short_ccy = min(scores, key=scores.get)
    pair_returns = {
        (a, b): scores[a] - scores[b]
        for a in scores
        for b in scores
        if a != b
    }
    max_pair = max(pair_returns, key=pair_returns.get)
    assert max_pair == (long_ccy, short_ccy)
    assert pair_returns[max_pair] == max(scores.values()) - min(scores.values())


def test_lagged_return_and_turnover_cost_path():
    weights = [1.0, 1.0, 0.0]
    returns = [0.20, 0.10, -0.30]
    held = [0.0] + weights[:-1]
    turnover = [abs(weights[0])] + [
        abs(weights[i] - weights[i - 1]) for i in range(1, len(weights))
    ]
    cost_rate = 1.0 / 10000.0
    net = [held[i] * returns[i] - turnover[i] * cost_rate for i in range(len(weights))]
    assert net[0] == -cost_rate
    assert net[1] == 0.10
    assert net[2] < 0.0
    assert turnover == [1.0, 0.0, 1.0]


def test_higher_timeframe_availability_alignment():
    htf_open = datetime(2026, 1, 2, 0, 0)
    htf_close = htf_open + timedelta(hours=1)
    small = timedelta(minutes=15)
    base_opens = [htf_open + small * i for i in range(4)]
    correct_merge_key = htf_open + timedelta(hours=1) - small
    visible = [t for t in base_opens if t >= correct_merge_key]
    assert visible == [datetime(2026, 1, 2, 0, 45)]
    signal_candle_close = visible[0] + small
    assert signal_candle_close == htf_close
    raw_open_timestamp_matches = [t for t in base_opens if t >= htf_open]
    assert raw_open_timestamp_matches == base_opens
    assert all(t < htf_close for t in raw_open_timestamp_matches[:3])


def main():
    checks = [
        ("prefix invariance", test_prefix_invariance),
        ("cross-sectional maximum-pair identity", test_pair_extreme_identity),
        ("lagged returns and applied turnover cost", test_lagged_return_and_turnover_cost_path),
        ("higher-timeframe availability alignment", test_higher_timeframe_availability_alignment),
    ]
    for name, check in checks:
        check()
        print(f"PASS {name}")
    print(f"RESULT: {len(checks)}/{len(checks)} passed; synthetic inputs only")


if __name__ == "__main__":
    main()
