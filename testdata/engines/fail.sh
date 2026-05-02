#!/bin/sh
printf 'fail stdout\n'
printf 'fail stderr\n' >&2
exit 7
