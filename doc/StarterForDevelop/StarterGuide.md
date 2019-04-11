# 開発の準備を整え、ローカルで動作テストをするまで

READMEにはyarnを用いた簡易的な手順のみが記載されているので、詳細な手順については以下に記載する。

## 開発ツールを用意

### 必須の開発ツール

* bash
* git
* 以下のいずれか
1. yarn
2. npm
* 以下のいずれか
1. pipenv
2. docker

#### pipenvを使う場合

* python(3.7, もしくは3.6)
* pip
* pipenv
* ffmpeg

#### dockerを使う場合

* docker

### 開発ツールを最短で用意するには

ubuntu上でbash,git,npm,dockerの4つをaptを用いて用意するのが最も早い。
windowsならば仮想環境でubuntuを実行すれば良い。

#### Windowsユーザーの場合

[参考サイト](http://tamori.3zoku.com/linux/ubuntu_on_win.html)のように、Linuxの一種であるUbuntuをWindows上で実行できるようにする。
あとはLinuxユーザーと同様の手順で、ツールの用意が全て済む。

#### Linuxユーザーの場合

パッケージ管理ツール等でそれぞれを用意すれば良い。
例えばUbuntuであれば、GNOME Terminalから以下のコマンドを実行するだけでツールの用意が全て済む。

```bash
$ sudo apt install nodejs npm git docker
```


## セットアップ及びサーバー起動

ツクリガをローカルPC上で動作確認するには、まずツクリガを動かせる環境を構築(セットアップ)し、その環境上でツクリガ本体を起動する(サーバー起動)という手順を踏む必要がある。
以下の0〜5の手順通りに実行することで、localhost:8000というアドレスにアクセスするという形でツクリガの動作確認をすることができる。
なお、0〜3がセットアップ、4〜5がサーバー起動である。

0. gitを用いてこのリポジトリをcloneする。

ツクリガ本体をgitというプログラムを使ってダウンロードするコマンドを実行する。

```bash
$ git clone https://github.com/Compeito/tsukuriga.git
$ cd tsukuriga
```

1. 使用するjavascriptモジュールをインストールする。

ツクリガを動かすためのプログラムの部品(モジュール)をダウンロードするコマンドを実行する。

### npmを使う場合

```bash
$ npm install
```

### yarnを使う場合

```bash
$ yarn install
```

2. 仮想環境の準備を行う。

ツクリガを動かす場合PCで直接動作テストすると必要なプログラムが多すぎてPCに何を入れたかがわからなくなる。
なので仮想的な環境を用意して、その中でツクリガを動かす。
ツクリガは仮想的な環境を作るソフトのpipenvとdockerの2つに対応している。

### pipenvを使う場合

```bash
$ pipenv install --dev
$ pipenv shell
(.venv)$ python manage_dev.py migrate
```

### dockerを使う場合

```bash
$ sudo ./docker/createDocker.sh
```

3. Djangoの環境変数を設定する。

Twitterログインを用いた機能のデバッグをする予定なら、ログインに必要なTWITTER_KEY, TWITTER_SECRETのみを記述し、残りの行は削除する。
TWITTER_KEYおよびTWITTER_SECRETを取得する方法は[ここ](https://github.com/Hayakuchi0/tsukuriga/blob/DocumentForContribute/doc/StarterForDevelop/HowToGetTwitterAPIKey.md)を参照すること。

```bash
$ mv .env.example .env
$ vim .env
```

4. モジュールをパッキングする。

手順2でダウンロードしたモジュールをツクリガと結合(パッキング)しなければツクリガは動かない。
その結合をこの段階で行う。

### パッキングのみ行う場合

#### yarnを使う場合

```bash
$ yarn run clean;yarn run webpack --mode development
```

#### npmを使う場合

```bash
$ npm run clean;npm run webpack --mode development
```

### パッキングしつつ、変更の監視も行う場合

この操作は別の端末で実行する必要がある。
これが実行されている間、ツクリガのプログラムを書き換えたとき自動的にモジュールをパッキングしてくれる。

#### yarnを使う場合

```bash
$ yarn run dev
```

#### npmを使う場合

```bash
$ npm run clean;npm run webpack --mode development -watch
```

5. 開発サーバーを起動する。

ツクリガが動いているPCはサーバーとして機能する。(開発サーバーという。)

### pipenvを使う場合

```bash
(.venv)$ python manage_dev.py migrate;python manage_dev.py runserver_plus
```

### dockerを使う場合

```bash
$ sudo ./docker/debugDocker.sh
```


## デバッグ

「セットアップ及びサーバの起動」における4番以降を実行し、ブラウザにてlocalhost:8000へアクセスすることでローカル環境で動作を確認することができる。
また、以下の操作を必要に応じて行う必要がある。

### 管理ユーザーの作成

#### pipenvを使う場合

##### 最初にログインしたユーザーをスーパーユーザー化する

```bash
(.venv)$ python manage_dev.py setsuperuser
```

##### スーパーユーザーの作成(localhost:8000/admin/でのみログイン可能)

```bash
(.venv)$ python manage_dev.py createsuperuser
```

#### dockerを使う場合

##### スーパーユーザーの作成

```bash
$ sudo docker exec -it tsukuruga /bin/bash
(docker)$ export PYTHONIOENCODING=utf-8;python3 /var/www/html/manage_dev.py createsuperuser;exit
```

### アップロード動画のサムネイル作成とエンコード処理

#### pipenvを使う場合

```bash
(.venv)$ python manage_dev.py encode
```

#### dockerを使う場合

```bash
$ sudo docker exec -it tsukuruga /bin/bash
(docker)$ export PYTHONIOENCODING=utf-8;python3 /var/www/html/manage_dev.py encode;exit
```
