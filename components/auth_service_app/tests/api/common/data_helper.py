from pathlib import Path

from tests.api.common.file_helper import json_to_namespace
from tests.api.common.file_parser import JsonParser


def load_json_data(base_dir, file_name):
    """Load JSON test data and convert to SimpleNamespace for dot-access."""
    data_file_path = Path(base_dir) / "data" / file_name

    if not data_file_path.exists():
        raise FileNotFoundError(f"Test data file not found: {data_file_path}")

    parsed = JsonParser(str(data_file_path.resolve())).read()
    return json_to_namespace(parsed)


def get_test_cases_from_section(json_data, section):
    """Extract test cases list from a named section."""
    if not hasattr(json_data, section):
        raise KeyError(f"Section '{section}' not found in test data.")
    return getattr(json_data, section)
