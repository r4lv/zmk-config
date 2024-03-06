import re
from pathlib import Path


def process_block(content) -> str:
    row = 0
    data = []

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("/*"):
            continue
        parts = [x.strip() for x in line.split("&") if x.strip() != ""]
        if (row < 3 and len(parts) != 12) or (row == 3 and len(parts) != 6):
            print(f"Error in row {row}: {parts}")
            exit(1)

        if row == 3:
            parts = ["", "", ""] + parts + ["", "", ""]
        data.append(parts)

        row += 1

    mw = []

    for ic in range(12):
        mw.append(max([len(data[ir][ic]) for ir in range(4)]) + 2)

    l = "─"

    out = []

    out.append(
        f"/* ╭{l*mw[0]}┬{l*mw[1]}┬{l*mw[2]}┬{l*mw[3]}┬{l*mw[4]}┬{l*mw[5]}╮   "
        + f"╭{l*mw[6]}┬{l*mw[7]}┬{l*mw[8]}┬{l*mw[9]}┬{l*mw[10]}┬{l*mw[11]}╮ */"
    )
    out.append(
        "    "
        + "  ".join(f"&{data[0][i]: <{mw[i]-2}}" for i in [0, 1, 2, 3, 4, 5])
        + "      "
        + "  ".join(f"&{data[0][i]: <{mw[i]-2}}" for i in [6, 7, 8, 9, 10, 11])
    )
    out.append(
        f"/* ├{l*mw[0]}┼{l*mw[1]}┼{l*mw[2]}┼{l*mw[3]}┼{l*mw[4]}┼{l*mw[5]}┤   "
        + f"├{l*mw[6]}┼{l*mw[7]}┼{l*mw[8]}┼{l*mw[9]}┼{l*mw[10]}┼{l*mw[11]}┤ */"
    )
    out.append(
        "    "
        + "  ".join(f"&{data[1][i]: <{mw[i]-2}}" for i in [0, 1, 2, 3, 4, 5])
        + "      "
        + "  ".join(f"&{data[1][i]: <{mw[i]-2}}" for i in [6, 7, 8, 9, 10, 11])
    )

    out.append(
        f"/* ├{l*mw[0]}┼{l*mw[1]}┼{l*mw[2]}┼{l*mw[3]}┼{l*mw[4]}┼{l*mw[5]}┤   "
        + f"├{l*mw[6]}┼{l*mw[7]}┼{l*mw[8]}┼{l*mw[9]}┼{l*mw[10]}┼{l*mw[11]}┤ */"
    )

    out.append(
        "    "
        + "  ".join(f"&{data[2][i]: <{mw[i]-2}}" for i in [0, 1, 2, 3, 4, 5])
        + "      "
        + "  ".join(f"&{data[2][i]: <{mw[i]-2}}" for i in [6, 7, 8, 9, 10, 11])
    )
    out.append(
        f"/* ╰{l*mw[0]}┴{l*mw[1]}┴{l*mw[2]}┼{l*mw[3]}┼{l*mw[4]}┼{l*mw[5]}┤   "
        + f"├{l*mw[6]}┼{l*mw[7]}┼{l*mw[8]}┼{l*mw[9]}┴{l*mw[10]}┴{l*mw[11]}╯ */"
    )
    out.append(
        "    "
        + "  ".join(
            f"&{data[3][i]: <{mw[i]-2}}" if data[3][i] else " " * (mw[i] - 1)
            for i in [0, 1, 2, 3, 4, 5]
        )
        + "      "
        + "  ".join(
            f"&{data[3][i]: <{mw[i]-2}}" if data[3][i] else " " * (mw[i] - 1)
            for i in [6, 7, 8, 9, 10, 11]
        )
    )
    out.append(
        f"/*  {' '*mw[0]} {' '*mw[1]} {' '*mw[2]}╰{l*mw[3]}┴{l*mw[4]}┴{l*mw[5]}╯   "
        + f"╰{l*mw[6]}┴{l*mw[7]}┴{l*mw[8]}╯{' '*mw[9]} {' '*mw[10]} {' '*mw[11]}  */"
    )
    return "\n".join(l.rstrip() for l in out)



if __name__ == "__main__":
    p = Path("config/corne.keymap")
    content = p.read_text()

    def process_re_block(match):
        return match.group(1) + process_block(match.group(2)) + match.group(3)

    c2 = re.sub(r"(bindings\s*=\s*<\n)(.*?)(\s*>;)", process_re_block, content, flags=re.DOTALL)
    with p.open("w") as f:
        f.write(c2)
