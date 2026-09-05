import os
import json

def load():
    """
    Loads the HTTP status code guide dataset from 'data.jsonl'.

    The 'data.jsonl' file is expected to be in the same directory
    as this module. Each line in the file should be a valid JSON object.

    Returns:
        list: A list of dictionaries, where each dictionary represents
              an ambiguous API scenario and its recommended HTTP status code.
              Returns an empty list if the file is not found or malformed.
    """
    filepath = os.path.join(os.path.dirname(__file__), 'data.jsonl')
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
    except FileNotFoundError:
        print(f"Warning: Dataset file not found at '{filepath}'. Returning empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{filepath}': {e}. Returning partial data up to error.")
        return data # Return partial data if some lines were valid
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        return []
    return data
