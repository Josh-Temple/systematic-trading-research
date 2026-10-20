---
id: DEC-CSM-002
type: Decision
research_line_id: RL-CSM-001
created_at: 2026-10-01
status: ACTIVE_PREPARATION_ONLY
decision: HUMAN_BOUNDARY
based_on:
  - REVIEW-CSM-002
  - HYP-CSM-002
  - SPEC-CSM-002-v01
relations:
  - type: derived_from
    target: REVIEW-CSM-002
---

# Authorize preparation; keep market outcome gate closed

Research Architectの判断: A–Dのoutcome-blind準備とE/Iによる監査・統合は実行可能。各workerは自分のpathに成果を書き、canonical仕様やdataset roleを変更しない。

市場outcomeの計算は未許可。人間がSPEC-CSM-002-v01の具体契約を確定し、source/code/test/gate receiptを揃えた後、Xへ別指示を渡す。既存provisional branchを正本化したり、そのFROZEN宣言を承認に置き換えたりしない。

negative evidenceの既存報告は低費用screenを妨げないが、large infrastructureや戦略採用を正当化しない。H3/Pilot source、results、Web projectionの更新はscope外。
