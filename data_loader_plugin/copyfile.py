from shutil import copyfile

from data_loader_plugin.base import DataLoaderBase


class DataLoader(DataLoaderBase):
    def _load(self) -> None:
        copyfile(src=self._external_url, dst=self._local_path)
