import argparse
import subprocess
import slackweb
import pathlib
from pathlib import Path
import toml
import time
import datetime
import sys

direc = sys.argv[1:]

def pre_exec_attachments(command_list):
    _attachments = [
            {
            "Title": "Command Execution",
            "color": "good",
            "fields": [
                {
                    "title": "command",
                    "value": "`{}`".format(' '.join(command_list)),
                    "short": "false"
                },
                {
                    "title": "directory",
                    "value": "`{}`".format(str(Path.cwd())),
                    "short": "false"
                },
                {
                    "title": "executed time",
                    "value": "{}".format(datetime.datetime.now()),
                    "short": "true"
                },
            ]
            }]
    return _attachments

def post_exec_succeed_attachments(command_list, elapsed_time):
    _attachments = [
            {
            "Title": "Results",
            "color": "good",
            "fields": [
                {
                    "title": "command",
                    "value": "`{}`".format(' '.join(command_list)),
                    "short": "false"
                },
                {
                    "title": "directory",
                    "value": "`{}`".format(str(Path.cwd())),
                    "short": "false"
                },
                {
                    "title": "finished time",
                    "value": "{}".format(datetime.datetime.now()),
                    "short": "true"
                },
                {
                    "title": "elapsed time",
                    "value": "{:.2}".format(elapsed_time),
                    "short": "true"
                },
            ]
            }]
    return _attachments

def post_exec_failed_attachments(command_list, elapsed_time, ):
    _attachments = [
            {
            "Title": "Results",
            "color": "danger",
            "fields": [
                {
                    "title": "command",
                    "value": "`{}`".format(' '.join(command_list)),
                    "short": "false"
                },
                {
                    "title": "directory",
                    "value": "`{}`".format(str(Path.cwd())),
                    "short": "false"
                },
                {
                    "title": "finished time",
                    "value": "{}".format(datetime.datetime.now()),
                    "short": "true"
                },
                {
                    "title": "elapsed time",
                    "value": "{:.2}".format(elapsed_time),
                    "short": "true"
                },
            ]
            }]
    return _attachments


def main():

    config_path = pathlib.Path.home() / '.yabumi.toml'
    with open(config_path, 'r') as f:
        dict_toml = toml.load(f)
    environment = 'default'

    if 'url' not in dict_toml[environment] and 'username' not in dict_toml[environment]:
        raise ValueError("Invalid configuration")
    else:
        _slack_url = dict_toml[environment]['url']
        _slack_username = dict_toml[environment]['username']

    slack = slackweb.Slack(url=_slack_url)
    mention = "<{}>\n".format(dict_toml[environment]['target_username']) if 'target_username' in dict_toml[environment] else ""

    slack.notify(text="{} 以下の労働の監視を開始するよ！".format(mention), attachments=pre_exec_attachments(direc))

    return_code = 1
    start = time.time()
    output = subprocess.run(direc, stderr=sys.stderr, stdout=sys.stdout)
    elapsed_time = time.time() - start

    if output.returncode == 0:
        slack.notify(text="{} 以下の労働は無事に終了したよ!:ok_woman:".format(mention), attachments=post_exec_succeed_attachments(direc, elapsed_time))
    else:
        slack.notify(text="{} 以下の労働に異常事態が発生したよ!:no_good:".format(mention), attachments=post_exec_failed_attachments(direc, elapsed_time,))


if __name__ == '__main__':
    main()
