#!/usr/bin/env python3
"""
Local server to trigger video sync and to receive playback/download events.
Run this on the same machine that has the OneDrive folder; the web UI will attempt to call
http://localhost:8600/sync to update videos.
"""
import os
import json
import subprocess
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from threading import Thread, Event
import time
import importlib.util
import smtplib
from email.message import EmailMessage

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_VIDEOS = ROOT / 'public' / 'videos'
PUBLIC_DOCS = ROOT / 'public' / 'docs'

app = Flask(__name__)
CORS(app)

# watcher instance (started/stopped via endpoints)
WATCHER = None

@app.route('/list', methods=['GET'])
def list_videos():
    j = PUBLIC_VIDEOS / 'videos.json'
    if not j.exists():
        return jsonify([])
    return jsonify(json.loads(j.read_text(encoding='utf-8')))

@app.route('/sync', methods=['POST','GET'])
def sync():
    # Run the sync script
    try:
        py = os.environ.get('PYTHON', 'python')
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        # optional source path can be provided as JSON { "source": "C:\\path\\to\\videos" }
        data = request.get_json(silent=True) or {}
        src = data.get('source')
        cmd = [py, str(ROOT / 'scripts' / 'sync_videos.py')]
        if src:
            cmd.append(src)
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return jsonify({'ok': True, 'stdout': proc.stdout, 'stderr': proc.stderr})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/sync_docs', methods=['POST','GET'])
def sync_docs():
    try:
        py = os.environ.get('PYTHON', 'python')
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        data = request.get_json(silent=True) or {}
        src = data.get('source')
        cmd = [py, str(ROOT / 'scripts' / 'sync_docs.py')]
        if src:
            cmd.append(src)
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return jsonify({'ok': True, 'stdout': proc.stdout, 'stderr': proc.stderr})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/event', methods=['POST'])
def event():
    data = request.get_json() or {}
    action = data.get('action') or data.get('event') or 'unknown'
    file = data.get('file') or data.get('filename') or ''
    timestamp = data.get('timestamp')

    subject = f"Video {action} — {Path(file).name}"
    body = f"Action: {action}\nFile: {file}\nTime: {timestamp or ''}\nUser-Agent: {request.headers.get('User-Agent')}\nRemote: {request.remote_addr}\n"

    # Send via SMTP if configured
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    smtp_port = int(os.environ.get('SMTP_PORT') or 587)
    email_from = os.environ.get('EMAIL_FROM') or smtp_user or 'noreply@ingecart.local'
    email_to = os.environ.get('EMAIL_TO') or 'cgo@ingecart.es'

    if smtp_host and smtp_user and smtp_pass:
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = email_from
            msg['To'] = email_to
            msg.set_content(body)
            with smtplib.SMTP(smtp_host, smtp_port) as s:
                s.starttls()
                s.login(smtp_user, smtp_pass)
                s.send_message(msg)
            return jsonify({'ok': True, 'sent': True})
        except Exception as e:
            # fallback to log
            log_event(body)
            return jsonify({'ok': False, 'error': str(e)})

    # If SMTP not configured, write to a local log file
    log_event(body)
    return jsonify({'ok': True, 'logged': True})


@app.route('/list_docs', methods=['GET'])
def list_docs():
    j = PUBLIC_DOCS / 'docs.json'
    if not j.exists():
        return jsonify([])
    return jsonify(json.loads(j.read_text(encoding='utf-8')))

def log_event(text):
    try:
        with open(ROOT / 'video_events.log', 'a', encoding='utf-8') as fh:
            fh.write(text + '\n---\n')
    except Exception as e:
        # If logging fails, print to stderr (best-effort)
        try:
            print('log_event failed:', e)
        except Exception:
            pass


