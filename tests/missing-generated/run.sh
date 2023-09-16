#!/bin/bash

cd $(dirname $0)

echo foo > foo.out
rm goes-missing.out
