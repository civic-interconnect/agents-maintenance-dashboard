// File: components/ci-agent/ci-agent.js
const styleURL = new URL("./ci-agent.css", import.meta.url);
const coreFields = ["version", "schema_source", "action_status"];

class CiAgent extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._agentData = null; // Hold agent data if set early
  }

  async connectedCallback() {
    const style = await fetch(styleURL).then((res) => res.text());

    this.shadowRoot.innerHTML = `
      <style>${style}</style>
      <article class="agent-card"></article>
    `;

    this.container = this.shadowRoot.querySelector(".agent-card");

    // Now render if data was set before connectedCallback finished
    if (this._agentData) {
      this.render(this._agentData);
    }

    const updateTheme = () => {
      const theme = document.body.dataset.theme || "light";
      this.setAttribute("data-theme", theme);
    };
    const observer = new MutationObserver(updateTheme);
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
    updateTheme();
    this._themeObserver = observer;
  }

  set data(agent) {
    if (this.container) {
      this.render(agent);
    } else {
      this._agentData = agent; // Save until connectedCallback runs
    }
  }

  render(agent) {
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
      .filter(
        ([key]) =>
          !["name", "repo", "last_commit", ...coreFields, "report_url"].includes(key)
      )
      .map(
        ([key, value]) =>
          `<p><strong>${formatLabel(key)}:</strong> ${value}</p>`
      )
      .join("\n");

    this.container.innerHTML = `
      <header>
        <h2><a href="${safeField("repo")}" target="_blank" rel="noopener">
          ${safeField("name")}</a></h2>
        <small>Last commit: ${safeField("last_commit")}</small>
      </header>
      <section>
        <p><strong>Version:</strong> ${safeField("version")}</p>
        <p><strong>Schema Source:</strong> ${safeField("schema_source")}</p>
        <p><strong>Status:</strong> <span class="${statusClass}">${safeField("action_status")}</span></p>
        ${extraFields}
      </section>
    `;
  }
}

function formatLabel(key) {
  return key.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

customElements.define("ci-agent", CiAgent);
