#!/usr/bin/env python
"""
creates
    - keys_de.h (for ZMK)
    - raw_binding_map.gen.yaml (for generate_drawer_config.py / keymap-drawer)
from de-mac.yaml.
"""
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

yaml = YAML()
yaml.default_flow_style = False

HERE = Path(__file__).parent


header = [
    "german macOS keyboard definitions for ZMK",
    f"generated with {Path(__file__).name} from de-mac.yaml",
]
out_raw_binding = CommentedMap()
out_raw_binding.yaml_set_start_comment("\n".join(header))
out_defines = "// " + "\n// ".join(header) + "\n\n"

with open(HERE / "de-mac.yaml") as f:
    data = yaml.load(f)

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
                    + f"/* {tcfg[lookup]['pretty']} */\n"
                )
    out_defines += "\n"

with open(HERE / "keys_de.h", "w") as f:
    f.write(out_defines)

with open(HERE / "raw_binding_map.gen.yaml", "w") as f:
    yaml.dump(out_raw_binding, f)
