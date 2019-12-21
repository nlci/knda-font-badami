#!/bin/bash

face="$1"
style="$2"
ufo="$3"

oryaf="Asika"
devaf="Maurya"
tamlf="Vaigai"

if [ "$style" = "BoldItalic" ]
then
    styleo="Bold"
else
    styleo="$style"
fi
psfcopyglyphs -f --rename rename --unicode usv -i ../cs/asika/main4knda.csv -s "${orya}/${oryaf}-${styleo}.ufo" ${ufo}
psfcopyglyphs -f --rename rename --unicode usv -i ../cs/panini/main4knda.csv -s "${deva}/${devaf}-${style}.ufo" ${ufo}
psfcopyglyphs -f --rename rename --unicode usv -i ../cs/thiruvalluvar/main.csv -s "${taml}/${tamlf}-${style}.ufo" ${ufo}
