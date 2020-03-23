"""
Usage:
    In the project root directory,
    `python -m examples.tabular_example`
"""
from kaishi.tabular import TabularDataset


if __name__ == "__main__":
    tds = TabularDataset(
        "tests/data/tabular", use_predefined_pipeline=True, out_dir="tmp"
    )
    tds.run_pipeline(verbose=True)
    tds.report()
