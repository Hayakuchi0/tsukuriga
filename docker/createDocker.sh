#!/bin/sh

which docker > /dev/null 2>&1
if [ $? -eq 0 ] ; then
	here=`dirname ${0}`
	here=`cd ${here};pwd`
	cp ${here}/../Pipfile ${here}/Pipfile
	docker pull ubuntu:latest
	docker build -t tsukuriga:dev `dirname ${0}`
else
	echo "You need docker."
fi
