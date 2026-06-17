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
        viewHref: "public/videos/index.html"
      },
      {
        name: "FOLDER GLUER - EASY PACK (ES)",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "public/videos/folder-gluer-easy-pack-espanol-720p-hd.mp4"
      },
      {
        name: "INGECART SUPERCORR 2024",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "public/videos/ingecart-supercorr-2024-720p-hd.mp4"
      },
      {
        name: "Ingetrans 280 - Automated Reel Transport System",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "public/videos/ingetrans-280-automated-reel-transport-system-720p-hd.mp4"
      },
      {
        name: "IP AMR INGECART (Digital Twin Trials)",
        type: "MP4",
        detail: "Direct video file (edited)",
        viewHref: "public/videos/ip-amr-project-digital-twin-trials-2-2026-06-12-165030-editado.mp4",
        downloadHref: "public/videos/ip-amr-project-digital-twin-trials-2-2026-06-12-165030-editado.mp4",
        downloadName: "ip-amr-project-digital-twin-trials-2-2026-06-12-165030-editado.mp4"
      },
      {
        name: "PALETIZADOR FFG - Robot paletizador",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "public/videos/paletizador-ffg-robot-paletizador-el-mas-rapido-720p-hd.mp4"
      },
      {
        name: "SR1400 - Solucion para recoger y transportar",
        type: "MP4",
        detail: "Direct video file",
        viewHref: "public/videos/sr1400-la-solucion-para-recoger-y-transportar-to-720p-hd.mp4"
      },
      {
        name: "Product Brochure May 2026",
        type: "PDF",
        detail: "Requested PDF document",
        viewHref: "public/docs/product-brochure-may-2026.pdf",
        downloadHref: "public/docs/product-brochure-may-2026.pdf",
        downloadName: "product-brochure-may-2026.pdf"
      },
      {
        name: "ESTUDIO FERIAS CORRUGADO INGECART DEEP 2026-2028",
        type: "HTML",
        detail: "Requested strategic study document",
        viewHref: "public/docs/estudio-ferias-corrugado-ingecart-deep-2026-2028.html"
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
  const existingFiles = new Set();

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
    // remember file basenames already listed to avoid duplicates when auto-loading
    const candidate = (entry.viewHref || entry.downloadHref || "").split('/').pop();
    if (candidate) existingFiles.add(decodeURIComponent(candidate));
  });

  // If opening the academy branch, try to fetch the videos index and append any files
  if (branchKey === 'academy') {
    fetch('public/videos/index.html').then((resp) => {
      if (!resp.ok) throw new Error('Failed to fetch video index');
      return resp.text();
    }).then((htmlText) => {
      try {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlText, 'text/html');
        const sources = Array.from(doc.querySelectorAll('video source[src]'));
        const anchors = Array.from(doc.querySelectorAll('a[href$=".mp4"]'));
        const found = new Set();

        sources.forEach(s => { const src = s.getAttribute('src'); if (src) found.add(src); });
        anchors.forEach(a => { const href = a.getAttribute('href'); if (href && href.toLowerCase().endsWith('.mp4')) found.add(href); });

        found.forEach((file) => {
          const base = file.split('/').pop();
          if (!base || existingFiles.has(decodeURIComponent(base))) return;

          const item = document.createElement('li');
          const meta = document.createElement('div');
          const name = document.createElement('span');
          const detail = document.createElement('span');
          const right = document.createElement('div');
          const type = document.createElement('span');

          meta.className = 'document-meta';
          right.className = 'document-right';
          name.textContent = base;
          detail.textContent = 'Video file (auto-discovered)';
          type.className = 'document-type';
          type.textContent = 'MP4';

          meta.append(name, detail);

          const actions = document.createElement('div');
          actions.className = 'document-actions';
          const viewLink = document.createElement('a');
          let href = file;
          if (!href.startsWith('/') && !href.startsWith('http')) href = 'public/videos/' + href;
          viewLink.href = encodeURI(href);
          viewLink.target = '_blank';
          viewLink.rel = 'noreferrer';
          viewLink.textContent = 'Open';
          actions.append(viewLink);

          right.append(type, actions);
          item.append(meta, right);
          documentList.append(item);
          existingFiles.add(decodeURIComponent(base));
        });
      } catch (e) { console.error('Error parsing videos index:', e); }
    }).catch(err => { console.error('Could not load video index:', err); });
  }
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

// Populate a small preview grid on the landing page with latest videos from public/videos
function populateLandingVideos() {
  const container = document.getElementById('training-videos');
  if (!container) return;

  fetch('public/videos/index.html').then(r => { if (!r.ok) throw new Error('no index'); return r.text(); })
    .then(html => {
      try {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const cards = Array.from(doc.querySelectorAll('.card'));
        // take first 4 cards for preview
        cards.slice(0,4).forEach(card => {
          const src = card.querySelector('video source')?.getAttribute('src');
          const title = card.querySelector('.card-title')?.textContent || card.querySelector('h2')?.textContent || 'Video';
          const link = card.querySelector('a[download]')?.getAttribute('href') || src;
          const thumb = card.querySelector('img')?.getAttribute('src') || '';

          const item = document.createElement('a');
          item.href = link || ('/public/videos/' + (src || ''));
          item.className = 'mini-video-card';
          item.style.cssText = 'display:block;background:#0f1720;padding:6px;border-radius:8px;text-decoration:none;color:inherit;border:1px solid rgba(255,255,255,0.04);';

          const preview = document.createElement('div');
          preview.style.cssText = 'width:100%;height:90px;background:#000;border-radius:6px;display:flex;align-items:center;justify-content:center;overflow:hidden;';
          if (thumb) {
            const img = document.createElement('img'); img.src = thumb; img.style.width = '100%'; img.style.height = '100%'; img.style.objectFit = 'cover'; preview.appendChild(img);
          } else if (src) {
            const vid = document.createElement('video'); vid.src = src; vid.preload = 'metadata'; vid.muted = true; vid.style.width = '100%'; vid.style.height = '100%'; vid.style.objectFit = 'cover'; preview.appendChild(vid);
          } else {
            preview.textContent = 'Video';
          }

          const t = document.createElement('div'); t.style.cssText = 'font-size:0.85rem;margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;';
          t.textContent = title;
          item.appendChild(preview);
          item.appendChild(t);
          container.appendChild(item);
        });
      } catch (e) { console.error(e); }
    }).catch(() => { /* silent */ });
}

// Run on load
document.addEventListener('DOMContentLoaded', populateLandingVideos);
