DXR
=========
Installation / 首次安装
--------------------------
    pip install DXR
Installation / 更新安装
--------------------------
    pip install -U DXR
Usage / 使用
--------------------------
```
from Dxr_mqtt.dxr_mqtt import *
from Dxr_mqtt.msg import *
from Dxr_utils.dxr_utils import *

# 设置mqtt连接地址，端口号，客户端id
setServerUrl(url="xxx.xxx.xxx.xxx", port=1883, clientID="dxr_mqtt")
# 设置模块名称，用于自动绑定日志话题
setModuleName("dxr_mqtt")

# 日志模块这边需要注意的是
# 如果mqtt连接不是本地的，那么需要先设置mqtt连接地址，端口号，客户端id
# 之后才能调用log模块
from Dxr_log.log import *

# 设置日志的打印,主要分为info,error,debug三种级别
setLogPrint(info=False, error=False, debug=False)

# 定义一个发布器，并绑定消息类型app_cmd_vel
pub = Dxr_Publisher(app_cmd_vel)


# 使用dxr_subscriber的装饰器直接绑定订阅回调
@dxr_subscriber(app_cmd_vel)
def app_cmd_vel_callback(data, topic):
    # 用msg中的静态方法getMsg来获取消息,并指定消息类型为app_cmd_vel
    mm: app_cmd_vel = msg.getMsg(data, app_cmd_vel)
    # 鼠标放到消息类型上，可以看到消息类型的结构体，可以根据结构体的字段来解析消息
    print_info(f'priority: {mm.priority},v: {mm.msg.v},w: {mm.msg.w}')
    # 进行后续的操作
    pass


# 绑定一个日志的话题，用来接收日志消息
# 话题格式为/response/log_manager/{模块名}/{日志类型}
# 日志类型分为all,debug,error
# 模块名和日志类型如果不确定或者不固定可以用'+'进行通配
@dxr_subscriber('/response/log_manager/dxr_mqtt/all')
def all_log_callback(data, topic):
    mm = msg.getMsg(data)
    print(f'data: {mm.data}, status: {mm.status}, error: {mm.error}')


# 为了测试回调函数的调用，这里使用一个简单的发布消息
i = 100
while i > 0:
    # 使用对应的消息类型的构造函数来创建一个消息
    m = app_cmd_vel()
    m.priority = time.time()
    m.msg.v = time.time()
    m.msg.w = time.time()
    m.msg.sn = time.time()
    # 发布消息
    pub.publish(m)
    i -= 1
    time.sleep(1)

```
Usage / 进阶使用（闭环消息的实现）
--------------------------
使用await_publish订阅闭环消息
```
import threading
import time
from Dxr_mqtt.dxr_mqtt import *
from Dxr_mqtt.msg import *

setServerUrl("127.0.0.1")

# 创建消息发布器，消息类型为data_record
data_record_pub = Dxr_Publisher(data_record)


def test():
    # 循环发布消息类型为data_record的消息
    while True:
        # 实例化消息
        m = data_record()
        m.msg.action = "stop"
        m.msg.sn = "123456789"
        """
        使用await_publish来实现消息闭环
        await_publish(msg, timeout, topic)
        {
            msg 为发送的消息
            timeout 不指定的时候，为一直等待设定话题的消息，指定后超时时间中未收到消息，会接收到一个None消息
            topic 为指定闭环消息的话题类型，如果不指定，则默认为原话题类型后追加'_response',可以传递字符串类型的话题，也可以传递消息类型
        }
        """
        res = data_record_pub.await_publish(m, timeout=5, topic=app_cmd_vel)
        print(f'test: {res}')


# threading.Thread(target=test1).start()
test()
```
在另外一个文件中实现消息的发布
```
import threading
import time
from Dxr_mqtt.dxr_mqtt import *
from Dxr_mqtt.msg import *

setServerUrl("127.0.0.1")
app_cmd_vel_pub = Dxr_Publisher(app_cmd_vel)
    
# 每1s发送app_cmd_vel消息    
while True:
    time.sleep(1)
    m = app_cmd_vel()
    m.priority = 1
    m.msg.v = 0.1
    m.msg.w = 0.1
    m.msg.sn = time.time()
    app_cmd_vel_pub.publish(m)
    print(f'test: {m}')
```
