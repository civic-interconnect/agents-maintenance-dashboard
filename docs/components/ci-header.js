// components/ci-header.js

class CiHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
  <header style="background: var(--color-blue); color: white; padding: 1rem; text-align: center;">
    <h1>Civic Interconnect Dashboard</h1>
    <h1>Agent Status and Mapping Overview</h1>
          <button class="theme-toggle" onclick="document.body.dataset.theme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';">
      🔆
    </button>
  </header>
`;
  }
}

customElements.define("ci-header", CiHeader);
