from queue import Queue

import pytest
from py_cui import PyCUI

import recoverpy


@pytest.fixture()
def PARAMETERS_SCREEN():
    screen = recoverpy.screens.screen_parameters.ParametersScreen.__new__(
        recoverpy.screens.screen_parameters.ParametersScreen
    )
    screen.master = PyCUI(10, 10)

    partitions = [
        ["sda", "disk"],
        ["sda1", "part", "ext4", "/media/disk1"],
        ["sdb", "disk"],
        ["sdb1", "part", "ext4", "/media/disk2"],
        ["mmcblk0", "disk"],
        ["mmcblk0p1", "part", "vfat", "/boot/firmware"],
        ["mmcblk0p2", "part", "ext4", "/"],
        ["system-root", "lvm", "btrfs", "/test"],
        ["vdb", "disk", "LVM2_member"],
        ["vda2", "part", "LVM2_member"],
    ]
    screen.partitions_list = partitions

    return screen


@pytest.fixture()
def SEARCH_SCREEN():
    screen = recoverpy.screens.screen_search.SearchScreen.__new__(
        recoverpy.screens.screen_search.SearchScreen
    )
    screen.master = PyCUI(10, 10)
    screen.queue_object = Queue()
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod"
    screen.queue_object.put(f"- 1000: {lorem}")
    screen.queue_object.put(f"- 2000: {lorem}")
    screen.queue_object.put(f"- 3000: {lorem}")
    screen.blockindex = 0
    screen.grep_progress = ""
    screen.block_size = 512
    screen.searched_string = "test"
    screen.inodes = [512, 1024, 2056]

    return screen


@pytest.fixture()
def RESULTS_SCREEN():
    screen = recoverpy.screens.screen_results.BlockScreen.__new__(
        recoverpy.screens.screen_results.BlockScreen
    )
    screen.master = PyCUI(10, 10)
    screen.partition = "/dev/sda1"
    screen.saved_blocks_dict = {}
    screen.current_block = 5

    return screen


@pytest.fixture()
def CONFIG_SCREEN():
    screen = recoverpy.screens.screen_config.ConfigScreen.__new__(
        recoverpy.screens.screen_config.ConfigScreen
    )
    screen.master = PyCUI(10, 10)
    screen._log_enabled = True

    return screen


@pytest.fixture(scope="session")
def TEST_FILE(tmp_path_factory):
    lorem = "Integer vitae ultrices magna. Nam non cursus odio. In dapibus augue.\n"
    file = tmp_path_factory.mktemp("data") / "file"
    with file.open("w", encoding="utf-8") as f:
        f.write(lorem * 20000 + "TEST STRING" + lorem * 20000)

    return file


@pytest.fixture(scope="session")
def TEST_SEARCH_SCREEN(TEST_FILE):
    return recoverpy.screens.screen_search.SearchScreen(
        master=PyCUI(10, 10),
        partition=TEST_FILE,
        string_to_search="TEST STRING",
    )
