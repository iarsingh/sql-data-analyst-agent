import re
from decimal import Decimal, InvalidOperation

TOOLS = ["profile_table", "aggregate"]
WRITES = ("delete", "drop", "update", "insert")
MAX_ROWS = 10000


class InputError(ValueError):
    pass


def run(goal, payload):
    if not isinstance(goal, str) or not goal.strip() or len(goal) > 2000:
        raise InputError("goal must contain 1 to 2000 characters")
    if set(re.findall(r"[a-z]+", goal.lower())) & set(WRITES):
        return {"refused": True, "reason": "This agent only reads or plans. It does not write.", "tools": [], "wrote": False, "applied": False}
    if not isinstance(payload, dict):
        raise InputError("payload must be an object")
    rows = payload.get("rows", [])
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise InputError(f"rows must be a list with at most {MAX_ROWS} entries")
    totals, counts = {}, {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise InputError(f"row {index} must be an object")
        region = row.get("region", "unknown")
        if not isinstance(region, str) or not region.strip() or len(region) > 100:
            raise InputError(f"row {index} has an invalid region")
        region = region.strip()
        raw = row.get("revenue", 0)
        try:
            if isinstance(raw, bool):
                raise InvalidOperation
            if len(str(raw)) > 100:
                raise InvalidOperation
            value = Decimal(str(raw))
            if not value.is_finite() or value.copy_abs() > Decimal("1e12") or value.as_tuple().exponent < -6:
                raise InvalidOperation
        except (InvalidOperation, ValueError, TypeError):
            raise InputError(f"row {index} revenue must be finite with at most six decimal places") from None
        totals[region] = totals.get(region, Decimal(0)) + value
        counts[region] = counts.get(region, 0) + 1
    ordered = dict(sorted(totals.items()))
    return {"refused": False, "tools": TOOLS, "totals": {k: float(v) for k, v in ordered.items()},
            "totals_decimal": {k: str(v) for k, v in ordered.items()}, "row_count": len(rows),
            "region_counts": dict(sorted(counts.items())), "wrote": False, "applied": False}
