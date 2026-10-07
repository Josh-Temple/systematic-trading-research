import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { execFileSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import yaml from "js-yaml";

const ROOT = process.cwd();
const REPO = "Josh-Temple/systematic-trading-research";
const CANONICAL_ROOT = "research/lines/horizontal-reaction-v0.1";
const WEB_DATA_PATH = "web/data/horizontal-reaction-v0.1.js";
const ID_RE = /^(?:RL|HYP|SPEC|DATA|EXP|RUN|RES|INT|DEC|DIAG)-HR-\d{3}(?:-v\d{2}|-ATTEMPT-\d+)?$/;
const RECORD_TYPES = new Map([
  ["RL", "ResearchLine"], ["HYP", "Hypothesis"], ["SPEC", "Specification"],
  ["DATA", "Dataset"], ["EXP", "Experiment"], ["RES", "Result"],
  ["INT", "Interpretation"], ["DEC", "Decision"], ["RUN", "Run"],
  ["DIAG", "Diagnostic"],
]);
const RELATION_TYPES = new Set([
  "tests_hypothesis", "uses_specification", "uses_dataset", "produced_by_run",
  "interprets_result", "supports", "contradicts", "supersedes", "invalidates",
  "corrects", "derived_from",
]);

const EXECUTION_STATUSES = new Set(["NOT_RUN", "SUCCESS", "FAILED", "BLOCKED"]);
const EVIDENCE_STATUSES = new Set(["VALID", "INVALID", "PARTIAL", "UNVERIFIED"]);
const SCIENTIFIC_STATUSES = new Set([
  "EXPLORATORY",
  "TESTING",
  "SUPPORTED",
  "NOT_SUPPORTED",
  "INCONCLUSIVE",
  "SUPERSEDED",
  "NOT_APPLICABLE",
]);

function fail(message) {
  throw new Error(message);
}

function assert(condition, message) {
  if (!condition) fail(message);
}

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const p = path.join(dir, entry.name);
    assert(!entry.isSymbolicLink(), `${p}: symbolic links are not canonical records`);
    return entry.isDirectory() ? walk(p) : [p];
  });
}

function repoRelative(filePath, root = ROOT) {
  return path.relative(root, filePath).replaceAll(path.sep, "/");
}

export function parseFrontmatter(text, file) {
  const normalized = text.replace(/^\uFEFF/, "").replaceAll("\r\n", "\n");
  if (!/^---[ \t]*(?:\n|$)/.test(normalized)) return null;
  const match = normalized.match(/^---[ \t]*\n([\s\S]*?)^---[ \t]*(?:\n|$)/m);
  assert(match, `${file}: YAML frontmatter is missing its closing delimiter`);
  try {
    return yaml.load(match[1], { schema: yaml.JSON_SCHEMA });
  } catch (error) {
    fail(`${file}: YAML frontmatter parse failed: ${error.message}`);
  }
}

// YAML aliases can form cycles. Reject them before recursive reference scanning;
// ordinary shared aliases are valid and are visited only once.
function validateMetadataGraph(value, file, active = new Set(), seen = new Set(), depth = 0) {
  if (!value || typeof value !== "object") return;
  assert(!active.has(value), `${file}: cyclic YAML aliases are not valid record metadata`);
  if (seen.has(value)) return;
  assert(depth <= 100, `${file}: record metadata nesting exceeds 100 levels`);
  assert(seen.size < 100_000, `${file}: record metadata exceeds 100000 objects`);
  seen.add(value);
  active.add(value);
  for (const child of Object.values(value)) validateMetadataGraph(child, file, active, seen, depth + 1);
  active.delete(value);
}

