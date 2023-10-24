#!/bin/bash

cd $(dirname $0)

echo -n -e '\xde\xad\xbe\xef' > foo.out
echo -n -e '\xbe\xef\xde\xad' > bar-mismatch.out
