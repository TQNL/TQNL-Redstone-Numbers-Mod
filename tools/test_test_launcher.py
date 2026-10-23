"""Local integration checks; uses prepared QA caches, never normal saves."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_launcher as launcher


@unittest.skipUnless((launcher.CAMPAIGN / "clients/1.21.11/minimal/profile.json").is_file(), "Prepared local QA caches required")
class PickerChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = launcher.Catalog("1.21.11")

    def test_prepared_presets_and_nested_library_selection(self):
        count = 0
        for game in launcher.GAMES:
            catalog = self.catalog if game == "1.21.11" else launcher.Catalog(game)
            for name, selected in catalog.presets.items():
                with self.subTest(game=game, preset=name):
                    self.assertEqual(catalog.resolve(selected), selected)
                count += 1
        self.assertEqual(count, 41)  # 40 published cases + installed-mod selection.

    def test_voxy_auto_dependencies_and_renderer_conflicts(self):
        c = self.catalog
        voxy = next(k for k in c.presets["Voxy"] if c.mods[k].primary["id"] == "voxy")
        selected = c.resolve({voxy})
        self.assertIn("0.8.12+mc1.21.11", c.provided(selected)["sodium"])
        with self.assertRaisesRegex(ValueError, "conflicts"):
            c.resolve(c.presets["VulkanMod"] | c.presets["Sodium + native settings"])
        with self.assertRaisesRegex(ValueError, "only one version"):
            c.resolve(c.presets["Voxy"] | c.presets["Sodium + native settings"])

    def test_instance_boundary_reuse_and_modified_jar_preservation(self):
        c = self.catalog
        with tempfile.TemporaryDirectory(prefix="picker-check-", dir=launcher.CAMPAIGN) as folder:
            with patch.object(launcher, "STORE", Path(folder)):
                for name in ("../outside", "CON", "a/b", "C:\\mods"):
                    with self.assertRaises(ValueError):
                        launcher.instance_path(c.game, name, c.core, None)
                client, selected = launcher.prepare(c, "smoke", c.core)
                self.assertTrue((client / "saves" / launcher.WORLD / "level.dat").is_file())
                self.assertFalse((client / "saves" / launcher.WORLD / "region").exists())
                sentinel = client / "saves" / "keep-my-save.txt"
                sentinel.write_text("keep")
                self.assertEqual(launcher.prepare(c, "smoke", selected)[0], client)
                self.assertEqual(sentinel.read_text(), "keep")
                jar = next((client / "mods").glob("*.jar"))
                jar.write_bytes(b"local edit")
                with self.assertRaisesRegex(ValueError, "edited outside"):
                    launcher.prepare(c, "smoke", selected)
                self.assertEqual(jar.read_bytes(), b"local edit")


if __name__ == "__main__":
    unittest.main()
