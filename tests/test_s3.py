from filecmp import cmp
from pathlib import Path
from shutil import rmtree
from unittest import TestCase

import boto3
from boto3 import resource
from data_loader_plugin.s3 import DataLoader
from moto import mock_s3


class TestExternalDataLoad(TestCase):
    def setUp(self) -> None:
        self.dir_name = "external_dir"
        self.file_name = "external_file.txt"
        self.external_dir = Path(__file__).parent / self.dir_name
        self.local_dir = Path(__file__).parent / "local_dir"
        self.external_file = self.external_dir / self.file_name
        self.local_file = self.local_dir / self.file_name
        self.external_dir.mkdir(exist_ok=True)
        self.local_dir.mkdir(exist_ok=True)
        with open(self.external_file, "w") as f:
            f.write("some data")

    @staticmethod
    def _create_s3_bucket() -> str:
        conn = resource("s3", region_name="us-east-1")
        bucket = "mybucket"
        conn.create_bucket(Bucket=bucket)
        return bucket

    @mock_s3
    def test_files_are_copied(self):
        bucket = self._create_s3_bucket()

        s3 = boto3.client("s3")
        s3_file_path = f"{self.dir_name}/{self.file_name}"
        s3.upload_file(self.external_file.as_posix(), bucket, s3_file_path)
        s3_url = f"s3://{bucket}/{s3_file_path}"

        loader = DataLoader(local_path=self.local_file, external_url=s3_url)
        with self.assertLogs(level="INFO") as cm:
            success, message = loader.load()

        self.assertTrue(success)
        self.assertTrue(cmp(self.external_file, self.local_file))
        self.assertIn(s3_url, message)
        self.assertIn(s3_url, "".join(cm.output))
        self.assertIn(self.local_file.as_posix(), message)
        self.assertIn(self.local_file.as_posix(), "".join(cm.output))

        rmtree(self.external_dir)
        rmtree(self.local_dir)

    @mock_s3
    def test_download_fails(self):
        bucket = self._create_s3_bucket()

        s3_file_path = f"{self.dir_name}/{self.file_name}.txt"
        s3_url = f"s3://{bucket}/{s3_file_path}"

        loader = DataLoader(local_path=self.local_file, external_url=s3_url)
        with self.assertLogs(level="INFO") as cm:
            success, message = loader.load()

        self.assertFalse(success)
        self.assertFalse(self.local_file.is_file())
        self.assertIn(s3_url, message)
        self.assertIn(s3_url, "".join(cm.output))
        self.assertIn(self.local_file.as_posix(), message)
        self.assertIn(self.local_file.as_posix(), "".join(cm.output))

        rmtree(self.external_dir)
        rmtree(self.local_dir)

