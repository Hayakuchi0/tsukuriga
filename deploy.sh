docker-compose down
rm -rf nginx/assets/bundles/*
rm -rf nginx/assets/webpack-stats.json
docker-compose run node bash -c "yarn && yarn run build"
docker-compose run web python manage.py collectstatic --no-input
docker-compose up -d
