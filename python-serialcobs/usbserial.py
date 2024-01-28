import serial
import struct

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
        
        # 次の0の位置を計算
        next_zero += decoded[next_zero + 1]
        
        # エラーチェック
        if next_zero > decoded_data_length or next_zero == 0:
            break
    
    return decoded
# COBS逆変換とデータ解析を行う関数
def decode_packet(packet):
    # COBS逆変換
    decoded = cobs_decode(116, packet)

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
        print(f"Received packet: {packet}")
        print(f"Packet size: {len(packet)}")

        # パケットをデコードしてデータを取得
        data = decode_packet(packet)
        if data is not None:
            # データの処理 (例: プリント、データベースへの書き込みなど)
            print(f"Decoded data: {data}")
        else:
            print("Data is None, possible structure mismatch or decode error.")