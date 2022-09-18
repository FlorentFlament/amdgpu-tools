#!/usr/bin/env python3
import os
import sys
import re
import time

SYSFS_ROOT="/sys/class/drm/card0/device"

class AmdgpuMonitor:
    def __init__(self):
        self.fd_pp_dpm_sclk = open(os.path.join(SYSFS_ROOT, "pp_dpm_sclk"))
        self.fd_pp_dpm_mclk = open(os.path.join(SYSFS_ROOT, "pp_dpm_mclk"))
        self.fd_pp_dpm_pcie = open(os.path.join(SYSFS_ROOT, "pp_dpm_pcie"))
        self.fd_gpu_busy_percent = open(os.path.join(SYSFS_ROOT, "gpu_busy_percent"))
        self.fd_mem_busy_percent = open(os.path.join(SYSFS_ROOT, "mem_busy_percent"))

        self.re_pp_dpm_sclk = re.compile("\d+: (\d+)Mhz \*")
        self.re_pp_dpm_mclk = re.compile("\d+: (\d+)Mhz \*")
        self.re_pp_dpm_pcie = re.compile("\d+: \d\.\dGT/s, x(\d+) \*")

    def close(self):
        self.fd_pp_dpm_sclk.close()
        self.fd_pp_dpm_mclk.close()
        self.fd_pp_dpm_pcie.close()
        self.fd_gpu_busy_percent.close()
        self.fd_mem_busy_percent.close()

    @staticmethod
    def extract_value(cur_fd, cur_re):
        cur_fd.seek(0)
        for l in cur_fd.readlines():
            match = cur_re.match(l)
            if match is not None:
                return match.group(1)
        
    def read_pp_dpm_sclk(self):
        return self.extract_value(self.fd_pp_dpm_sclk, self.re_pp_dpm_sclk)

    def read_pp_dpm_mclk(self):
        return self.extract_value(self.fd_pp_dpm_mclk, self.re_pp_dpm_mclk)

    def read_pp_dpm_pcie(self):
        return self.extract_value(self.fd_pp_dpm_pcie, self.re_pp_dpm_pcie)

    def read_fd_gpu_busy_percent(self):
        self.fd_gpu_busy_percent.seek(0)
        return self.fd_gpu_busy_percent.readline().strip()

    def read_fd_mem_busy_percent(self):
        self.fd_mem_busy_percent.seek(0)
        return self.fd_mem_busy_percent.readline().strip()


def main():
    monitor = AmdgpuMonitor()

    while True:
        toks = (
            monitor.read_pp_dpm_sclk(),
            monitor.read_pp_dpm_mclk(),
            monitor.read_pp_dpm_pcie(),
            monitor.read_fd_gpu_busy_percent(),
            monitor.read_fd_mem_busy_percent(),
        )
        print("\t".join(toks))
        sys.stdout.flush()
        time.sleep(.1)

    monitor.close()

main()
