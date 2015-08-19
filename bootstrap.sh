#!/usr/bin/env sh
git submodule init
git submodule update
git submodule foreach git pull origin master
