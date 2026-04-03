import types


def json_to_namespace(data):
    """Convert dict/list to SimpleNamespace for dot-access."""
    if isinstance(data, dict):
        return types.SimpleNamespace(**{k: json_to_namespace(v) for k, v in data.items()})
    if isinstance(data, list):
        return [json_to_namespace(item) for item in data]
    return data


def namespace_to_dict(obj):
    """Convert SimpleNamespace back to dict (for httpx calls)."""
    if isinstance(obj, types.SimpleNamespace):
        return {k: namespace_to_dict(v) for k, v in vars(obj).items()}
    if isinstance(obj, list):
        return [namespace_to_dict(item) for item in obj]
    return obj
