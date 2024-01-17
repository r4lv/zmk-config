from pathlib import Path
from ruamel.yaml import YAML


from ruamel.yaml.scalarstring import LiteralScalarString

def LS(s):
    return LiteralScalarString(s) # textwrap.dedent(s))

yaml = YAML()
yaml.default_flow_style = False

HERE = Path(__file__).parent

with open(HERE / "config.template.yaml") as f:
    keymap = yaml.load(f)

with open(HERE / "style.gen.css") as f:
    keymap["draw_config"]["svg_style"] = LS(f.read() + "\n" + keymap["draw_config"].get("svg_style", ""))
with open(HERE / "raw_binding_map.gen.yaml")  as f:
    raw_binding_data = yaml.load(f)
    for k, v in raw_binding_data.items():
        if k in keymap["parse_config"]["raw_binding_map"]:
            print(f"Warning: key {k} already in template file")
        keymap["parse_config"]["raw_binding_map"][k] = v

with open(HERE / "config.gen.yaml", "w") as f:
    yaml.dump(keymap, f)

