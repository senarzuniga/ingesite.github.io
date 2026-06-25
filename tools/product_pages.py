#!/usr/bin/env python3
"""Generate and edit product pages using the HTML template.

Usage:
  python tools/product_pages.py render data/ingetrans.json output/ingetrans.html
  python tools/product_pages.py new data/newproduct.json
  python tools/product_pages.py edit data/ingetrans.json

This script performs simple templating by replacing placeholder tokens.
"""
import json
import sys
from pathlib import Path


TEMPLATE = Path('templates/product-template.html')


def load_template():
    return TEMPLATE.read_text(encoding='utf-8')


def render(data: dict) -> str:
    html = load_template()
    # simple replacements
    replacements = {
        '{{title}}': data.get('title',''),
        '{{eyebrow}}': data.get('eyebrow',''),
        '{{hero_image}}': data.get('hero_image','/assets/images/ingecart-world.png'),
        '{{hero_alt}}': data.get('hero_alt','Product image'),
        '{{hero_image_onerror}}': data.get('hero_image_onerror','/assets/images/ingecart-world.png'),
        '{{hero_video}}': data.get('hero_video',''),
        '{{hero_cta_text}}': data.get('hero_cta_text','Ver vídeo'),
        '{{description}}': data.get('description',''),
        '{{overview}}': data.get('overview',''),
        '{{payback_period}}': data.get('payback_period',''),
        '{{short_title}}': data.get('short_title',''),
        '{{case_study_title}}': data.get('case_study_title',''),
        '{{case_study_text}}': data.get('case_study_text',''),
    }
    for k,v in replacements.items():
        html = html.replace(k, str(v))

    # lists
    def join_list(tag, items):
        if not items:
            return ''
        return '\n'.join(f'<li>{i}</li>' for i in items)

    html = html.replace('<!-- KEY_FUNCTIONS_LIST -->', join_list('li', data.get('key_functions',[])))
    html = html.replace('<!-- HOW_IT_WORKS_LIST -->', join_list('li', data.get('how_it_works',[])))
    html = html.replace('<!-- BENEFITS_LIST -->', join_list('li', data.get('benefits',[])))

    # technical specs
    specs = data.get('technical_specifications', [])
    rows = []
    for p in specs:
        param = p.get('parameter')
        spec = p.get('spec')
        if param and spec is not None:
            rows.append(f'<tr><td>{param}</td><td>{spec}</td></tr>')
    html = html.replace('<!-- TECH_SPECS_ROWS -->', '\n'.join(rows))

    # investment
    inv = data.get('investment_summary', [])
    inv_rows = []
    for i in inv:
        inv_rows.append(f'<tr><td>{i.get("component")}</td><td>{i.get("estimate")}</td></tr>')
    html = html.replace('<!-- INVESTMENT_ROWS -->', '\n'.join(inv_rows))

    # contact
    contact = data.get('contact', [])
    contact_html = '\n'.join(f'<li><strong>{c.get("label")}</strong> {c.get("value")}</li>' for c in contact)
    html = html.replace('<!-- CONTACT_LIST -->', contact_html)

    # conditionally show hero button
    if data.get('hero_video'):
        html = html.replace('{{#if_hero_video}}', '')
        html = html.replace('{{/if_hero_video}}', '')
    else:
        # remove the block
        start = html.find('{{#if_hero_video}}')
        end = html.find('{{/if_hero_video}}')
        if start!=-1 and end!=-1:
            html = html[:start] + html[end+len('{{/if_hero_video}}'):]

    return html


def cmd_render(infile, outfile):
    data = json.loads(Path(infile).read_text(encoding='utf-8'))
    out = render(data)
    Path(outfile).write_text(out, encoding='utf-8')
    print('Rendered', outfile)


def cmd_new(outfile):
    example = {
        'title':'New Product',
        'eyebrow':'Product Category',
        'hero_image':'/assets/images/ingecart-world.png',
        'hero_alt':'Product hero',
        'hero_video':'',
        'hero_cta_text':'Ver vídeo',
        'description':'Short product description',
        'overview':'Overview text',
        'key_functions':['Automated movement','Delivery to multiple points'],
        'technical_specifications':[{'parameter':'System Type','spec':'Surface rail‑guided transfer carriage + floor tracks'}],
        'how_it_works':['Step one','Step two'],
        'benefits':['Benefit 1','Benefit 2'],
        'investment_summary':[{'component':'System','estimate':'~ $1.0M USD'}],
        'payback_period':'< 18 months',
        'short_title':'NEWPROD',
        'case_study_title':'',
        'case_study_text':'',
        'contact':[{'label':'Company:','value':'INGECART'},{'label':'Email:','value':'hablemos@ingecart.eu'}]
    }
    Path(outfile).write_text(json.dumps(example, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Created sample data', outfile)


def main(argv):
    if len(argv)<2:
        print(__doc__)
        return
    cmd = argv[1]
    if cmd=='render' and len(argv)==4:
        cmd_render(argv[2], argv[3])
    elif cmd=='new' and len(argv)==3:
        cmd_new(argv[2])
    else:
        print('Usage: product_pages.py render data.json output.html | new data.json')


if __name__=='__main__':
    main(sys.argv)
