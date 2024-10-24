# カメラ付きロケットMk.2内蔵プログラム

## 概要

本プログラムは、鹿児島高専2024年度高専祭にて物理部が打ち上げる「カメラ付きロケットMk.2」に搭載したプログラムです。

## 説明

### send_video.sh

動画の撮影には、OS付属のプログラムである `rpicam-vid` を使用します。コーデックはh264、tcpを用いて簡易的な配信サーバを建てます。画像サイズは1640x1232、フレームレートは20です。

### mpu9250.py

加速度、角速度の取得にはmpu9250（9軸センサ）を使用しています。プログラムはRaspberry Pi Studio様のものを使用させていただいています。以下のURLをご覧ください。

「９軸センサーMPU9250へのカルマンフィルタ適用」 https://team432.jpn.org/?p=666

### bme280.py

気圧、温度の取得にはbme280を使用しています。プログラムはyukataoka（幸人 片岡）様のものを使用させていただいています。以下のURLをご覧ください。

「Qiita Raspberry Pi で温湿度気圧センサを使う」 https://qiita.com/yukataoka/items/8f9046587c978e91f689

### telemetry.py

センサデータを標準出力に表示するプログラムです。

### receiver.py

telemetry.pyの表示内容をグラフ化するプログラムです。加速度を3Dベクトル、角速度をグラフ、気圧と温度を折れ線グラフで表現しています。

## 使い方

send_video.shを起動し、動画転送用のサーバを建てます。任意のビデオプレーヤーからこれにアクセスします。

例： `tcp://raspberrypi2.local:55554`

加えて、receiver.py、telemetry.pyの順で起動します。データ転送にはncコマンドを使用します。

PC側： `yourPC:~$ nc -l 63100 | python receiver.py`

ラスパイ側： `pi@raspberrypi:~$ python telemetry.py | nc 192.168.12.1 63100`

イメージ画像：

![image](https://github.com/sato1701/RocketWithCamera/blob/main/2024-10-17-085317_1920x1080_scrot_mozaiku.png)
