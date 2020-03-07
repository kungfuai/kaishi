import pytest
import numpy as np
from kaishi.core.pipeline import Pipeline
from kaishi.core.pipeline_component import PipelineComponent


def test_init():
    pipeline = Pipeline()
    assert len(pipeline.components) == 0


def test_add_component():
    pipeline = Pipeline()
    pipeline.add_component(PipelineComponent())
    assert len(pipeline.components) == 1


def test_remove_component():
    pipeline = Pipeline()
    pipeline.add_component(PipelineComponent())
    pipeline.remove_component(0)
    assert len(pipeline.components) == 0


def test_str():
    pipeline = Pipeline()
    assert "Empty" in str(pipeline)
    pipeline.add_component(PipelineComponent())
    assert "PipelineComponent" in str(pipeline)


def test_reset():
    pipeline = Pipeline()
    pipeline.add_component(PipelineComponent())
    pipeline.reset()
    assert len(pipeline.components) == 0
