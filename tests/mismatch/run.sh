#!/bin/bash

cd $(dirname $0)

echo foo > foo-matches.out
(echo "first line in" && echo "bar-actual" && echo "last line!") > bar-mismatch.out
