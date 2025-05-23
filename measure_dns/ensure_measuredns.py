import os
import platform
import subprocess

# Get the absolute path of the shared library
SRC_NAME = "measuredns.c"
SRC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC_NAME)

IS_WINDOWS = platform.system() == "Windows"

LIBRARY_NAME = "measuredns.dll" if IS_WINDOWS else "measuredns.so"
LIBRARY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), LIBRARY_NAME)


def _exec_gcc(cc_name, flags, output_file, input_file):
    import subprocess

    try:
        cmd = cc_name + " " + " ".join(flags) + f" -o {output_file}" + f" {input_file}"
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        return False
    return True


def _check_gcc(cc_name):
    try:
        subprocess.check_call(
            [cc_name, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return True


def ensure_measuredns():
    if not _check_gcc("gcc"):
        # Build system gcc not found
        exit(-1)

    FLAGS = [
        "-shared",
        "-fPIC",
        "-fno-strict-overflow",
        "-Wsign-compare",
        "-DNDEBUG",
        "-g",
        "-O2",
        "-Wall",
    ]

    # print(f"{LIBRARY_PATH=}")
    return _exec_gcc("gcc", FLAGS, LIBRARY_PATH, SRC_PATH)
