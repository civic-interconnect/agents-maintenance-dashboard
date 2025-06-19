//components/ci-agent.js

class CiAgent extends HTMLElement {
  set data(agent) {
    const status = agent.action_status.toLowerCase();

    const statusClass =
      status.includes("success") || status.includes("passed")
        ? "status-ok"
        : status.includes("pending")
        ? "status-warn"
        : "status-bad";

    this.innerHTML = `
      <article class="agent-card">
        <header>
          <h2><a href="${agent.repo}" target="_blank" rel="noopener">${agent.name}</a></h2>
          <small>Last commit: ${agent.last_commit}</small>
        </header>
        <section>
          <p><strong>Version:</strong> ${agent.version}</p>
          <p><strong>Schema Source:</strong> ${agent.schema_source}</p>
          <p><strong>Status:</strong> <span class="${statusClass}">${agent.action_status}</span></p>
        </section>
      </article>
    `;
  }
}

customElements.define("ci-agent", CiAgent);
