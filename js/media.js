// Media Hub frontend logic
(function(){
  const TAB_SELECTOR = '.media-tab';
  const VIDEO_JSON_PATHS = [
    '/public/videos/videos.json',
    '/videos/videos.json',
    '/public/videos/videos.json'
  ];

  function $(s, el=document) { return el.querySelector(s); }
  function $all(s, el=document) { return Array.from(el.querySelectorAll(s)); }

  function setActiveTab(name) {
    $all(TAB_SELECTOR).forEach(b => b.classList.toggle('active', b.dataset.tab === name));
    $all('.media-panel').forEach(p => p.style.display = p.id === 'tab-'+name ? '' : 'none');
    if (name === 'videos') loadVideos();
    if (name === 'docs') loadDocs();
    if (name === 'images') loadImages();
    if (name === 'news') loadNews();
  }

  function fetchJsonAny(paths) {
    return paths.reduce((acc, p) => acc.catch(() => fetch(p).then(r => r.ok ? r.json() : Promise.reject(new Error('no')))), Promise.reject())
  }

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    return Promise.resolve();
  }

  async function loadVideos() {
    const container = $('#video-list');
    if (!container) return;
    container.innerHTML = '<p style="grid-column:1/-1;color:var(--text-muted);">Cargando videos...</p>';
    try {
      const data = await fetchJsonAny(VIDEO_JSON_PATHS).catch(async () => {
        // Try local sync server
        try {
          const r = await fetch('http://localhost:8600/list');
          if (r.ok) return r.json();
        } catch(e) {}
        throw new Error('No video index found');
      });
      renderVideoCards(data, container);
    } catch (e) {
      container.innerHTML = '<p style="grid-column:1/-1;color:var(--text-muted);">No hay videos disponibles.</p>';
      console.warn('loadVideos error', e);
    }
  }

  function renderVideoCards(list, container) {
    container.innerHTML = '';
    if (!Array.isArray(list) || list.length === 0) {
      container.innerHTML = '<p style="grid-column:1/-1;color:var(--text-muted);">No hay videos actualmente.</p>';
      return;
    }

    list.forEach(item => {
      const card = document.createElement('article');
      card.className = 'card video-card';
      card.style.padding = '10px';

      const title = document.createElement('h3');
      title.textContent = item.title || item.filename || item.name || (item.url || '').split('/').pop();
      title.style.fontSize = '0.95rem';
      title.style.margin = '0 0 8px 0';

      const preview = document.createElement('div');
      preview.style.height = '140px';
      preview.style.background = '#000';
      preview.style.borderRadius = '8px';
      preview.style.overflow = 'hidden';
      preview.style.display = 'flex';
      preview.style.alignItems = 'center';
      preview.style.justifyContent = 'center';

      if (item.poster) {
        const img = document.createElement('img'); img.src = item.poster; img.alt = title.textContent; img.style.width = '100%'; img.style.height = '100%'; img.style.objectFit = 'cover'; preview.appendChild(img);
      } else {
        const vid = document.createElement('video'); vid.src = encodeURI(item.url); vid.preload = 'metadata'; vid.muted = true; vid.style.width = '100%'; vid.style.height = '100%'; vid.style.objectFit = 'cover'; preview.appendChild(vid);
      }

      const actions = document.createElement('div');
      actions.style.display = 'flex';
      actions.style.gap = '8px';
      actions.style.marginTop = '8px';

      const play = document.createElement('button'); play.className = 'button button-secondary'; play.textContent = '▶ Reproducir';
      play.addEventListener('click', () => openPlayer(item));

      const dl = document.createElement('a'); dl.className = 'button button-primary'; dl.textContent = '⬇ Descargar'; dl.href = encodeURI(item.url); dl.setAttribute('download', '');
      dl.addEventListener('click', (ev) => { sendEvent('download', item); });

      const share = document.createElement('button'); share.className = 'button'; share.textContent = '🔗 Compartir';
      share.addEventListener('click', async () => {
        try {
          const ref = prompt('Etiqueta para personalizar el enlace (opcional)');
          let url = item.share_url || item.url || ('/public/videos/' + (item.slug || item.filename));
          if (ref) url += (url.indexOf('?') >= 0 ? '&' : '?') + 'ref=' + encodeURIComponent(ref);
          const full = location.origin + url;
          await copyToClipboard(full);
          alert('Enlace copiado al portapapeles');
          sendEvent('share', Object.assign({}, item, { share_link: full }));
        } catch (e) {
          console.warn('Share failed', e);
        }
      });

      const meta = document.createElement('div'); meta.style.marginTop = '8px'; meta.style.color = 'var(--text-muted)';
      meta.textContent = (item.size ? humanFileSize(item.size) + ' · ' : '') + (item.mtime || '');

      actions.appendChild(play); actions.appendChild(dl); actions.appendChild(share);

      card.appendChild(title); card.appendChild(preview); card.appendChild(actions); card.appendChild(meta);
      container.appendChild(card);
    });
  }

  function humanFileSize(bytes) {
    if (!bytes) return '';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(1) * 1 + ' ' + ['B','KB','MB','GB','TB'][i];
  }

  function openPlayer(item) {
    const modal = document.createElement('div');
    modal.style.position = 'fixed'; modal.style.inset = 0; modal.style.background = 'rgba(0,0,0,0.6)'; modal.style.display='flex'; modal.style.alignItems='center'; modal.style.justifyContent='center'; modal.style.zIndex = 9999;
    const panel = document.createElement('div'); panel.style.width='min(960px,95%)'; panel.style.maxHeight='90%'; panel.style.background='#071018'; panel.style.padding='12px'; panel.style.borderRadius='10px'; panel.style.boxShadow='0 12px 45px rgba(0,0,0,0.6)';
    const title = document.createElement('h3'); title.textContent = item.title || item.filename || item.name; title.style.margin='0 0 8px 0';
    const video = document.createElement('video'); video.src = encodeURI(item.url); video.controls = true; video.autoplay = true; video.style.width = '100%'; video.style.maxHeight='70vh';
    const close = document.createElement('button'); close.className = 'button button-secondary'; close.textContent = 'Cerrar'; close.style.marginTop='8px';
    close.addEventListener('click', () => { document.body.removeChild(modal); });
    panel.appendChild(title); panel.appendChild(video); panel.appendChild(close);
    modal.appendChild(panel); document.body.appendChild(modal);
    sendEvent('play', item);
  }

  function sendEvent(action, item) {
    const payload = { action, file: item.url || item.filename || item.name || '', timestamp: new Date().toISOString(), userAgent: navigator.userAgent };
    // Try serverless function (SendGrid or SMTP on Netlify)
    fetch('/.netlify/functions/notify_event', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify(payload) }).catch(() => {
      // fallback to local server
      try { fetch('http://localhost:8600/event', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) }); } catch(e) { /* ignore */ }
    });
  }

  async function loadDocs() {
    const list = document.getElementById('media-docs-list'); if (!list) return; list.innerHTML = '<li style="color:var(--text-muted);">Cargando...</li>';
    try {
      // try to load public/docs folder index
      const r = await fetch('/public/docs/index.html');
      if (!r.ok) throw new Error('no docs index');
      const text = await r.text();
      const parser = new DOMParser(); const doc = parser.parseFromString(text, 'text/html');
      const anchors = Array.from(doc.querySelectorAll('a[href]'));
      list.innerHTML = '';
      anchors.forEach(a => {
        const li = document.createElement('li'); li.style.display='flex'; li.style.justifyContent='space-between'; li.style.alignItems='center';
        const name = document.createElement('span'); name.textContent = a.textContent || a.getAttribute('href');
        const link = document.createElement('a'); link.href = a.getAttribute('href'); link.target = '_blank'; link.className = 'text-link'; link.textContent = 'Open';
        li.appendChild(name); li.appendChild(link); list.appendChild(li);
      });
      if (anchors.length === 0) list.innerHTML = '<li style="color:var(--text-muted);">No hay documentos.</li>';
    } catch (e) { list.innerHTML = '<li style="color:var(--text-muted);">No hay documentos.</li>'; }
  }

  async function loadImages() {
    const grid = document.getElementById('media-images-grid'); if (!grid) return; grid.innerHTML = '<div style="grid-column:1/-1;color:var(--text-muted);">Cargando...</div>';
    try {
      // try to fetch assets/images by requesting a small known file list path if exists
      const example = '/assets/images';
      // best-effort: list a few known images
      const candidates = ['assets/images/logo.svg','assets/images/industrial-network.svg','assets/images/simple-in.png'];
      grid.innerHTML = '';
      candidates.forEach(p => {
        const img = document.createElement('img'); img.src = '/' + p.replace(/^\//,''); img.alt = p; img.style.width='100%'; img.style.height='120px'; img.style.objectFit='cover'; img.style.borderRadius='8px'; img.style.border='1px solid rgba(255,255,255,0.04)';
        const wrapper = document.createElement('div'); wrapper.appendChild(img); grid.appendChild(wrapper);
      });
    } catch (e) { grid.innerHTML = '<div style="color:var(--text-muted);">No hay imágenes.</div>'; }
  }

  function loadNews() {
    const list = document.getElementById('media-news-list'); if (!list) return; list.innerHTML = '';
    // Placeholder news items — user can replace these with a simple JSON feed later
    const items = [
      { title: 'Nuevo catálogo comercial', date: '2026-06-01', body: 'Catálogo actualizado con nuevos equipos y soluciones.' },
      { title: 'Fechas de feria 2026', date: '2026-05-10', body: 'Presencia confirmada en ferias de empaquetado y automatización.' }
    ];
    items.forEach(n => { const node = document.createElement('article'); node.className='card'; node.innerHTML = `<h4 style="margin:0">${n.title}</h4><small style="color:var(--text-muted)">${n.date}</small><p style="color:var(--text-muted);margin-top:6px">${n.body}</p>`; list.appendChild(node); });
  }

  // Sync button handler — try local sync server
  function setupSyncButton() {
    const btn = document.getElementById('sync-videos'); if (!btn) return;
    btn.addEventListener('click', async () => {
      btn.disabled = true; btn.textContent = 'Actualizando…';
      try {
        const r = await fetch('http://localhost:8600/sync', { method: 'POST' });
        if (!r.ok) throw new Error('Sync failed');
        const res = await r.json();
        console.log('sync result', res);
        // reload videos
        await loadVideos();
        btn.textContent = 'Actualizado';
      } catch (e) {
        console.warn('Sync failed', e);
        btn.textContent = 'Error — ejecutar localmente el script de sincronización';
      } finally { setTimeout(()=>{ btn.disabled = false; btn.textContent = '🔄 Actualizar videos'; }, 3000); }
    });
  }

  // Initialize tab handlers
  document.addEventListener('DOMContentLoaded', () => {
    $all(TAB_SELECTOR).forEach(b => b.addEventListener('click', () => setActiveTab(b.dataset.tab)));
    setActiveTab('docs');
    setupSyncButton();
  });

})();