export function loadRecords(repositoryRoot = ROOT) {
  const root = path.join(repositoryRoot, CANONICAL_ROOT);
  const files = walk(root).filter((p) => /\.(?:md|ya?ml)$/i.test(p));
  const records = [];

  for (const filePath of files) {
    const rel = repoRelative(filePath, repositoryRoot);
    const filenameId = path.basename(filePath).replace(/\.(?:md|ya?ml)$/i, "");
    const text = fs.readFileSync(filePath, "utf8");
    let data = null;

    if (/\.md$/i.test(filePath)) {
      data = parseFrontmatter(text, rel);
      if (data === null) {
        assert(!ID_RE.test(filenameId), `${rel}: canonical record is missing YAML frontmatter`);
        continue;
      }
    } else {
      try {
        data = yaml.load(text, { schema: yaml.JSON_SCHEMA });
      } catch (error) {
        fail(`${rel}: YAML parse failed: ${error.message}`);
      }
    }

    assert(data && typeof data === "object" && !Array.isArray(data), `${rel}: metadata must be a mapping`);
    validateMetadataGraph(data, rel);

    const primaryId =
      typeof data.id === "string"
        ? data.id
        : typeof data.run_id === "string"
          ? data.run_id
          : typeof data.diagnostic_id === "string"
            ? data.diagnostic_id
            : null;

    if (!primaryId) {
      assert(
        !ID_RE.test(filenameId) && ![...RECORD_TYPES.values()].includes(data.type)
          && !["id", "run_id", "diagnostic_id"].some((key) => Object.hasOwn(data, key)),
        `${rel}: canonical record is missing a valid stable ID`
      );
      continue;
    }
    assert(ID_RE.test(primaryId), `${rel}: invalid stable ID ${primaryId}`);
    if (ID_RE.test(filenameId)) {
      assert(primaryId === filenameId, `${rel}: stable ID ${primaryId} does not match filename ${filenameId}`);
    }

    records.push({ path: rel, data, primaryId });
  }

  return records;
}

function collectExactIdStrings(value, out = new Set(), seen = new Set()) {
  if (typeof value === "string") {
    if (ID_RE.test(value)) out.add(value);
    return out;
  }
  if (value && typeof value === "object") {
    if (seen.has(value)) return out;
    seen.add(value);
    for (const item of Object.values(value)) collectExactIdStrings(item, out, seen);
  }
  return out;
}

export function validateRecordStructure(records) {
  const byId = new Map();

  for (const record of records) {
    const prefix = record.primaryId.split("-")[0].toUpperCase();
    const expectedType = RECORD_TYPES.get(prefix);
    assert(expectedType, `${record.path}: unsupported stable ID ${record.primaryId}`);
    if (prefix === "RUN" || prefix === "DIAG") {
      const identityField = prefix === "RUN" ? "run_id" : "diagnostic_id";
      assert(record.data[identityField] === record.primaryId, `${record.path}: invalid ${identityField}`);
      assert(record.data.type === undefined || record.data.type === expectedType,
        `${record.path}: type must be ${expectedType} when present`);
    } else {
      assert(record.data.id === record.primaryId && record.data.type === expectedType,
        `${record.path}: ID ${record.primaryId} requires type ${expectedType}`);
      if (prefix !== "RL") {
        assert(record.data.research_line_id === "RL-HR-001", `${record.path}: missing or wrong research_line_id`);
      }
    }
    if (byId.has(record.primaryId)) {
      fail(
        `duplicate stable ID ${record.primaryId}: ${byId.get(record.primaryId).path} and ${record.path}`
      );
    }
    byId.set(record.primaryId, record);
  }

  for (const record of records) {
    if (record.data.relations !== undefined) {
      assert(Array.isArray(record.data.relations), `${record.path}: relations must be an array`);
      for (const relation of record.data.relations) {
        assert(relation && RELATION_TYPES.has(relation.type) && typeof relation.target === "string"
          && ID_RE.test(relation.target) && byId.has(relation.target),
        `${record.path}: invalid relation type or target`);
      }
    }
    const refs = collectExactIdStrings(record.data);
    for (const ref of refs) {
      if (!byId.has(ref)) {
        fail(`${record.path}: structured reference ${ref} has no matching canonical record`);
      }
    }

    if (record.data.type === "Result") {
      const { execution_status, evidence_validity, scientific_status } = record.data;
      assert(
        EXECUTION_STATUSES.has(execution_status),
        `${record.path}: invalid or missing execution_status: ${execution_status}`
      );
      assert(
        EVIDENCE_STATUSES.has(evidence_validity),
        `${record.path}: invalid or missing evidence_validity: ${evidence_validity}`
      );
      assert(
        SCIENTIFIC_STATUSES.has(scientific_status),
        `${record.path}: invalid or missing scientific_status: ${scientific_status}`
      );
      assert(typeof record.data.run_id === "string" && record.data.run_id.startsWith("RUN-HR-"),
        `${record.path}: Result requires a run_id`);
      const run = byId.get(record.data.run_id);
      assert(run?.data.execution_status === execution_status,
        `${record.path}: Result execution_status differs from its Run`);
      if (execution_status !== "SUCCESS") {
        assert(scientific_status === "NOT_APPLICABLE",
          `${record.path}: a non-successful execution cannot have a scientific outcome`);
      }
    }
    if (record.primaryId.startsWith("RUN-")) {
      assert(EXECUTION_STATUSES.has(record.data.execution_status), `${record.path}: invalid Run execution_status`);
      for (const [key, prefix] of [["experiment_id", "EXP-HR-"], ["specification_id", "SPEC-HR-"]]) {
        assert(typeof record.data[key] === "string" && record.data[key].startsWith(prefix) && byId.has(record.data[key]),
          `${record.path}: invalid or missing ${key}`);
      }
    }
    if (record.primaryId.startsWith("DIAG-")) {
      assert(typeof record.data.target_run === "string" && record.data.target_run.startsWith("RUN-HR-")
        && byId.has(record.data.target_run), `${record.path}: invalid or missing target_run`);
    }
  }

  return byId;
}

