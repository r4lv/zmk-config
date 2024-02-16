#!/usr/bin/env python
"""
Generates config.gen.yaml from config.template.yaml + style.gen.css + raw_binding_map.gen.yaml
"""
from pathlib import Path
from urllib.request import urlopen
import re
import io

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

for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    cfg["parse_config"]["raw_binding_map"][f"&kp HYPER(DE_{char})"] = f"$$combo:atom/text:{char}$$"

with open(HERE / "../de-mac/raw_binding_map.gen.yaml") as f:
    raw_binding_data = yaml.load(f)
    for k, v in raw_binding_data.items():
        if k in cfg["parse_config"]["raw_binding_map"]:
            print(f"Warning: key {k} already in template file")
        else:
            cfg["parse_config"]["raw_binding_map"][k] = v


def get_glyph(key) -> tuple[str, str, str]:
    key = dict(alt="apple-keyboard-option", cmd="apple-keyboard-command").get(key, key)
    if ":" not in key:
        key = f"mdi:{key}"
    group, key = key.split(":")
    if group == "text":
        return group, key, ""

    url = cfg["draw_config"]["glyph_urls"][group].format(key)
    try:
        with urlopen(url) as f:
            # TODO: it would be nicer to re-use keymap-drawer's cache here.
            data = f.read().decode("utf-8")
            data = re.sub(r"id=\".*?\"", "", data).replace("<svg", f"<svg id='rglyph:{key}'")
            data = re.sub(r"viewBox=\"(.*?)\"", r"viewBox='\g<1>'", data, flags=re.IGNORECASE)
            # this is a fix for nested SVGs - the regex in keymap-drawer always picks up the LAST
            # viewBox attribute with double quotes, so we use single quotes to hide the inner SVGs.
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        raise e
    return group, key, data


def yaml_dumps(data) -> str:
    buf = io.StringIO()
    yaml.dump(data, buf)
    return buf.getvalue()


for left, right in re.findall(r"\$\$combo:(.*?)/(.*?)\$\$", yaml_dumps(cfg)):
    lgrp, lkey, ldef = get_glyph(left)
    rgrp, rkey, rdef = get_glyph(right)
    svg = f"""<svg viewBox="0 0 48 24"><defs>{ldef}{rdef}</defs>"""
    svg += f"""<use href="#rglyph:{lkey}" x="-12" y="0" width="24" height="24"/>"""
    if rgrp == "text":
        svg += f"""<text x="24" y="14" style="font-size: 24px; text-anchor: start;">{rkey}</text>"""
    else:
        svg += f"""<use href="#rglyph:{rkey}" x="12" y="0" width="24" height="24" />"""
    svg += """</svg>"""
    cfg["draw_config"]["glyphs"][f"combo:{left}/{right}"] = LS(svg)


with open(HERE / "config.gen.yaml", "w") as f:
    yaml.dump(cfg, f)
