import subprocess
from os import environ
from logging import debug, error


def cliAskChoice():
    yes = {"yes", "yep", "y", "ye"}
    no = {"no", "nope", "n"}

    choice = input("Input: (y/n) > ").lower()
    debug("input is:" + choice)
    if choice in yes:
        debug("Choice is yes")
        return True
    elif choice in no:
        debug("Choice is no")
        return False
    else:
        print("Please respond with 'y' or 'n'")
        cliAskChoice()


def findLocation(config_data, chroot_name):
    if "custom-location" not in config_data["chroots"][chroot_name]:
        return (
            config_data["general"]["unified-location"]
            + config_data["chroots"][chroot_name]["location"]
        )
    else:
        return config_data["chroots"][chroot_name]["custom-location"]


def validChrootName(config_data, chroot_name):
    if chroot_name not in config_data["chroots"]:
        error(f"{chroot_name} is not in the configuration file!")
        error(f"Available options are: {list(config_data['chroots'])}")
        return False
    else:
        return True


def getChrootCommand(config_data, distro, chroot_name, command_name):
    try:
        command = config_data["general"]["distro-settings"][distro][command_name]
    except KeyError:
        debug("distro is not in configured list, using default")
        command = config_data["general"]["distro-settings"]["default"][command_name]

    command = command.replace(
        "$rootfs_location", findLocation(config_data, chroot_name)
    )
    command = command.replace("~", environ["HOME"])
    debug(f"Command loaded:\n{command}")
    return command

def chkMountStatus(config_data ,chroot_name):
    chrootPath = findLocation(config_data, chroot_name).replace('~', environ["HOME"])
    output = subprocess.run(["mount"], capture_output=True).stdout
    debug(f"Path is: {chrootPath}, mountpoints are: {str(output)}")
    if chrootPath in str(output):
        return True
    else:
        return False

def suRunCommand(
    config_data, chroot_name, su_provider, command, command_type
):
    if validChrootName(config_data, chroot_name):
        print(f"Executing {command_type}")
        child = subprocess.run([su_provider, "sh", "-c", command])
        print(f"{command_type} executed and returned {child.returncode}")
