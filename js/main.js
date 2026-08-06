const pageLang = (document.documentElement.lang || "en").toLowerCase();
const isSpanish = pageLang.startsWith("es");

const uiText = isSpanish
  ? {
      open: "Abrir",
      download: "Descargar",
      autoDiscoveredVideo: "Archivo de video (detectado automaticamente)",
      requestCaptured: "Solicitud registrada",
      videoFallback: "Video"
    }
  : {
      open: "Open",
      download: "Download",
      autoDiscoveredVideo: "Video file (auto-discovered)",
      requestCaptured: "Request Captured",
      videoFallback: "Video"
    };

const branchDocuments = isSpanish
  ? {
      engineering: {
        title: "Ingenieria y Diseno",
        description: "Paquetes tecnicos, entregables 2D/3D y recursos de planificacion productiva.",
        documents: [
          { name: "Manual de Estandares de Diseno", type: "PDF", detail: "Version 1.0 · Borrador" },
          { name: "Paquete de Planos de Fabricacion", type: "PDF", detail: "Paquete A · Borrador" },
          { name: "Matriz de Coste BOM", type: "XLSX", detail: "Workbook de planificacion Q2" },
          { name: "Checklist de Site Survey", type: "PDF", detail: "Guia de ingenieria de campo" },
          { name: "Matriz de Seleccion de Materiales", type: "XLSX", detail: "Biblioteca de componentes industriales" },
          { name: "Registro de Control de Revisiones", type: "PDF", detail: "Plantilla de gobernanza documental" }
        ]
      },
      automation: {
        title: "Automatizacion y Control",
        description: "Arquitectura de control, mapeo de senales, commissioning y registros de automatizacion.",
        documents: [
          { name: "Guia de Commissioning PLC", type: "PDF", detail: "Flujo de arranque de automatizacion" },
          { name: "Workbook de Mapeo IO", type: "XLSX", detail: "Registro de senales y tags" },
          { name: "Arbol de Alarmas de Mantenimiento", type: "PDF", detail: "Referencia de escalado de control" },
          { name: "Matriz de Tareas Preventivas", type: "XLSX", detail: "Calendario recurrente de servicio" },
          { name: "Checklist de Handover SCADA", type: "PDF", detail: "Paquete de preparacion operativa" }
        ]
      },
      operations: {
        title: "Inteligencia Operacional",
        description: "Cuadros de mando, reporting y visibilidad de servicio por unidad operativa.",
        documents: [
          { name: "Dashboard KPI de Produccion", type: "XLSX", detail: "Plantilla de reporting semanal" },
          { name: "Executive Operations Brief", type: "PDF", detail: "Formato resumen para direccion" },
          { name: "Tracker de Utilizacion de Unidad", type: "XLSX", detail: "Modelo de capacidad de servicio" },
          { name: "Registro de Riesgo Industrial", type: "PDF", detail: "Ficha de mitigacion operativa" }
        ]
      },
      academy: {
        title: "Documentacion y Formacion",
        description: "Acceso centralizado a activos de video y documentos tecnicos clave.",
        documents: [
          {
            name: "ING_DOCLOUD Video Library",
            type: "HTML",
            detail: "Landing con todos los videos disponibles",
            viewHref: "public/videos/index.html"
          },
          {
            name: "FOLDER GLUER - EASY PACK (ES)",
            type: "MP4",
            detail: "Archivo de video directo",
            viewHref: "public/videos/folder-gluer-easy-pack-espanol-720p-hd.mp4"
          },
          {
            name: "INGECART SUPERCORR 2024",
            type: "MP4",
            detail: "Archivo de video directo",
            viewHref: "public/videos/ingecart-supercorr-2024-720p-hd.mp4"
          },
          {
            name: "Ingetrans 280 - Automated Reel Transport System",
            type: "MP4",
            detail: "Archivo de video directo",
            viewHref: "public/videos/ingetrans-280-automated-reel-transport-system-720p-hd.mp4"
          },
          {
            name: "IP AMR INGECART (Digital Twin Trials)",
            type: "MP4",
            detail: "Archivo de video directo (editado)",
            viewHref: "public/videos/ip-amr-project-digital-twin-trials-2-2026-06-12-165030-editado.mp4",
            downloadHref: "public/videos/ip-amr-project-digital-twin-trials-2-2026-06-12-165030-editado.mp4",
            downloadName: "ip-amr-project-digital-twin-trials-2-2026-06-12-165030-editado.mp4"
          },
          {
            name: "PALETIZADOR FFG - Robot paletizador",
            type: "MP4",
            detail: "Archivo de video directo",
            viewHref: "public/videos/paletizador-ffg-robot-paletizador-el-mas-rapido-720p-hd.mp4"
          },
          {
            name: "SR1400 - Solucion para recoger y transportar",
            type: "MP4",
            detail: "Archivo de video directo",
            viewHref: "public/videos/sr1400-la-solucion-para-recoger-y-transportar-to-720p-hd.mp4"
          },
          {
            name: "Product Brochure May 2026",
            type: "PDF",
            detail: "Documento PDF solicitado",
            viewHref: "public/docs/product-brochure-may-2026.pdf",
            downloadHref: "public/docs/product-brochure-may-2026.pdf",
            downloadName: "product-brochure-may-2026.pdf"
          },
          {
            name: "ESTUDIO FERIAS CORRUGADO INGECART DEEP 2026-2028",
            type: "HTML",
            detail: "Documento estrategico solicitado",
            viewHref: "public/docs/estudio-ferias-corrugado-ingecart-deep-2026-2028.html"
          }
        ]
      }
    }
  : {
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
        viewLink.textContent = uiText.open;
        actions.append(viewLink);
      }

      if (entry.downloadHref) {
        const downloadLink = document.createElement("a");
        downloadLink.href = encodeURI(entry.downloadHref);
        if (entry.downloadName) {
          downloadLink.setAttribute("download", entry.downloadName);
        }
        downloadLink.textContent = uiText.download;
        actions.append(downloadLink);
      }

      right.append(type, actions);
    } else {
      right.append(type);
    }

    item.append(meta, right);
    documentList.append(item);
    const candidate = (entry.viewHref || entry.downloadHref || "").split("/").pop();
    if (candidate) {
      existingFiles.add(decodeURIComponent(candidate));
    }
  });

  if (branchKey === "academy") {
    fetch("public/videos/index.html")
      .then((resp) => {
        if (!resp.ok) throw new Error("Failed to fetch video index");
        return resp.text();
      })
      .then((htmlText) => {
        try {
          const parser = new DOMParser();
          const doc = parser.parseFromString(htmlText, "text/html");
          const sources = Array.from(doc.querySelectorAll("video source[src]"));
          const anchors = Array.from(doc.querySelectorAll('a[href$=".mp4"]'));
          const found = new Set();

          sources.forEach((source) => {
            const src = source.getAttribute("src");
            if (src) found.add(src);
          });
          anchors.forEach((anchor) => {
            const href = anchor.getAttribute("href");
            if (href && href.toLowerCase().endsWith(".mp4")) found.add(href);
          });

          found.forEach((file) => {
            const base = file.split("/").pop();
            if (!base || existingFiles.has(decodeURIComponent(base))) return;

            const item = document.createElement("li");
            const meta = document.createElement("div");
            const name = document.createElement("span");
            const detail = document.createElement("span");
            const right = document.createElement("div");
            const type = document.createElement("span");

            meta.className = "document-meta";
            right.className = "document-right";
            name.textContent = base;
            detail.textContent = uiText.autoDiscoveredVideo;
            type.className = "document-type";
            type.textContent = "MP4";

            meta.append(name, detail);

            const actions = document.createElement("div");
            actions.className = "document-actions";
            const viewLink = document.createElement("a");
            let href = file;
            if (!href.startsWith("/") && !href.startsWith("http")) href = "public/videos/" + href;
            viewLink.href = encodeURI(href);
            viewLink.target = "_blank";
            viewLink.rel = "noreferrer";
            viewLink.textContent = uiText.open;
            actions.append(viewLink);

            right.append(type, actions);
            item.append(meta, right);
            documentList.append(item);
            existingFiles.add(decodeURIComponent(base));
          });
        } catch (error) {
          console.error("Error parsing videos index:", error);
        }
      })
      .catch((error) => {
        console.error("Could not load video index:", error);
      });
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

  submitButton.textContent = uiText.requestCaptured;
  submitButton.disabled = true;
});

