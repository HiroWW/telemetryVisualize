# telemetryVisualizer



<img src="./docs/p231102p03.jpg" width="500">

GAIA - **G**roundstation **A**ssembeled by **I**nfluxDB and gr**A**fana (仮称)

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
### Grafana環境
- docker compose up -d
    - grafanaの立ち上げ
        - そのうちlocalでdbも立てられるようにしたい
    - "http://localhost:8086"にブラウザでアクセス
- docker compose down
    - dockerコンテナの終了
    - データは永続化される
### influxdb3-python環境(ubuntu)
- python3 -m venv .venv
    - 仮想環境の作成
- source .venv/bin/activate
    - python仮想環境のアクティベート
- pip install -r requirements.txt
    - 必要ライブラリのインストール
- PCにTeensyを接続
- main.pyを実行
- deactivate
    - venv環境の終了
### influxdb3-python環境(windows)
- 未動確
- python3 -m venv .venv
    - 仮想環境の作成
-　./.venv/Scripts/activate
    - python仮想環境のアクティベート
- pip install -r requirements.txt
    - 必要ライブラリのインストール
- PCにTeensyを接続
- main.pyを実行
- deactivate
    - venv環境の終了
## 動作環境
- OS
    - Python : ubuntu20.04 LTSのみ
    - Grafana : WSL2 / Ubuntu20.04LTS 
- Grafana : grafana-oss:latest
- InfluxDB : cloud serverless (Influx3.0 = SQLでのクエリに対応している唯一のver,OSS版未リリース)
