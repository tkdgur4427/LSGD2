import os

from numpy import power

import SGDPyUtil.main as utils
import SGDPyUtil.powershell_utils as powershell_utils
from SGDPyUtil.logging_utils import Logger


def main():
    # set the python version 3.7
    py_version = "37"

    # check python is installed
    if not utils.is_python_installed(py_version):
        Logger.instance().info(f"[ERROR] python package {py_version} is NOT installed")
        raise RuntimeError()

    # make sure that miktex installed
    miktex_dir = os.path.normpath("C:\\Program Files\\MiKTeX")
    if not os.path.isdir(miktex_dir):
        Logger.instance().info(f"[ERROR] MiKTeX[{miktex_dir}] is NOT installed")
        raise RuntimeError()
    else:
        # get the env.paths
        paths = os.environ["PATH"]
        paths = paths.split(";")

        miktex_bin_dir = os.path.normpath("C:\\Program Files\\MiKTeX\\miktex\\bin\\x64")
        if not miktex_bin_dir in paths:
            Logger.instance().info(
                f"[LOG] MikTeX binary directory is not in PATH[{miktex_bin_dir}], please add it!"
            )
            # raise RuntimeError()

    # math python directory
    math_dir = os.path.abspath("./Math")

    # math python filename
    filename = "math_statistics_tutorial.py"

    # manim scene name
    scene_name = "UnionAndIntersection"

    # construct math filename
    math_filepath = os.path.normpath(os.path.join(math_dir, filename))

    # construct args
    math_args = f"{scene_name}"

    # manim command
    manim_cmd = f'manim -pql "{math_filepath}" {math_args}'

    Logger.instance().info(f"[LOG] executing manim cmd [{manim_cmd}]")

    # execute manim command
    manim_command = f"""
# activate .venv
.venv\\Scripts\\activate;
    
# execute manim
{manim_cmd};
"""

    powershell_utils.execute_powershell_content(manim_command)

    Logger.instance().info("[LOG] successfully DONE building math")


main()
