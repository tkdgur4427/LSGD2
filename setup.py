import os

import SGDPyUtil.powershell_utils as powershell_utils
import SGDPyUtil.main as utils

from SGDPyUtil.logging_utils import Logger
from SGDPyUtil.bootstrap_utils import bootstrap_main

ROOT_DIR = None


def setup_dev():
    ROOT_DIR = os.path.abspath(".")
    return


def setup_py_dev():
    """setup python developement environments"""
    # global variables
    global ROOT_DIR

    # set python version 3.7.X
    py_version = "37"

    # check python is installed
    if not utils.is_python_installed(py_version):
        Logger.instance().info(f"[ERROR] python package {py_version} is NOT installed")
        raise RuntimeError()

    # get python command
    py_command = utils.prepare_py_env(py_version)

    # execute pip command
    pip_content = f"""
# install x86 and x64 virtual env
{py_command} -m pip install virtualenv;

# set the cwd
cd "{ROOT_DIR}";

# create virtual enviornment
{py_command} -m virtualenv .venv;

# activate .venv
.venv\\Scripts\\activate;

# log the state
python --version;

# install packages
pip install -r requirements.txt;
"""
    powershell_utils.execute_powershell_content(pip_content)

    Logger.instance().info("[LOG] successfully DONE setup_py_dev()")
    return


def main():
    # setup dev
    setup_dev()

    # setup python dev
    setup_py_dev()

    # execute bootstrap
    bootstrap_root = os.path.abspath(os.path.join(".", "LSGD", "ThirdLibrary"))
    bootstrap_cmd_args = ""
    bootstrap_main(bootstrap_root, bootstrap_cmd_args)

    return


main()
