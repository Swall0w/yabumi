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


def generate_attachments(command_list, status='success', elapsed_time=None,):
    _attachments = [
            {
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
                    "value": "{}".format(get_current_datetime()),
                    "short": "true"
                },
            ]
    }]

    if status == "success":
        _attachments[0]["color"] = 'good'
    else:
        _attachments[0]["color"] = 'danger'

    if elapsed_time != None:
        _attachments[0]["Title"] = 'Results'
        _attachments[0]["fields"].append(
                {
                    "title": "elapsed time",
                    "value": "{:.2}".format(elapsed_time),
                    "short": "true"
                })
    else:
        _attachments[0]["Title"] = "Command Execution"

    return _attachments


def get_current_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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

    pre_message = dict_toml[environment]['pre_message'] if 'pre_message' in dict_toml[environment] else "Monitoring the following processes"
    success_message = dict_toml[environment]['success_message'] if 'success_message' in dict_toml[environment] else "The following process was successfully completed."
    failure_message = dict_toml[environment]['failure_message'] if 'failure_message' in dict_toml[environment] else "The following process was terminated due to an abnormal situation."


    slack.notify(text="{}{}".format(mention, pre_message), attachments=generate_attachments(direc, 'success'))

    return_code = 1
    start = time.time()
    output = subprocess.run(direc, stderr=sys.stderr, stdout=sys.stdout)
    elapsed_time = time.time() - start

    if output.returncode == 0:
        slack.notify(text="{}{}".format(mention, success_message), attachments=generate_attachments(direc, 'success', elapsed_time))
    else:
        slack.notify(text="{}{}".format(mention, failure_message), attachments=generate_attachments(direc, 'failure', elapsed_time,))


if __name__ == '__main__':
    main()
