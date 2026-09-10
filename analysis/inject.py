"""Inject the freshly built HEBE blob into tool/page.html, replacing the previous one."""
import re, os
from paths import ROOT, o
blob = open(o('blob3.js')).read().strip()
if not blob.startswith('const HEBE='):
    raise SystemExit('blob3.js does not start with const HEBE=')
page = os.path.join(ROOT, 'tool', 'page.html')
s = open(page).read()
new, n = re.subn(r'^const HEBE=\{.*\};$', lambda m: blob, s, count=1, flags=re.M)
if n != 1:
    raise SystemExit('expected exactly one HEBE blob line in page.html, found %d' % n)
open(page, 'w').write(new)
print('injected %d bytes into tool/page.html' % len(blob))
