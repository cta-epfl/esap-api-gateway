#!/bin/bash
# ESAP 'production' run script
# version 10 aug 2021

echo "=== ESAP Installation PART 2 ==="

export ESAP_ROOT=~/esap_root
export ESAP_SHARED=~/esap_shared

export ESAP_GUI_DIR=$ESAP_ROOT/esap-gui

cd $ESAP_GUI_DIR

echo "building esap-gui frontend in $ESAP_GUI_DIR"
npm run build

cp -r $ESAP_GUI_DIR/build $ESAP_SHARED/public_html/esap-gui
cp -r $ESAP_GUI_DIR/build/static $ESAP_SHARED


# start esap
docker-compose -f $ESAP_SHARED/docker-compose.yml up --build -d


echo "=== ESAP Installation PART 2 done ==="