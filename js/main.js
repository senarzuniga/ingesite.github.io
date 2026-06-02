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
    description: "Centralized access to video assets and key technical documents.",
    documents: [
      {
        name: "ING_DOCLOUD Video Library",
        type: "HTML",
        detail: "Landing page with all available videos",
        viewHref: "/public/videos/index.html"
      },
      {
        name: "FOLDER GLUER - EASY PACK (ES)",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "/public/videos/FOLDER GLUER _ EASY PACK - ESPAÑOL(720P_HD).mp4"
      },
      {
        name: "INGECART SUPERCORR 2024",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "/public/videos/INGECART SUPERCORR 2024(720P_HD).mp4"
      },
      {
        name: "Ingetrans 280 - Automated Reel Transport System",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "/public/videos/Ingetrans 280_ Automated Reel Transport System(720P_HD).mp4"
      },
      {
        name: "IP AMR INGECART",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "/public/videos/IP AMR INGECART(720P_HD).mp4"
      },
      {
        name: "PALETIZADOR FFG - Robot paletizador",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "/public/videos/PALETIZADOR FFG - Robot paletizador. El más rápido(720P_HD).mp4"
      },
      {
        name: "SR1400 - Solucion para recoger y transportar",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "/public/videos/SR1400 - La solución para recoger y transportar to(720P_HD).mp4"
      },
      {
        name: "Product Brochure May 2026",
        type: "PDF",
        detail: "Requested PDF document",
        viewHref: "/public/docs/product-brochure-may-2026.pdf",
        downloadHref: "/public/docs/product-brochure-may-2026.pdf",
        downloadName: "product-brochure-may-2026.pdf"
      },
      {
        name: "ESTUDIO FERIAS CORRUGADO INGECART DEEP 2026-2028",
        type: "HTML",
        detail: "Requested strategic study document",
        viewHref: "/public/docs/ESTUDIO_FERIAS_CORRUGADO_INGECART_DEEP_2026_2028.html"
      }
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

  branch.documents.forEach((entry) => {
    const item = document.createElement("li");
    const meta = document.createElement("div");
    const name = document.createElement("span");
    const detail = document.createElement("span");
    const right = document.createElement("div");
    const type = document.createElement("span");

    meta.className = "document-meta";
    right.className = "document-right";
    name.textContent = entry.name;
    detail.textContent = entry.detail;
    type.className = "document-type";
    type.textContent = entry.type;

    meta.append(name, detail);

    if (entry.viewHref || entry.downloadHref) {
      const actions = document.createElement("div");
      actions.className = "document-actions";

      if (entry.viewHref) {
        const viewLink = document.createElement("a");
        viewLink.href = encodeURI(entry.viewHref);
        viewLink.target = "_blank";
        viewLink.rel = "noreferrer";
        viewLink.textContent = "Open";
        actions.append(viewLink);
      }

      if (entry.downloadHref) {
        const downloadLink = document.createElement("a");
        downloadLink.href = encodeURI(entry.downloadHref);
        if (entry.downloadName) {
          downloadLink.setAttribute("download", entry.downloadName);
        }
        downloadLink.textContent = "Download";
        actions.append(downloadLink);
      }

      right.append(type, actions);
    } else {
      right.append(type);
    }

    item.append(meta, right);
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
