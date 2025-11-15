#! /usr/bin/bash

if [[ ! $EUID -ne 0 ]]; then
    echo "Dieses skript darf NICHT als root ausgeführt werden! (sudo)"
    exit 1
fi

echo Lösche alte CLI-Tools...
export CLIDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
rm -rf $HOME/.local/roboarm-cli
mkdir $HOME/.local/roboarm-cli

echo Kopiere neue...
export OLDPWD=$(pwd)
cd $CLIDIR

for file in !(*.*); do
    cp -- "$file" $HOME/.local/roboarm-cli
done

Überprüfe .bashrc
export isPathSet=$(cat $HOME/.bashrc | grep -c 'export PATH=$PATH:~/.local/roboarm-cli')

if [[ $isPathSet -ne 0 ]]; then
    echo Eintrag in $HOME/.bashrc nicht gefunden, erstelle ihn...
    echo 'export PATH=$PATH:~/.local/roboarm-cli' >> $HOME/.bashrc
    echo 'Konfiguriere $PATH...'
    export PATH=$PATH:~/.local/roboarm-cli
fi