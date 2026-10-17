"""Run one checker on one candidate in an isolated interpreter.
Usage: python -I checker_runner.py <checker.py> <candidate.json>  → prints PASS or FAIL."""
import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location("checker", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
with open(sys.argv[2], encoding="utf-8") as f:
    candidate = json.load(f)
print("PASS" if mod.check(candidate) is True else "FAIL")
