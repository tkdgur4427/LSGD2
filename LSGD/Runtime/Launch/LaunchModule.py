import os

from SGDPyUtil.fbuild_utils import FBModule, FastBuild


class LaunchModule(FBModule):
    def __init__(self):
        # calculate src path
        src_path = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(src_path, "src")

        # init FBModule
        super().__init__("Launch", src_path)

        # override properties
        self.is_executable = True

        # add dependencies
        self.add_dependency("Engine")
        self.add_dependency("glad")

        return


# add module to FastBuild
FastBuild.instance().add_module(LaunchModule())
