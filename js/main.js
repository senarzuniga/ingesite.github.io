const branchDocuments = {
  engineering: {
    title: "Engineering & Design",
    description: "Technical packages, 2D/3D deliverables, and production planning resources.",
    documents: [
      { name: "Design Standards Manual", type: "PDF", detail: "Version 1.0 · Draft placeholder" },
      { name: "Fabrication Drawing Set", type: "PDF", detail: "Package A · Draft placeholder" },
      { name: "BOM Cost Matrix", type: "XLSX", detail: "Q2 planning workbook" },
      { name: "Site Survey Checklist", type: "PDF", detail: "Field engineering guide" },
      { name: "Material Selection Matrix", type: "XLSX", detail: "Industrial components library" },
      { name: "Revision Control Log", type: "PDF", detail: "Documentation governance template" }
    ]
  },
  automation: {
    title: "Automation & Control",
    description: "Control architecture, signal mapping, commissioning, and automation records.",
    documents: [
      { name: "PLC Commissioning Guide", type: "PDF", detail: "Automation startup workflow" },
      { name: "IO Mapping Workbook", type: "XLSX", detail: "Signals and tag registry" },
      { name: "Maintenance Alarm Tree", type: "PDF", detail: "Control escalation reference" },
      { name: "Preventive Tasks Matrix", type: "XLSX", detail: "Recurring service schedule" },
      { name: "SCADA Handover Checklist", type: "PDF", detail: "Operator readiness pack" }
    ]
  },
  operations: {
    title: "Operations Intelligence",
    description: "Operational scorecards, reporting, and branch-level service visibility.",
    documents: [
      { name: "Production KPI Dashboard", type: "XLSX", detail: "Weekly reporting template" },
      { name: "Executive Operations Brief", type: "PDF", detail: "Holding-level summary layout" },
      { name: "Branch Utilization Tracker", type: "XLSX", detail: "Service capacity model" },
      { name: "Industrial Risk Register", type: "PDF", detail: "Operational mitigation sheet" }
    ]
  },
  academy: {
    title: "Documentation & Training",
    description: "Knowledge libraries, onboarding kits, and procedures for rapid replication.",
    documents: [
      { name: "Branch Induction Booklet", type: "PDF", detail: "New team onboarding" },
      { name: "Operational SOP Library", type: "PDF", detail: "Core process handbook" },
      { name: "Training Attendance Tracker", type: "XLSX", detail: "Instruction records" },
      { name: "Field Audit Checklist", type: "PDF", detail: "Site quality verification" },
      { name: "Client Handover Pack", type: "PDF", detail: "Delivery completion template" },
      { name: "Documentation Index", type: "XLSX", detail: "Cross-branch reference sheet" },
      { name: "Trainer Planning Calendar", type: "XLSX", detail: "Session scheduling workbook" }
    ]
  }
};

const modal = document.getElementById("documents-modal");
const modalTitle = document.getElementById("documents-title");
const modalDescription = document.getElementById("documents-description");
const documentList = document.getElementById("document-list");
const triggerButtons = document.querySelectorAll("[data-open-documents]");
const closeButtons = document.querySelectorAll("[data-close-modal]");
const contactForm = document.querySelector(".contact-form");

function renderDocuments(branchKey) {
  const branch = branchDocuments[branchKey];

  if (!branch) {
    return;
  }

  modalTitle.textContent = branch.title;
  modalDescription.textContent = branch.description;
  documentList.innerHTML = "";

  branch.documents.forEach((document) => {
    const item = document.createElement("li");
    const meta = document.createElement("div");
    const name = document.createElement("span");
    const detail = document.createElement("span");
    const type = document.createElement("span");

    meta.className = "document-meta";
    name.textContent = document.name;
    detail.textContent = document.detail;
    type.className = "document-type";
    type.textContent = document.type;

    meta.append(name, detail);
    item.append(meta, type);
    documentList.append(item);
  });
}

function openModal(branchKey) {
  renderDocuments(branchKey);
  modal.classList.add("is-open");
  modal.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeModal() {
  modal.classList.remove("is-open");
  modal.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

triggerButtons.forEach((button) => {
  button.addEventListener("click", () => {
    openModal(button.dataset.openDocuments);
  });
});

closeButtons.forEach((button) => {
  button.addEventListener("click", closeModal);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && modal.classList.contains("is-open")) {
    closeModal();
  }
});

contactForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const submitButton = contactForm.querySelector("button[type='submit']");

  submitButton.textContent = "Request Captured";
  submitButton.disabled = true;
});
