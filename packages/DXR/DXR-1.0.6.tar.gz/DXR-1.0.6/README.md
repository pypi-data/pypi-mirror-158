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
