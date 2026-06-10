from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from web_print.web import create_app, main

app = create_app()


if __name__ == "__main__":
    main()