function populateLandingVideos() {
  const container = document.getElementById("training-videos");
  if (!container) return;

  fetch("public/videos/index.html")
    .then((response) => {
      if (!response.ok) throw new Error("no index");
      return response.text();
    })
    .then((html) => {
      try {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");
        const cards = Array.from(doc.querySelectorAll(".card"));
        cards.slice(0, 4).forEach((card) => {
          const src = card.querySelector("video source")?.getAttribute("src");
          const title = card.querySelector(".card-title")?.textContent || card.querySelector("h2")?.textContent || uiText.videoFallback;
          const link = card.querySelector("a[download]")?.getAttribute("href") || src;
          const thumb = card.querySelector("img")?.getAttribute("src") || "";

          const item = document.createElement("a");
          item.href = link || ("/public/videos/" + (src || ""));
          item.className = "mini-video-card";
          item.style.cssText = "display:block;background:#0f1720;padding:6px;border-radius:8px;text-decoration:none;color:inherit;border:1px solid rgba(255,255,255,0.04);";

          const preview = document.createElement("div");
          preview.style.cssText = "width:100%;height:90px;background:#000;border-radius:6px;display:flex;align-items:center;justify-content:center;overflow:hidden;";
          if (thumb) {
            const img = document.createElement("img");
            img.src = thumb;
            img.style.width = "100%";
            img.style.height = "100%";
            img.style.objectFit = "cover";
            preview.appendChild(img);
          } else if (src) {
            const vid = document.createElement("video");
            vid.src = src;
            vid.preload = "metadata";
            vid.muted = true;
            vid.style.width = "100%";
            vid.style.height = "100%";
            vid.style.objectFit = "cover";
            preview.appendChild(vid);
          } else {
            preview.textContent = uiText.videoFallback;
          }

          const text = document.createElement("div");
          text.style.cssText = "font-size:0.85rem;margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;";
          text.textContent = title;
          item.appendChild(preview);
          item.appendChild(text);
          container.appendChild(item);
        });
      } catch (error) {
        console.error(error);
      }
    })
    .catch(() => {});
}

document.addEventListener("DOMContentLoaded", populateLandingVideos);
