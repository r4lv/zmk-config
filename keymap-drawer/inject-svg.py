#!/usr/bin/env python
import sys
from pathlib import Path

svg = Path(sys.argv[1]).read_text()
inj = Path(sys.argv[2]).read_text()

svg = svg.replace("</style>", f"</style>{inj}")
Path(sys.argv[1]).write_text(svg)
