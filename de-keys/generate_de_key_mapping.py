#!/usr/bin/env python
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.default_flow_style = False

HERE = Path(__file__).parent

with open(HERE / "de-mac.yaml") as f:
    data = yaml.load(f)


out_raw_binding = {}
out_defines = "// german macOS keyboard definitions for ZMK\n// generated from de-keys.yaml\n\n"

for tname, tcfg in data["tasten"].items():
    if "tap" not in tcfg:
        tcfg["tap"] = dict(pretty=tcfg["zmk_key"], alias=[tcfg["zmk_key"]])
    out_defines += f"/* {tname} */\n"
    for alias in tcfg["tap"]["alias"]:
        if "shifted" in tcfg:
            out_raw_binding[f"&kp DE_{alias}"] = dict(
                tap=tcfg["tap"]["pretty"], shifted=tcfg["shifted"]["pretty"]
            )
        else:
            out_raw_binding[f"&kp DE_{alias}"] = tcfg["tap"]["pretty"]
        out_defines += f"#define DE_{alias} ({tcfg['zmk_key']})\n"
    out_defines += "\n"
    for lookup, mod in [("shifted", "LS({})"), ("alt", "LA({})"), ("alt_shifted", "LS(LA({}))")]:
        if lookup in tcfg:
            for alias in tcfg[lookup]["alias"]:
                out_raw_binding[f"&kp DE_{alias}"] = tcfg[lookup]["pretty"]
                out_defines += (
                    f"#define DE_{alias} ({mod.format(tcfg['zmk_key'])})  "
                    + f"// {tcfg[lookup]['pretty']}\n"
                )
    out_defines += "\n"

with open(HERE / "../config/keys_de.h", "w") as f:
    f.write(out_defines)
with open(HERE / "../keymap-drawer/raw_binding_map.gen.yaml", "w") as f:
    yaml.dump(out_raw_binding, f)
