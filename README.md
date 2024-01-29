# telemetryVisualizer

GAIA(仮称)

Groundstation Assembeled by InfluxDB and grAfana

## システム概要
マイコンからのデータをGrafanaによって可視化するソフトウェア

- 通信の流れ
    - MCU <-(USBserial)> Python3 <-(https)-> InfluxDB Cloud serverless <-(https / FlightSQL)-> Grafana
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
        - そのうちlocalでdbも立てられるようにしたい
    - http://localhost:8086へブラウザでアクセス
- source ./envs/virtual-env/bin/activate
    - envs/virtual-env以下のpython仮想環境のアクティベート
- PCにTeensyを接続
- main.pyを実行
- docker compose down
    - dockerコンテナの終了
    - データは永続化される
- deactivate
    - venv環境の終了

## 動作環境
- OS
    - Python : ubuntu20.04 LTSのみ
    - Grafana : WSL2 / Ubuntu20.04LTS 
- Grafana : grafana-oss:latest
- InfluxDB : cloud serverless (Influx3.0 = SQLでのクエリに対応している唯一のver,OSS版未リリース)