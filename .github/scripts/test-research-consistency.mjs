import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import test from "node:test";
import yaml from "js-yaml";
import {
  loadRecords, parseFrontmatter, validateRecordStructure, validateSourceCommit,
} from "./validate-research-consistency.mjs";

const canonicalRoot = "research/lines/horizontal-reaction-v0.1";
const repositoryRoot = path.resolve(import.meta.dirname, "../..");

function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "research-consistency-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, canonicalRoot), { recursive: true });
  return root;
}

function write(root, filename, text) {
  const target = path.join(root, canonicalRoot, filename);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, text);
}

function entity(id, type, extra = {}) {
  return { id, type, ...(type === "ResearchLine" ? {} : { research_line_id: "RL-HR-001" }), ...extra };
}

function writeEntity(root, filename, metadata) {
  write(root, filename, `---\n${yaml.dump(metadata)}---\n# Synthetic record\n`);
}

function seed(root) {
  writeEntity(root, "LINE.md", entity("RL-HR-001", "ResearchLine"));
  writeEntity(root, "hypotheses/HYP-HR-001.md", entity("HYP-HR-001", "Hypothesis"));
  writeEntity(root, "specifications/SPEC-HR-001-v01.md", entity("SPEC-HR-001-v01", "Specification"));
  writeEntity(root, "experiments/EXP-HR-001.md", entity("EXP-HR-001", "Experiment"));
  write(root, "runs/RUN-HR-001.yaml", yaml.dump({
    run_id: "RUN-HR-001", experiment_id: "EXP-HR-001",
    specification_id: "SPEC-HR-001-v01", execution_status: "BLOCKED",
  }));
  writeEntity(root, "results/RES-HR-001.md", entity("RES-HR-001", "Result", {
    run_id: "RUN-HR-001", execution_status: "BLOCKED",
    evidence_validity: "UNVERIFIED", scientific_status: "NOT_APPLICABLE",
  }));
}

