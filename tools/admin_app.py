#!/usr/bin/env python3
"""Simple Flask admin for creating/editing product pages.

Run: python tools/admin_app.py
Open: http://localhost:5000/admin

This app saves product JSON to `data/<slug>.json` and renders a preview
to `solutions/<slug>.generated.html` using `tools/product_pages.py`.
Uploads are stored under `assets/images/products/<slug>/`.
"""
import os
import json
import pathlib
import importlib.util
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
ASSETS_DIR = ROOT / 'assets' / 'images' / 'products'
SOLUTIONS_DIR = ROOT / 'solutions'

app = Flask(__name__, template_folder=str(pathlib.Path(__file__).parent / 'admin_templates'))
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.secret_key = 'dev-secret'


def load_generator():
    # load tools/product_pages.py as module 'product_pages'
    gen_path = ROOT / 'tools' / 'product_pages.py'
    spec = importlib.util.spec_from_file_location('product_pages', str(gen_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def slugify(s: str) -> str:
    s = s.strip().lower()
    return ''.join(c if c.isalnum() or c=='-' else '-' for c in s).strip('-')


def list_products():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sorted([p.stem for p in DATA_DIR.glob('*.json')])


@app.route('/admin')
def admin_index():
    prods = []
    for slug in list_products():
        data = json.loads((DATA_DIR / f'{slug}.json').read_text(encoding='utf-8'))
        prods.append({'slug': slug, 'title': data.get('title','')})
    return render_template('list.html', products=prods)


@app.route('/admin/new')
def admin_new():
    return render_template('form.html', data={}, slug='')


@app.route('/admin/edit/<slug>')
def admin_edit(slug):
    p = DATA_DIR / f'{slug}.json'
    if not p.exists():
        flash('Product not found', 'error')
        return redirect(url_for('admin_index'))
    data = json.loads(p.read_text(encoding='utf-8'))
    return render_template('form.html', data=data, slug=slug)


@app.route('/admin/save', methods=['POST'])
def admin_save():
    form = request.form
    files = request.files
    title = form.get('title','').strip()
    if not title:
        flash('Title is required', 'error')
        return redirect(request.referrer or url_for('admin_index'))
    slug = form.get('slug') or slugify(title)

    product = {
        'title': title,
        'eyebrow': form.get('eyebrow',''),
        'hero_image': form.get('hero_image',''),
        'hero_alt': form.get('hero_alt',''),
        'hero_image_onerror': form.get('hero_image_onerror','/assets/images/ingecart-world.png'),
        'hero_video': form.get('hero_video',''),
        'hero_cta_text': form.get('hero_cta_text','Ver vídeo'),
        'description': form.get('description',''),
        'overview': form.get('overview',''),
        'key_functions': [l for l in (form.get('key_functions') or '').splitlines() if l.strip()],
        'technical_specifications': [],
        'how_it_works': [l for l in (form.get('how_it_works') or '').splitlines() if l.strip()],
        'benefits': [l for l in (form.get('benefits') or '').splitlines() if l.strip()],
        'investment_summary': [],
        'payback_period': form.get('payback_period',''),
        'short_title': form.get('short_title',''),
        'case_study_title': form.get('case_study_title',''),
        'case_study_text': form.get('case_study_text',''),
        'contact': []
    }

    # parse technical specs lines like "Parameter|Specification"
    for line in (form.get('technical_specifications') or '').splitlines():
        if not line.strip():
            continue
        if '|' in line:
            param, spec = line.split('|',1)
        elif '\t' in line:
            param, spec = line.split('\t',1)
        else:
            param, spec = line, ''
        product['technical_specifications'].append({'parameter':param.strip(), 'spec':spec.strip()})

    # investment summary: "Component|Estimate"
    for line in (form.get('investment_summary') or '').splitlines():
        if not line.strip():
            continue
        if '|' in line:
            comp, est = line.split('|',1)
        else:
            comp, est = line, ''
        product['investment_summary'].append({'component':comp.strip(), 'estimate':est.strip()})

    # contact: "Label|Value"
    for line in (form.get('contact') or '').splitlines():
        if not line.strip():
            continue
        if '|' in line:
            lab, val = line.split('|',1)
        else:
            lab, val = line, ''
        product['contact'].append({'label':lab.strip(), 'value':val.strip()})

    # handle hero image upload
    upload = files.get('hero_image_file')
    if upload and upload.filename:
        dest_dir = ASSETS_DIR / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        filename = upload.filename.replace(' ', '_')
        dest = dest_dir / filename
        upload.save(str(dest))
        product['hero_image'] = f'/assets/images/products/{slug}/{filename}'

    # save JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / f'{slug}.json').write_text(json.dumps(product, indent=2, ensure_ascii=False), encoding='utf-8')

    # render preview
    generator = load_generator()
    html = generator.render(product)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SOLUTIONS_DIR / f'{slug}.generated.html'
    out_path.write_text(html, encoding='utf-8')

    flash(f'Saved {slug} and rendered preview ({out_path.name})', 'success')
    return redirect(url_for('admin_index'))


@app.route('/assets/images/products/<slug>/<path:filename>')
def prod_image(slug, filename):
    folder = ASSETS_DIR / slug
    return send_from_directory(str(folder), filename)


if __name__=='__main__':
    app.run(debug=True)
