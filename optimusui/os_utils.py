import subprocess
from enum import Enum
from os import environ

'''
Various OS and flatpak related utilities
'''

FLATPAK_SPAWN = ["flatpak-spawn", "--host"]


class Distribution(Enum):
    UNKNOWN = -1
    SUSE = 0
    UBUNTU = 1
    DEBIAN = 2


class DisplayServer(Enum):
    UNKNOWN = -1
    X11 = 0
    WAYLAND = 1


def get_display_server() -> DisplayServer:
    """
    Checks the currently running display server
    :return:
    display server enum
    """
    xdg_session = environ.get("XDG_SESSION_TYPE")
    match xdg_session:
        case "x11":
            return DisplayServer.X11
        case "wayland":
            return DisplayServer.WAYLAND
    return DisplayServer.UNKNOWN


def is_flatpak() -> bool:
    """
    Test if the app is running as  flatpak
    """
    return environ.get("FLATPAK_ID") is not None


def run_command_no_pipe(base_command: []):
    """
    Runs a command as a subprocess but does not return the result and does not
    wait for the command to finish. Useful for running binaries which do not terminate
    """
    if is_flatpak():
        return subprocess.run(FLATPAK_SPAWN + base_command)
    return subprocess.run(base_command)


def run_command(base_command: []):
    """
    Runs a given array as a subprocess and returns the result.
    If the app is running inside flatpak it will use flatpak-spawn
    """
    if is_flatpak():
        return subprocess.run(FLATPAK_SPAWN + base_command, stdout=subprocess.PIPE)
    return subprocess.run(base_command, stdout=subprocess.PIPE)


def get_distro() -> Distribution:
    """
    Test the running Linux distribution.
    This is used later to guess which prime-select like package might be installed
    """
    os_release_cmd = ["cat", "/etc/os-release"]
    os_release_result = run_command(os_release_cmd)
    os_release_dict = {}
    for line in os_release_result.stdout.decode("utf-8").rstrip().split("\n"):
        column = line.split("=")
        if len(column) == 2:
            os_release_dict[column[0]] = column[1].replace("\"", "")
    for id_like in os_release_dict["ID_LIKE"].split(" "):
        match id_like:
            case "opensuse" | "suse":
                return Distribution.SUSE
            case "debian":
                match os_release_dict["ID"]:
                    case "ubuntu":
                        return Distribution.UBUNTU
                return Distribution.DEBIAN
    return Distribution.UNKNOWN


def is_distro_known():
    """
    Effectively checks if the system is Debian as this is the only (known) Distribution
    to not have a prime-select like package
    :return:
    If distro is supported or not
    """
    detected_distro = get_distro()
    match detected_distro:
        case Distribution.SUSE | Distribution.UBUNTU:
            return True
    return False
