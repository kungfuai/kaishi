import pytest
import numpy as np
from kaishi.image.file_group import ImageFileGroup
from kaishi.core.pipeline import Pipeline
from kaishi.core.pipeline_component import PipelineComponent


def test_init():
    pipeline = Pipeline()
    assert len(pipeline.components) == 0


def test_add_component():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pipeline = Pipeline()
    pipeline.add_component(PipelineComponent(test))
    assert len(pipeline.components) == 1


def test_remove_component():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pipeline = Pipeline()
    pipeline.add_component(PipelineComponent(test))
    pipeline.remove_component(0)
    assert len(pipeline.components) == 0


def test_str():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pipeline = Pipeline()
    assert "Empty" in str(pipeline)
    pipeline.add_component(PipelineComponent(test))
    assert "PipelineComponent" in str(pipeline)


def test_reset():
    test = ImageFileGroup("tests/data/image", recursive=True)
    pipeline = Pipeline()
    pipeline.add_component(PipelineComponent(test))
    pipeline.reset()
    assert len(pipeline.components) == 0
