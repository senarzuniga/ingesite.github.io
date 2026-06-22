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
import smtplib
from email.message import EmailMessage

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_VIDEOS = ROOT / 'public' / 'videos'

app = Flask(__name__)
CORS(app)

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
        proc = subprocess.run([py, str(ROOT / 'scripts' / 'sync_videos.py')], capture_output=True, text=True, env=env)
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

if __name__ == '__main__':
    port = int(os.environ.get('VIDEO_SYNC_PORT', 8600))
    app.run(host='127.0.0.1', port=port)
