# Eero-AdGuard-Sync
Sync Eero DHCP client list to AdGuard Home

[![Release](https://github.com/amickael/eero-adguard-sync/actions/workflows/python-publish.yml/badge.svg)](https://github.com/amickael/eero-adguard-sync/actions/workflows/python-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/eero-adguard-sync?color=blue)](https://pypi.org/project/wipeit/)
[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)


![eero-adguard-sync](https://repository-images.githubusercontent.com/445873210/a0dcb692-fe53-4e6e-83a9-4507664080c1)

Table of Contents
=================
* [Eero-Adguard-Sync](#eero-adguard-sync)
   * [Dependencies](#-dependencies)
   * [Installation](#️-installation)
   * [Usage](#-usage)
   * [Options](#️-options)
      * [eag-sync](#eag-sync)
      * [eag-sync sync](#eag-sync-sync)
      * [eag-sync clear](#eag-sync-clear)
   * [Autocompletion](#-autocompletion)
      * [bash](#bash)
      * [zsh](#zsh)
   * [License](#️-license)

## 👶 Dependencies
* [Python 3.7 or higher](https://www.python.org/downloads/)

## 🛠️ Installation
Install from PyPI using `pip`, you may need to use `pip3` depending on your installation:
```shell
pip install eero-adguard-sync
```

## 🚀 Usage
**eag-sync** is a command-line program to sync your Eero DHCP client list to AdGuard Home, note that it is a one-way sync from Eero to AdGuard. It requires Python interpreter version 3.7+.

To run a sync process run the `eag-sync sync` command, you can find a full list of options below. Sample usage:
```shell
eag-sync sync -d
```

You may be prompted for an Eero email or SMS code the first time you run this program. Your credentials never leave your computer, all processing is done client side.

To clear all locally cached credentials run the `clear` command:
```shell
eag-sync clear
```


## ⚙️ Options
### `eag-sync`
```
Usage: eag-sync [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  sync
```

### `eag-sync sync`
```
Usage: eag-sync sync [OPTIONS]

Options:
  --adguard-host TEXT      AdGuard Home host IP address
  --adguard-user TEXT      AdGuard Home username
  --adguard-password TEXT  AdGuard Home password
  --eero-user TEXT         Eero email address or phone number
  -d, --delete             Delete AdGuard clients not found in Eero DHCP list
  -y, --confirm            Skip interactive confirmation
  --help                   Show this message and exit.
```

### `eag-sync clear`
```
Usage: eag-sync clear [OPTIONS]

Options:
  -y, --confirm  Skip interactive confirmation
  --help         Show this message and exit.
```

## 🪄 Autocompletion
To enable tab completion you will need to configure your preferred shell to use it. Currently `bash` and `zsh` are supported.

This configuration is totally optional, but may be useful if you use `eag-sync` often.

### bash
Add the following to ` ~/.bashrc`:
```shell
eval "$(_EAG_SYNC_COMPLETE=bash_source eag-sync)"
```

### zsh
Add the following to `~/.zshrc`:
```shell
eval "$(_EAG_SYNC_COMPLETE=zsh_source eag-sync)"
```


## ⚖️ License
[MIT © 2022 Andrew Mickael](https://github.com/amickael/eero-adguard-sync/blob/master/LICENSE)
