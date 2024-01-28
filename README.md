# telemetryVisualizer

## システム概要
MCU <-USBserial-> Python3 <-https-> InfluxDB Cloud serverless <-FLightSQL-> Grafana

で通信を行い、MCUからのデータの可視化を行う

- MCU
    - Teensy4.1
    - COBS変換してシリアル通信でPCへ送信
- Python
    - venv仮想環境
    - シリアル通信でのデータ読み取り
    - COBSデコード
    - influxdb line protocolへの変換
    - databaseへの書き込み

## How To Use
- docker compose up -d
    - grafanaの立ち上げ
    - http://localhost:8086へブラウザでアクセス
- source ./envs/virtual-env/bin/activate
    - envs/virtual-env以下のpython仮想環境のアクティベート
- PCにTeensyを接続
- usbserial.pyを実行

## 動作環境
- OS : ubuntu20.04 LTS
- Grafana : grafana-oss:latest
- InfluxDB : cloud serverless (Influx3.0 = SQLでのクエリに対応している唯一のver,OSS版未リリース)