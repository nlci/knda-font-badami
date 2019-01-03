#!/bin/bash

face="$1"
style="$2"
ufo="$3"

devaf="Maurya"
tamlf="Vaigai"

psfcopyglyphs -f --rename rename --unicode usv -i ../cs/panini/main4knda.csv -s "${deva}/${devaf}-${style}.ufo" ${ufo}
psfcopyglyphs -f --rename rename --unicode usv -i ../cs/thiruvalluvar/main.csv -s "${taml}/${tamlf}-${style}.ufo" ${ufo}
