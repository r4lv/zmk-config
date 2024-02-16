# zmk-config for Corne Keyboard / QWERTZ / macOS

![layout](keymap-drawer/corne.png)


## Features

- **QWERTZ** This layout is intended to be used with macOS' German keyboard layout (`Deutsch > Deutsch` or `Deutsch > ABC — QWERTZ`)
- **screen brightness** The F16 and F17 keys on the `tri` layer are intended to be mapped to external screen brightness control, e.g. with [superduper/BrightnessMenulet](https://github.com/superduper/BrightnessMenulet).
- **hyper** Many keys on the `tri` layer are mapped to the `HYPER` modifier (`⇧⌃⌥⌘`), symbolized by the atom symbol. Those keys can be remapped on-the-fly with [karabiner-elements](https://karabiner-elements.pqrs.org), instead of re-flashing the firmware each time.
- **magic shift** The right _magic_ shift key on the base layer behaves like
   - a regular RSHIFT when held,
   - a sticky RSHIFT when tapped (to capitalize the next letter), and
   - like `&caps_word` when double-tapped (to capitalize the next word).


## German QWERTZ on macOS

While most keyboards send the US keycodes to the operating system, even if the keycaps printed on the keyboard are in a different language, it is the operating system's job to map the **keycodes** to the **characters** which will appear on the screen, depending on the selected input source.

To simplify the configuration in the ZMK keymap file, the mapping between the desired (German) characters and the (US) keycodes is defined in `de-mac/de-mac.yaml`. It is used to generate the `keys_de.h` mapping which provides `DE_Y`, `DE_SZ` etc for `corne.keymap`, and the correct symbols for keymap-drawer.


## usage

Use [just](https://github.com/casey/just) to run the recipes in `justfile`:

``` bash
just       # list recipes
just draw  # update keymap-drawer/corne.png
just build # build zmk firmware with Docker
```

## macOS input sources

The following input sources should be set up in System Preferences > Keyboard > Input Sources:

- Deutsch → **Deutsch** (or **ABC — QWERTZ**)
- ~~Andere → Unicode Hex-Eingabe~~ (no unicode symbols in the keymap for now)

Use `ctrl+space` to toggle between the input sources.


## macOS keyboard shortcuts

### fn / globe key

The Apple Magic Keyboard A1644 has an `fn` key, while the newer 2nd generation keyboards (A2449, A2450) have `🌐 fn` printed on it.

The `fn` key is used to input:

- `fn ←`: `HOME` <kbd>↖</kbd>
- `fn →`: `END` <kbd>↘</kbd>
- `fn ↑`: `PG_UP` <kbd>⇞</kbd>
- `fn ↓`: `PG_DN` <kbd>⇟</kbd>
- `fn ↵`: `KP_ENTER`/`keypad_enter` <kbd>⌤</kbd>, "Enter" (macOS calls the normal <kbd>↵</kbd> key "Return") 
- `fn ⌫`: `DEL` <kbd>⌦</kbd>, "forward delete" (macOS calls <kbd>⌫</kbd>/`BACKSPACE` "Delete", and <kbd>⌦</kbd>/`DELETE` "Forward Delete")

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

