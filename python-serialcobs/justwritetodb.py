from influxdb_client_3 import InfluxDBClient3
import os

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
    "telemetrytest,flight=no time=26725.5, 1706385600"
]
client.write(lines2,write_precision='s')