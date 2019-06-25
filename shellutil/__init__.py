import argparse
import os
import shutil
import subprocess
import sys
import re
import time
import glob

import future        # pip install future
import six           # pip install six

def __shell(cmd, env_vars=None, should_return_output=False, continue_if_fail=False, suppress_output=False):
    env = os.environ.copy()

    if sys.version_info.major == 3:

        # needs to be surrounded with single quotes,
        # otherwise inner double quotes need to be escaped
        formatted_cmd = "/bin/bash -c '{}'".format(cmd)        
        if env_vars is not None:
            for k, v in env_vars.items():
                env[k] = v
        try:
            #print(f'`{cmd}`') 
            print("{}".format(cmd))

            if should_return_output:
                output = subprocess.run(formatted_cmd, env=env, shell=True, check=True, text=True, stdout=subprocess.PIPE).stdout
                if not suppress_output:
                    print(output)
                return output.strip()
            else:
                std_out = subprocess.DEVNULL if suppress_output else None
                subprocess.run(formatted_cmd, env=env, shell=True, check=True, text=True, stdout=std_out)

        except subprocess.CalledProcessError as error:
            if not continue_if_fail:
                raise error

    else:

        cmd = "/bin/bash -c '{}'".format(cmd)
        if env_vars is not None:
            for k, v in env_vars.items():
                env[k] = v
        try:
            print(cmd)

            if should_return_output:
                output = subprocess.check_output(cmd, env=env, shell=True)
                print(output)
                return output
            else:
                subprocess.call(cmd, env=env, shell=True)

        except subprocess.CalledProcessError as error:
            sys.exit(error.returncode)


def shell_value(cmd, continue_if_fail=False, suppress_output=False):
    """
    Runs a command in shell -- returns and prints the output at the end.

    :param suppress_output: if the python script should suppress the output from the shell command
    :param continue_if_fail: if the python script should continue after an failure or if it should raise an exception
    :param cmd: string version of the command to be run
    :return: output of the cmd
    """

    return __shell(cmd, should_return_output=True, continue_if_fail=continue_if_fail, suppress_output=suppress_output)


def shell(cmd, continue_if_fail=False, suppress_output=False):
    """
    Runs a command as if it were in run in shell.

    :param suppress_output: if the python script should suppress the output from the shell command
    :param continue_if_fail: if the python script should continue after an failure or if it should raise an exception
    :param cmd: string of the cmd to be run
    :return: nothing
    """

    __shell(cmd, continue_if_fail=continue_if_fail, suppress_output=suppress_output)