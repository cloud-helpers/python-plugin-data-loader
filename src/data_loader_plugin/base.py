#
# File: https://github.com/cloud-helpers/python-plugin-data-loader/blob/main/data_loader_plugin/base.py
# Authors: Stanislav Khrapov, Denis Arnaud
#

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple

class DataLoaderBase(ABC):
    def __init__(self, local_path: Path, external_url: str,
                 recursive: bool=False) -> None:
        self._local_path = local_path
        self._external_url = external_url
        self._recursive = recursive
        self._logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> Tuple[bool, str]:
        is_success = False
        
        try:
            message = "Will try to create the destination directory on the " \
                f"local file-system: {self._local_path}..."
            self._logger.info(message)

            self._local_path.parent.mkdir(exist_ok=True)
            f"Will try loading data from {self._external_url} to {self._local_path}..."
            self._logger.info(message)

            self._load()
            message = "Done. The data has been downloaded from " \
                f"{self._external_url} to {self._local_path}."
            self._logger.info(message)
            is_success = True
        
        except Exception as error:
            message = f"Failed to download data from {self._external_url} " \
                f"to {self._local_path} with {error.__class__} ({error})."
            self._logger.info(message)
            is_success = False

        return is_success, message

    @abstractmethod
    def _load(self) -> None:
        pass
