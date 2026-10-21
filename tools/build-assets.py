"""Repack selected legacy artwork; never copy shader/model/compilation files."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image
from package_cosmetic import build as build_cosmetic, TEXTURE_NAMES

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
    cosmetic_source = ROOT / 'cosmetic/textures'
    cosmetic_source.mkdir(parents=True, exist_ok=True)
    for name in TEXTURE_NAMES:
        (cosmetic_source / name).write_bytes((src / name).read_bytes())
    build_cosmetic()
    print('Built 16-glyph private font and six-member optional cosmetic pack.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=ROOT.parent / 'TQNL-Redstone-Numbers')
    build(parser.parse_args().source)
