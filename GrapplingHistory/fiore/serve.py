"""
Dev server for the Fiore reader page.
Serves static files + handles POST /save-edit to write edits back to index.html.
Run: python3 serve.py
"""

import http.server
import json
import re
from pathlib import Path

PORT = 8847
ROOT = Path(__file__).resolve().parents[2]  # project root
HTML_FILE = Path(__file__).resolve().parent / "index.html"


class EditHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path == '/save-edit':
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            self._apply_edits(body)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else:
            self.send_error(404)

    def _apply_edits(self, sections):
        html = HTML_FILE.read_text()

        if 'analysis' in sections:
            html = self._replace_section(html,
                '<div class="analysis-section">',
                '<!-- ── Section Nav',
                sections['analysis'],
                wrap_tag='div', wrap_class='analysis-section')

        if 'epigraph' in sections:
            html = self._replace_section(html,
                '<div class="epigraph">',
                '</div>\n\n    <!-- ── Lead',
                sections['epigraph'],
                wrap_tag='div', wrap_class='epigraph')

        if 'lead' in sections:
            html = self._replace_inner(html, '<p class="lead">', '</p>', sections['lead'])

        HTML_FILE.write_text(html)
        print(f"  Saved edits to {HTML_FILE.name}")

    def _replace_inner(self, html, open_tag, close_tag, new_inner):
        """Replace innerHTML between open_tag and the next close_tag."""
        start = html.find(open_tag)
        if start < 0:
            return html
        inner_start = start + len(open_tag)
        end = html.find(close_tag, inner_start)
        if end < 0:
            return html
        return html[:inner_start] + '\n' + new_inner + '\n    ' + html[end:]

    def _replace_section(self, html, start_marker, end_marker, new_inner, wrap_tag='div', wrap_class=''):
        """Replace a whole section's innerHTML."""
        start = html.find(start_marker)
        if start < 0:
            return html
        inner_start = start + len(start_marker)
        end = html.find(end_marker, inner_start)
        if end < 0:
            return html
        cls = f' class="{wrap_class}"' if wrap_class else ''
        return html[:inner_start] + '\n' + new_inner + '\n    ' + html[end:]

    def log_message(self, format, *args):
        if '/save-edit' in str(args):
            print(f"  {args[0]}")


if __name__ == '__main__':
    print(f"Fiore reader dev server at http://localhost:{PORT}/GrapplingHistory/fiore/")
    print(f"Edit mode: click 'Edit Mode' button (bottom-right)")
    print(f"Edits save to: {HTML_FILE}")
    print(f"Ctrl+C to stop\n")
    server = http.server.HTTPServer(('', PORT), EditHandler)
    server.serve_forever()
