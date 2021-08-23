#!/bin/bash
# ESAP 'production' run script
# version 23 aug 2021

echo "=== ESAP Installation script 2 of 2 ==="

export ESAP_ROOT=~/esap_root
export ESAP_SHARED=~/esap_shared

export ESAP_GUI_DIR=$ESAP_ROOT/esap-gui

cd $ESAP_GUI_DIR

mkdir -p $ESAP_SHARED/public_html
mkdir -p $ESAP_SHARED/public_html/esap-gui
mkdir -p $ESAP_SHARED/static

echo "building esap-gui frontend in $ESAP_GUI_DIR"
npm run build

cp -r $ESAP_GUI_DIR/build/*.* $ESAP_SHARED/public_html/esap-gui
cp -r $ESAP_GUI_DIR/build/static/* $ESAP_SHARED/static

# start esap
docker-compose -f $ESAP_SHARED/docker-compose.yml up --build -d

# copy the generated databases in the container to the shared location (do not override)
if [ ! -f $ESAP_SHARED/esap_ida_config.sqlite3 ]
then
  docker exec -it esap_api_gateway cp esap/esap_ida_config.sqlite3 /shared/esap_ida_config.sqlite3
fi

if [ ! -f $ESAP_SHARED/esap_rucio_config.sqlite3 ]
then
  docker exec -it esap_api_gateway cp esap/esap_rucio_config.sqlite3 /shared/esap_rucio_config.sqlite3
fi

if [ ! -f $ESAP_SHARED/esap_accounts_config.sqlite3 ]
then
  docker exec -it esap_api_gateway cp esap/esap_accounts_config.sqlite3 /shared/esap_accounts_config.sqlite3
fi

if [ ! -f $ESAP_SHARED/esap_config.sqlite3 ]
then
  docker exec -it esap_api_gateway cp esap/esap_config.sqlite3 /shared/esap_config.sqlite3
fi

echo "=== ESAP Installation PART 2 done ==="

