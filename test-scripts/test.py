import ctypes
import time

'''
CONFIGURATION AREA ==========================
'''
# USBシリアル通信の設定
SERIALPORT = 'COM19'  # ポートは環境によって異なる
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
    print("declength is ", ctypes.sizeof(TelemetryPack))
    decoded = cobs_decode(ctypes.sizeof(TelemetryPack), packet)
    print("decoded packet", decoded)
    # パケットサイズが正しいかチェック
    if len(decoded) != ctypes.sizeof(TelemetryPack):
        return None  # サイズが一致しない場合はNoneを返す
    # バイト列を構造体に展開
    telemetry_pack = TelemetryPack.from_buffer_copy(decoded)
    # 構造体のフィールドを辞書に変換
    data = {field[0]: getattr(telemetry_pack, field[0]) for field in TelemetryPack._fields_}
    return data

binary_data = b'\x00\xc0\xdcD\x01\x03@@\x01\x016@/\xf3\x11Bg\xf5\x0bC1\xd1\x1b\xc1\xdb\x9c\xe8>@\x87H?\xcd\xcc\xcc\xbd1\xe2 >\xe2\xc4\xa6\xbd*\xefi=\xac@\xe1\xbdp\xaa/\xbd;\xde\r\xbeM\\\x8c<\x04\x800D\x01\x03\xfdC\x01\x1fNC\x85\xeb\xc7BH\xe1\xc7B\x88e\xe6\xa7o\x12\x83:o\x12\x03;\xa6\x9bD;o\x12\x83;\x01\x01\x02@\x01\x05@@n,\x01\x01'

# バイナリデータを16進数の文字列に変換
hex_string = ' '.join(f'{byte:02x}' for byte in binary_data)

# 16進数の文字列を表示
print(hex_string)