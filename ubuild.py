import os
import subprocess


def main(build):
    build.packages.install("../web-transmute", develop=True)
    build.packages.install(".", develop=True)


def test(build):
    main(build)
    build.packages.install("jedi")
    build.packages.install("sphinx")
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    pytest = os.path.join(build.root, "bin", "py.test")
    subprocess.call([
        pytest, "--cov", "tornado_transmute",
        "tornado_transmute/tests",
        "--cov-report", "term-missing"
    ])


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "upload"
    ])


def _download_swagger_ui(build):
    pass
    # _script: "uscripts/download_swagger_ui.py"
