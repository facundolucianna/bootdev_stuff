import os
import shutil
from pathlib import Path


def clean_dir(path: Path) -> None:
    if not path.exists():
        return None
    shutil.rmtree(path) 
    return None


def copy_dir(src: Path, dst: Path) -> None:
    if not dst.exists():
        dst.mkdir()
    for file in os.listdir(src):
        if (src / file).is_file():
            shutil.copy(src / file, dst / file)
        else:
            (dst / file).mkdir()
            copy_dir(src / file, dst / file)
    return None


def clean_and_copy(src: Path, dst: Path) -> None:
    clean_dir(dst)
    copy_dir(src, dst)
    return None