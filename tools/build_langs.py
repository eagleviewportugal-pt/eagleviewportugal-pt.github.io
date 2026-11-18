#!/usr/bin/env python3
"""Gera es.html e en.html a partir de index.html (que é a fonte única).
Correr sempre depois de editar index.html:  python3 tools/build_langs.py
Os textos vêm do dicionário T (pt/es/en) que está no próprio index.html; são escritos
diretamente no HTML para que o Google indexe cada língua."""
import re, json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
BASE = 'https://eagleviewportugal.com/'
META = {
 'es': dict(file='es.html', locale='es_ES',
   title='Eagleview Portugal · Producción de vídeo, dron y redes sociales',
   desc='Eagleview Productions: producción de vídeo, filmación aérea con dron, Reels, gestión de redes sociales y webs para restaurantes y alojamientos. Desde Mourão, en el Alentejo, para todo Portugal.',
   ogt='Eagleview Portugal — Vídeo, dron y redes sociales',
   ogd='Vídeos promocionales, Reels y gestión de redes sociales para hoteles, restaurantes, marcas y ayuntamientos. Con sede en Mourão, en el Alentejo, trabajando en todo Portugal.'),
 'en': dict(file='en.html', locale='en_GB',
   title='Eagleview Portugal · Video production, drone and social media',
   desc='Eagleview Productions: video production, aerial drone filming, Reels, social media management and websites for restaurants and holiday rentals. Based in Mourão, Alentejo, working all over Portugal.',
   ogt='Eagleview Portugal — Video, drone and social media',
   ogd='Promotional videos, Reels and social media management for hotels, restaurants, brands and local councils. Based in Mourão, in the Alentejo, working all over Portugal.'),
}
def dictionary(lang):
    m = re.search(r'\n%s:\{\n(.*?)\n\}' % lang, SRC, re.S)
    body = m.group(1).strip().rstrip(',')
    return json.loads('{' + body + '}')
def attr(tag_html, name, value):
    return re.sub(r'(%s=")[^"]*(")' % name, lambda m: m.group(1) + html.escape(value, quote=True) + m.group(2), tag_html, count=1)
for lang, M in META.items():
    T = dictionary(lang); P = dictionary('pt')
    t = lambda k: T.get(k, P.get(k, ''))
    out = SRC
    head, rest = out.split('<body', 1)
    body, scripts = rest.split('<script>', 1)
    # visible texts with data-i
    body = re.sub(r'(<(\w+)\b[^>]*\bdata-i="([^"]+)"[^>]*>)(.*?)(</\2>)',
                  lambda m: m.group(1) + html.escape(t(m.group(3)), quote=False) + m.group(5), body, flags=re.S)
    body = re.sub(r'(<[^>]*\bdata-ph="([^"]+)"[^>]*>)', lambda m: attr(m.group(1), 'placeholder', t(m.group(2))), body)
    body = re.sub(r'(<button type="button" data-lang="(\w+)" aria-pressed=")(true|false)(")',
                  lambda m: m.group(1) + ('true' if m.group(2) == lang else 'false') + m.group(4), body)
    # head
    head = head.replace('<html lang="pt" data-page="pt">', '<html lang="%s" data-page="%s">' % (lang, lang))
    head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(M['title']), head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(M['desc']), head)
    head = head.replace('<link rel="canonical" href="%s">' % BASE, '<link rel="canonical" href="%s%s">' % (BASE, M['file']))
    head = head.replace('<meta property="og:url" content="%s">' % BASE, '<meta property="og:url" content="%s%s">' % (BASE, M['file']))
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(M['ogt']), head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(M['ogd']), head)
    head = head.replace('<meta property="og:locale" content="pt_PT">', '<meta property="og:locale" content="%s">' % M['locale'])
    out = head + '<body' + body + '<script>' + scripts
    open(os.path.join(ROOT, M['file']), 'w', encoding='utf-8').write(out)
    print('gerado', M['file'], len(out))
