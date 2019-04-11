#!/bin/sh

here=`dirname ${0}`/../
here=`cd ${here};pwd`
cd ${here}
docker system prune
docker run -v ${here}:/var/www/html -p 8000:8000 -it --name tsukuriga tsukuriga:dev /bin/bash
