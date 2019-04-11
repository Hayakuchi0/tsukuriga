# 開発者用TwitterAPIの取得方法

以下の全ての手順を上から順に実行する。

# 既存のTwitterアカウントを開発者として登録する。

## User profile

以下にアクセスし、Continueをクリック

https://developer.twitter.com/en/apply/user


## Add your account details

* Who are you requesting access for?に対し、I am requesting access for my own personal useを選択

* 上記を入れたら以下2つがいれるのでそれぞれ入力

1. Account name に自分のアカウント名

2. Primary country of operationでJapan

* 上記全て入れたらContinueをクリック


## Use case details

* What use case(s) are you interested in?に対し、以下の3つにチェック

1. Cunsumer/end-user experience
2. Student project / Learning to code
3. Other

* Describe in your own words what you are buildingに以下を書き込んで送信

```
1. I want to use twitter authentication and Twitter users information. Because contribute to development to this project ( https://github.com/Compeito/tsukuriga ) for this site ( https://tsukuriga.net/ ).
2. I plan to use Twitter users username, icon, header-image, profile text, email-address, with video tweet and the authentication token for operation test. But I want to use data of mine only. Because API key of the production environment haven by project leader. So I need only to will use twitter API for development.
3. Yes, I will. Because our sites users want to be able to do it when they want to import the video of the posted by users self from Twitter to our site.
4. Each data displayed as follow.
4-1. username, icon, header-image, profile text: As the users profile in our site.
4-2. the video tweet: As the posted movie.
4-3. email-address: As the address for notification in user config. ( display to user self only. )
4-4. the authentication token: Do not display.
```

*Will your product, service of analysis make Twitter content or derived information available to a goverment entity?に対し、Noにチェック

* 上記全て入れたらContinueをクリック


## Read and agree to the Terms of Service

* 利用規約をAccept

* By clicking on the box, You indicate that you have read and agree to 〜と書かれているチェックボックスにチェックをつける

* Submit applicationをクリック


## メールが届く

1. Twitterに登録したメールアドレスから、Verify your Twitter Developer Account的なタイトルのメールが届くのでそこに書かれてるConfirm your emailをクリック

2. 使いやすいか使いにくいかのアンケがくるので適当にチェックボックスを全部埋めてSUBMITする。
真面目に答えるなら以下のようになる。
* 上の欄はこの手順がイライラしたかスッキリできたかの基準。笑顔ならスッキリ登録できた。プンスコならイライラした。
* Confusingがややこしい登録手順だった、Clearがわかりにくい登録手順だった。


# 開発者登録が終わったのでアプリケーションのキーを生成する。

## Create an App

以下にアクセスし、Create an appをクリックする

https://developer.twitter.com/en/apps

# App details

* App-name(required)に、tsukurigaの開発段階だとわかる名前を入れる

* Application descriptionに以下を書き込む

```
Open source the post movie site. ( https://tsukuriga.net/ )
I will contribute to it.
I use the key only for pull request creation or local test.
```

* Website URL(required)に、自分のgithubリポジトリのアドレスを入れる

* Enable Sign in with Twitterにチェックを入れる

* Callback URLs(required)に、http://localhost:8000/complete/twitter/といれる

* Tell us how this app will be used(required)に以下を書き込む

```
1. When our sites users want to use Twitter authentication at registration in our site, They can do it. And import the users data from Twitter to our site.
2. When our sites users want to import the video of the posted by users self from Twitter to our site, they can do it.

I plan to use Twitter users username, icon, header-image, profile text, email-address, with video tweet and the authentication token for operation test. But I want to use data of mine only. Because API key of the production environment haven by project leader. So I need only to will use twitter API for development.
I will use twitter authentication and Twitter users information.

Each data display to user as follow.
1. username, icon, header-image, profile text: As the users profile in our site.
2. the video tweet: As the posted movie.
3. email-address: As the address for notification in user config. ( display to user self only. )
4. the authentication token: Do not display.
```

# キーとトークンを確認する

1. 以下にアクセスし、Detailsをクリック(複数ある場合はさっき入れたapp-nameと同じものを入れる)

https://developer.twitter.com/en/apps/

2. Keys and tokensをクリックする

3. Consumer API keysに(API key)と(API secret key)が見えるので、API keyは.envのTWITTER_APIに、API secret keyは.envのTWITTER_SECRETに記述。
