# HTTP Status Code Guide for Ambiguous API Scenarios

This dataset provides guidance on selecting appropriate HTTP status codes in common, yet ambiguous, API development situations. It helps developers make consistent and semantically correct choices, improving API predictability and client integration.

**25 rows** · category: `reference` · licence: CC0-1.0 (public domain)

## Usage

```python
import http_status_guide # Assuming the module is saved as http_status_guide.py

scenarios = http_status_guide.load()

if scenarios:
    print(f"Loaded {len(scenarios)} HTTP status code scenarios.")
    print("\nFirst scenario example:")
    print(f"  Input: {scenarios[0]['input']}")
    print(f"  Label: {scenarios[0]['label']}")
    print(f"  Note: {scenarios[0]['note']}")
else:
    print("No scenarios loaded. Check if 'data.jsonl' exists and is correctly formatted.")

```

## Sample rows

```json
{"input": "Request for /users/123/posts/456 where user 123 doesn't exist.", "label": "404 Not Found", "note": "The specific resource (post 456) cannot be found because its parent (user 123) does not exist, making the entire path invalid."}
{"input": "Request body is malformed JSON (syntax error).", "label": "400 Bad Request", "note": "The server cannot parse the request payload due to incorrect syntax."}
{"input": "Attempting to access a protected resource without providing any authentication credentials.", "label": "401 Unauthorized", "note": "The request lacks valid authentication credentials for the target resource."}
```

## Files

| File | What |
|---|---|
| `data.jsonl` | the dataset, one JSON object per line |
| `tool.py` | stdlib-only loader and helpers |
| `test_tool.py` | tests that pass against the data |

Also on Hugging Face: https://huggingface.co/datasets/SharkSkin/http-status-ambiguity-guide

Source: https://github.com/simalidudu-boop/http-status-ambiguity-guide

## Support

This is free and public domain. If it saved you time, zap it: `SharkSkin@coinos.io`

---
*Generated and maintained by an autonomous pipeline. Issues and PRs welcome.*
