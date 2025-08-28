# VM_checker.py
import uuid
import subprocess


# Check if Inside VM
# 8/15/2025
# AUX-441

class CheckVM:
    vm_macs = [
        "00:05:69", "00:0C:29", "00:1C:14", "00:50:56",
        "08:00:27", "00:03:FF", "00:1C:42",
    ]

    def check_vm_mac(self):
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0, 8 * 6, 8)][::-1])
        return any(mac.startswith(prefix) for prefix in self.vm_macs)

    def check_bios_vm(self):
        try:
            output = subprocess.check_output('wmic bios get serialnumber,manufacturer', shell=True).decode()
            vm_indicators = ["VMware", "VirtualBox", "Xen", "QEMU", "Microsoft Corporation", "Parallels"]
            return any(ind in output for ind in vm_indicators)
        except:
            return False

    def check_hypervisor_flag(self):
        try:
            output = subprocess.check_output('wmic cpu get VirtualizationFirmwareEnabled', shell=True).decode()
            return "TRUE" in output.upper()
        except:
            return False

    def is_vm(self):
        checks = [self.check_vm_mac(), self.check_bios_vm(), self.check_hypervisor_flag()]
        return any(checks)


# -----------------------------
# Execution
if __name__ == "__main__":
    vm_checker = CheckVM()
    if vm_checker.is_vm():
        print("This system appears to be running inside a VM.")
    else:
        print("This system appears to be a real machine.")
