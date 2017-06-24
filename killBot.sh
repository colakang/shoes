#!/bin/bash

kill -9 `ps -ef | grep foot | grep -v grep | awk '{print $2}'`
kill -9 `ps -ef | grep eastbay | grep -v grep | awk '{print $2}'`
kill -9 `ps -ef | grep champssports | grep -v grep | awk '{print $2}'`

