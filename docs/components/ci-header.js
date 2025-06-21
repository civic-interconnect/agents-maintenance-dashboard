// components/ci-header.js

const styleURL = new URL('./styles/ci-header.css', import.meta.url);


class CiHeader extends HTMLElement {
    constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });

    // Attach external CSS
    const link = document.createElement('link');
    link.setAttribute('rel', 'stylesheet');
    link.setAttribute('href', styleURL);
    shadow.appendChild(link);

    // Container for content
    this.container = document.createElement('div');
    shadow.appendChild(this.container);
  }

connectedCallback() {
  this.container.innerHTML = `
    <header class="ci-header">
      <h1>Civic Interconnect Dashboard</h1>
      <h1>Agent Status and Mapping Overview</h1>
    </header>
  `;
}

}

customElements.define("ci-header", CiHeader);
