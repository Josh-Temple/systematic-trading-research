window.RESEARCH_UI_DATA = {
  meta: {
    title: "Systematic Trading Research",
    subtitle: "研究状態を、現在・証拠・履歴・データ境界に分けて読む",
    projectionGeneratedAt: "2026-09-28",
    canonicalSourceCommit: "78a3f335a6c66bcfda605f53435d3ec72cde0743",
    authority: "Derived view. Canonical authority is the GitHub research record."
  },
  line: {
    id: "RL-HR-001",
    title: "Horizontal Reaction Strategy v0.1",
    instrument: "XAU/USD",
    scope: "直近の水平サポート／レジスタンス反応が、確認後の実行・SL/TP・15分time stop・BID/ASKコストを経ても残るかを検証する研究。",
    status: "ACTIVE RESEARCH",
    canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/LINE.md",
    current: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/CURRENT.md"
  },
  current: {
    conflict: {
      active: true,
      label: "SOURCE CONFLICT",
      title: "H1 D1–D5の履歴資料に未解決の不一致",
      body: "2026-09-13資料は EDGE_LOST_BEFORE_ENTRY、2026-09-23資料／Project Briefは MULTIPLE_DRIVERS / INCONCLUSIVE。endpoint数・一部推定値も一致せず、Knowledge Baseは統合せず両方を保持している。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-005.md"
    },
    nextTest: {
      label: "NEXT",
      title: "Post-H2 Confirmation Selection Effect",
      status: "WAITING FOR MATURITY",
      body: "DEC-HR-004でexact H2 legacy generatorの実装同一性をoutcome-blindに固定済み。2026-07-10以降の最初の60 structurally eligible sessionsをfreezeし、source gateがPASSした後に1回だけ既存preregistrationを実行する。それまではoutcome-blindなsource/sample準備だけが許可される。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/experiments/EXP-HR-007.md"
    },
    forbidden: [
      "2026H1 / 2026H2でのparameter・threshold・subset・horizon・filter rescue",
      "H3の60-session maturityとsource gate PASS前のtouch outcome閲覧",
      "CONFIRMED vs UNCONFIRMED比較・primary contrast・bootstrapの先行計算",
      "provider substitution / price imputation / broker・live trade"
    ]
  },
  hypotheses: [
    {
      id: "HYP-HR-001",
      label: "H1 · EXECUTION-AWARE",
      title: "v0.1 confirmation-entry strategy",
      status: "NOT SUPPORTED",
      tone: "negative",
      summary: "凍結したv0.1は、消費済み2026H1 sampleでexecution-aware候補として支持されなかった。",
      metrics: [
        ["Trades", "2,685"],
        ["Mean", "−0.2016 R"],
        ["Profit Factor", "0.660"],
        ["Max DD", "542.17 R"]
      ],
      note: "この結果は全てのhorizontal reactionの不存在を意味しない。H1診断はexploratoryで、現在の統合解釈にはsource conflictが残る。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-001.md"
    },
    {
      id: "HYP-HR-002",
      label: "H2 · UNCONDITIONAL TOUCH",
      title: "Unconditional touch replication",
      status: "NO UNCONDITIONAL TOUCH SUPPORT",
      tone: "negative",
      summary: "別の固定60-session sampleで、無条件touch→+15分のdirection-aware反応は支持されなかった。",
      metrics: [
        ["Events", "4,786"],
        ["Mean", "−1.379 bps"],
        ["Positive", "46.95%"],
        ["95% CI", "−1.909 to −0.862 bps"]
      ],
      note: "これはprofitabilityやhorizontal reactionの普遍的不在を示すものではない。H2 sampleはconsumed。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-006.md"
    },
    {
      id: "HYP-HR-003",
      label: "H3 · CONFIRMATION SELECTION",
      title: "Confirmation Selection Effect",
      status: "WAITING FOR MATURITY",
      tone: "pending",
      summary: "CONFIRMED touchがUNCONFIRMED touchより+15分反応が高いかを、別のunused sampleで検証するpreregistered test。",
      metrics: [
        ["Dataset", "FINAL HOLDOUT"],
        ["Consumption", "UNUSED"],
        ["Start", "2026-07-10"],
        ["Run", "NOT RUN"]
      ],
      note: "60 eligible sessionsのfreezeとsource gate PASSまでoutcome accessは禁止。legacy Gammaのtemporal-information limitationはDEC-HR-004で明示的に保持。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-003-v01.md"
    }
  ],
  diagnostics: {
    currentLabel: "MULTIPLE_DRIVERS / INCONCLUSIVE",
    currentSummary: "2026-09-23の統合資料では、touch後の反応の一部はentry前に消費／減衰し、entry後pathとspread costも結果を悪化させたという複数要因の記述。ただしexploratoryで因果は確定していない。",
    points: [
      ["D1 touch→entry", "+0.331 R", "反応の一部はentry前に存在"],
      ["D4 touch→+15m", "+0.125 R", "固定matched populationでtouch後反応"],
      ["D2 entry→+15m", "−0.205 R", "entry後のno-barrier pathは負"],
      ["D3 stopped→+15m", "−1.034 R", "stop後反実仮想も平均では弱い"],
      ["Spread drag", "+0.1603 R", "same-exit timestamp midpoint比較。formal D5ではない"]
    ],
    canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/interpretations/INT-HR-002.md",
    links: [
      ["Current interpretation", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/interpretations/INT-HR-002.md"],
      ["Source-conflict result", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-005.md"]
    ]
  },
  datasets: [
    {
      id: "DATA-HR-001",
      title: "2026H1 execution-aware evaluation",
      role: "CONSUMED HOLDOUT",
      tone: "consumed",
      window: "Eligibility 2026-01-02 → 2026-06-30 / frozen 60 sessions",
      use: "再現・明示的error correction・既定diagnosticは可。新しいrule選択には使用不可。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-001.md"
    },
    {
      id: "DATA-HR-002",
      title: "2026H2 unconditional-touch replication",
      role: "CONSUMED HOLDOUT",
      tone: "consumed",
      window: "Selected sessions 2026-04-13 → 2026-07-09",
      use: "H2 outcome access済み。parameter / horizon / subset / trading-rule designには再利用不可。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-002.md"
    },
    {
      id: "DATA-HR-003",
      title: "Post-H2 confirmation-selection sample",
      role: "FINAL HOLDOUT / UNUSED",
      tone: "unused",
      window: "2026-07-10 onward / first 60 eligible sessions",
      use: "source/sample identity準備のみ。maturity + source gate前のoutcome access禁止。",
      canonical: "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/datasets/DATA-HR-003.md"
    }
  ],
  timeline: [
    {
      date: "2026-09-11",
      kind: "FREEZE",
      title: "v0.1 preregistration / H1 evaluation freeze",
      refs: [["SPEC-HR-001-v01", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-001-v01.md"]]
    },
    {
      date: "2026-09-11",
      kind: "RESULT",
      title: "H1 execution-aware result: NOT SUPPORTED",
      refs: [["RES-HR-001", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-001.md"]]
    },
    {
      date: "2026-09-12",
      kind: "BLOCKED",
      title: "D1–D5 replay stopped before computation",
      refs: [["RES-HR-003", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-003.md"]]
    },
    {
      date: "2026-09-13+",
      kind: "EXPLORATORY",
      title: "H1 ledger / D1–D5 diagnostic work",
      refs: [
        ["RES-HR-004", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-004.md"],
        ["RES-HR-005", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-005.md"]
      ]
    },
    {
      date: "2026-09-13+",
      kind: "BLOCKED",
      title: "H2 first attempt stopped at source gate",
      refs: [["RES-HR-006-ATTEMPT-1", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-006-ATTEMPT-1.md"]]
    },
    {
      date: "2026-09-13+",
      kind: "RESULT",
      title: "H2 unconditional-touch replication completed",
      refs: [["RES-HR-006", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/results/RES-HR-006.md"]]
    },
    {
      date: "2026-09-23",
      kind: "FREEZE",
      title: "H3 confirmation-selection preregistered",
      refs: [["SPEC-HR-003-v01", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/specifications/SPEC-HR-003-v01.md"]]
    },
    {
      date: "2026-09-27",
      kind: "CURRENT",
      title: "H3 WAITING FOR MATURITY / outcome access held",
      refs: [["DEC-HR-003", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/decisions/DEC-HR-003.md"]]
    },
    {
      date: "2026-09-28",
      kind: "DECISION",
      title: "H3 legacy implementation identity frozen outcome-blind",
      refs: [["DEC-HR-004", "https://github.com/Josh-Temple/systematic-trading-research/blob/main/research/lines/horizontal-reaction-v0.1/decisions/DEC-HR-004.md"]]
    }
  ],
  canonicalBase: "https://github.com/Josh-Temple/systematic-trading-research/tree/main/research/lines/horizontal-reaction-v0.1"
};