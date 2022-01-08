# Eero-AdGuard Sync
Sync Eero DHCP client list to AdGuard Home

[![Release](https://github.com/amickael/eero-adguard-sync/actions/workflows/python-publish.yml/badge.svg)](https://github.com/amickael/wipeit/actions/workflows/python-publish.yml)
[![PyPI](https://img.shields.io/pypi/v/eero-adguard-sync?color=blue)](https://pypi.org/project/wipeit/)
[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)


![eero-adguard-sync](https://repository-images.githubusercontent.com/365859955/17783580-b1d0-11eb-9738-6d2bc92644e6)

Table of Contents
=================
* [Eero-Adguard Sync](#wipeit)
   * [Dependencies](#-dependencies)
   * [Installation](#️-installation)
   * [Usage](#-usage)
   * [Options](#️-options)
      * [eag-sync](#eero-adguard-sync-1)
      * [eag-sync sync](#eero-adguard-sync-sync)
   * [Autocompletion](#-autocompletion)
      * [bash](#bash)
      * [zsh](#zsh)
   * [License](#️-license)

## 👶 Dependencies
* [Python 3.7 or higher](https://www.python.org/downloads/)

## 🛠️ Installation
Install from PyPI using `pip`, you may need to use `pip3` depending on your installation:
```sh
pip install wipeit
```

## 🚀 Usage
**wipeit** is a command-line program to purge your Reddit history. It requires a Python interpreter version 3.7+.

To authenticate without wiping history you can use the `login` command, a browser window will open prompting you to login to Reddit:
```shell
wipeit login
```
---
To wipe your Reddit history you can use the `wipe` command. The following command will clear the last 30 days of comment and submission history, and will overwrite them with random text before deletion:
```shell
wipeit wipe -d 30 -sco
```
> Note: A browser window will open to request access to your account if you have not previously authenticated.
---
To remove Reddit credentials from your computer you can use the `logout` command:
```shell
wipeit logout
```


## ⚙️ Options
### `eag-sync`
```
Usage: wipeit [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show help message and exit.

Commands:
  login   Authorize wipeit with a Reddit account, will open a browser
          window...

  logout  Remove Reddit credentials from wipeit, you will be prompted to...
  wipe    Wipe your Reddit history.
```

### `eag-sync sync`
```
Usage: wipeit wipe [OPTIONS]

  Wipe your Reddit history.

Options:
  -d, --days INTEGER RANGE  Number of days worth of content to delete.
                            Defaults to 365.

  -f, --from-date TEXT      Date relative to --days, in ISO format (YYYY-MM-
                            DD). Defaults to today.

  -c, --comments            Delete comments.
  -s, --submissions         Delete submissions.
  -o, --overwrite           Overwrite content with random text before
                            deletion.

  --help                    Show help message and exit.
```

## 🪄 Autocompletion
To enable tab completion you will need to configure your preferred shell to use it. Currently `bash` and `zsh` are supported.

This configuration is totally optional, but may be useful if you use `eag-sync` often.

### bash
Add the following to ` ~/.bashrc`:
```shell
eval "$(_WIPEIT_COMPLETE=bash_source wipeit)"
```

### zsh
Add the following to `~/.zshrc`:
```shell
eval "$(_WIPEIT_COMPLETE=zsh_source wipeit)"
```


## ⚖️ License
[MIT © 2022 Andrew Mickael](https://github.com/amickael/eero-adguard-sync/blob/master/LICENSE)
