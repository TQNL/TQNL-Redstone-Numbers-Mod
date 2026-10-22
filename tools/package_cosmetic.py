"""Package the committed dust artwork; Python's standard library is sufficient."""
from pathlib import Path
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TEXTURE_NAMES = ('redstone_dust_dot.png', 'redstone_dust_line0.png', 'redstone_dust_line1.png')


def build():
    output = ROOT / 'outputs'
    output.mkdir(exist_ok=True)
    cosmetic = output / 'TQNL-Redstone-Dust-Cosmetic-mc1.21.11.zip'
    members = {
        'pack.mcmeta': json.dumps({'pack': {'min_format': [75, 0], 'max_format': [75, 0],
            'description': 'Optional redstone dust textures only. No numbers or shaders.'}}, indent=2).encode(),
        'credits.txt': (ROOT / 'credits.txt').read_bytes(),
        'pack.png': (ROOT / 'src/main/resources/assets/redstonenumbers/icon.png').read_bytes(),
        'ASSET-LICENSES.md': (ROOT / 'ASSET-LICENSES.md').read_bytes(),
    }
    for name in TEXTURE_NAMES:
        members['assets/minecraft/textures/block/' + name] = (ROOT / 'cosmetic/textures' / name).read_bytes()
    with zipfile.ZipFile(cosmetic, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(members.items()):
            item = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(item, data)
    return cosmetic


if __name__ == '__main__':
    print('Built ' + build().name)
