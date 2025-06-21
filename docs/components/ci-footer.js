const styleURL = new URL("./styles/ci-footer.css", import.meta.url);

class CiFooter extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: "open" });

    const link = document.createElement("link");
    link.setAttribute("rel", "stylesheet");
    link.setAttribute("href", styleURL);
    shadow.appendChild(link);

    this.container = document.createElement("div");
    shadow.appendChild(this.container);
  }

  connectedCallback() {
    this.render();
  }

  render() {
    const siteURL =
      "https://civic-interconnect.github.io/agents-maintenance-dashboard/";
    const sourceURL =
      "https://github.com/civic-interconnect/agents-maintenance-dashboard";

    const dashboardVersion = this.getAttribute("dashboardVersion") || "v0.0.0";
    const lastUpdated =
      this.getAttribute("lastUpdated") || new Date().toLocaleDateString();

    this.container.innerHTML = `
      <footer class="ci-footer">
        <p>
          <strong>Civic Interconnect: </strong>
          <a href="${siteURL}" target="_blank" rel="noopener">Site</a> |
          <a href="${sourceURL}" target="_blank" rel="noopener">Source</a>
        </p>
        <p>Version: ${dashboardVersion} • Updated: ${lastUpdated}</p>
        <p>&copy; 2025 Civic Interconnect</p>
      </footer>
    `;
  }

  update() {
    this.render();
  }
}

customElements.define("ci-footer", CiFooter);
