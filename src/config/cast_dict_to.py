from typing import Any, Dict, Union, get_type_hints


def cast_dict_to(d: Dict, cls: Any):
    kwargs = {}
    for name, t in get_type_hints(cls).items():
        v = d.get(name)
        cast_val = cast_to(v, t)
        kwargs[name] = cast_val
    return cls(**kwargs)


def cast_to(v: Any, t: Any):
    if hasattr(t, "from_dict") and isinstance(v, dict):
        return cast_dict_to(v, t)
    try:
        if isinstance(v, t):
            return v
    except TypeError:
        pass

    v_type = type(v)
    origin = getattr(t, "__origin__", None)

    if origin == Union:
        args = t.__args__
        if v_type in args:
            return v
        for subtype in args:
            try:
                return cast_to(v, subtype)
            except TypeError:
                pass

    raise TypeError(f"{v} has wrong type {type(v)} instead of {t}")
