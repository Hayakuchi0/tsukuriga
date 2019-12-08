#!/bin/sh
cd `dirname $0`
docker-compose down

# イメージの再ビルド
docker-compose build

# 依存関係の更新とDBマイグレーション
docker-compose run web bash -c "pipenv install --ignore-pipfile && python manage.py migrate"

# js/cssの再ビルドと配置
rm -rf nginx/assets/bundles/*
rm -rf nginx/assets/webpack-stats.json
docker-compose run node bash -c "yarn && yarn run build"
docker-compose run web python manage.py collectstatic --no-input

docker-compose up -d
