import os

from SGDPyUtil.fbuild_utils import FBModule, FastBuild


class gladModule(FBModule):
    def __init__(self):
        # calculate src path
        root_path = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(root_path, "src")

        # init FBModule
        super().__init__("glad", src_path)

        # add additional include path
        self.add_include_path(os.path.join(root_path, "include"))

        return


# add module to FastBuild
FastBuild.instance().add_module(gladModule())
