const styleURL = new URL('./ci-footer.css', import.meta.url);
const templateURL = new URL('./ci-footer.html', import.meta.url);

class CiFooter extends HTMLElement {
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

    const updated = this.getAttribute('lastUpdated') || new Date().toLocaleDateString();
    const version = this.getAttribute('dashboardVersion') || 'v0.0.0';
    const year = this.getAttribute('year') || new Date().getFullYear();

    const updatedEl = this.shadowRoot.querySelector('#updated-date');
    if (updatedEl) updatedEl.textContent = updated;

    const versionSlot = this.shadowRoot.querySelector('slot[name="version"]');
    if (versionSlot && !this.querySelector('[slot="version"]')) {
      versionSlot.innerHTML = `Version: ${version}`;
    }

    const yearEl = this.shadowRoot.querySelector('#year');
    if (yearEl) yearEl.textContent = year;

    const siteSlot = this.querySelector('[slot="siteURL"]');
    if (!siteSlot) {
      const siteAnchor = this.shadowRoot.querySelector('a[slot="siteURL"]');
      siteAnchor.setAttribute(
        'href',
        this.getAttribute('siteURL') ||
          'https://civic-interconnect.github.io/app-agents/'
      );
    }

    const sourceSlot = this.querySelector('[slot="sourceURL"]');
    if (!sourceSlot) {
      const sourceAnchor = this.shadowRoot.querySelector('a[slot="sourceURL"]');
      sourceAnchor.setAttribute(
        'href',
        this.getAttribute('sourceURL') ||
          'https://github.com/civic-interconnect/app-agents'
      );
    }
  }
}

customElements.define('ci-footer', CiFooter);
