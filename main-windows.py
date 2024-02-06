from influxdb_client_3 import InfluxDBClient3
import os
import serial
import ctypes
import time

'''
CONFIGURATION AREA ==========================
'''
# USBシリアル通信の設定
SERIALPORT = 'COM6'  # ポートは環境によって異なる
BAUDRATE = 9600  # ボーレートはデバイスによって異なる

# TelemetryPack構造体の定義
class TelemetryPack(ctypes.Structure):
    _fields_ = [
        ('setuptime', ctypes.c_float),
        ('mode', ctypes.c_float),
        ('gps_acc', ctypes.c_float),
        ('pi1', ctypes.c_float),
        ('pi2', ctypes.c_float),
        ('pi3', ctypes.c_float),
        ('vi1', ctypes.c_float),
        ('vi2', ctypes.c_float),
        ('vi3', ctypes.c_float),
        ('euler_l1', ctypes.c_float),
        ('euler_l2', ctypes.c_float),
        ('euler_c1', ctypes.c_float),
        ('euler_c2', ctypes.c_float),
        ('euler_r1', ctypes.c_float),
        ('euler_r2', ctypes.c_float),
        ('heading', ctypes.c_float),
        ('att_dt', ctypes.c_float),
        ('ctrl_dt', ctypes.c_float),
        ('main_dt', ctypes.c_float),
        ('battery_level1', ctypes.c_float),
        ('battery_level2', ctypes.c_float),
        ('pitotPressure', ctypes.c_float),
        ('pitchDiff_left', ctypes.c_float),
        ('pitchDiff_right', ctypes.c_float),
        ('rollDiff_left', ctypes.c_float),
        ('rollDiff_right', ctypes.c_float),
        ('power1', ctypes.c_float),
        ('power2', ctypes.c_float),
        ('checkSum', ctypes.c_char * 4)
    ]

# 環境変数からトークンを取得
token = os.getenv('INFLUX_TOKEN')
# InfluxDBクライアントの設定
client = InfluxDBClient3(
    host='https://us-east-1-1.aws.cloud2.influxdata.com/',
    token=token,
    database='telemetryDatabase'
)

'''
FUNCTIONS ==========================
'''
# COBSデコード
def cobs_decode(decoded_data_length, raw_data):
    # decoded_data_length = len(raw_data) - 1  # 最初のバイトは長さのため、デコードされたデータの長さは1小さい
    decoded = bytearray(decoded_data_length)
    # 最初のバイトは次の0の位置を示す
    next_zero = raw_data[0] - 1
    # データをコピー（最初のバイトは除く）
    for i in range(decoded_data_length):
        decoded[i] = raw_data[i + 1]
    # 0を置き換える
    while next_zero < decoded_data_length:
        # 現在の0の位置を0に置き換え
        decoded[next_zero] = 0
        # 次の0の位置を確認する前に範囲チェックを追加
        if next_zero + 1 >= decoded_data_length:
            break  # 範囲外ならループを終了
        next_zero += decoded[next_zero + 1]
        # エラーチェック
        if next_zero > decoded_data_length or next_zero == 0:
            break
    return decoded

# データ解析
def decode_packet(packet):
    # COBS逆変換
    decoded = cobs_decode(ctypes.sizeof(TelemetryPack), packet)
    # パケットサイズが正しいかチェック
    if len(decoded) != ctypes.sizeof(TelemetryPack):
        return None  # サイズが一致しない場合はNoneを返す
    # バイト列を構造体に展開
    telemetry_pack = TelemetryPack.from_buffer_copy(decoded)
    # 構造体のフィールドを辞書に変換
    data = {field[0]: getattr(telemetry_pack, field[0]) for field in TelemetryPack._fields_}
    return data

# databaseへの書き込み
def write_to_influx(data):
    # Line Protocol形式の文字列を構築
    # measurementを"telemetry"とし、各fieldをデータから取得
    # タグはflight=no1として固定
    fields = ','.join([f'{key}={value:.6e}' for key, value in data.items() if key != 'checkSum'])
    # 現在のUnixタイムスタンプを秒単位で取得
    current_time = int(time.time())
    line = f"telemetry,flight=no1 {fields} {current_time}"
    # print("============influxdbLINEPROTOCOL============")
    # print(line)
    # InfluxDBに書き込む
    client.write([line], write_precision='s')

'''
MAIN ==========================
'''

# シリアルポートを開く
ser = serial.Serial(SERIALPORT, BAUDRATE)

# メインループ
while True:
    # データを読み込む
    if ser.in_waiting > 0:
        # 0x00 まで読み込む (COBSの終端を意味する)
        packet = ser.read_until(b'\x00')
        print(f"Received packet: {packet}")
        print(f"Packet size: {len(packet)}")

        # パケットをデコードしてデータを取得
        data = decode_packet(packet)
        if data is not None:
            # データの処理 (例: プリント、データベースへの書き込みなど)
            print("=======STRUCT=======")
            print(f"Decoded data: {data}")
            # InfluxDBに書き込む
            write_to_influx(data)
        else:
            print("Data is None, possible structure mismatch or decode error.")
