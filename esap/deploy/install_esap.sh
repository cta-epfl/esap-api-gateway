#!/bin/bash
# ESAP 'production' install script
# version 13 aug 2021

echo "=== ESAP Installation PART 1 ==="

export ESAP_ROOT=~/esap_root
export ESAP_SHARED=~/esap_shared

# create work directory and shared directory
mkdir -p $ESAP_ROOT
mkdir -p $ESAP_SHARED
mkdir -p $ESAP_SHARED/public_html

# get backend code
echo "downloading esap-api backend..."
cd $ESAP_ROOT
export ESAP_API_DIR=$ESAP_ROOT/esap-api-gateway/esap

if [ ! -d $ESAP_API_DIR ]
then
   echo "git clone repository..."
   git clone https://git.astron.nl/astron-sdc/esap-api-gateway.git
else
   echo "git pull repository..."
   cd esap-api-gateway
   git pull
fi

# build it
echo "building esap-api backend..."
cd $ESAP_API_DIR
docker build -t esap_api_gateway:latest .

# copy files to shared directory
echo "copy shared files..."
if [ ! -f $ESAP_SHARED/esap_config.sqlite3 ]
then
  cp $ESAP_API_DIR/esap/*.sqlite3 $ESAP_SHARED
fi

if [ ! -f $ESAP_SHARED/oidc.env ]
then
  cp $ESAP_API_DIR/deploy/shared/oidc.env $ESAP_SHARED
fi

if [ ! -f $ESAP_SHARED/esap.env ]
then
  cp $ESAP_API_DIR/deploy/shared/esap.env $ESAP_SHARED
fi

if [ ! -f $ESAP_SHARED/nginx.conf ]
then
  cp $ESAP_API_DIR/deploy/shared/nginx.conf $ESAP_SHARED
fi

if [ ! -f $ESAP_SHARED/docker-compose.yml ]
then
  cp $ESAP_API_DIR/deploy/shared/docker-compose.yml $ESAP_SHARED
fi

if [ ! -f $ESAP_SHARED/Dockerfile ]
then
  cp $ESAP_API_DIR/deploy/shared/Dockerfile $ESAP_SHARED
fi

# get frontend code
echo "downloading esap-gui frontend..."
cd $ESAP_ROOT
export ESAP_GUI_DIR=$ESAP_ROOT/esap-gui

if [ ! -d $ESAP_GUI_DIR ]
then
   echo "git clone repository..."
   git clone https://git.astron.nl/astron-sdc/esap-gui.git
else   
  echo "git pull repository..."
  cd esap-gui
  git pull
fi  

echo "installing frontend dependencies..."
cd $ESAP_GUI_DIR
npm install

# edit the api_host for production 
echo ""
echo "=== ESAP Installation PART 1 done ==="
echo "configure the frontend by pointing 'api_host' to <your_host>/esap-api/"
echo "> nano $ESAP_GUI_DIR/src/contexts/GlobalContext.js"
echo ""
echo "configure the OIDC settings for your client"
echo "nano ~/esap_shared/oidc.env"
echo ""
echo "...then run the 'run_esap.sh' script."


