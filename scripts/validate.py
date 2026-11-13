#!/usr/bin/env python3
"""Walidator obu trybów: JSON-HTML i JSON-IMAGE (bez zewnętrznych bibliotek)."""
import json
import re
from pathlib import Path

ROOT = (Path(__file__).resolve().parents[1] / 'public').resolve()
SLUG = re.compile(r'^[a-z0-9][a-z0-9_-]*$')
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg'}


def safe_file(relative, extensions):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT) or path.suffix.lower() not in extensions:
        raise ValueError(f'Niedozwolona ścieżka: {relative}')
    if not path.is_file():
        raise ValueError(f'Brak pliku: {relative}')
    return path


def read_json(relative):
    return json.loads(safe_file(relative, {'.json'}).read_text(encoding='utf-8'))


def valid_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Brak wymaganego tekstu: {label}')


def valid_slug(value, label, used):
    if not isinstance(value, str) or not SLUG.fullmatch(value) or value in used:
        raise ValueError(f'Niepoprawne lub powtórzone ID {label}: {value}')
    used.add(value)


def check():
    for name in ('index.html', 'app.js', 'styles.css'):
        if not (ROOT / name).is_file():
            raise ValueError(f'Brak public/{name}')
    site = read_json('content/site.json')
    valid_text(site.get('title'), 'site.title')
    if not isinstance(site.get('pages'), list) or not site['pages']:
        raise ValueError('Brak listy site.pages')
    page_ids = set()
    command_count = image_count = section_count = 0
    for record in site['pages']:
        pid = record.get('id')
        valid_slug(pid, 'zakładki', page_ids)
        valid_text(record.get('label'), f'{pid}.label')
        location = Path(record['file'])
        page = read_json(location)
        if page.get('id') != pid:
            raise ValueError(f'ID strony nie zgadza się: {location}')
        mode = page.get('type', 'json-html')
        if mode not in {'json-html', 'json-image'}:
            raise ValueError(f'Nieobsługiwany tryb: {mode}')
        valid_text(page.get('heading'), f'{pid}.heading')
        if not isinstance(page.get('sections'), list):
            raise ValueError(f'{pid}: sections musi być listą')
        section_ids = set()
        for rel in page['sections']:
            sec = read_json(location.parent / rel)
            sid = sec.get('id')
            valid_slug(sid, f'sekcji strony {pid}', section_ids)
            valid_text(sec.get('title'), f'{pid}/{sid}.title')
            section_count += 1
            if mode == 'json-html':
                groups = set()
                for group in sec.get('subsections', []):
                    gid = group.get('id')
                    valid_slug(gid, f'podsekcji {sid}', groups)
                    valid_text(group.get('title'), f'{sid}/{gid}.title')
                    for entry in group.get('commands', []):
                        valid_text(entry.get('command'), f'{sid}/{gid}.command')
                        valid_text(entry.get('description'), f'{sid}/{gid}.description')
                        command_count += 1
            else:
                if not isinstance(sec.get('images'), list) or not sec['images']:
                    raise ValueError(f'{pid}/{sid}: images musi zawierać grafiki')
                image_ids = set()
                for pic in sec['images']:
                    image_id = pic.get('id')
                    valid_slug(image_id, f'obrazu w {sid}', image_ids)
                    valid_text(pic.get('title'), f'{sid}/{image_id}.title')
                    valid_text(pic.get('alt'), f'{sid}/{image_id}.alt')
                    src = pic.get('src')
                    valid_text(src, f'{sid}/{image_id}.src')
                    # Obrazy danej zakładki muszą leżeć tylko w jej katalogu sections/images/.
                    # Nie akceptujemy odwołań do innych zakładek ani katalogów współdzielonych.
                    expected = Path('content') / pid / 'sections' / 'images'
                    src_path = Path(src)
                    if src_path.is_absolute() or src_path.parent != expected:
                        raise ValueError(
                            f'{pid}/{sid}/{image_id}: src musi wskazywać plik w {expected}/'
                        )
                    safe_file(src, IMAGE_EXTS)
                    image_count += 1
    if site.get('defaultPage') not in page_ids:
        raise ValueError('defaultPage nie wskazuje istniejącej zakładki')
    if command_count < 186:
        raise ValueError(f'Za mało oryginalnych komend: {command_count}')
    if image_count < 1:
        raise ValueError('Brak grafik JSON-IMAGE')
    print(f'OK: {len(page_ids)} zakładki, {section_count} sekcji, {command_count} komend, {image_count} grafik.')
    return {'pages': len(page_ids), 'sections': section_count, 'commands': command_count, 'images': image_count}


if __name__ == '__main__':
    check()
