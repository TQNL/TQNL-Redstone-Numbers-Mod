"""Reject unrelated assets, shaders, unsafe publication paths and identity leaks."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def require(condition, message):
    if not condition:
        raise SystemExit(message)

def main():
    jar = ROOT / 'build/libs/redstone-numbers-0.1.0+mc1.21.11.jar'
    require(jar.is_file(), 'Build the release JAR first.')
    with zipfile.ZipFile(jar) as archive:
        names = archive.namelist()
        require(not archive.testzip(), 'Corrupt JAR')
        require(not any(n.startswith('assets/minecraft/') for n in names), 'Mod overrides vanilla assets')
        require(not any(n.lower().endswith(('.glsl', '.vsh', '.fsh', '.comp', '.spv')) for n in names), 'Authored shaders included')
        require(not any(n.startswith(('work/', 'run/', 'logs/', 'saves/')) for n in names), 'Runtime data included')
        meta = json.loads(archive.read('fabric.mod.json'))
        require(meta['environment'] == 'client', 'Mod must be client-only')
        require(meta['depends']['minecraft'] == '1.21.11', 'Wrong Minecraft target')
        require(set(meta['depends']) == {'fabricloader','minecraft','java','fabric-api'}, 'Unexpected required dependency')
        require('assets/redstonenumbers/font/numbers.json' in names, 'Private font missing')
        require(not any(n.endswith('.jar') for n in names), 'Unexpected bundled library')
    font = json.loads((ROOT / 'src/main/resources/assets/redstonenumbers/font/numbers.json').read_text())
    require(''.join(font['providers'][0]['chars']) == ''.join(chr(0xE000 + n) for n in range(16)), 'Wrong glyph mapping')
    image = Image.open(ROOT / 'src/main/resources/assets/redstonenumbers/textures/font/numbers.png').convert('RGBA')
    for n in range(16):
        cell = image.crop((n % 4 * 16, n // 4 * 16, n % 4 * 16 + 16, n // 4 * 16 + 16))
        require(cell.getchannel('A').getbbox() is not None, 'Blank number artwork')
    cosmetic = ROOT / 'outputs/TQNL-Redstone-Dust-Cosmetic-mc1.21.11.zip'
    with zipfile.ZipFile(cosmetic) as archive:
        expected = {'pack.mcmeta', 'credits.txt', 'ASSET-LICENSES.md'} | {
            'assets/minecraft/textures/block/' + n for n in ['redstone_dust_dot.png','redstone_dust_line0.png','redstone_dust_line1.png']}
        require(set(archive.namelist()) == expected, 'Cosmetic pack violates asset allowlist')
    tracked = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
    for name in tracked:
        path = ROOT / name
        if not path.is_file() or path.suffix in {'.jar','.png'}:
            continue
        data = path.read_text(encoding='utf-8', errors='replace')
        require(not re.search(r'[A-Za-z]:[\\/]Users[\\/]|/[h]ome/|/[U]sers/', data), 'Personal filesystem path in publication source: ' + name)
        require(not re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]+|Bearer [A-Za-z0-9_-]{15,}',data), 'Credential pattern in publication source')
    authors = subprocess.run(['git','log','--format=%an <%ae>'],cwd=ROOT,text=True,capture_output=True)
    if authors.returncode == 0:
        require(set(authors.stdout.splitlines()) <= {'TQNL <TQNL@users.noreply.github.com>'}, 'Unexpected commit identity')
    files = [jar, cosmetic]
    output = ROOT / 'outputs'
    (output / 'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files),encoding='utf-8')
    print(json.dumps({'artifact_audit':'PASS','glyphs':16,'cosmetic_members':6,'publication_files_scanned':len(tracked)}))

if __name__ == '__main__':
    main()
