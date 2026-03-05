import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient, Point , WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#influx configuration
influx_token = ""
influx_bucket =""
influx_url = "http://localhost:8086"

#mqtt configuration
mqtt_broker = "" 
mqtt_port = ""
mqtt_user = ""
mqtt_pw = ""
mqtt_topic = ""

client = InfluxDBClient(url=influx_url,token=influx_token,org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

id_counter = 0

def on_connect(client,userdata,flags,rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client,userdata,msg):
    global id_counter
    try:
        payload = json.loads(msg.payload.decode())
        print(f"收到数据:{payload['id']}")
        id_counter +=1

        point = Point("pressure_data")\
            .tag("device_id",payload["id"])\
            .field("bar_stp1",payload["PSTR_bar"]["stp1"])\
            .field("bar_stp2",payload["PSTR_bar"]["stp2"])\
            .field("bar_stp3",payload["PSTR_psi"]["stp3"])\
            .field("ma_dig1",payload["PDIG_ma"]["dig1"])
        
        write_api.write(bucket=influx_bucket,org=influx_org,record=point)
        print("数据已存入InfluxDB")
        print(f"id:{id_counter}")

    except Exception as e:
        print(f"处理数据出错：{e}")

#--start up mqtt client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_user,mqtt_pw)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker,mqtt_port,60)
mqtt_client.loop_forever()


