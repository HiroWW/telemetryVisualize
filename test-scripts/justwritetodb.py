from influxdb_client_3 import InfluxDBClient3
import os
import time
import serial
import struct
# 環境変数からトークンを取得
# token = os.getenv('INFLUX_TOKEN')
token = "WeoauU5NpcJYeKxFS0-jIFjS4Qs_eZv79CkVn2wbdA9UsnIsLhFuxK_tk-2xqJiYx1a5fgGP0Oooyw0s50Vt4A=="
# InfluxDBクライアントの設定
client = InfluxDBClient3(
    host='https://us-east-1-1.aws.cloud2.influxdata.com/',
    token=token,
    database='testDatabase'
)

lines = [
    "hello,room=Living\ Room temp=21.1,hum=35.9,co=0i 1706342400",
    "hello,room=Kitchen temp=21.0,hum=35.9,co=0i 1706342400",
    "hello,room=Living\ Room temp=21.4,hum=35.9,co=0i 1706346000",
    "hello,room=Kitchen temp=23.0,hum=36.2,co=0i 1706346000",
    "hello,room=Living\ Room temp=21.8,hum=36.0,co=0i 1706349600",
    "hello,room=Kitchen temp=22.7,hum=36.1,co=0i 1706349600",
    "hello,room=Living\ Room temp=22.2,hum=36.0,co=0i 1706353200",
    "hello,room=Kitchen temp=22.4,hum=36.0,co=0i 1706353200",
    "hello,room=Living\ Room temp=22.2,hum=35.9,co=0i 1706356800",
    "hello,room=Kitchen temp=22.5,hum=36.0,co=0i 1706356800",
    "hello,room=Living\ Room temp=22.4,hum=36.0,co=0i 1706360400",
    "hello,room=Kitchen temp=22.8,hum=36.5,co=1i 1706360400",
    "hello,room=Living\ Room temp=22.3,hum=36.1,co=0i 1706364000",
    "hello,room=Kitchen temp=22.8,hum=36.3,co=1i 1706364000",
    "hello,room=Living\ Room temp=22.3,hum=36.1,co=1i 1706367600",
    "hello,room=Kitchen temp=22.7,hum=36.2,co=3i 1706367600",
    "hello,room=Living\ Room temp=22.4,hum=36.0,co=4i 1706371200",
    "hello,room=Kitchen temp=22.4,hum=36.0,co=7i 1706371200",
    "hello,room=Living\ Room temp=22.6,hum=35.9,co=5i 1706374800",
    "hello,room=Kitchen temp=22.7,hum=36.0,co=9i 1706374800",
    "hello,room=Living\ Room temp=22.8,hum=36.2,co=9i 1706378400",
    "hello,room=Kitchen temp=23.3,hum=36.9,co=18i 1706378400",
    "hello,room=Living\ Room temp=22.5,hum=36.3,co=14i 1706382000",
    "hello,room=Kitchen temp=23.1,hum=36.6,co=22i 1706382000",
    "hello,room=Living\ Room temp=22.2,hum=36.4,co=17i 1706385600",
    "hello,room=Kitchen temp=22.7,hum=36.5,co=26i 1706385600"
]

lines2 = [
    "telemetry,flight=no1 time=2.462e+03,mode=9.850e+03,gps_acc=1.250e+01,pi1=6.669e+00,pi2=9.341e+00,pi3=-2.463e+02,vi1=-1.490e+00,vi2=3.570e-01,vi3=-1.000e-01,euler_l1=1.156e-01,euler_l2=-5.736e-02,euler_c1=1.561e-02,euler_c2=-6.516e-02,euler_r1=-8.439e-02,euler_r2=-7.297e-02,heading=4.683e-03,att_dt=7.025e+02,ctrl_dt=5.025e+02,main_dt=2.025e+02,battery_level1=9.996e+01,battery_level2=9.994e+01,pitotPressure=1.018e-28,pitchDiff_left=1.000e-03,pitchDiff_right=2.000e-03,rollDiff_left=3.000e-03,rollDiff_right=4.000e-03,power1=2.031e+00,power2=3.000e+00"
]
# 現在のUnixタイムスタンプを秒単位で取得
current_time = int(time.time())
print(current_time)
client.write(lines2,write_precision='s')