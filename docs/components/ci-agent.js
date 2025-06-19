const coreFields = ["version", "schema_source", "action_status"];

class CiAgent extends HTMLElement {
  set data(agent) {
    const status = (agent.action_status || "").toLowerCase();
    const statusClass =
      status.includes("success") || status.includes("passed")
        ? "status-ok"
        : status.includes("pending")
        ? "status-warn"
        : "status-bad";

    const safeField = (field) =>
      agent[field] !== undefined ? agent[field] : "—";

    const extraFields = Object.entries(agent)
      .filter(([key]) => !["name", "repo", "last_commit", ...coreFields].includes(key))
      .map(
        ([key, value]) =>
          `<p><strong>${formatLabel(key)}:</strong> ${value}</p>`
      )
      .join("\n");

    this.innerHTML = `
      <article class="agent-card">
        <header>
          <h2><a href="${safeField("repo")}" target="_blank" rel="noopener">${safeField("name")}</a></h2>
          <small>Last commit: ${safeField("last_commit")}</small>
        </header>
        <section>
          <p><strong>Version:</strong> ${safeField("version")}</p>
          <p><strong>Schema Source:</strong> ${safeField("schema_source")}</p>
          <p><strong>Status:</strong> <span class="${statusClass}">${safeField("action_status")}</span></p>
          ${extraFields}
        </section>
      </article>
    `;
  }
}

// Helper to convert keys like `openstates_jurisdiction` → `Openstates Jurisdiction`
function formatLabel(key) {
  return key.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

customElements.define("ci-agent", CiAgent);