function loadWebData() {
  const code = fs.readFileSync(path.join(ROOT, WEB_DATA_PATH), "utf8");
  const sandbox = { window: {} };
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, { filename: WEB_DATA_PATH });
  const data = sandbox.window.RESEARCH_UI_DATA;
  assert(data && typeof data === "object", `${WEB_DATA_PATH}: RESEARCH_UI_DATA missing`);
  return data;
}

function normalizeStatus(value) {
  return String(value).replaceAll("_", " ");
}

function formatInteger(value) {
  return Number(value).toLocaleString("en-US");
}

function formatFixed(value, digits, suffix = "") {
  const number = Number(value);
  const sign = number < 0 ? "−" : "";
  return `${sign}${Math.abs(number).toFixed(digits)}${suffix}`;
}

function metricsMap(hypothesis) {
  return new Map(hypothesis.metrics.map(([key, value]) => [key, value]));
}

function getRecord(byId, id) {
  const record = byId.get(id);
  if (!record) fail(`canonical record missing: ${id}`);
  return record;
}

function assertMetric(map, key, expected, scope) {
  assert(map.has(key), `${scope}: web metric missing: ${key}`);
  assert(
    map.get(key) === expected,
    `${scope}: web metric ${key} mismatch; expected "${expected}", got "${map.get(key)}"`
  );
}

function githubUrlToPath(url) {
  if (typeof url !== "string") return null;
  const prefix = `https://github.com/${REPO}/`;
  if (!url.startsWith(prefix)) return null;

  const rest = url.slice(prefix.length);
  const match = rest.match(/^(?:blob|tree)\/main\/(.+)$/);
  if (!match) return null;
  return decodeURIComponent(match[1]);
}

function collectStrings(value, out = []) {
  if (typeof value === "string") {
    out.push(value);
    return out;
  }
  if (Array.isArray(value)) {
    for (const item of value) collectStrings(item, out);
    return out;
  }
  if (value && typeof value === "object") {
    for (const item of Object.values(value)) collectStrings(item, out);
  }
  return out;
}

function validateWebLinks(web, byId) {
  const strings = collectStrings(web);

  for (const value of strings) {
    const localPath = githubUrlToPath(value);
    if (!localPath) continue;
    assert(
      fs.existsSync(path.join(ROOT, localPath)),
      `web projection link points to missing repository path: ${localPath}`
    );
  }

  for (const item of web.timeline) {
    for (const [label, url] of item.refs) {
      if (!ID_RE.test(label)) continue;
      const record = getRecord(byId, label);
      const localPath = githubUrlToPath(url);
      assert(localPath, `timeline ${label}: expected repository-local GitHub URL`);
      assert(
        localPath === record.path,
        `timeline ${label}: URL points to ${localPath}, canonical record is ${record.path}`
      );
    }
  }
}

