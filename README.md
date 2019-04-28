![ツクリガ](assets/images/ogp.png)

# Tsukuriga
[Altwug.net](https://altwug.net)を継承する自主制作動画専用の投稿サイト
名前は「作\(ツクり\)画(ガ)」から。アイコンは「乍」

## 開発
必要なもの
* bash
* python(3.7, もしくは3.6)
* pip
* pipenv
* yarn(npm)
* ffmpeg

### セットアップ
```bash
$ pipenv install --dev
$ pipenv shell
(.venv)$ python manage_dev.py migrate

# ログインに必要なTWITTER_KEY, TWITTER_SECRETのみ変更
$ mv .env.example .env
$ vim .env
# 最初にログインしたユーザーをスーパーユーザー化する
(.venv)$ python manage_dev.py setsuperuser

# もしくは、スーパーユーザーの作成(localhost:8000/admin/でのみログイン可能)
(.venv)$ python manage_dev.py createsuperuser
```

### 開発サーバーの起動
下記2つのコマンドを別々のターミナルで実行
```bash
(.venv)$ python manage_dev.py runserver_plus
```
```bash
$ yarn run dev
```

### アップロード動画のサムネイル作成とエンコード処理
```bash
(.venv)$ python manage_dev.py encode
```

### Dockerを用いる場合

#### セットアップ

```bash
# Dockerイメージの作成
$ sudo docker-compose build

# ログインに必要なTWITTER_KEY, TWITTER_SECRETのみ変更
$ mv .env.example .env
$ vim .env

# スーパーユーザーの作成
$ sudo docker-compose run web python manage_dev.py createsuperuser
```

#### 開発サーバーの起動

下記2つのコマンドを別々のターミナルで実行

```bash
$ sudo docker-compose up
```
```bash
$ yarn run dev
```

#### アップロード動画のサムネイル作成とエンコード処理
```bash
$ sudo docker-compose run web python manage_dev.py encode
```

## Author

https://github.com/Compeito/tsukuriga/graphs/contributors
