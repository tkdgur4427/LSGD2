import os

from SGDPyUtil.fbuild_utils import FBModule, FastBuild


class EngineModule(FBModule):
    def __init__(self):
        # calculate src path
        src_path = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(src_path, "src")

        # init FBModule
        super().__init__("Engine", src_path)

        return


# add module to FastBuild
FastBuild.instance().add_module(EngineModule())
