import _winapi
from pathlib import Path
from typing import Union


def make_link(target_path: Union[str, Path], link_path: Union[str, Path], is_hard: bool = False):
    target_path = Path(target_path).absolute()
    link_path = Path(link_path).absolute()
    try:
        if not is_hard:
            link_path.symlink_to(target_path)
        else:
            if target_path.is_file():
                link_path.hardlink_to(target_path)
            elif target_path.is_dir():
                _winapi.CreateJunction(str(target_path), str(link_path))
    except FileExistsError:
        raise FileExistsError(f"Невозможно создать файл, так как он уже существует: '{target_path}' -> '{link_path}'")
    except FileNotFoundError:
        raise FileNotFoundError(f"Системе не удается найти указанный путь: '{target_path}' -> '{link_path}'")
