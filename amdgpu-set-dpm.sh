#!/usr/bin/bash
set -eu

# Examples of values to be written in power_dpm_force_performance_level: auto, low, high
# See https://www.kernel.org/doc/html/latest/gpu/amdgpu/thermal.html#power-dpm-force-performance-level

DPM_SETUP_FILE=/sys/class/drm/card0/device/power_dpm_force_performance_level
PERF_LEVEL=${1:-low}

echo "Updating amdgpu device power management setting (power_dpm_force_performance_level)"
echo "Initial value of \"${DPM_SETUP_FILE}\" is $(cat ${DPM_SETUP_FILE})"
echo "Setting \"${DPM_SETUP_FILE}\" to ${PERF_LEVEL}"

if [ ! -f ${DPM_SETUP_FILE} ]; then
    echo "*ERROR* file \"${DPM_SETUP_FILE}\" is missing. Exiting."
    exit 1
fi

echo ${PERF_LEVEL} > ${DPM_SETUP_FILE}
echo "New value of \"${DPM_SETUP_FILE}\" is $(cat ${DPM_SETUP_FILE})"
