from filecmp import cmp
from pathlib import Path
from shutil import rmtree
from unittest import TestCase

from data_loader_plugin.copyfile import DataLoader


class TestExternalDataLoad(TestCase):
    def test_files_are_copied(self):
        external_dir = Path(__file__).parent / "external_dir"
        local_dir = Path(__file__).parent / "local_dir"
        external_dir.mkdir(exist_ok=True)
        local_dir.mkdir(exist_ok=True)
        external_file = external_dir / "external_file.txt"
        local_file = local_dir / "local_file.txt"
        with open(external_file, "w") as f:
            f.write("some data")
        loader = DataLoader(local_path=local_file, external_url=external_file)
        with self.assertLogs(level="INFO") as cm:
            success, message = loader.load()

        self.assertTrue(success)
        self.assertTrue(cmp(external_file, local_file))
        self.assertIn(external_file.as_posix(), message)
        self.assertIn(external_file.as_posix(), "".join(cm.output))
        self.assertIn(local_file.as_posix(), message)
        self.assertIn(local_file.as_posix(), "".join(cm.output))

        rmtree(external_dir)
        rmtree(local_dir)

