#!/bin/bash

face="$1"
style="$2"
ufo="$3"

bengf="Bhagirati"
devaf="Maurya"
tamlf="Vaigai"

if [ "$style" = "BoldItalic" ]
then
    styleb="Bold"
else
    styleb="$style"
fi
psfcopyglyphs -f --rename rename --unicode usv -i ../cs/bhagirati/main4knda.csv -s "${beng}/${bengf}-${styleb}.ufo" ${ufo}
psfcopyglyphs -f --rename rename --unicode usv -i ../cs/panini/main4knda.csv -s "${deva}/${devaf}-${style}.ufo" ${ufo}
psfcopyglyphs -f --rename rename --unicode usv -i ../cs/thiruvalluvar/main.csv -s "${taml}/${tamlf}-${style}.ufo" ${ufo}
