#!/usr/bin/bash
set -eu

ROOT=/sys/class/drm/card0/device

# power_dpm_state is a legacy interface - avoid using
# p_num_states and pp_cur_state most probably alike

for f in \
	power_dpm_force_performance_level \
	pp_dpm_sclk \
	pp_dpm_mclk \
	pp_dpm_pcie \
	gpu_busy_percent \
	mem_busy_percent \
	pp_power_profile_mode \
; do
    echo ${ROOT}/${f}
    cat ${ROOT}/${f}
    echo
done

sensors amdgpu-pci-0100
