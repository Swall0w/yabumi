<div align="center"> <img src="https://github.com/Swall0w/yabumi/blob/main/docs/logo.png" width="800"/> </div>

# Yabumi
## Install
```bash
    git clone https://github.com/Swall0w/yabumi
    cd yabumi
    pip install -e .
```

Before using yabumi, you need to prepare the configuration in `~/.yabumi.toml`.
```toml
[default]
url = "slack url"
username = "bot name"
target_username = "@hoge"
```
We remark that `target_username` is defined user member id.

## Usage
As lik the `time` command, add `yabumi` before the target command.
For example, if you want execute `python train.py`, your command should be like this.
```bash
    yabumi python train.py
```
