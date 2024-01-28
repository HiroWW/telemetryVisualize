import serial
from cobs import cobs  # cobsライブラリを使用
import struct

# COBS逆変換とデータ解析を行う関数
def decode_packet(packet):
    # COBS逆変換
    try:
        decoded = cobs.decode(packet)
    except cobs.DecodeError:
        return None  # デコード失敗時にはNoneを返す

    # データのフォーマットを定義
    # fは4バイトのfloat、4sは4バイトの文字列
    data_format = '<' + 'f' * 28 + '4s'

    # パケットサイズが正しいかチェック
    if len(decoded) != struct.calcsize(data_format):
        return None  # サイズが一致しない場合はNoneを返す

    # バイト列を構造体に展開
    unpacked_data = struct.unpack(data_format, decoded)

    # データを適切な形式で返す (例: 辞書型)
    keys = ['time', 'mode', 'gps_acc', 'pi1', 'pi2', 'pi3', 'vi1', 'vi2', 'vi3', 'euler_l1', 'euler_l2',
            'euler_c1', 'euler_c2', 'euler_r1', 'euler_r2', 'heading', 'att_dt', 'ctrl_dt', 'main_dt',
            'battery_level1', 'battery_level2', 'pitotPressure', 'pitchDiff_left', 'pitchDiff_right',
            'rollDiff_left', 'rollDiff_right', 'power1', 'power2', 'checkSum']
    return dict(zip(keys, unpacked_data))

# USBシリアル通信の設定
serial_port = '/dev/ttyACM0'  # ポートは環境によって異なる
baud_rate = 9600  # ボーレートはデバイスによって異なる

# シリアルポートを開く
ser = serial.Serial(serial_port, baud_rate)

# メインループ
while True:
    # データを読み込む
    if ser.in_waiting > 0:
        # 0x00 まで読み込む (COBSの終端を意味する)
        packet = ser.read_until(b'\x00')
        print(packet)

        # パケットをデコードしてデータを取得
        data = decode_packet(packet)
        if data is not None:
            # データの処理 (例: プリント、データベースへの書き込みなど)
            print(data)
