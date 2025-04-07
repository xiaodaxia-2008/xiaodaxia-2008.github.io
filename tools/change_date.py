import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def change_date(path: Path):
    if not path.exists():
        return
    if path.is_dir():
        for p in path.iterdir():
            change_date(p)
    elif path.suffix == ".md":
        with open(path, "r+", encoding="utf8") as f:
            data = f.read()
            expr = r"date:\s+(\d{4}-\d+-\d+)"
            m = re.search(expr, data)
            if m is None:
                return
            original_date = m.group(1)
            data = re.sub(expr, "date: 2017-02-08", data)
            f.seek(0)
            f.write(data)
            f.write("\n\n")
            f.write(f"*{original_date}*")
            f.write("\n")
            logger.debug(f"Changed date in {path}")


if __name__ == "__main__":
    import sys

    path = Path(sys.argv[1])
    change_date(path)
