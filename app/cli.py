"""Ask from the terminal.

Usage:
  python -m app.cli "How do I get VPN access?"
  python -m app.cli --gaps
"""
import logging
import sys

from . import assistant, gaps


def main() -> None:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == "--gaps":
        s = gaps.stats()
        print(f"{s['total']} questions, {s['gaps']} without a good answer\n")
        for g in gaps.gap_report():
            print(f"[{g['count']}x] {g['topic']}  ({', '.join(g['reasons'])})")
            for q in g["questions"]:
                print(f"      - {q}")
        return

    r = assistant.ask(" ".join(sys.argv[1:]))
    print(f"\n{r['answer']}\n")
    print(f"mode={r['mode']}  answered={r['answered']}  gap={r['gap']}"
          + (f"  missing_topic={r['missing_topic']!r}" if r["missing_topic"] else ""))
    print("\nSources:")
    for s in r["sources"]:
        mark = "*" if s["cited"] else " "
        print(f" {mark} [{s['ref']}] {s['score']:.2f}  {s['title']}")


if __name__ == "__main__":
    main()
