import "./components/ci-agent.js";
import "./components/ci-footer.js";
import "./components/ci-header.js";

fetch("status.json")
  .then((res) => res.json())
  .then((data) => {
    const footer = document.querySelector("ci-footer");
    if (footer) {
      footer.setAttribute("dashboardVersion", data.dashboard_version);
      footer.setAttribute("lastUpdated", data.generated);
      footer.update();
    }

    const container = document.getElementById("agents-list");
    if (Array.isArray(data.agents)) {
      data.agents.forEach((agent) => {
        const card = document.createElement("ci-agent");
        card.data = agent;
        container.appendChild(card);
      });
    } else {
      console.warn("No agents found in status.json.");
    }
  })
  .catch((error) => console.error("Failed to load status.json:", error));
