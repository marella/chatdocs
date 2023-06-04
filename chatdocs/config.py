from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

from .utils import merge

FILENAME = "chatdocs.yml"


def _get_config(path: Union[Path, str]) -> Dict[str, Any]:
    path = Path(path)
    if path.is_dir():
        path = path / FILENAME
    with open(path) as f:
        return yaml.safe_load(f)


def get_config(path: Optional[Union[Path, str]] = None) -> Dict[str, Any]:
    default_config = _get_config(Path(__file__).parent / "data")
    if path is None:
        path = Path() / FILENAME
        if not path.is_file():
            return default_config
    config = _get_config(path)
    return merge(default_config, config)
