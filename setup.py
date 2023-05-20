import setuptools


def get_version():
    """

    try using `git rev-parse HEAD --short` here to get the git commit.
    then append that to the version string.
    """
    version = "0.0.3"
    try:
        command = "git rev-parse --verify --short=4 @"
        import os
        version = version + "+" + os.popen(command, mode='r').read()
    except Exception as e:
        pass
    return version


setuptools.setup(
    name='notebookinit',  # it seems that doing that in setup.cfg doesn't work for me
    version=get_version(),
)



