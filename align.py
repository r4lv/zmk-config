from pathlib import Path
import re

from IPython import embed
import pasteboard

pb = pasteboard.Pasteboard()

content = pb.get_contents()



row = 0
max_lengths_per_row = [0, 0, 0, 0]
pre = ""
post = ""
data = []

for line in content.strip().splitlines():
    line = line.strip()
    if line.replace(" ", "") == "bindings=<":
        pre = "            bindings = <\n"
        continue
    if line.replace(" ", "") == ">;":
        post = "\n            >;"
        continue
    if line.startswith("/*"):
        continue
    parts = [x.strip() for x in line.split("&") if x.strip() != ""]
    # print(parts, len(parts))
    if (row < 3 and len(parts) != 12) or (row == 3 and len(parts) != 6):
        print(f"Error in row {row}: {parts}")
        exit(1)
    # embed(color="neutral")
    # exit(0)

    if row == 3:
        parts = ["", "", ""] + parts + ["", "", ""]
    data.append(parts)

    row += 1


mw = []

for ic in range(12):
    mw.append(max([len(data[ir][ic]) for ir in range(4)]) + 2)


l = "─"

out = ""

out += (
    pre + f"/* ╭{l*mw[0]}┬{l*mw[1]}┬{l*mw[2]}┬{l*mw[3]}┬{l*mw[4]}┬{l*mw[5]}╮   ╭{l*mw[6]}┬{l*mw[7]}┬{l*mw[8]}┬{l*mw[9]}┬{l*mw[10]}┬{l*mw[11]}╮ */"
     + "\n"
)
out += (
    "    "
    + "  ".join(f"&{data[0][i]: <{mw[i]-2}}" for i in [0, 1, 2, 3, 4, 5])
    + "      "
    + "  ".join(f"&{data[0][i]: <{mw[i]-2}}" for i in [6, 7, 8, 9, 10, 11])
     + "\n"
)
out += (
    f"/* ├{l*mw[0]}┼{l*mw[1]}┼{l*mw[2]}┼{l*mw[3]}┼{l*mw[4]}┼{l*mw[5]}┤   ├{l*mw[6]}┼{l*mw[7]}┼{l*mw[8]}┼{l*mw[9]}┼{l*mw[10]}┼{l*mw[11]}┤ */"
     + "\n"
)
out += (
    "    "
    + "  ".join(f"&{data[1][i]: <{mw[i]-2}}" for i in [0, 1, 2, 3, 4, 5])
    + "      "
    + "  ".join(f"&{data[1][i]: <{mw[i]-2}}" for i in [6, 7, 8, 9, 10, 11])
     + "\n"
)
out += (
    f"/* ├{l*mw[0]}┼{l*mw[1]}┼{l*mw[2]}┼{l*mw[3]}┼{l*mw[4]}┼{l*mw[5]}┤   ├{l*mw[6]}┼{l*mw[7]}┼{l*mw[8]}┼{l*mw[9]}┼{l*mw[10]}┼{l*mw[11]}┤ */"
     + "\n"
)
out += (
    "    "
    + "  ".join(f"&{data[2][i]: <{mw[i]-2}}" for i in [0, 1, 2, 3, 4, 5])
    + "      "
    + "  ".join(f"&{data[2][i]: <{mw[i]-2}}" for i in [6, 7, 8, 9, 10, 11])
     + "\n"
)
out += (
    f"/* ╰{l*mw[0]}┴{l*mw[1]}┴{l*mw[2]}┼{l*mw[3]}┼{l*mw[4]}┼{l*mw[5]}┤   ├{l*mw[6]}┼{l*mw[7]}┼{l*mw[8]}┼{l*mw[9]}┴{l*mw[10]}┴{l*mw[11]}╯ */"
     + "\n"
)
out += (
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
     + "\n"
)
out += (
    f"/*  {' '*mw[0]} {' '*mw[1]} {' '*mw[2]}╰{l*mw[3]}┴{l*mw[4]}┴{l*mw[5]}╯   ╰{l*mw[6]}┴{l*mw[7]}┴{l*mw[8]}╯{' '*mw[9]} {' '*mw[10]} {' '*mw[11]}  */" + post + "\n"
)
# print(out)

pb.set_contents(out)
print("Copied to pasteboard.")