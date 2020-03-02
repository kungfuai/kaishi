import pytest
import numpy as np
from kaishi.image.file_group import ImageFileGroup
from kaishi.core.pipeline_component import PipelineComponent


def test_init():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    assert pc.target_criteria[0] == ".*"


@pytest.mark.filterwarnings("ignore:No options to configure")
def test_configure():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    pc.configure()
    assert pc.target_criteria[0] == ".*"


def test_applies_to_when_not_list():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    pc.applies_to_available = True
    pc.applies_to(0)
    assert len(pc.target_criteria) == 1 and pc.target_criteria[0] == 0


def test_applies_to_when_list():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    pc.applies_to_available = True
    pc.applies_to([0])
    assert len(pc.target_criteria) == 1 and pc.target_criteria[0] == 0


def test_get_target_indexes_when_int():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    pc.applies_to_available = True
    pc.applies_to([0])
    targets = pc.get_target_indexes()
    assert len(targets) == 1 and targets[0] == 0


def test_get_target_indexes_when_regex():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    pc.applies_to_available = True
    pc.applies_to(["real_near.*"])
    assert len(pc.get_target_indexes()) == 2


def test_is_valid_target_int():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    assert pc._is_valid_target_int(0) == True
    assert pc._is_valid_target_int(np.int8(0)) == True
    assert pc._is_valid_target_int(np.int16(0)) == True
    assert pc._is_valid_target_int(np.int32(0)) == True
    assert pc._is_valid_target_int(np.int64(0)) == True
    assert pc._is_valid_target_int(str(0)) == False


def test_is_valid_target_int():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent(test)
    assert pc._is_valid_target_str(0) == False
    assert pc._is_valid_target_str(np.int8(0)) == False
    assert pc._is_valid_target_str(np.int16(0)) == False
    assert pc._is_valid_target_str(np.int32(0)) == False
    assert pc._is_valid_target_str(np.int64(0)) == False
    assert pc._is_valid_target_str(str(0)) == True
