import pytest
import numpy as np
from kaishi.image.file_group import ImageFileGroup
from kaishi.core.pipeline_component import PipelineComponent


def test_init():
    pc = PipelineComponent()
    assert pc.target_criteria[0] == ".*"


@pytest.mark.filterwarnings("ignore:No options to configure")
def test_configure():
    pc = PipelineComponent()
    pc.configure()
    assert pc.target_criteria[0] == ".*"


def test_applies_to_when_not_list():
    pc = PipelineComponent()
    pc.applies_to_available = True
    pc.applies_to(0)
    assert len(pc.target_criteria) == 1 and pc.target_criteria[0] == 0


def test_applies_to_when_list():
    pc = PipelineComponent()
    pc.applies_to_available = True
    pc.applies_to([0])
    assert len(pc.target_criteria) == 1 and pc.target_criteria[0] == 0


def test_get_target_indexes_when_int():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent()
    pc.applies_to_available = True
    pc.applies_to([0])
    targets = pc.get_target_indexes(test)
    assert len(targets) == 1 and targets[0] == 0


def test_get_target_indexes_when_regex():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pc = PipelineComponent()
    pc.applies_to_available = True
    pc.applies_to(["real_near.*"])
    assert len(pc.get_target_indexes(test)) == 2


def test_is_valid_target_int():
    pc = PipelineComponent()
    assert pc._is_valid_target_int(0)
    assert pc._is_valid_target_int(np.int8(0))
    assert pc._is_valid_target_int(np.int16(0))
    assert pc._is_valid_target_int(np.int32(0))
    assert pc._is_valid_target_int(np.int64(0))
    assert pc._is_valid_target_int(str(0)) is False


def test_is_valid_target_str():
    pc = PipelineComponent()
    assert pc._is_valid_target_str(0) is False
    assert pc._is_valid_target_str(np.int8(0)) is False
    assert pc._is_valid_target_str(np.int16(0)) is False
    assert pc._is_valid_target_str(np.int32(0)) is False
    assert pc._is_valid_target_str(np.int64(0)) is False
    assert pc._is_valid_target_str(str(0))
