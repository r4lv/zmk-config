# zmk-config for Corne / QWERTZ / macOS

![layout](keymap-drawer/corne.png)

## Deutsches Layout

The german macOS key mapping is defined in `de-mac/de-mac.yaml`. It is used to generate the `keys_de.h` mapping which provides `DE_Y`, `DE_SZ` etc for `corne.keymap`.

## usage

Use [just](https://github.com/casey/just) to run the recipes in `justfile`:

``` bash
just       # list recipes
just draw  # update keymap-drawer/corne.png
just build # build zmk firmware with Docker
```

## macOS Eingabequellen

Folgende beiden Eingabequellen müssen bei Systemeinstellungen > Tastatur > Eingabequellen hinterlegt sein:

- Deutsch → **Deutsch**
- Andere → Unicode Hex-Eingabe

Mit ctrl+space kann zwischen den Eingabequellen gewechselt werden.


## macOS Tastaturkurzbefehle

### fn

Auf dem Apple Magic Keyboard A1644 ist noch eine `fn` Taste aufgedruckt, die bei den neueren 2nd Generation (A2449, A2450) ist `🌐 fn` aufgedruckt.

Über die fn-Taste werden eingegeben:

- `fn ←`: HOME, `↖`
- `fn →`: END, `↘`
- `fn ↑`: `PG_UP`, page up, `⇞`
- `fn ↓`: `PG_DN``, page down, `⇟`
- `fn ↵`: `KP_ENTER`, keypad enter, `keypad_enter`, `⌤`, "Enter" (macOS calls the normal key "Return") 
- `fn ⌫`: `DEL` / forward delete, `⌦` (macOS calls `BACKSPACE` "Delete", and `DELETE` "Forward Delete")

und zusätzlich:

- die F-Tasten F1-F12, die ansonsten die Bildschirmhelligkeit, Lautstärke, Medien, etc steuern
- accessibility, über `fn ctrl F..`

Manche Apps verwenden die Globe-Taste als Shortcut, z.B.:

- `🌐 E`: Bearbeiten > Emoji & Symbole
- `🌐 F`: Darstellung > Vollbildmodus


### F-Tasten

- Key Codes.app zeigt die Key Codes der Tasten F13,F16-F19 an.
   - F14 und F15 verändern die Bildschirmhelligkeit
   - F20 wird angezeigt, aber nicht erkannt: `Unicode 16 / 0x10, Keys ----, Key Code 90 / 0x5a, Modifiers 256 / 0x100`
- Karabiner Elements zeigt F13–F23 an
   - F24 nicht getestet


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

