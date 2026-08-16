from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).parent
    out = root / "diagrams" / "generated"
    out.mkdir(parents=True, exist_ok=True)
    dot = shutil.which("dot")
    for source in (root / "diagrams").glob("*.dot"):
        if dot:
            target = out / f"{source.stem}.svg"
            subprocess.run([dot, "-Tsvg", str(source), "-o", str(target)], check=True)
            print(f"generated {target}")
        else:
            target = out / source.name
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"Graphviz not found; copied {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
