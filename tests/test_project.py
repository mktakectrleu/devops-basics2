import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate import check, read_json, safe_file, IMAGE_EXTS


class ProjectTests(unittest.TestCase):
    def test_all_data_valid(self):
        self.assertGreaterEqual(check()['commands'], 186)

    def test_branding_and_pages(self):
        site = read_json('content/site.json')
        self.assertEqual(site['title'], 'DevOps Basics 2')
        self.assertEqual({x['id'] for x in site['pages']}, {'lokalnie','github','vscode','diagramy'})

    def test_existing_sections_preserved(self):
        self.assertEqual(len(read_json('content/lokalnie/page.json')['sections']), 10)
        self.assertEqual(len(read_json('content/github/page.json')['sections']), 4)
        self.assertEqual(len(read_json('content/vscode/page.json')['sections']), 5)

    def test_two_modes(self):
        for name in ('lokalnie','github','vscode'):
            self.assertEqual(read_json(f'content/{name}/page.json')['type'], 'json-html')
        self.assertEqual(read_json('content/diagramy/page.json')['type'], 'json-image')

    def test_image_files_present(self):
        section = read_json('content/diagramy/sections/sekcja-01.json')
        for pic in section['images']:
            self.assertTrue(pic['src'].startswith('content/diagramy/sections/images/'))
            self.assertTrue(safe_file(pic['src'], IMAGE_EXTS).stat().st_size > 1000)

    def test_images_limited_to_own_tab(self):
        import json
        from unittest.mock import patch
        from validate import ROOT
        section_path = ROOT / 'content/diagramy/sections/sekcja-01.json'
        original = json.loads(section_path.read_text(encoding='utf-8'))
        modified = json.loads(json.dumps(original))
        modified['images'][0]['src'] = 'content/other/sections/images/test.jpg'
        from validate import check
        from unittest.mock import patch
        import validate
        original_reader = validate.read_json
        def reader(location):
            if str(location).endswith('diagramy/sections/sekcja-01.json'):
                return modified
            return original_reader(location)
        with patch('validate.read_json', side_effect=reader):
            with self.assertRaisesRegex(ValueError, 'sections/images'):
                check()

    def test_directory_traversal_rejected(self):
        with self.assertRaises(ValueError):
            read_json('../../README.md')


if __name__ == '__main__':
    unittest.main()
