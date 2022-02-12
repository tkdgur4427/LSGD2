import os
from SGDPyUtil.fbuild_utils import FastBuild, BuildConf
from SGDPyUtil.powershell_utils import execute_command


def main():
    # build configuration
    # build_configuration = BuildConf.DEBUG
    # build_configuration = BuildConf.PROFILE
    build_configuration = BuildConf.RELEASE

    # collect modules
    FastBuild.instance().collect_modules()

    # import modules
    FastBuild.instance().import_modules()

    # setup third libraries
    FastBuild.instance().setup_third_libraries(
        os.path.abspath(os.path.join(".", "LSGD", "ThirdLibrary"))
    )

    # setup
    output_path = os.path.abspath(os.path.join(".", "Output"))
    intermediate_path = os.path.abspath(os.path.join(".", "Intermediate"))
    FastBuild.instance().setup(output_path, intermediate_path)

    # create bff file
    FastBuild.instance().generate_bff_file(build_configuration)

    # define debug mode
    is_debug_mode = False
    debug_arg = ""
    if is_debug_mode:
        debug_arg = "-verbose"

    # execute fbuild.exe
    fbuild_path = os.path.abspath(os.path.join(".", "Tools", "FBuild"))
    bff_path = os.path.abspath(os.path.join(".", "Intermediate", "fbuild.bff"))
    fbuild_cmd = f"fbuild -config {bff_path} {debug_arg}"
    execute_command(fbuild_cmd, True, fbuild_path)

    # debug executable
    try_debug = True
    if try_debug:
        # get remedybg binary file path
        remedybg_path = os.path.abspath(
            os.path.join(".", "Tools", "RemedyBG", "remedybg.exe")
        )
        # get output path by build_configuration
        executable_path = FastBuild.instance().get_output_path(build_configuration)
        executable_filename = os.path.join(executable_path, "Launch.exe")
        # generate cmd
        remedybg_cmd = f"{remedybg_path} -g {executable_filename}"
        # try to debug
        execute_command(remedybg_cmd, True)

    return


main()