function validateProjection(web, byId) {
  assert(
    /^[0-9a-f]{40}$/.test(web.meta?.canonicalSourceCommit ?? ""),
    "web meta.canonicalSourceCommit must be a full 40-character commit SHA"
  );

  const h1 = web.hypotheses.find((x) => x.id === "HYP-HR-001");
  const h2 = web.hypotheses.find((x) => x.id === "HYP-HR-002");
  const h3 = web.hypotheses.find((x) => x.id === "HYP-HR-003");
  assert(h1 && h2 && h3, "web hypotheses H1/H2/H3 must all be present");

  const res1 = getRecord(byId, "RES-HR-001").data;
  const res5 = getRecord(byId, "RES-HR-005").data;
  const res6 = getRecord(byId, "RES-HR-006").data;
  const exp7 = getRecord(byId, "EXP-HR-007").data;
  const data1 = getRecord(byId, "DATA-HR-001").data;
  const data2 = getRecord(byId, "DATA-HR-002").data;
  const data3 = getRecord(byId, "DATA-HR-003").data;

  assert(
    h1.status === normalizeStatus(res1.scientific_status),
    `H1 status mismatch: expected ${normalizeStatus(res1.scientific_status)}, got ${h1.status}`
  );
  const h1Metrics = metricsMap(h1);
  assertMetric(h1Metrics, "Trades", formatInteger(res1.headline_metrics.trades), "H1");
  assertMetric(h1Metrics, "Mean", formatFixed(res1.headline_metrics.mean_R, 4, " R"), "H1");
  assertMetric(h1Metrics, "Profit Factor", Number(res1.headline_metrics.profit_factor).toFixed(3), "H1");
  assertMetric(h1Metrics, "Max DD", formatFixed(res1.headline_metrics.max_drawdown_R, 2, " R"), "H1");

  const h2ExpectedStatus = normalizeStatus(res6.headline_metrics.classification);
  assert(h2.status === h2ExpectedStatus, `H2 status mismatch: expected ${h2ExpectedStatus}, got ${h2.status}`);
  const h2Metrics = metricsMap(h2);
  assertMetric(h2Metrics, "Events", formatInteger(res6.headline_metrics.primary_event_count), "H2");
  assertMetric(h2Metrics, "Mean", formatFixed(res6.headline_metrics.primary_mean_bps, 3, " bps"), "H2");
  assertMetric(
    h2Metrics,
    "Positive",
    `${(Number(res6.headline_metrics.primary_positive_rate) * 100).toFixed(2)}%`,
    "H2"
  );
  const [ciLo, ciHi] = res6.headline_metrics.primary_clustered_95ci_bps;
  assertMetric(
    h2Metrics,
    "95% CI",
    `${formatFixed(ciLo, 3)} to ${formatFixed(ciHi, 3)} bps`,
    "H2"
  );

  assert(
    h3.status === normalizeStatus(exp7.status),
    `H3 status mismatch: expected ${normalizeStatus(exp7.status)}, got ${h3.status}`
  );
  const h3Metrics = metricsMap(h3);
  assertMetric(h3Metrics, "Dataset", normalizeStatus(data3.role), "H3");
  assertMetric(h3Metrics, "Consumption", normalizeStatus(data3.consumption_status), "H3");

  const h3Runs = [...byId.values()].filter(
    (record) => record.data.experiment_id === "EXP-HR-007"
  );
  assert(h3Runs.length === 0, "H3 web says NOT RUN but a canonical Run exists for EXP-HR-007");
  assertMetric(h3Metrics, "Run", "NOT RUN", "H3");

  const datasetWeb = new Map(web.datasets.map((item) => [item.id, item]));
  for (const [id, canonical] of [
    ["DATA-HR-001", data1],
    ["DATA-HR-002", data2],
  ]) {
    const projected = datasetWeb.get(id);
    assert(projected, `web dataset missing: ${id}`);
    assert(
      projected.role === normalizeStatus(canonical.role),
      `${id}: role mismatch; expected ${normalizeStatus(canonical.role)}, got ${projected.role}`
    );
    assert(
      canonical.consumption_status === "CONSUMED",
      `${id}: canonical consumption boundary unexpectedly changed from CONSUMED`
    );
  }

  const projectedData3 = datasetWeb.get("DATA-HR-003");
  assert(projectedData3, "web dataset missing: DATA-HR-003");
  const expectedData3Role = `${normalizeStatus(data3.role)} / ${normalizeStatus(data3.consumption_status)}`;
  assert(
    projectedData3.role === expectedData3Role,
    `DATA-HR-003: role mismatch; expected ${expectedData3Role}, got ${projectedData3.role}`
  );

  assert(
    res5.headline_metrics.source_discrepancy === "PRESENT_UNRESOLVED",
    "RES-HR-005 source-discrepancy status changed; update projection logic deliberately"
  );
  assert(web.current.conflict.active === true, "unresolved H1 source conflict must remain active in web projection");
  assert(web.current.conflict.label === "SOURCE CONFLICT", "H1 conflict label must remain SOURCE CONFLICT");
  assert(
    web.diagnostics.currentLabel === res5.headline_metrics.current_integrated_report.current_classification_in_project_brief,
    "diagnostic current label is stale relative to RES-HR-005"
  );

  for (const blockedId of ["RES-HR-003", "RES-HR-006-ATTEMPT-1"]) {
    const canonical = getRecord(byId, blockedId).data;
    assert(canonical.execution_status === "BLOCKED", `${blockedId}: canonical execution status is no longer BLOCKED`);
    assert(
      canonical.scientific_status === "NOT_APPLICABLE",
      `${blockedId}: blocked record unexpectedly has scientific outcome ${canonical.scientific_status}`
    );
    const timelineItem = web.timeline.find((item) => item.refs.some(([label]) => label === blockedId));
    assert(timelineItem, `timeline missing blocked record ${blockedId}`);
    assert(timelineItem.kind === "BLOCKED", `timeline ${blockedId} must remain labeled BLOCKED`);
  }

  validateWebLinks(web, byId);
}

