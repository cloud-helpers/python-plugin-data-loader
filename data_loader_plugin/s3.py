from urllib.parse import urlsplit

import boto3

from data_loader_plugin.base import DataLoaderBase


class DataLoader(DataLoaderBase):
    def _load(self) -> None:
        parsed_url = urlsplit(self._external_url)
        s3 = boto3.client("s3")
        s3.download_file(
            parsed_url.netloc, parsed_url.path[1:], self._local_path.as_posix()
        )
