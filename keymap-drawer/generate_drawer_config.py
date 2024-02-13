#!/usr/bin/env python
"""
Generates config.gen.yaml from config.template.yaml + style.gen.css + raw_binding_map.gen.yaml
"""
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString as LS


yaml = YAML()
yaml.default_flow_style = False

HERE = Path(__file__).parent

with open(HERE / "config.template.yaml") as f:
    cfg = yaml.load(f)

cfg.yaml_set_start_comment(f"generated with {Path(__file__).name}")

css = (HERE / "style.gen.css").read_text()
cfg["draw_config"]["svg_style"] = LS(css + "\n" + cfg["draw_config"].get("svg_style", ""))

for char in "abcdefghijklmnopqrstuvwxyz,.-":
    glyph = cfg["draw_config"]["glyphs"]["r:hyper-TEMPLATE"].replace("(CHAR)", char.upper())
    cfg["draw_config"]["glyphs"][f"r:hyper-{char}"] = glyph
    cfg["parse_config"]["raw_binding_map"][f"&kp HYPER(DE_{char.upper()})"] = f"$$r:hyper-{char}$$"

with open(HERE / "../de-mac/raw_binding_map.gen.yaml") as f:
    raw_binding_data = yaml.load(f)
    for k, v in raw_binding_data.items():
        if k in cfg["parse_config"]["raw_binding_map"]:
            print(f"Warning: key {k} already in template file")
        else:
            cfg["parse_config"]["raw_binding_map"][k] = v

with open(HERE / "config.gen.yaml", "w") as f:
    yaml.dump(cfg, f)
