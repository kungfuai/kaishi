"""
Usage:
    In the project root directory,
    `python -m examples.tabular_example`
"""
from kaishi.tabular import TabularDataInspector


if __name__ == "__main__":
    ins = TabularDataInspector("sample_data/simple_csv")
    ins.run_pipeline()
