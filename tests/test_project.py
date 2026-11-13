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
            self.assertTrue(safe_file(pic['src'], IMAGE_EXTS).stat().st_size > 1000)

    def test_directory_traversal_rejected(self):
        with self.assertRaises(ValueError):
            read_json('../../README.md')


if __name__ == '__main__':
    unittest.main()
