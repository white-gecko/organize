import os

import pytest
from mock import patch

from organize.utils import Path


def create_filesystem(tmp_path, files, config):
    # create files
    for f in files:
        p = tmp_path / "files" / Path(f)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
    # create config
    with (tmp_path / "config.yaml").open("w") as f:
        f.write(config)
    # change working directory
    os.chdir(str(tmp_path))


def assertdir(path, *files):
    os.chdir(str(path / "files"))
    assert set(files) == set(str(x) for x in Path(".").glob("**/*") if x.is_file())


@pytest.fixture
def mock_exists():
    with patch.object(Path, "exists") as mck:
        yield mck


@pytest.fixture
def mock_samefile():
    with patch.object(Path, "samefile") as mck:
        yield mck


@pytest.fixture
def mock_rename():
    with patch.object(Path, "rename") as mck:
        yield mck


@pytest.fixture
def mock_move():
    with patch("shutil.move") as mck:
        yield mck


@pytest.fixture
def mock_copy():
    with patch("shutil.copy2") as mck:
        yield mck


@pytest.fixture
def mock_remove():
    with patch("os.remove") as mck:
        yield mck


@pytest.fixture
def mock_trash():
    with patch("send2trash.send2trash") as mck:
        yield mck


@pytest.fixture
def mock_parent():
    with patch.object(Path, "parent") as mck:
        yield mck


@pytest.fixture
def mock_mkdir():
    with patch.object(Path, "mkdir") as mck:
        yield mck

