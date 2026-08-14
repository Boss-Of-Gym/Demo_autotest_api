from typing import Any


def generate_test_ids(data: list[Any]) -> list[str]:
    """
    Generates readable parametrize IDs.
    Format: "{test_id} | {METHOD} | {endpoint} | {status_body}"
    """
    ids: list[str] = []
    for item in data:
        case = item.values[0] if hasattr(item, 'values') else item
        ids.append(
            f'{case.test_id} | {case.description} | {case.expected.status_body}'
        )
    return ids
