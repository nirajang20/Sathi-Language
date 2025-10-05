#!/usr/bin/env python3
import sys, re

# Global context
variables = {}
functions = {}

def eval_expr(expr):
    """Evaluate expression within current variable scope."""
    try:
        return eval(expr, {}, variables)
    except Exception:
        return expr.strip('"')

def run_sathi(lines, start=0, end=None):
    """Execute Sathi code between start and end line numbers."""
    i = start
    while i < (end if end is not None else len(lines)):
        line = lines[i].strip()

        # Skip blank or comment lines
        if not line or line.startswith("#"):
            i += 1
            continue

        # -----------------------------
        # PRINT - sathi bhana "Hello"
        # -----------------------------
        if line.startswith("sathi bhana"):
            msg = line.split("bhana", 1)[1].strip()
            print(eval_expr(msg))

        # -----------------------------
        # VARIABLE - sathi yo ho x = 5
        # -----------------------------
        elif "yo ho" in line:
            match = re.match(r"sathi yo ho (\w+)\s*=\s*(.+)", line)
            if match:
                var, val = match.groups()
                variables[var] = eval_expr(val)

        # -----------------------------
        # IF CONDITION - sathi bhane x > 5
        # -----------------------------
        elif line.startswith("sathi bhane"):
            cond = line.split("bhane", 1)[1].strip()
            condition_result = bool(eval_expr(cond))

            # Find where this if-block ends
            block_start = i + 1
            block_end = find_block_end(lines, i + 1)
            else_index = find_keyword(lines, "sathi natra", block_start, block_end)

            if condition_result:
                run_sathi(lines, block_start, else_index or block_end)
            elif else_index:
                run_sathi(lines, else_index + 1, block_end)
            i = block_end  # skip to end of block

        # -----------------------------
        # LOOP - sathi dohorau 5 choti
        # -----------------------------
        elif line.startswith("sathi dohorau"):
            match = re.match(r"sathi dohorau (\d+) choti", line)
            if match:
                times = int(match.group(1))
                block_start = i + 1
                block_end = find_block_end(lines, i + 1)
                for _ in range(times):
                    run_sathi(lines, block_start, block_end)
                i = block_end  # skip block

        # -----------------------------
        # FUNCTION DEFINE - sathi kam gar greet(name)
        # -----------------------------
        elif line.startswith("sathi kam gar"):
            match = re.match(r"sathi kam gar (\w+)\((.*?)\)", line)
            if match:
                func_name, params = match.groups()
                params = [p.strip() for p in params.split(",") if p.strip()]
                block_start = i + 1
                block_end = find_block_end(lines, i + 1)
                functions[func_name] = {"params": params, "body": lines[block_start:block_end]}
                i = block_end

        # -----------------------------
        # FUNCTION CALL - sathi gara greet("Ram")
        # -----------------------------
        elif line.startswith("sathi gara"):
            match = re.match(r"sathi gara (\w+)\((.*?)\)", line)
            if match:
                func_name, args_str = match.groups()
                args = [eval_expr(a.strip()) for a in args_str.split(",") if a.strip()]
                if func_name in functions:
                    func = functions[func_name]
                    local_vars = dict(zip(func["params"], args))
                    prev_vars = variables.copy()
                    variables.update(local_vars)
                    run_sathi(func["body"])
                    variables.clear()
                    variables.update(prev_vars)
                else:
                    print(f"Sathi Error: Function '{func_name}' not defined")

        i += 1


# -----------------------------
# HELPERS
# -----------------------------
def find_block_end(lines, start):
    """Find where a sathi block ends (sakyo)."""
    for i in range(start, len(lines)):
        if lines[i].strip() == "sathi sakyo":
            return i
    return len(lines)

def find_keyword(lines, keyword, start, end):
    """Find a specific keyword inside a block."""
    for i in range(start, end):
        if lines[i].strip().startswith(keyword):
            return i
    return None

# -----------------------------
# MAIN ENTRY
# -----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: sathi <file.sathi>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        run_sathi(lines)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print("Sathi Error:", e)


if __name__ == "__main__":
    main()
