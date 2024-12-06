#!/bin/bash

# Establecemos que el código de retorno de un pipeline sea el del último programa con código de retorno
# distinto de cero, o cero si todos devuelven cero.
set -o pipefail

LLINDAR_RMAX=${1:-0.45}
LLINDAR_R1NORM=${2:-0.75}
LLINDAR_POT=${3:--50}
# Put here the program (maybe with path)
# GETF0="get_pitch --llindar-rmax $LLINDAR_RMAX"
# GETF1="get_pitch --llindar-r1norm $LLINDAR_R1NORM"
# GETF2="get_pitch --llindar-pot $LLINDAR_POT"
GETF="get_pitch --llindar-rmax $LLINDAR_RMAX --llindar-r1norm $LLINDAR_R1NORM --llindar-pot $LLINDAR_POT"

for fwav in pitch_db/train/*.wav; do
    ff0=${fwav/.wav/.f0}
    echo "$GETF $fwav $ff0 ----"
    $GETF $fwav $ff0 > /dev/null || { echo -e "\nError in $GETF $fwav $ff0" && exit 1; }
    # echo "$GETF0 $fwav $ff0 ----"
    # echo "$GETF1 $fwav $ff0 ----"
    # echo "$GETF2 $fwav $ff0 ----"
	# $GETF0 $fwav $ff0 > /dev/null || { echo -e "\nError in $GETF0 $fwav $ff0" && exit 1; }
    # $GETF1 $fwav $ff0 > /dev/null || { echo -e "\nError in $GETF1 $fwav $ff0" && exit 1; }
    # $GETF2 $fwav $ff0 > /dev/null || { echo -e "\nError in $GETF2 $fwav $ff0" && exit 1; }
done

pitch_evaluate pitch_db/train/*.f0ref

exit 0
