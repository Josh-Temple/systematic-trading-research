# Architecture artifact validation

対象: 2026-10-01に作成したpre-outcome plan。market executionやstrategy testのvalidationではない。

確認:

- 開始時mainと保存前main: `1bba695ea252863c3b7366b8b910aa36e211c325`、一致。
- 既存provisional head: `4b0a6e54f7186308c2e9b1e14a6605fae018c42e`、reviewのみ、変更/mergeなし。
- Markdown relative linksをlocal filesystemで照合しbroken linkなし。
- 8PacketにRole/Objective/Required fresh reads/Allowed/Forbidden/Outcome permission/Failure/Completion/readbackの各fieldが存在。
- canonical entity/packet IDsに重複なし。provisional001 IDsを実行契約として再利用していない。
- gate templateはmarket_outcome_access=false、HUMAN_BOUNDARY、identity null。PASS receiptではない。
- A/B/C/D/E/X/Rのwrite pathは分離、shared canonical updatesはIに限定。
- 一回のempirical実行と後のInterpretationを別担当に分離。human freezeとexact-input独立監査の順序を固定。
- source欠測とnegative、scientific nullとinsufficiency、reference associationとcausal tradeを分離。
- first-monthのsource buffer: Nov2009 endpoint→Dec2009 formation→Jan2010 target。end Sep2026。翌月が未完成のeventを含めない。
- 数学の符号: q=foreign perEUR、v=-logq、P_ab=q_b/q_a（b per a）。random-directed-logpair期待0はsimple/cost/risk-adjusted returnへ外挿しない。
- documents-onlyでmarket code、dataset、Result、Runは作成していない。strategy/Sharpe/current ranking/horizon searchなし。

未検証:

- Dが作る実装/tests。Packetだけでimplementation readyとはしない。
- actual ECB7 series/coverage/API/schema/calendar、historical clock/original vintage。CとX preflightで確認する。
- external repo codeの独立execution/replication、全history/issues網羅。
- ZhangとIwanaga/Sakemoto full text。access gapはAに割当。
- empirical effect、net economics、factor independence、confirmation。

remote readbackでは保存commitの全file bytesをlocal SHA256と照合する。この文書のlocalチェックをremote保存の証明として代用しない。


## Independent review addendum — 2026-10-01

Reviewed proposal branch head: `4f71e41419cf3424b54b90ed6f267aede3a16ca7` (main remained `1bba695ea252863c3b7366b8b910aa36e211c325`).

- Added Hutchinson et al. (2022) after reading its author-accepted full text. The plan records the paper as an adverse post-2010 prior, while spelling out that its excess-return basket construction and sample are not the same as this single-extreme ECB-reference spot screen. The 2010–2026 window overlaps known published evidence and is not an independent holdout.
- Added official ECB copyright and ESCB statistics reuse conditions to the source review and C Packet: cite the source, preserve public source statistics/metadata accurately, disclose transformations, and account for possible revisions. Public snapshot storage remains a C qualification item.
- Re-read all 20 Markdown artifacts and 8 Work Packets at the reviewed head. Relative Markdown links: 0 broken. Duplicate entity/packet IDs: 0. Required role, objective, fresh-read, forbidden-action, outcome-permission, failure, and deliverable sections: present in all 8 Packets.
- Gate template still has `market_outcome_access=false`, `state=HUMAN_BOUNDARY`, and null input identities; it is not a PASS receipt.
- No historical FX series was downloaded and no selected-pair return, strategy metric, Sharpe ratio, or currency ranking was calculated.

The readback checks above apply to the proposal head named at the start of this addendum; this addendum records those checks and does not authorize market-outcome access.
