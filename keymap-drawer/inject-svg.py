#!/usr/bin/env python
import sys
from pathlib import Path

svg = Path(sys.argv[1]).read_text()
for infn in sys.argv[2:]:
    svg = svg.replace("</style>", f"</style>{Path(infn).read_text()}")

Path(sys.argv[1]).write_text(svg)
