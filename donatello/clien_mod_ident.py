import platform
import subprocess
from uuid import getnode


def command_line(command):
    return subprocess.getoutput(command)


def hard_driver_serial_number(os_pc):
    if os_pc == 'windows':
        return command_line('wmic diskdrive get serialnumber')
    elif os_pc == 'linux':
        return command_line('')
    elif os_pc == 'darwin':
        return command_line('')


os_pc = platform.system()
os_pc = os_pc.lower()

if os_pc == 'windows':
    os_pc
    hd_serial_number = hard_driver_serial_number(os_pc)
    mac_address = getnode()
    pc_serial_number = command_line('wmic bios get serialnumber')
elif os_pc == 'linux':
    os_pc
    hd_serial_number = ''
    mac_address = getnode()
    pc_serial_number = command_line()
elif os_pc == 'darwin':
    os_pc
    hd_serial_number = ''
    mac_address = getnode()
