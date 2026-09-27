(() => {
  const data = window.RESEARCH_UI_DATA;
  if (!data) return;

  const $ = (id) => document.getElementById(id);
  const link = (href, label = "Canonical ↗") =>
    `<a class="text-link" href="${href}" target="_blank" rel="noreferrer">${label}</a>`;

  $("line-id").textContent = data.line.id;
  $("line-title").textContent = data.line.title;
  $("line-scope").textContent = data.line.scope;
  $("canonical-link").href = data.line.current;
  $("all-files-link").href = data.canonicalBase;
  $("generated-at").textContent = data.meta.projectionGeneratedAt;
  $("source-commit").textContent = data.meta.canonicalSourceCommit.slice(0, 12);
  $("source-commit").href = `https://github.com/Josh-Temple/systematic-trading-research/commit/${data.meta.canonicalSourceCommit}`;

  $("current-status").innerHTML = data.hypotheses.map((h) => `
    <div class="current-row">
      <strong>${h.label}</strong>
      <span class="state">${h.title}</span>
      <span class="status-tag tone-${h.tone}">${h.status}</span>
    </div>
  `).join("");

  const conflict = data.current.conflict;
  $("conflict").innerHTML = conflict.active ? `
    <p class="eyebrow label">${conflict.label}</p>
    <h3>${conflict.title}</h3>
    <p>${conflict.body}</p>
    ${link(conflict.canonical, "Conflict record ↗")}
  ` : "";

  $("next-title").textContent = data.current.nextTest.title;
  $("next-body").textContent = data.current.nextTest.body;
  $("next-status").textContent = data.current.nextTest.status;
  $("forbidden-list").innerHTML = data.current.forbidden.map((x) => `<li>${x}</li>`).join("");

  $("hypotheses").innerHTML = data.hypotheses.map((h) => `
    <article class="evidence-item">
      <div>
        <p class="evidence-kicker">${h.label}</p>
        <p>${h.id}</p>
      </div>
      <div class="evidence-main">
        <span class="status-tag tone-${h.tone}">${h.status}</span>
        <h3>${h.title}</h3>
        <p>${h.summary}</p>
        <dl class="metrics">
          ${h.metrics.map(([k,v]) => `<div class="metric"><dt>${k}</dt><dd>${v}</dd></div>`).join("")}
        </dl>
        <p class="footnote">${h.note}</p>
        ${link(h.canonical)}
      </div>
    </article>
  `).join("");

  $("diag-label").textContent = data.diagnostics.currentLabel;
  $("diag-summary").textContent = data.diagnostics.currentSummary;
  $("diag-points").innerHTML = data.diagnostics.points.map(([k,v,n]) => `
    <div class="diag-row">
      <span>${k}</span>
      <strong>${v}</strong>
      <span>${n}</span>
    </div>
  `).join("");
  $("diag-links").innerHTML = data.diagnostics.links
    .map(([label, href]) => link(href, `${label} ↗`))
    .join(" · ");

  $("datasets").innerHTML = data.datasets.map((d) => `
    <article class="data-row">
      <div>
        <p class="eyebrow">${d.id}</p>
        <p class="data-role ${d.tone}">${d.role}</p>
      </div>
      <div>
        <h3>${d.title}</h3>
        <p>${d.window}</p>
        <p class="footnote">${d.use}</p>
      </div>
      <div>${link(d.canonical)}</div>
    </article>
  `).join("");

  $("timeline-list").innerHTML = data.timeline.map((item) => `
    <li>
      <time>${item.date}</time>
      <span class="kind">${item.kind}</span>
      <span>
        ${item.title}
        <span class="ref">${item.refs.map(([label, href]) => link(href, `${label} ↗`)).join(" · ")}</span>
      </span>
    </li>
  `).join("");
})();