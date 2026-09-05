const API_BASE = "";

const columnsByStatus = {
  "Open": document.getElementById("column-open"),
  "In Progress": document.getElementById("column-in-progress"),
  "Resolved": document.getElementById("column-resolved"),
};

const dashboardEls = {
  open: document.getElementById("dash-open"),
  critical: document.getElementById("dash-critical"),
  resolved: document.getElementById("dash-resolved"),
};

const errorBanner = document.getElementById("error-banner");
const severityFilter = document.getElementById("filter-severity");

let isDragging = false;

// ---------- Utilitários ----------

function showError(message) {
  errorBanner.textContent = message;
  errorBanner.hidden = false;
  setTimeout(() => {
    errorBanner.hidden = true;
  }, 5000);
}

function formatDateTime(isoString) {
  const date = new Date(isoString);
  return date.toLocaleString("pt-BR");
}

// ---------- Dashboard ----------

async function loadDashboard() {
  const response = await fetch(`${API_BASE}/dashboard`);
  if (!response.ok) return;
  const data = await response.json();
  dashboardEls.open.textContent = data.open_count;
  dashboardEls.critical.textContent = data.critical_unresolved_count;
  dashboardEls.resolved.textContent = data.resolved_count;
}

// ---------- Board / Cards ----------

function createCardElement(incident) {
  const card = document.createElement("div");
  card.className = "incident-card";
  card.draggable = true;
  card.dataset.id = incident.id;
  card.dataset.status = incident.status;

  const badge = document.createElement("span");
  badge.className = `badge badge-${incident.severity}`;
  badge.textContent = incident.severity;

  const title = document.createElement("h3");
  title.textContent = incident.title;

  const owner = document.createElement("div");
  owner.className = "owner";
  owner.textContent = `Responsável: ${incident.owner}`;

  card.appendChild(badge);
  card.appendChild(title);
  card.appendChild(owner);

  card.addEventListener("dragstart", (event) => {
    isDragging = true;
    event.dataTransfer.setData("text/plain", incident.id);
    card.classList.add("dragging");
  });

  card.addEventListener("dragend", () => {
    card.classList.remove("dragging");
    // Pequeno atraso para o listener de click não abrir o modal
    // logo depois de um drag-and-drop.
    setTimeout(() => {
      isDragging = false;
    }, 0);
  });

  card.addEventListener("click", () => {
    if (isDragging) return;
    openDetailModal(incident.id);
  });

  return card;
}

async function loadBoard() {
  const severity = severityFilter.value;
  const params = new URLSearchParams();
  if (severity) params.set("severity", severity);

  const response = await fetch(`${API_BASE}/incidents?${params.toString()}`);
  if (!response.ok) {
    showError("Não foi possível carregar os incidentes.");
    return;
  }
  const incidents = await response.json();

  Object.values(columnsByStatus).forEach((column) => {
    column.innerHTML = "";
  });

  incidents.forEach((incident) => {
    const column = columnsByStatus[incident.status];
    if (column) {
      column.appendChild(createCardElement(incident));
    }
  });
}

async function refreshAll() {
  await Promise.all([loadBoard(), loadDashboard()]);
}

// ---------- Drag and drop entre colunas ----------

Object.entries(columnsByStatus).forEach(([status, columnEl]) => {
  columnEl.addEventListener("dragover", (event) => {
    event.preventDefault();
    columnEl.classList.add("drag-over");
  });

  columnEl.addEventListener("dragleave", () => {
    columnEl.classList.remove("drag-over");
  });

  columnEl.addEventListener("drop", async (event) => {
    event.preventDefault();
    columnEl.classList.remove("drag-over");

    const incidentId = event.dataTransfer.getData("text/plain");
    if (!incidentId) return;

    try {
      const response = await fetch(
        `${API_BASE}/incidents/${incidentId}/status`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status }),
        }
      );

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        showError(
          errorBody.detail || "Não foi possível mover o incidente."
        );
      }
    } catch (err) {
      showError("Erro de conexão ao tentar mover o incidente.");
    } finally {
      // Sempre recarrega do servidor: se a transição foi rejeitada,
      // isso naturalmente "devolve" o card para a coluna correta.
      await refreshAll();
    }
  });
});

// ---------- Modal de criação ----------

const createModal = document.getElementById("create-modal");
const createForm = document.getElementById("create-form");

document.getElementById("open-create-modal").addEventListener("click", () => {
  createForm.reset();
  createModal.hidden = false;
});

document.getElementById("cancel-create").addEventListener("click", () => {
  createModal.hidden = true;
});

createForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    title: document.getElementById("create-title").value,
    description: document.getElementById("create-description").value,
    severity: document.getElementById("create-severity").value,
    owner: document.getElementById("create-owner").value,
  };

  try {
    const response = await fetch(`${API_BASE}/incidents`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      showError(errorBody.detail || "Não foi possível criar o incidente.");
      return;
    }

    createModal.hidden = true;
    await refreshAll();
  } catch (err) {
    showError("Erro de conexão ao tentar criar o incidente.");
  }
});

// ---------- Modal de detalhes ----------

const detailModal = document.getElementById("detail-modal");

async function openDetailModal(incidentId) {
  const response = await fetch(`${API_BASE}/incidents/${incidentId}`);
  if (!response.ok) {
    showError("Não foi possível carregar os detalhes do incidente.");
    return;
  }
  const incident = await response.json();

  document.getElementById("detail-title").textContent = incident.title;

  const badge = document.getElementById("detail-severity-badge");
  badge.textContent = incident.severity;
  badge.className = `badge badge-${incident.severity}`;

  document.getElementById("detail-description").textContent =
    incident.description;
  document.getElementById("detail-owner").textContent = incident.owner;
  document.getElementById("detail-status").textContent = incident.status;
  document.getElementById("detail-created").textContent = formatDateTime(
    incident.created_at
  );
  document.getElementById("detail-updated").textContent = formatDateTime(
    incident.updated_at
  );

  const historyList = document.getElementById("detail-history");
  historyList.innerHTML = "";
  if (incident.history.length === 0) {
    const li = document.createElement("li");
    li.textContent = "Nenhuma alteração de status registrada ainda.";
    historyList.appendChild(li);
  } else {
    incident.history.forEach((entry) => {
      const li = document.createElement("li");
      li.textContent = `${formatDateTime(entry.changed_at)} — ${entry.previous_status} → ${entry.new_status}`;
      historyList.appendChild(li);
    });
  }

  detailModal.hidden = false;
}

document.getElementById("close-detail").addEventListener("click", () => {
  detailModal.hidden = true;
});

// ---------- Filtros ----------

severityFilter.addEventListener("change", loadBoard);

// ---------- Inicialização ----------

refreshAll();