def _load_module(name, path):
    try:
        spec = importlib.util.spec_from_file_location(name, str(path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        print('Failed to load module', path, e)
        return None


class _DirWatcher:
    def __init__(self, paths, interval=5):
        self.paths = [Path(p) for p in (paths or [])]
        self.interval = interval
        self._stop = Event()
        self._thread = None
        self._snapshot = self._snapshot_paths()

    def _snapshot_paths(self):
        snap = {}
        for p in self.paths:
            try:
                if p.exists():
                    for f in p.iterdir():
                        if f.is_file():
                            snap[str(f)] = f.stat().st_mtime
            except Exception:
                pass
        return snap

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self):
        py = os.environ.get('PYTHON', 'python')
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        while not self._stop.is_set():
            time.sleep(self.interval)
            try:
                new_snap = self._snapshot_paths()
                if new_snap != self._snapshot:
                    print('Change detected in watched folders — running sync')
                    self._snapshot = new_snap
                    try:
                        subprocess.run([py, str(ROOT / 'scripts' / 'sync_videos.py')], capture_output=True, text=True, env=env)
                    except Exception as e:
                        print('Watcher sync_videos failed', e)
                    try:
                        subprocess.run([py, str(ROOT / 'scripts' / 'sync_docs.py')], capture_output=True, text=True, env=env)
                    except Exception as e:
                        print('Watcher sync_docs failed', e)
            except Exception as e:
                print('Watcher error', e)


@app.route('/watch/start', methods=['POST'])
def watch_start():
    global WATCHER
    if WATCHER and WATCHER._thread and WATCHER._thread.is_alive():
        return jsonify({'ok': True, 'status': 'already running'})
    data = request.get_json(silent=True) or {}
    paths = data.get('paths')
    interval = int(data.get('interval') or os.environ.get('VIDEO_SYNC_WATCH_INTERVAL') or 5)
    if not paths:
        paths = []
        sv = _load_module('sync_videos', ROOT / 'scripts' / 'sync_videos.py')
        if sv and hasattr(sv, 'SOURCE_DEFAULT'):
            paths.append(str(sv.SOURCE_DEFAULT))
        sd = _load_module('sync_docs', ROOT / 'scripts' / 'sync_docs.py')
        if sd and hasattr(sd, 'SOURCE_DEFAULT'):
            paths.append(str(sd.SOURCE_DEFAULT))
    WATCHER = _DirWatcher(paths, interval=interval)
    WATCHER.start()
    return jsonify({'ok': True, 'started': True, 'paths': paths})


@app.route('/watch/stop', methods=['POST','GET'])
def watch_stop():
    global WATCHER
    if not WATCHER:
        return jsonify({'ok': True, 'status': 'not running'})
    WATCHER.stop()
    WATCHER = None
    return jsonify({'ok': True, 'stopped': True})


@app.route('/watch/status', methods=['GET'])
def watch_status():
    running = WATCHER is not None and WATCHER._thread is not None and WATCHER._thread.is_alive()
    return jsonify({'running': running})

if __name__ == '__main__':
    # Optionally start watcher automatically if environment variable is set
    if os.environ.get('VIDEO_SYNC_WATCH'):
        paths = []
        sv = _load_module('sync_videos', ROOT / 'scripts' / 'sync_videos.py')
        if sv and hasattr(sv, 'SOURCE_DEFAULT'):
            paths.append(str(sv.SOURCE_DEFAULT))
        sd = _load_module('sync_docs', ROOT / 'scripts' / 'sync_docs.py')
        if sd and hasattr(sd, 'SOURCE_DEFAULT'):
            paths.append(str(sd.SOURCE_DEFAULT))
        if paths:
            WATCHER = _DirWatcher(paths, interval=int(os.environ.get('VIDEO_SYNC_WATCH_INTERVAL') or 5))
            WATCHER.start()

    port = int(os.environ.get('VIDEO_SYNC_PORT', 8600))
    host = os.environ.get('VIDEO_SYNC_HOST', '127.0.0.1')
    app.run(host=host, port=port)
