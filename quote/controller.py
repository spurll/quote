import random
import json
import re
import textwrap

from quote import app, contents


def get(root=app.config['DEFAULT_ROOT'], output_format='plain', width=''):
    item = random.choice(contents[root])

    if output_format == 'html':
        output = format_html(root, item)
    elif output_format == 'plain':
        output = format_plaintext(root, item, width)
    elif output_format == 'json':
        output = json.dumps(item)
    else:
        return ''

    return output


def format_html(root, item):
    content = item.get('content')
    content = re.sub(r'\n +', r'\n&nbsp;&nbsp;&nbsp;&nbsp;', content)
    content = re.sub(r'\n', r'\n<br/>', content)

    if root == 'poem':
        return '<h1>{}</h1>\n<h2>{}</h2>\n{}'.format(
            item.get('work'), item.get('author'), content
        )

    attribution = ''

    if 'character' in item:
        attribution = '&mdash;{}<br/>in <i>{}</i>'.format(
            item['character'], item.get('work')
        )
        if 'author' in item:
            attribution += ' by {}'.format(item['author'])
    elif 'work' in item:
        attribution = '&mdash;{},<br/><i>{}</i>'.format(
            item.get('author'), item['work']
        )
    elif 'author' in item:
        if item.get('dubious'):
            attribution = 'Generally attributed to ' + item['author']
        else:
            attribution = '&mdash;' + item['author']

    if 'link' in item:
        attribution = '<a href="{}">{}</a>'.format(
            item['link'], attribution if attribution else 'Source'
        )

    return '<div>{}</div>'.format(item.get('content')) + (
        '<div style="text-align:right;">{}</div>'
        .format(attribution) if attribution else ''
    )


def format_plaintext(root, item, width=''):
    if root == 'poem':
        output = '{}\n{}\n\n{}'.format(
            item.get('work'), item.get('author'), item.get('content')
        )

    else:
        attribution = ''

        if 'character' in item:
            author = (
                'in {} by {}'.format(item.get('work'), item['author'])
                if 'author' in item else 'in {}'.format(item.get('work'))
            )

            attribution = '{:>{width}}\n{:>{width}}'.format(
                '—' + item['character'], author, width=width
            )

        elif 'work' in item:
            attribution = '{:>{width}}\n{:>{width}}'.format(
                '—' + item.get('author') + ',', item['work'], width=width
            )

        elif 'author' in item:
            attribution = '{:>{width}}'.format(
                ('Generally attributed to ' if item.get('dubious') else '—')
                + item['author'], width=width
            )

        output = item.get('content') + (
            '\n{}'.format(attribution) if attribution else ''
        )

    if width:
        lines = map(
            lambda x: textwrap.fill(x, width=width, replace_whitespace=False),
            output.splitlines()
        )
        output = '\n'.join(lines)

    return output
