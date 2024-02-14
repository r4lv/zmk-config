# zmk-config for Corne / QWERTZ / macOS

![layout](keymap-drawer/corne.png)

## Deutsches Layout

The german macOS key mapping is defined in `de-mac/de-mac.yaml`. It is used to generate the `keys_de.h` mapping which provides `DE_Y`, `DE_SZ` etc for `corne.keymap`.

## Features

- **QWERTZ** This layout is intended to be used with macOS' German keyboard layout (`Deutsch > Deutsch` or `Deutsch > ABC — QWERTZ`)
- **screen brightness** The F16 and F17 keys on the `tri` layer are intended to be mapped to external screen brightness control, e.g. with [superduper/BrightnessMenulet](https://github.com/superduper/BrightnessMenulet).
- **hyper** Many keys on the `tri` layer are mapped to the `HYPER` modifier (`⇧⌃⌥⌘`), symbolized by the atom symbol. Those keys can be remapped on-the-fly with [karabiner-elements](https://karabiner-elements.pqrs.org).
- **magic shift** The right _magic_ shift key on the base layer behaves like
   - a regular RSHIFT when held,
   - a sticky RSHIFT when tapped (to capitalize the next letter), and
   - like `&caps_word` when double-tapped (to capitalize the next word).

## usage

Use [just](https://github.com/casey/just) to run the recipes in `justfile`:

``` bash
just       # list recipes
just draw  # update keymap-drawer/corne.png
just build # build zmk firmware with Docker
```

## macOS Eingabequellen

Folgende beiden Eingabequellen müssen bei Systemeinstellungen > Tastatur > Eingabequellen hinterlegt sein:

- Deutsch → **Deutsch** (oder **ABC — QWERTZ**)
- Andere → Unicode Hex-Eingabe

Mit ctrl+space kann zwischen den Eingabequellen gewechselt werden.


## macOS keyboard shortcuts

### fn / globe key

The Apple Magic Keyboard A1644 has an `fn` key, while the newer 2nd generation keyboards (A2449, A2450) have `🌐 fn` printed on it.

The `fn` key is used to input:

- `fn ←`: HOME, `↖`
- `fn →`: END, `↘`
- `fn ↑`: `PG_UP`, page up, `⇞`
- `fn ↓`: `PG_DN`, page down, `⇟`
- `fn ↵`: `KP_ENTER`, keypad enter, `keypad_enter`, `⌤`, "Enter" (macOS calls the normal key "Return") 
- `fn ⌫`: `DEL` / forward delete, `⌦` (macOS calls `BACKSPACE` "Delete", and `DELETE` "Forward Delete")

and additionally:

- the F-keys F1-F12, which would otherwise control the screen brightness, volume, media playback, etc
- accessibility, with `fn ctrl F..`

Some apps use the globe-key as shortcuts, e.g.:

- `🌐 E`: Bearbeiten > Emoji & Symbole
- `🌐 F`: Darstellung > Vollbildmodus


### F-keys

- Key Codes.app shows the key codes of the keys F13 and F16-F19.
   - F14 and F15 change the screen brightness (siehe [discussions.apple.com](https://discussions.apple.com/thread/253836891))
   - F20 is shown, but not (correctly) recognized: `Unicode 16 / 0x10, Keys ----, Key Code 90 / 0x5a, Modifiers 256 / 0x100`
- Karabiner Elements shows F13–F24


## dependencies

- python 3.6+, [ruamel.yaml](https://pypi.org/project/ruamel.yaml/) for processing templates
- [keymap-drawer](https://github.com/caksoylar/keymap-drawer) for generating keymap SVG (installed with pipx)
- [bun](https://bun.sh)/[sass](https://www.npmjs.com/package/sass) for compiling stylesheets
- [resvg](https://github.com/RazrFalcon/resvg) for converting keymap SVG to PNG
- Docker / [colima](https://github.com/abiosoft/colima) for building zmk firmware
- [just](https://github.com/casey/just) instead of make
- [entr](https://eradman.com/entrproject/) for re-building on file changes


For `build`, you need to have a checked out working copy of the [zmkfirmware/zmk](https://github.com/zmkfirmware/zmk) repository one directory up, e.g.:

``` text
my-keyboard-stuff
├── zmk            <- zmkfirmware/zmk repository
│  ├── app
│  ├── docs
│  ├── zephyr
│  └── ...
└── zmk-config     <- this repository
   ├── README.md   <- this file
   ├── config
   └── ...
```

