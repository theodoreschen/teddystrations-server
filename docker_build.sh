#!/bin/sh

rm -rf static/
mkdir static

curl -sL https://github.com/theodoreschen/ng-teddystrations-game/releases/download/v1.1/ng-teddystrations-game.tgz --output ng-teddystrations-game.tgz
tar xzvf ng-teddystrations-game.tgz
mv ng-teddystrations-game/* static/.
mv static/index.html static/game.html
rmdir ng-teddystrations-game

curl -sL https://github.com/theodoreschen/ng-teddystrations-players/releases/download/v1.1/ng-teddystrations-players.tgz --output ng-teddystrations-players.tgz
tar xzvf ng-teddystrations-players.tgz
mv ng-teddystrations-players/* static/.
mv static/index.html static/player.html
rmdir ng-teddystrations-players

rm ng-teddystrations-game.tgz ng-teddystrations-players.tgz

docker build -t teddystrations .
docker network create ted-net