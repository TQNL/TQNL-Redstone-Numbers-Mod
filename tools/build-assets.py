"""Repack selected legacy artwork; never copy shader/model/compilation files."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def build(source):
    src = source / 'src/baseline/core/assets/minecraft/textures/block'
    target = ROOT / 'src/main/resources/assets/redstonenumbers'
    (target / 'textures/font').mkdir(parents=True, exist_ok=True)
    (target / 'font').mkdir(parents=True, exist_ok=True)
    atlas = Image.new('RGBA', (64, 64))
    hashes = {}
    for power in range(16):
        name = f'redstone_power_level_{power:02d}.png'
        path = src / name
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        with Image.open(path) as original:
            w, h = original.size
            glyph = original.convert('RGBA').crop((0, 0, w // 4, h // 4))
            glyph = glyph.resize((16, 16), Image.Resampling.NEAREST)
            atlas.paste(glyph, ((power % 4) * 16, (power // 4) * 16))
    atlas.save(target / 'textures/font/numbers.png')
    font = {'providers': [{'type': 'bitmap', 'file': 'redstonenumbers:font/numbers.png',
             'height': 16, 'ascent': 16,
             'chars': [''.join(chr(0xE000 + row * 4 + col) for col in range(4)) for row in range(4)]}]}
    (target / 'font/numbers.json').write_text(json.dumps(font, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs/artwork-inputs.json').write_text(json.dumps({
        'source': 'TQNL/TQNL-Redstone-Numbers', 'revision': 'a29eab7c38270e8dddfb2b64a1f56fb8291bbc73',
        'transformation': 'top-left sampled quarter, nearest scale to 16px, 4x4 atlas',
        'glyph_inputs_sha256': hashes}, indent=2) + '\n', encoding='utf-8')
    output = ROOT / 'outputs'
    output.mkdir(exist_ok=True)
    cosmetic = output / 'TQNL-Redstone-Dust-Cosmetic-mc1.21.11.zip'
    members = {'pack.mcmeta': json.dumps({'pack': {'min_format': [75, 0], 'max_format': [75, 0],
                  'description': 'Optional redstone dust textures only. No numbers or shaders.'}}, indent=2).encode(),
               'credits.txt': (ROOT / 'credits.txt').read_bytes(),
               'ASSET-LICENSES.md': (ROOT / 'ASSET-LICENSES.md').read_bytes()}
    for name in ['redstone_dust_dot.png', 'redstone_dust_line0.png', 'redstone_dust_line1.png']:
        members['assets/minecraft/textures/block/' + name] = (src / name).read_bytes()
    with zipfile.ZipFile(cosmetic, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(members.items()):
            item = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(item, data)
    print('Built 16-glyph private font and six-member optional cosmetic pack.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=ROOT.parent / 'TQNL-Redstone-Numbers')
    build(parser.parse_args().source)
