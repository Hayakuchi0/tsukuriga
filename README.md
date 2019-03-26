# Tsukuriga
Altwugを継承する自主制作動画専用の投稿サイト

## 開発
必要なもの
* python(3.7, もしくは3.6)
* pip
* pipenv
* npm
* ffmpeg

### セットアップ
```bash
$ pipenv install --dev
$ pipenv shell
(.venv)$ python manage.py migrate

# ログインに必要なTWITTER_KEY, TWITTER_SECRETのみ変更
$ mv .env.example .env
$ vim .env

# もしくは、スーパーユーザーの作成(localhost:8000/admin/でのみログイン可能)
(.venv)$ python manage.py createsuperuser
```

### 開発サーバーの起動
下記2つのコマンドを別々のターミナルで実行
```bash
(.venv)$ python manage.py runserver_plus
```
```bash
$ yarn run dev
```