export function validateSourceCommit(web, repositoryRoot = ROOT) {
  const sourceCommit = web.meta.canonicalSourceCommit;
  assert(typeof sourceCommit === "string" && /^[0-9a-f]{40}$/.test(sourceCommit),
    "web meta.canonicalSourceCommit must be a full 40-character commit SHA");
  const git = (args) => execFileSync("git", args, { cwd: repositoryRoot, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
  try {
    git(["cat-file", "-e", `${sourceCommit}^{commit}`]);
    git(["merge-base", "--is-ancestor", sourceCommit, "HEAD"]);
  } catch {
    fail(`web canonicalSourceCommit ${sourceCommit} is missing or is not an ancestor of HEAD`);
  }
  try {
    git(["merge-base", "--is-ancestor", sourceCommit, "refs/remotes/origin/main"]);
  } catch {
    fail(`web canonicalSourceCommit ${sourceCommit} is not in origin/main history, or origin/main is missing; fetch full main history before validation`);
  }

  // Compare the bytes being validated, including staged/unstaged changes.
  // A HEAD-only diff misses local edits and an untracked new canonical record.
  const changedCanonical = [
    ...git(["diff", "--name-only", "-z", sourceCommit, "--", CANONICAL_ROOT]).split("\0"),
    ...git(["ls-files", "--others", "-z", "--", CANONICAL_ROOT]).split("\0"),
  ].filter(Boolean);

  assert(
    changedCanonical.length === 0,
    [
      `web projection is stale: canonical research changed after ${sourceCommit}`,
      ...changedCanonical.map((p) => `  - ${p}`),
      "Update the Web projection from the new canonical main state, then set meta.canonicalSourceCommit to that already-merged canonical commit.",
    ].join("\n")
  );
}

function runNegativeSelfTests(web, byId) {
  const metricMismatch = structuredClone(web);
  const h1 = metricMismatch.hypotheses.find((x) => x.id === "HYP-HR-001");
  h1.metrics = h1.metrics.map(([k, v]) => (k === "Trades" ? [k, "2,686"] : [k, v]));

  let metricFailed = false;
  try {
    validateProjection(metricMismatch, byId);
  } catch {
    metricFailed = true;
  }
  assert(metricFailed, "negative self-test failed: deliberate H1 metric mismatch was not detected");

  const brokenLink = structuredClone(web);
  brokenLink.current.conflict.canonical =
    `https://github.com/${REPO}/blob/main/research/lines/horizontal-reaction-v0.1/results/DOES-NOT-EXIST.md`;

  let linkFailed = false;
  try {
    validateProjection(brokenLink, byId);
  } catch {
    linkFailed = true;
  }
  assert(linkFailed, "negative self-test failed: deliberate missing canonical link was not detected");
}

export function validateResearchConsistency() {
  const records = loadRecords();
  const byId = validateRecordStructure(records);
  const web = loadWebData();

  validateProjection(web, byId);
  validateSourceCommit(web);
  runNegativeSelfTests(web, byId);

  const results = [...byId.values()].filter((record) => record.data.type === "Result").length;
  return {
    status: "PASS",
    canonicalRecordCount: byId.size,
    resultRecordCount: results,
    webProjection: WEB_DATA_PATH,
    canonicalSourceCommit: web.meta.canonicalSourceCommit,
    negativeSelfTests: ["metric mismatch detected", "missing canonical link detected"],
    note: "This checks structural/projection consistency only; it does not recompute scientific results.",
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  console.log(JSON.stringify(validateResearchConsistency(), null, 2));
}
