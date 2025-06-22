import "./components/ci-agent/ci-agent.js";
import "./components/ci-footer/ci-footer.js";
import "./components/ci-header/ci-header.js";

fetch("status.json")
  .then((res) => res.json())
  .then((data) => {
    // Update footer slots (optional fallback support)
    const footer = document.querySelector("ci-footer");
    if (footer) {
      footer
        .querySelector('[slot="version"]')
        ?.replaceWith(
          createSlotSpan("version", `Version: ${data.dashboard_version || "—"}`)
        );
      footer
        .querySelector('[slot="updated"]')
        ?.replaceWith(
          createSlotSpan("updated", `Updated: ${data.generated || "—"}`)
        );
    }

    const container = document.getElementById("agents-list");
    container.innerHTML = ""; // Remove loading message

    data.agents.forEach((agent) => {
      const card = document.createElement("ci-agent");
      card.data = agent;
      container.appendChild(card);
    });
  })
  .catch((error) => console.error("Failed to load status.json:", error));

function createSlotSpan(name, value = "—") {
  const span = document.createElement("span");
  span.setAttribute("slot", name);
  span.textContent = value;
  return span;
}
