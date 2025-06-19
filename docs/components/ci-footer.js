// docs/components/ci-footer.js

class CiFooter extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    const siteURL = "https://civic-interconnect.github.io/agents-maintenance-dashboard/";
    const sourceURL = "https://github.com/civic-interconnect/agents-maintenance-dashboard";

    this.setAttribute("siteURL", siteURL);
    this.setAttribute("sourceURL", sourceURL);

    const dashboardVersion = this.getAttribute("dashboardVersion") || "v0.0.0";
    const lastUpdated =
      this.getAttribute("lastUpdated") || new Date().toLocaleDateString();

    this.innerHTML = `
      <footer class="ci-footer">
        <p style="margin: 0;">
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
