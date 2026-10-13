"""
where_am_i.py — the memory-loss recovery script.
Run every morning. Prints: current day, gate status, and the ONE next action.
Also verifies the IP fence (docs/07) by checking git-tracked files.
"""
import os, re, json, datetime, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

def read(p):
    with open(p) as f:
        return f.read()

def check_fence():
    """Fail loudly if Layer-3 (private) material is tracked by git."""
    blocked = [r"\.env", r"secrets/", r"passages_full", r"prompts/final/"]
    try:
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT,
                                 capture_output=True, text=True).stdout.splitlines()
    except Exception:
        return ["(git unavailable — run fence check manually)"]
    hits = [t for t in tracked if any(re.search(b, t) for b in blocked)]
    return hits

def gate_status():
    cp = read(os.path.join(DOCS, "CHECKPOINTS.md"))
    boxes = re.findall(r"- \[( |x)\] (CP-\d+\.\d+)", cp)
    done = [c for m, c in boxes if m == "x"]
    todo = [c for m, c in boxes if m != "x"]
    return done, todo

def main():
    today = datetime.date.today()
    print("=" * 60)
    print("PAGEZY/N-ATLAS SPRINT — STATUS REPORT")
    print("=" * 60)
    print(f"Kit date anchor: Day 1 = 2026-10-07. Today per system: {datetime.date.today()}")

    done, todo = gate_status()
    print(f"\nCheckpoints cleared: {len(done)} / {len(done) + len(todo)}")
    print(f"Next checkpoint: {todo[0] if todo else 'ALL CLEAR — submit or rest'}")

    for dayfile in sorted(os.listdir(os.path.join(ROOT, "day_plans"))):
        p = os.path.join(ROOT, "day_plans", dayfile)
        content = read(p)
        total = len(re.findall(r"- \[ \]", content))
        if total:
            print(f"  {dayfile}: {total} open task(s)")

    fence = check_fence()
    if fence:
        print("\n⚠ FENCE BREACH — Layer-3 material is publicly tracked:")
        for f in fence:
            print("   ", f)
        print("   Fix per docs/07_ip_and_moat.md BEFORE any other work.")
    else:
        print("\n✓ IP fence intact.")

    print("\nFIRST ACTION: open docs/CHECKPOINTS.md, find the first unchecked")
    print("checkpoint, open that day's plan, do only that box. Nothing else.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
