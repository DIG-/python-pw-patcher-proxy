DIG PW Patcher Proxy
====================
[![License](https://img.shields.io/badge/license-CC_BY--ND_4.0-blue
)](https://creativecommons.org/licenses/by-nd/4.0/)
[![Python Version](https://img.shields.io/badge/python-3.8_%7C_3.9_%7C_3.10_%7C_3.11_%7C_3.12-blue)](https://github.com/DIG-/python-pw-patcher-proxy/)
[![Version](https://img.shields.io/badge/version-v0.2.1-blue)](https://github.com/DIG-/python-pw-patcher-proxy/)

[![Windows - Supported](https://img.shields.io/badge/windows-supported-success?logo=windows&logoColor=dddddd)](#)
[![Linux - Supported](https://img.shields.io/badge/linux-supported-success?logo=linux&logoColor=dddddd)](#)
![MacOS - Partial](https://img.shields.io/badge/macos-partial-orange?logo=apple&logoColor=dddddd)

Simple PW patcher proxy to speed up the update process. Downloading all update and caching it.

How to use
==========
Edit file `[game]/patcher/server/updateserver.txt`, adding line:
```
"proxy"  "http://localhost:8080/"
```

Open terminal and execute the follow line to start this project:
```sh
python -m dig_pw_patcher_proxy
```

Open game patcher and choose **proxy** as update server.

Enjoy!

Options
-------
||||
|-|-|-|
| `-s` | `--server`      | Url to original update server                               |
| `-c` | `--cache`       | Path to cache dir                                           |
|      | `--clear-cache` | Clear entire cache before start                             |
| `-j` | `--jobs`        | Number of parallel downloads for cache                      |
| `-p` | `--port`        | Port of proxy server                                        |
|      | `--bind`        | Bind proxy server to that ip, allowing external connections |

Instalation
===========
### Option 1:
- Download this repository
- Open terminal on downloaded folder and execute:
```sh
python -m pip install .
```

### Option 2:
- Open terminal and execute:
```sh
python -m pip install "https://github.com/DIG-/python-pw-patcher-proxy/releases/download/0.2.1/dig_pw_patcher_proxy-0.2.1-py3-none-any.whl"
```

Uninstall
=========
Execute:
```sh
python -m pip uninstall dig_pw_patcher_proxy
```

License
=======
[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/)

- You can use and redist freely.
- You can also modify, but only for yourself.
- You can use it as a part of your project, but without modifications in this project.