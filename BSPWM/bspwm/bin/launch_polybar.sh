#!/usr/bin/env bash

killall -q polybar # kill all running instances of polybar

# start polybar
polybar left &
polybar middle &
polybar right &