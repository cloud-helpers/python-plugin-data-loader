import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple


class DataLoaderBase(ABC):
    def __init__(self, local_path: Path, external_url: str) -> None:
        self._local_path = local_path
        self._external_url = external_url
        self._logger = logging.getLogger(self.__class__.__name__)

    def load(self) -> Tuple[bool, str]:
        try:
            self._local_path.parent.mkdir(exist_ok=True)
            self._logger.info(
                f"Will try loading data from {self._external_url} to {self._local_path}."
            )
            self._load()
            message = (
                f"OK. Loaded data from {self._external_url} to {self._local_path}."
            )
            self._logger.info(message)
            return True, message
        except Exception as error:
            message = (
                f"Failed to load data from {self._external_url} to {self._local_path} "
                f"with {error.__class__}({error})."
            )
            self._logger.info(message)
            return False, message

    @abstractmethod
    def _load(self) -> None:
        pass
