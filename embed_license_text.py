import base64
from pathlib import Path


SOURCE = Path("licenses.txt")
TARGET = Path("oscduplicator") / Path("license_text.py")


with open(SOURCE, "r", encoding="utf-8") as f:
    license_text = f.read()


encoded_text = base64.b64encode(license_text.encode("utf-8")).decode("utf-8")


with open(TARGET, "a", encoding="utf-8") as f:
    f.write(f"""
import base64
encoded_text = "{encoded_text}"
LICENSE_TEXT = base64.b64decode(encoded_text).decode("utf-8")
""")
