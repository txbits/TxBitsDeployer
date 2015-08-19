#!/bin/sh
if [ -e playbook/${2}_hosts ]; then
  exit 0
else
  echo ${2}_hosts is not a valid environment.
  echo Usage: ${1} environment
  exit 1
fi