function validate(root) { return validateRecordStructure(loadRecords(root)); }
function git(root, ...args) { return execFileSync("git", args, { cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim(); }
function commit(root) {
  git(root, "add", ".");
  git(root, "-c", "user.name=Synthetic test", "-c", "user.email=test@example.invalid", "commit", "-qm", "Synthetic fixture");
  return git(root, "rev-parse", "HEAD");
}
function gitFixture(t) {
  const root = fixture(t);
  write(root, "LINE.md", "# Synthetic source\n");
  git(root, "init", "-q", "-b", "main");
  const sha = commit(root);
  git(root, "update-ref", "refs/remotes/origin/main", sha);
  return { root, web: { meta: { canonicalSourceCommit: sha } } };
}

test("valid synthetic records preserve BLOCKED versus scientific outcome", (t) => {
  const root = fixture(t); seed(root);
  assert.equal(validate(root).size, 6);
});

test("ordinary narrative and CurrentProjection remain noncanonical", (t) => {
  const root = fixture(t); seed(root);
  write(root, "NOTES.md", "# Narrative without metadata\n");
  writeEntity(root, "CURRENT.md", { type: "CurrentProjection", research_line_id: "RL-HR-001" });
  assert.equal(validate(root).size, 6);
});

test("frontmatter accepts BOM and CRLF without changing string dates", () => {
  const metadata = parseFrontmatter("\uFEFF---\r\nid: HYP-HR-001\r\ncreated_at: 2026-10-08\r\n---\r\n# Title", "fixture.md");
  assert.equal(metadata.id, "HYP-HR-001");
  assert.equal(metadata.created_at, "2026-10-08");
});

test("unclosed frontmatter fails instead of silently skipping a record", () => {
  assert.throws(() => parseFrontmatter("---\nid: HYP-HR-001\n", "fixture.md"), /fixture.md:.*closing delimiter/);
});

test("invalid YAML and duplicate YAML keys fail with the source path", () => {
  for (const text of ["id: [", "id: HYP-HR-001\nid: HYP-HR-002"]) {
    assert.throws(() => parseFrontmatter(`---\n${text}\n---\n`, "fixture.md"), /fixture.md:.*parse failed/);
  }
});

test("an ID-named entity cannot lose all frontmatter", (t) => {
  const root = fixture(t); seed(root);
  write(root, "hypotheses/HYP-HR-001.md", "# Synthetic missing metadata\n");
  assert.throws(() => validate(root), /missing YAML frontmatter/);
});

test("metadata must be a mapping, not a scalar or sequence", (t) => {
  const root = fixture(t);
  for (const text of ["- HYP-HR-001", "scalar", "null"]) {
    write(root, "invalid.yaml", text);
    assert.throws(() => validate(root), /metadata must be a mapping/);
  }
});

test("missing, non-string and malformed stable IDs are rejected", (t) => {
  const root = fixture(t);
  for (const id of [undefined, 7, "HYP-HR-BAD", "hyp-hr-001"]) {
    writeEntity(root, "candidate.md", { type: "Hypothesis", ...(id === undefined ? {} : { id }) });
    assert.throws(() => validate(root), /stable ID/);
  }
});

test("entity type and line identity cannot bypass Result status validation", (t) => {
  const root = fixture(t); seed(root);
  writeEntity(root, "results/RES-HR-001.md", entity("RES-HR-001", "Reslut"));
  assert.throws(() => validate(root), /requires type Result/);
  writeEntity(root, "results/RES-HR-001.md", { id: "RES-HR-001", type: "Result" });
  assert.throws(() => validate(root), /research_line_id/);
});

test("ID-named files must agree with their stable ID", (t) => {
  const root = fixture(t); seed(root);
  writeEntity(root, "hypotheses/HYP-HR-001.md", entity("HYP-HR-002", "Hypothesis"));
  assert.throws(() => validate(root), /does not match filename/);
});

test("duplicate IDs and dangling structured references fail", (t) => {
  const root = fixture(t); seed(root);
  writeEntity(root, "copy.md", entity("HYP-HR-001", "Hypothesis"));
  assert.throws(() => validate(root), /duplicate stable ID/);
  fs.rmSync(path.join(root, canonicalRoot, "copy.md"));
  writeEntity(root, "experiments/EXP-HR-001.md", entity("EXP-HR-001", "Experiment", { tests_hypothesis: "HYP-HR-999" }));
  assert.throws(() => validate(root), /reference HYP-HR-999/);
});

test("cyclic aliases fail explicitly and ordinary shared aliases remain valid", (t) => {
  const root = fixture(t); seed(root);
  write(root, "hypotheses/HYP-HR-001.md", "---\nid: HYP-HR-001\ntype: Hypothesis\nresearch_line_id: RL-HR-001\nnotes: &cycle [*cycle]\n---\n");
  assert.throws(() => validate(root), /cyclic YAML aliases/);
  write(root, "hypotheses/HYP-HR-001.md", "---\nid: HYP-HR-001\ntype: Hypothesis\nresearch_line_id: RL-HR-001\nnotes: &note {ref: RL-HR-001}\nshared: [*note, *note]\n---\n");
  assert.equal(validate(root).size, 6);
});

test("symbolic links cannot introduce metadata outside the repository", (t) => {
  const root = fixture(t); seed(root);
  const target = path.join(root, "external.md");
  fs.writeFileSync(target, "# External synthetic narrative\n");
  fs.symlinkSync(target, path.join(root, canonicalRoot, "external.md"));
  assert.throws(() => validate(root), /symbolic links/);
});

test("a blocked Result cannot claim a scientific outcome", (t) => {
  const root = fixture(t); seed(root);
  writeEntity(root, "results/RES-HR-001.md", entity("RES-HR-001", "Result", {
    run_id: "RUN-HR-001", execution_status: "BLOCKED", evidence_validity: "VALID", scientific_status: "SUPPORTED",
  }));
  assert.throws(() => validate(root), /non-successful execution/);
});

test("Result and Run execution statuses must agree", (t) => {
  const root = fixture(t); seed(root);
  writeEntity(root, "results/RES-HR-001.md", entity("RES-HR-001", "Result", {
    run_id: "RUN-HR-001", execution_status: "SUCCESS", evidence_validity: "VALID", scientific_status: "NOT_SUPPORTED",
  }));
  assert.throws(() => validate(root), /differs from its Run/);
});

test("Run references cannot substitute a different entity kind", (t) => {
  const root = fixture(t); seed(root);
  write(root, "runs/RUN-HR-001.yaml", yaml.dump({ run_id: "RUN-HR-001", experiment_id: "HYP-HR-001", specification_id: "SPEC-HR-001-v01", execution_status: "BLOCKED" }));
  assert.throws(() => validate(root), /invalid or missing experiment_id/);
});

test("malformed relations cannot disappear from reference scanning", (t) => {
  const root = fixture(t); seed(root);
  for (const relation of [null, { type: "uses_datset", target: "HYP-HR-001" }, { type: "derived_from", target: "HYP-HR-BAD" }]) {
    writeEntity(root, "hypotheses/HYP-HR-001.md", entity("HYP-HR-001", "Hypothesis", { relations: [relation] }));
    assert.throws(() => validate(root), /invalid relation/);
  }
});

test("an unchanged source and unrelated work can pass freshness", (t) => {
  const { root, web } = gitFixture(t);
  fs.writeFileSync(path.join(root, "README.md"), "# Unrelated synthetic change\n");
  commit(root);
  fs.writeFileSync(path.join(root, "untracked.txt"), "unrelated\n");
  assert.doesNotThrow(() => validateSourceCommit(web, root));
});

for (const stage of ["unstaged", "staged", "committed"]) {
  test(`freshness rejects ${stage} canonical changes`, (t) => {
    const { root, web } = gitFixture(t);
    write(root, "LINE.md", "# Synthetic source changed\n");
    if (stage === "staged") git(root, "add", ".");
    if (stage === "committed") commit(root);
    assert.throws(() => validateSourceCommit(web, root), /web projection is stale/);
  });
}

test("freshness rejects new untracked and ignored canonical files", (t) => {
  const { root, web } = gitFixture(t);
  write(root, "NEW.md", "# Synthetic addition\n");
  assert.throws(() => validateSourceCommit(web, root), /NEW.md/);
  fs.writeFileSync(path.join(root, ".gitignore"), `${canonicalRoot}/NEW.md\n`);
  assert.throws(() => validateSourceCommit(web, root), /NEW.md/);
});

test("freshness rejects deleted canonical files", (t) => {
  const { root, web } = gitFixture(t);
  fs.rmSync(path.join(root, canonicalRoot, "LINE.md"));
  assert.throws(() => validateSourceCommit(web, root), /web projection is stale/);
});

test("an unmerged source commit cannot certify its own branch", (t) => {
  const { root } = gitFixture(t);
  write(root, "LINE.md", "# Synthetic unmerged source\n");
  const sha = commit(root);
  assert.throws(() => validateSourceCommit({ meta: { canonicalSourceCommit: sha } }, root), /not in origin\/main history/);
});

test("missing main history fails instead of weakening source identity", (t) => {
  const { root, web } = gitFixture(t);
  git(root, "update-ref", "-d", "refs/remotes/origin/main");
  assert.throws(() => validateSourceCommit(web, root), /origin\/main is missing/);
});

test("freshness rejects unknown commits, revisions and non-ancestor commits", (t) => {
  const { root } = gitFixture(t);
  for (const source of ["HEAD", "0".repeat(40), "--help"]) {
    assert.throws(() => validateSourceCommit({ meta: { canonicalSourceCommit: source } }, root), /commit SHA|missing or is not an ancestor/);
  }
  git(root, "switch", "--orphan", "other-history");
  fs.writeFileSync(path.join(root, "other.txt"), "Synthetic unrelated history\n");
  const sha = commit(root);
  git(root, "switch", "main");
  assert.throws(() => validateSourceCommit({ meta: { canonicalSourceCommit: sha } }, root), /not an ancestor/);
});

test("Pages uploads only after validation and deployment depends on that job", () => {
  const workflow = yaml.load(fs.readFileSync(path.join(repositoryRoot, ".github/workflows/pages.yml"), "utf8"));
  assert.equal(workflow.permissions["pages"], undefined);
  assert.equal(workflow.permissions["id-token"], undefined);
  const gate = workflow.jobs.validate;
  assert.equal(gate.if, "github.ref == 'refs/heads/main'");
  const validation = gate.steps.findIndex((step) => step.run === "npm run check");
  const upload = gate.steps.findIndex((step) => step.uses?.startsWith("actions/upload-pages-artifact@"));
  assert.ok(validation >= 0 && upload > validation, "validation must precede artifact upload");
  assert.equal(gate.steps[validation]["continue-on-error"], undefined);
  assert.equal(gate.steps[upload].if, undefined);
  assert.equal(gate.steps.find((step) => step.uses?.startsWith("actions/checkout@"))?.with?.["fetch-depth"], 0);
  assert.equal(workflow.jobs.deploy.needs, "validate");
  assert.equal(workflow.jobs.deploy.if, undefined);
  assert.ok(!workflow.jobs.deploy.steps.some((step) => step.uses?.startsWith("actions/checkout@")), "deployment must consume the validated artifact");
  for (const target of ["research/lines/horizontal-reaction-v0.1/**", "package-lock.json", ".github/scripts/test-research-consistency.mjs"]) {
    assert.ok(workflow.on.push.paths.includes(target), `Pages trigger must include ${target}`);
  }
});
