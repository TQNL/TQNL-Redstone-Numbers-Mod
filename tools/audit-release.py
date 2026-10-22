"""Reject unrelated assets, shaders, unsafe publication paths and identity leaks."""
from pathlib import Path
import hashlib
import io
import json
import re
import subprocess
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PERSONAL_PATH = re.compile(rb'[A-Za-z]:[\\/]+Users[\\/]+|/(?:home|Users)/', re.IGNORECASE)
CREDENTIAL = re.compile(rb'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]+|Bearer [A-Za-z0-9_-]{15,}|sk-[A-Za-z0-9_-]{20,}')
PUBLIC_IDENTITY = 'TQNL <TQNL@users.noreply.github.com>'

def require(condition, message):
    if not condition:
        raise SystemExit(message)

def audit_privacy(data, label):
    # Class-file strings are UTF-8. Removing NULs also catches ASCII paths and
    # credentials encoded as UTF-16/32, without printing any matched value.
    for candidate in (data, data.replace(b'\0', b'')):
        require(not PERSONAL_PATH.search(candidate), 'Personal filesystem path in publication content: ' + label)
        require(not CREDENTIAL.search(candidate), 'Credential pattern in publication content: ' + label)

def audit_png(data, label):
    with Image.open(io.BytesIO(data)) as image:
        # Numeric colour/encoding information is useful artwork data. Reject
        # comments, EXIF, timestamps, profiles and other descriptive metadata.
        technical_keys = {'srgb', 'gamma', 'dpi', 'interlace', 'transparency'}
        require(set(image.info) <= technical_keys, 'Remove descriptive PNG metadata before publication: ' + label)

def audit_archive(path):
    members = 0
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.endswith('/'):
                continue
            label = path.name + '!' + name
            data = archive.read(name)
            audit_privacy(name.encode('utf-8') + b'\n' + data, label)
            if name.lower().endswith(('.json', '.mcmeta', '.md', '.txt', '.java')):
                require(b'shader' not in data.lower(), 'Obsolete wording in packaged text: ' + label)
            if name.lower().endswith('.png'):
                audit_png(data, label)
            members += 1
    return members

def main():
    jar = ROOT / 'build/libs/redstone-numbers-0.1.3+mc1.21.11.jar'
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
        prefix = 'resourcepacks/clean_lines/'
        expected_builtin = {'pack.mcmeta', 'pack.png', 'credits.txt', 'ASSET-LICENSES.md'} | {
            'assets/minecraft/textures/block/' + n for n in
            ['redstone_dust_dot.png', 'redstone_dust_line0.png', 'redstone_dust_line1.png']}
        require({n[len(prefix):] for n in names if n.startswith(prefix) and not n.endswith('/')} == expected_builtin,
                'Built-in pack violates asset allowlist')
        icon = (ROOT / 'src/main/resources/assets/redstonenumbers/icon.png').read_bytes()
        require(archive.read(meta['icon']) == icon, 'Mod icon differs from branding')
        require(archive.read(prefix + 'pack.png') == icon, 'Built-in pack icon differs from branding')
        for name in ['redstone_dust_dot.png', 'redstone_dust_line0.png', 'redstone_dust_line1.png']:
            require(archive.read(prefix + 'assets/minecraft/textures/block/' + name)
                    == (ROOT / 'cosmetic/textures' / name).read_bytes(), 'Built-in dust differs from source')
    font = json.loads((ROOT / 'src/main/resources/assets/redstonenumbers/font/numbers.json').read_text())
    require(''.join(font['providers'][0]['chars']) == ''.join(chr(0xE000 + n) for n in range(16)), 'Wrong glyph mapping')
    image = Image.open(ROOT / 'src/main/resources/assets/redstonenumbers/textures/font/numbers.png').convert('RGBA')
    for n in range(16):
        cell = image.crop((n % 4 * 16, n // 4 * 16, n % 4 * 16 + 16, n // 4 * 16 + 16))
        require(cell.getchannel('A').getbbox() is not None, 'Blank number artwork')
    cosmetic = ROOT / 'outputs/TQNL-Redstone-Dust-Cosmetic-mc1.21.11.zip'
    with zipfile.ZipFile(cosmetic) as archive:
        expected = {'pack.mcmeta', 'pack.png', 'credits.txt', 'ASSET-LICENSES.md'} | {
            'assets/minecraft/textures/block/' + n for n in ['redstone_dust_dot.png','redstone_dust_line0.png','redstone_dust_line1.png']}
        require(set(archive.namelist()) == expected, 'Cosmetic pack violates asset allowlist')
        require(archive.read('pack.png') == (ROOT / 'src/main/resources/assets/redstonenumbers/icon.png').read_bytes(),
                'Cosmetic pack icon differs from branding')
    tracked = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
    for name in tracked:
        path = ROOT / name
        if not path.is_file() or name == 'gradle/wrapper/gradle-wrapper.jar':
            continue
        data = path.read_bytes()
        audit_privacy(data, name)
        if path.suffix.lower() == '.png':
            audit_png(data, name)
        elif path.suffix.lower() in {'.jar', '.zip'}:
            audit_archive(path)
    sources = jar.with_name(jar.stem + '-sources.jar')
    require(sources.is_file(), 'Build the sources JAR before the final audit.')
    archive_members = sum(audit_archive(path) for path in (jar, sources, cosmetic))
    identities = subprocess.run(['git','log','--format=%an <%ae>%n%cn <%ce>'],cwd=ROOT,text=True,capture_output=True)
    require(identities.returncode == 0, 'Cannot audit Git author and committer identities')
    require(set(identities.stdout.splitlines()) == {PUBLIC_IDENTITY}, 'Unexpected Git author or committer identity')
    files = [jar, cosmetic]
    output = ROOT / 'outputs'
    (output / 'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files),encoding='utf-8')
    print(json.dumps({'artifact_audit':'PASS','glyphs':16,'cosmetic_members':7,'builtin_pack_members':7,
        'publication_files_scanned':len(tracked),'decompressed_artifact_members_scanned':archive_members,
        'git_author_and_committer':'PASS','png_metadata':'PASS'}))

if __name__ == '__main__':
    main()
