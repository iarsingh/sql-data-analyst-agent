TOOLS = ["profile_table", "aggregate"]
WRITES = ("delete", "drop", "update", "insert",)


class InputError(ValueError):
    pass


def run(goal, payload):
    if not isinstance(goal, str) or not goal.strip():
        raise InputError("goal is empty")
    if any(word in goal.lower() for word in WRITES):
        return {"refused": True, "reason": "This agent only reads or plans. It does not write.", "tools": [], "wrote": False, "applied": False}
    rows = payload.get("rows") or []; totals = {};
    for row in rows:
        totals[row.get("region", "unknown")] = totals.get(row.get("region", "unknown"), 0) + float(row.get("revenue", 0))
    result = totals
    return {"refused": False, "tools": TOOLS, "totals": result, "wrote": False, "applied": False}
