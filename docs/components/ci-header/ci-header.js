// components/ci-header/ci-header.js

const styleURL = new URL('./ci-header.css', import.meta.url);
const templateURL = new URL('./ci-header.html', import.meta.url);

class CiHeader extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  async connectedCallback() {
    const [style, html] = await Promise.all([
      fetch(styleURL).then(res => res.text()),
      fetch(templateURL).then(res => res.text())
    ]);

    this.shadowRoot.innerHTML = `
      <style>${style}</style>
      ${html}
    `;
  }
}

customElements.define('ci-header', CiHeader);
