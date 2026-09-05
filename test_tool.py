import pytest
import os
import json
from unittest.mock import patch

# Assuming the tool_code is in a file named `http_status_guide.py`
# and you are importing `load` from it.
# For direct testing, copy the `load` function into the test file or mock its path.

# Mock the `load` function here for testing as if it were in the module.
# In a real scenario, you'd import `from http_status_guide import load`
# For this response, we'll redefine a minimal `load` that can be patched.

def _mockable_load_func():
    filepath = os.path.join(os.path.dirname(__file__), 'data.jsonl')
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return data
    return data

@pytest.fixture
def mock_data_jsonl(tmp_path):
    # Create a dummy data.jsonl file in the temporary directory
    data = [
        {"input": "Request for non-existent user", "label": "404 Not Found", "note": "User does not exist"},
        {"input": "Malformed JSON body", "label": "400 Bad Request", "note": "Syntax error in JSON"}
    ]
    file_path = tmp_path / "data.jsonl"
    with open(file_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return file_path

def test_load_function_loads_data_correctly(mock_data_jsonl, monkeypatch):
    # Mock os.path.dirname(__file__) to point to the tmp_path
    monkeypatch.setattr(os.path, 'dirname', lambda x: str(mock_data_jsonl.parent))

    scenarios = _mockable_load_func()

    assert isinstance(scenarios, list)
    assert len(scenarios) == 2
    assert scenarios[0]["input"] == "Request for non-existent user"
    assert scenarios[1]["label"] == "400 Bad Request"
    assert all(k in scenarios[0] for k in ["input", "label", "note"])

def test_load_function_handles_file_not_found(tmp_path, monkeypatch, capsys):
    # Ensure data.jsonl does not exist in tmp_path
    monkeypatch.setattr(os.path, 'dirname', lambda x: str(tmp_path))

    scenarios = _mockable_load_func()

    assert scenarios == []
    captured = capsys.readouterr()
    assert "Warning: Dataset file not found" in captured.out

def test_load_function_handles_empty_file(tmp_path, monkeypatch):
    empty_file = tmp_path / "data.jsonl"
    empty_file.touch() # Create an empty file
    monkeypatch.setattr(os.path, 'dirname', lambda x: str(tmp_path))

    scenarios = _mockable_load_func()

    assert scenarios == []

def test_load_function_handles_malformed_json_line(tmp_path, monkeypatch, capsys):
    malformed_data = [
        {"input": "Valid entry", "label": "200 OK"},
        "{'input': 'Bad JSON', 'label': '400'"
    ]
    file_path = tmp_path / "data.jsonl"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(malformed_data[0]) + "\n")
        f.write(malformed_data[1] + "\n") # Write malformed line

    monkeypatch.setattr(os.path, 'dirname', lambda x: str(tmp_path))

    scenarios = _mockable_load_func()

    # Should load the first valid entry and stop or return partial
    assert len(scenarios) == 1
    assert scenarios[0]["input"] == "Valid entry"
    captured = capsys.readouterr()
    assert "Error decoding JSON" in captured.out
