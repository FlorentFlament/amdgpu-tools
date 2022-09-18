#!/usr/bin/bash
set -eu

gnuplot -e "datafname='$1'" -e "pngfname='$2'" monitor.plot
