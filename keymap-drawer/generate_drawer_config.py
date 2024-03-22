#!/usr/bin/env python
"""Generate config.gen.yaml from config.template.yaml + style.gen.css + raw_binding_map.gen.yaml."""

import io
import re
from pathlib import Path
from urllib.request import urlopen

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString as STR

yaml = YAML()
yaml.default_flow_style = False

HERE = Path(__file__).parent

with open(HERE / "config.template.yaml") as f:
    cfg = yaml.load(f)

cfg.yaml_set_start_comment(f"generated with {Path(__file__).name}")

css = (HERE / "style.gen.css").read_text()
cfg["draw_config"]["svg_style"] = STR(css + "\n" + cfg["draw_config"].get("svg_style", ""))

for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    cfg["parse_config"]["raw_binding_map"].setdefault(
        f"&kp HY(DE_{char})", f"$$combo:lucide-orbit/text:{char}$$"
    )
for key, char in dict(COMMA=",", DOT=".", MINUS="\u2013", O_UML="Ö", A_UML="Ä").items():
    # endash for Minus, for better readability
    cfg["parse_config"]["raw_binding_map"].setdefault(
        f"&kp HY(DE_{key})", f"$$combo:lucide-orbit/text:{char}$$"
    )

with open(HERE / "../de-mac/raw_binding_map.gen.yaml") as f:
    raw_binding_data = yaml.load(f)
    for k, v in raw_binding_data.items():
        if k in cfg["parse_config"]["raw_binding_map"]:
            print(f"Warning: key {k} already in template file")
        else:
            cfg["parse_config"]["raw_binding_map"][k] = v


def get_glyph(key) -> tuple[str, str, str]:
    global cfg
    key = dict(
        alt="apple-keyboard-option",
        cmd="apple-keyboard-command",
        shift="apple-keyboard-shift",
        ctrl="apple-keyboard-control",
    ).get(key, key)  # short aliases for modifier keys

    if key in cfg["draw_config"]["glyphs"]:
        key = f"local:{key}"
    if ":" not in key:
        key = f"mdi:{key}"

    group, key = key.split(":")
    if group == "text":
        return (
            group,
            f"text-{key}",
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox=\'0 0 24 24\' id="rglyph:text-{key}">'
            + f'<text x="10" y="14" text-anchor="middle" style="font-size: 24px;">{key}</text>'
            + "</svg>",
        )
    elif group == "local":
        data = cfg["draw_config"]["glyphs"][key]
        data = re.sub(r"id=\".*?\"", "", data)
        data = data.replace("<svg", f"<svg id='rglyph:{key}'")
        data = re.sub(r"viewBox=\"(.*?)\"", r"viewBox='\g<1>'", data, flags=re.IGNORECASE)
    else:
        url = cfg["draw_config"]["glyph_urls"][group].format(key)
        try:
            with urlopen(url) as f:  # noqa: S310
                # TODO: it would be nicer to re-use keymap-drawer's cache here.
                data = f.read().decode("utf-8")
                data = re.sub(r"id=\".*?\"", "", data)
                data = data.replace("<svg", f"<svg id='rglyph:{key}'")
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


for small, l, m, r in re.findall(r"\$\$(small)?combo:(.*?)/(.*?)/(.*?)\$\$", yaml_dumps(cfg)):
    lgrp, lkey, ldef = get_glyph(l)
    mgrp, mkey, mdef = get_glyph(m)
    rgrp, rkey, rdef = get_glyph(r)
    viewbox = "0 -6 72 36" if small else "0 0 72 24"

    svg = f"""<svg viewBox="{viewbox}"><defs>{ldef}{mdef}{rdef}</defs>"""
    # use single quotes to block _scrub_dims_re in keymap-drawer/glyph.py
    svg += f"""<use href="#rglyph:{lkey}" x="0" y="0" width='24' height='24'/>"""
    svg += f"""<use href="#rglyph:{mkey}" x="24" y="0" width='24' height='24'/>"""
    svg += f"""<use href="#rglyph:{rkey}" x="48" y="0" width='24' height='24' />"""
    svg += """</svg>"""
    cfg["draw_config"]["glyphs"][f"{small}combo:{l}/{m}/{r}"] = STR(svg)

for l, r in re.findall(r"\$\$combo:([^/]*?)/([^/]*?)\$\$", yaml_dumps(cfg)):
    lgrp, lkey, ldef = get_glyph(l)
    rgrp, rkey, rdef = get_glyph(r)
    svg = f"""<svg viewBox="0 0 48 24"><defs>{ldef}{rdef}</defs>"""
    # here, width and height are scrubbed by keymap-drawer
    svg += f"""<use href="#rglyph:{lkey}" x="-12" y="0" width="24" height="24"/>"""
    svg += f"""<use href="#rglyph:{rkey}" x="12" y="0" width="24" height="24" />"""
    svg += """</svg>"""
    cfg["draw_config"]["glyphs"][f"combo:{l}/{r}"] = STR(svg)


with open(HERE / "config.gen.yaml", "w") as f:
    yaml.dump(cfg, f)
