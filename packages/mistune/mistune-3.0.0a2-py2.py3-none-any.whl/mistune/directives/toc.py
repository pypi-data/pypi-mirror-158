"""
    TOC directive
    ~~~~~~~~~~~~~

    The TOC directive syntax looks like::

        .. toc:: Title
           :depth: 3

    "Title" and "depth" option can be empty. "depth" is an integer less
    than 6, which defines the max heading level writers want to include
    in TOC.
"""

from .base import Directive, parse_options
from ..toc import normalize_toc_item, render_toc_ul


class DirectiveToc(Directive):
    def __init__(self, depth=3, heading_id=None):
        self.depth = depth

        if callable(heading_id):
            self.heading_id = heading_id
        else:
            def heading_id(token, index):
                return 'toc_' + str(index + 1)
            self.heading_id = heading_id

    def parse(self, block, m, state):
        title = m.group('value')
        depth = None
        options = parse_options(m)
        if options:
            depth = dict(options).get('depth')
            if depth:
                try:
                    depth = int(depth)
                except (ValueError, TypeError):
                    return {
                        'type': 'block_error',
                        'raw': 'TOC depth MUST be integer',
                    }

        if depth is None:
            depth = self.depth
        elif depth < 1 or depth > 6:
            depth = self.depth

        attrs = {'title': title, 'depth': depth}
        return {'type': 'toc', 'raw': '', 'attrs': attrs}

    def toc_hook(self, md, state):
        sections = []
        headings = []

        for tok in state.tokens:
            if tok['type'] == 'toc':
                sections.append(tok)
            elif tok['type'] == 'heading':
                headings.append(tok)

        if sections:
            toc_items = []
            # adding ID for each heading
            for i, tok in enumerate(headings):
                tok['attrs']['id'] = self.heading_id(tok, i)
                toc_items.append(normalize_toc_item(md, tok))

            for sec in sections:
                depth = sec['attrs']['depth']
                toc = [item for item in toc_items if item[0] <= depth]
                sec['raw'] = render_toc_ul(toc)

    def __call__(self, md):
        if md.renderer and md.renderer.NAME == 'html':
            # only works with HTML renderer
            self.register_directive(md, 'toc')
            md.before_render_hooks.append(self.toc_hook)
            md.renderer.register('toc', render_html_toc)


def render_html_toc(renderer, text, title, depth):
    if not title:
        title = 'Table of Contents'

    html = '<details class="toc">\n<summary>' + title + '</summary>\n'
    return html + text + '</details>\n'
