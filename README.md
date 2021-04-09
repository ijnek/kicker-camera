# キッカーカメラ

スキー場のパークで練習時に「自分の滑りを動画で見返したい」、という思いから始めたプロジェクトです。


キッカーを飛ぶ直前にLINEアプリから録画をスタートする事で、ゲレンデに設置されたカメラからの動画を飛んだ直後にLINEのメッセージで動画が送られてくる仕組みです。


## LINE使用流れ
![](docs/screenshots.png)

## 動画例（Hakuba47）
![](docs/kicker_camera.gif)


# 必要な機材
1. スマートフォン\
    iPhone・Androidでの動作を確認済み
2. 三脚\
    スマホが固定出来る三脚が必要です。持ってない場合は[Amazonの安価スマホ三脚](https://www.amazon.co.jp/gp/product/B07PVNBL74/)がオススメ。
3. simカード\
    アップロード速度の早いsimが必須。また、アップロード速度はカメラを設置する場所の電波と関係しているので、simプランを組む前に、キャリアを試したい場合はプリペイドsimで試した方が良い。[AmazonのSoftbank10GBデータsim](https://www.amazon.co.jp/gp/product/B07SG23VMN/)がオススメ。


# システム構造

設置カメラのセットアップは少し手間がかかります。以下のシステム構造を分かっておくと、セットアップ手順が分かりやすくなります。

![](docs/structure.png)

# セットアップ手順

セットアップは以下の手順で行ってください。

1. [Gmail アカウントを作成](#Gmail-アカウントを作成)
1. [Twitch アカウントを作成](#Twitch-アカウントを作成)
1. [LINE Developers アカウントを作成](#LINE-Developers-アカウントを作成)
1. [チャンネルシークレットとチャンネルトークンの取得](#チャンネルシークレットとチャンネルトークンの取得)
1. [Heroku デプロイする](#Heroku-デプロイする)
1. [LINEでWebhook URLを設定する](#LINEでWebhook-URLを設定する)

## Gmail アカウントを作成

[Gmailサインアップ](https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F%3Fpc%3Dtopnav-about-n-en&flowName=GlifWebSignIn&flowEntry=SignUp)から新しいアカウントを作成します。
電話番号と再設定用のメールアドレスは入力しなくて良いです。
**メールアドレスとパスワードは忘れないように保管してください。**

## Twitch アカウントを作成

[Twitch Sign Up](https://www.twitch.tv/signup) からアカウントを無料で作成します。メールアドレスは先程作成したアカウントを使用します。
**ユーザーネームとパスワードは忘れないように保管してください。**


## LINEセットアップ
### LINE Business アカウントを作成

![](docs/line_sign_up.png)

[LINE Businessサインアップ画面](https://account.line.biz/signup?redirectUri=https%3A%2F%2Fmanager.line.biz%2F&_ga=2.259523146.1728940530.1617949361-1384753008.1617949361)から [**メールアドレスで登録**] を選択して、Line Businessのアカウントを作ります。

### LINE Developers チャネル作成

![](docs/line_dev_login.png)

サインアップが終わり、[LineDevelopersページ](https://developers.line.biz/en/)にログインします。[**ビジネスアカウントでログイン**]を選択して、開発用のアカウントを作ります。次の画面が開きます。

![](docs/create_a_new_provider.png)

Providersタブを開き [**新規プロバイダーを作成**] をクリックします。

![](docs/provider_name.png)

プロバイダー名は何でも良いです、上のようにKickerCameraで問題ありません。[**作成**]をクリックします。

![](docs/new_messaging_api.png)

上の画面で、**Messaging API** を選択して、MessagingAPIを作ります。

**チャネル名は、ユーザーの携帯に表示されるボットのラインアカウントの名前になります。**(例：キッカーカメラ）\
チャネル説明、大業種、小業種は、適当に選択してチャンネルを作成します。


## チャンネルシークレットとチャンネルトークンの取得

![](docs/click-channel.png)

[チャンネル基本設定]タブの**チャンネルシークレット**は後で使うので、メモアプリ等に控えておきます。\
[Messaging API設定]タブの**チャンネルアクセストークン**を発行します。後で使うので控えておきます。



## Heroku デプロイする

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ijnek/kicker-camera)

上の**Deploy to Heroku**をクリックして、アカウントを作成します。

次に出てきた画面にアプリ名（例：hakuba-47-kicker-camera-1)を入力し、
先ほど控えておいた以下を入力して、サーバーを作成します。
* ラインチャンネルシークレット
* ラインチャンネルトークン
* Twitch ユーザー名

## LINE Developers で Webhook URLを設定する

LINE Developersに戻り、
LINE Developersコンソールで、Messaging APIチャネルの［Messaging API設定］タブをクリックします。

「https://{HEROKU_APP_NAME}.herokuapp.com/callback」というURL形式で、Webhook URLを入力します。

例：アプリ名が「kicker-camera-test-1」の場合、Webhook URLは `https://kicker-camera-test-1.herokuapp.com/callback` になります。

![](docs/webhook_url.png)

[**Webhookの利用**］を有効にします。