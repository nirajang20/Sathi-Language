#!/usr/bin/env python3
import sys, re

variables = {}

def eval_expr(expr):
    try:
        return eval(expr, {}, variables)
    except Exception:
        return expr.strip('"')

def run_sathi(code):
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or not line.startswith("sathi"):
            i += 1
            continue

        if "bhanna" in line:
            msg = line.split("bhanna", 1)[1].strip()
            print(eval_expr(msg))
        elif "yo ho" in line:
            match = re.match(r"sathi yo ho (\w+)\s*=\s*(.+)", line)
            if match:
                var, val = match.groups()
                variables[var] = eval_expr(val)
        i += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sathi <file.sathi>")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()
    run_sathi(code)
