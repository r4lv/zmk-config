ZEPHYR_SDK_VERSION := "0.16.3"

_default:
	just --list

# generate German macOS key mapping
generate-mapping:
	python de-mac/generate_de_key_mapping.py  # generates de-mac/keys_de.h

# draw keyboard layout as PNG
draw: generate-mapping
    bunx sass@1.54.0 --no-source-map keymap-drawer/style.scss keymap-drawer/style.gen.css
    python keymap-drawer/generate_drawer_config.py  # generate config.gen.yaml
    keymap -c keymap-drawer/config.gen.yaml parse -z config/corne.keymap > keymap-drawer/corne.gen.yaml
    keymap -c keymap-drawer/config.gen.yaml draw keymap-drawer/corne.gen.yaml | sed 's/tabler:/tabler__/g' \
        | sed 's/>base</></g' \
        > keymap-drawer/corne.svg
    resvg --background white -w 2000 keymap-drawer/corne.svg keymap-drawer/corne.png \
        --use-fonts-dir keymap-drawer/fonts/Quicksand/static \
        --skip-system-fonts

# watch for changes and redraw keyboard layout
draw-watch:
	ls config/* keymap-drawer/*template* keymap-drawer/*.py keymap-drawer/style.scss | entr just draw

# build ZMK firmware for one side
build side: generate-mapping
    #!/usr/bin/env bash
    # TODO: generate-mapping breaks ninjas change detection. build aways takes 9s,
    # even when nothing changed. I never get a "ninja: no work to do" message.
    set -euo pipefail
    source .venv/bin/activate
    cd zmk/app
    if [ -d build/{{side}} ]; then
        west build -d build/{{side}}
    else
        west build -d build/{{side}} -b nice_nano_v2 -- -DSHIELD=corne_{{side}} -DZMK_CONFIG=$PWD/../../config
    fi
    cp build/{{side}}/zephyr/zmk.uf2  ../../firmware/{{side}}.uf2


# flash ZMK firmware to nice!nano
flash side:
    #!/usr/bin/env bash
    set -euo pipefail
    source .venv/bin/activate
    cd zmk/app
    if [ ! -d build/{{side}} ]; then
        echo "ERROR: firmware/{{side}}.uf2 does not exist"
        exit 1
    fi
    for i in {1..15}; do
        if [ -d /Volumes/NICENANO ]; then
            sleep 1
            west flash -d build/{{side}}
            exit 0
        fi
        echo -n "."
        sleep 1
    done
    echo "ERROR - count not find nice!nano"


flash-manual side:
	#!/usr/bin/env bash
	set -euo pipefail
	if [ ! -f firmware/{{side}}.uf2 ]; then
		echo "ERROR: firmware/{{side}}.uf2 does not exist"
		exit 1
	fi
	for i in {1..15}; do
		if [ -d /Volumes/NICENANO ]; then
			sleep 1
			cp firmware/{{side}}.uf2 /Volumes/NICENANO
			echo 'flashed {{side}} side!'
			echo -n "Waiting for nice!nano to reboot"
			for i in {1..15}; do
				if [ ! -d /Volumes/NICENANO ]; then
					echo 'okay!'
					exit 0
				fi
				echo -n "."
				sleep 1
			done
			echo 'error: something went wrong...'
			exit 1
		fi
		echo -n "."
		sleep 1
	done
	echo "ERROR! Couldn't find nice!nano."

# update venv, zmk and zephyr modules
update:
    #!/usr/bin/env bash
    set -euxo pipefail

    # python venv
    test ! -d .venv && python -m venv .venv
    source .venv/bin/activate

    # west
    pip install -q -U west

    # zmk firmware
    test ! -d zmk  && git clone https://github.com/zmkfirmware/zmk.git
    cd zmk
    git pull

    # west workspace
    test ! -d .west && west init -l app/

    # dependencies
    west update
    west zephyr-export
    pip install -r zephyr/scripts/requirements.txt

# setup zephyr SDK
setup-zephyr-sdk:
    #!/usr/bin/env bash
    set -euxo pipefail
    brew install -q --formula cmake ninja gperf ccache qemu dtc wget libmagic
    # python3 should already be installed (e.g. with pyenv)
    mkdir -p zephyr-sdk
    cd zephyr-sdk
    if [ ! -d zephyr-sdk-{{ZEPHYR_SDK_VERSION}} ]; then
        if [ ! -f zephyr-sdk-{{ZEPHYR_SDK_VERSION}}_macos-x86_64.tar.xz ]; then
            wget -q https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v{{ZEPHYR_SDK_VERSION}}/zephyr-sdk-{{ZEPHYR_SDK_VERSION}}_macos-x86_64.tar.xz
        fi
        echo "verify checksum..."
        wget -q -O - https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v{{ZEPHYR_SDK_VERSION}}/sha256.sum | shasum --check --ignore-missing
        tar xf zephyr-sdk-{{ZEPHYR_SDK_VERSION}}_macos-x86_64.tar.xz
        rm -rf zephyr-sdk-{{ZEPHYR_SDK_VERSION}}_macos-x86_64.tar.xz
    fi

    cd zephyr-sdk-{{ZEPHYR_SDK_VERSION}}
    # only keep arm-zephyr-eabi, 7,0G -> 913M
    rm -rf aarch* arc* microblazeel* mips* nios2* risc* sparc* x86* xtensa*
    ./setup.sh -c
