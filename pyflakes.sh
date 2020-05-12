#!/bin/bash
find -maxdepth 1 -type d | grep -vP "^.($|/nfvnr|/\..*)" | xargs pyflakes > pyflakes.out
cat pyflakes.out
test \! -s pyflakes.out
