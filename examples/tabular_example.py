"""
Usage:
    In the project root directory,
    `python -m examples.tabular_example`
"""
from kaishi.tabular import TabularDataInspector


if __name__ == "__main__":
    ins = TabularDataInspector("sample_data/simple_csv", use_predefined_pipeline=True)
    ins.run_pipeline(verbose=True)
