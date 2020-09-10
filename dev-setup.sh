#!/usr/bin/env bash

set -e

echo "Downloading SoundFont..."

rm -f ./tabby/synth/soundfonts/GeneralUserGS-modified.sf2
curl -L -o ./tabby/synth/soundfonts/GeneralUserGS-modified.sf2 "https://drive.google.com/uc?export=download&id=1ozWrcvLIHz4enEUNE_3fM1RvpH4lTPbn"

echo "Done."
