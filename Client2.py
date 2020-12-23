import socket
import time
import random
from threading import Thread


class TemperatureSensor:
    def __init__(self):
        self.temperature = 0

    def ChangeTem(self):
        self.temperature = random.randint(0, 30)


class MoistureSensor:
    def __init__(self):
        self.moisture = 0

    def ChangeTem(self):
        self.moisture = round(random.uniform(0, 1), 2)


class AirCondition:

    def __init__(self):
        Mode = ['制冷', '制热', '送风']
        Speed = ['低速', '中速', '高速']
        self.AirOn = 0
        self.modechoice = 0
        self.speedchoice = 0
        self.mode = Mode[self.modechoice]
        self.speed = Speed[self.speedchoice]
        self.temperature = 25

    def ChangeOn(self, choice):
        self.AirOn = choice

    def ChangeMode(self, choice):
        Mode = ['制冷', '制热', '送风']
        self.modechoice = choice
        self.mode = Mode[choice]

    def ChangeSpeed(self, choice):
        Speed = ['低速', '中速', '高速']
        self.speedchoice = choice
        self.speed = Speed[choice]


class HomeCard:
    def __init__(self):
        self.on = 1

    def InsertCard(self):
        self.on = 1

    def TakeCard(self):
        self.on = 0


class Light:
    def __init__(self):
        self.LightOn = 0
        self.Force = 1

    def ChangeOn(self, choice):
        self.LightOn = choice

    def ChangeForce(self, force):
        self.Force = force


class Window:

    def __init__(self):
        self.WindowOn = 0

    def ChangeOn(self, choice):
        self.WindowOn = choice


def ReceiveData(s):
    while True:
        # data = s.recv(1024).decode()
        # print('Received:', data)
        # if data == 'exit':
        #    break
        SendData(s)
    s.close()


def SendData():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect((host, port))
    print('连接成功')
    global control
    while True:
        TemData = Tem.temperature
        MoiData = Moi.moisture
        # Car.InsertCard()
        CardData = Car.on

        controlmode = ['手动控制', '自动控制']
        cardmode = ['断电', '通电']
        MechineMode = ['关闭', '开启']
        # control = 1     # 0手控，1自动
        heart = 0  # 0不是心跳检测，1是心跳检测

        SendTest = '6C' + str(heart) + str(control) + str(TemData) + 'F' + str(MoiData) + 'F' + str(CardData) + \
                   str(1) + str(Light1.LightOn) + str(Light1.Force) + str(Air.AirOn) + str(Air.modechoice) + \
                   str(Air.speedchoice) + str(Air.temperature) + str(Win.WindowOn)

        s.send(SendTest.encode())

        data = s.recv(1024).decode()
        print('Received:', data)
        protocol = data
        # print('测试协议:', protocol)
        top = protocol[0:2]
        print('首部为：', top)
        heart = int(protocol[2:3])
        if heart == 1:
            print('设备不调整')
            nowtime = str(protocol[3:])
            print('时间为：', nowtime)
        elif control == 1:
            print('设备需要自动调整，服务器传过的详细参数为：')
            control = int(protocol[3:4])

            tem_index = protocol.find('F', 4, 8)
            temperature = int(protocol[4:tem_index])

            mov_index = protocol.find('F', tem_index + 1, 13)
            moisture = float(protocol[tem_index + 1:mov_index])

            protocol = protocol[mov_index + 1:]
            cardon = int(protocol[0:1])

            lightnum = int(protocol[1:2])

            lighton = int(protocol[2:3])
            Light1.ChangeOn(lighton)

            lightforce = int(protocol[3:4])
            Light1.ChangeForce(lightforce)

            airon = int(protocol[4:5])
            Air.ChangeOn(airon)

            airmode = int(protocol[5:6])
            Air.ChangeMode(airmode)

            airspeed = int(protocol[6:7])
            Air.ChangeSpeed(airspeed)

            airtemperature = int(protocol[7:9])
            Air.temperature = airtemperature

            windowon = int(protocol[9:10])
            Win.ChangeOn(windowon)

            nowtime = str(protocol[10:])

            print('控制模式为', controlmode[control])
            # print('温度为：', temperature)
            # print('湿度为：', moisture)
            print('总开关状态为：', cardmode[cardon])
            print('灯光数量为：', lightnum)
            print('灯光状态为：', MechineMode[lighton])
            print('灯光强度为：', lightforce)
            print('空调状态为：', MechineMode[airon])
            print('空调模式为：', Air.mode)
            print('空调风速为', Air.speed)
            print('空调温度为:', Air.temperature)
            print('窗户状态为:', MechineMode[windowon])
            print('时间为：', nowtime)

        elif control == 0:
            print('设备当前为手动控制，参数由用户提供')

        """


        # for i in range(0, 1):
        SendTest = '6C' + str(2) + str(CardData)
        print('门卡测试协议：', SendTest)
        s.send(SendTest.encode())
        print('send the car')

        data = s.recv(1024).decode()
        print('Received:', data)

        SendTest = '6C'+str(0) + str(TemData)
        print('温度测试协议：', SendTest)
        s.send(SendTest.encode())
        print('send the tem')

        data = s.recv(1024).decode()
        print('Received:', data)

        SendTest = '6C' + str(1) + str(MoiData)
        print('湿度测试协议：', SendTest)
        s.send(SendTest.encode())
        print('send the moi')

        data = s.recv(1024).decode()
        print('Received:', data)

        print('Now the new temperature is:', TemData)
        print('Now the new moisture is:', Moi.moisture)

        """
        Tem.ChangeTem()
        Moi.ChangeTem()
        print('完成一次数据调整')
        time.sleep(5)

    # time.sleep(10)


def SendHeart():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect((host, port))
    global control
    while True:
        TemData = Tem.temperature
        MoiData = Moi.moisture
        # Car.InsertCard()
        CardData = Car.on

        controlmode = ['手动控制', '自动控制']
        cardmode = ['断电', '通电']
        MechineMode = ['关闭', '开启']
        # control = 1     # 0手控，1自动
        heart = 1  # 0不是心跳检测，1是心跳检测

        SendTest = '6C' + str(heart) + str(control) + str(TemData) + 'F' + str(MoiData) + 'F' + str(CardData) + \
                   str(1) + str(Light1.LightOn) + str(Light1.Force) + str(Air.AirOn) + str(Air.modechoice) + \
                   str(Air.speedchoice) + str(Air.temperature) + str(Win.WindowOn)
        s.send(SendTest.encode())

        data = s.recv(1024).decode()
        print('Received:', data)
        protocol = data
        # print('测试协议:', protocol)
        top = protocol[0:2]
        print('首部为：', top)
        heart = int(protocol[2:3])
        if heart == 1:
            print('此为心跳检测回复')
            nowtime = str(protocol[3:])
            print('时间为：', nowtime)
        '''

        else:
            print('设备需要调整，详细参数为：')
            control = int(protocol[3:4])

            tem_index = protocol.find('F', 4, 8)
            temperature = int(protocol[4:tem_index])

            mov_index = protocol.find('F', tem_index + 1, 13)
            moisture = float(protocol[tem_index + 1:mov_index])

            protocol = protocol[mov_index + 1:]
            cardon = int(protocol[0:1])

            lightnum = int(protocol[1:2])

            lighton = int(protocol[2:3])
            Light1.ChangeOn(lighton)

            lightforce = int(protocol[3:4])
            Light1.ChangeForce(lightforce)

            airon = int(protocol[4:5])
            Air.ChangeOn(airon)

            airmode = int(protocol[5:6])
            Air.ChangeMode(airmode)

            airspeed = int(protocol[6:7])
            Air.ChangeSpeed(airspeed)

            airtemperature = int(protocol[7:9])
            Air.temperature = airtemperature

            windowon = int(protocol[9:10])
            Win.ChangeOn(windowon)

            nowtime = str(protocol[10:])

            print('控制模式为', controlmode[control])
            # print('温度为：', temperature)
            # print('湿度为：', moisture)
            print('总开关状态为：', cardmode[cardon])
            print('灯光数量为：', lightnum)
            print('灯光状态为：', MechineMode[lighton])
            print('灯光强度为：', lightforce)
            print('空调状态为：', MechineMode[airon])
            print('空调模式为：', Air.mode)
            print('空调风速为', Air.speed)
            print('空调温度为:', Air.temperature)
            print('窗户状态为:', Win.WindowOn)
            print('时间为：', nowtime)
            '''
        print('完成一次心跳检测回复')
        time.sleep(10)


def HandControl():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect((host, port))
    global control

    while True:
        control = input('please input control mode:')
        Light1.ChangeOn(1)
        Light1.ChangeForce(8)
        Air.ChangeOn(1)
        Air.ChangeMode(2)
        Air.ChangeSpeed(2)
        TemData = Tem.temperature
        MoiData = Moi.moisture
        Car.InsertCard()
        CardData = Car.on

        controlmode = ['手动控制', '自动控制']
        cardmode = ['断电', '通电']
        MechineMode = ['关闭', '开启']
        # control = 1     # 0手控，1自动
        heart = 0  # 0不是心跳检测，1是心跳检测

        SendTest = '6C' + str(heart) + str(control) + str(TemData) + 'F' + str(MoiData) + 'F' + str(CardData) + \
                   str(1) + str(Light1.LightOn) + str(Light1.Force) + str(Air.AirOn) + str(Air.modechoice) + \
                   str(Air.speedchoice) + str(Air.temperature) + str(Win.WindowOn)

        s.send(SendTest.encode())

        data = s.recv(1024).decode()
        print('Received:', data)
        protocol = data
        # print('测试协议:', protocol)
        top = protocol[0:2]
        print('首部为：', top)
        heart = int(protocol[2:3])
        if heart == 1:
            print('设备不调整')
            nowtime = str(protocol[3:])
            print('时间为：', nowtime)
        else:
            print('设备需要调整，详细参数为：')
            control = int(protocol[3:4])

            tem_index = protocol.find('F', 4, 8)
            temperature = int(protocol[4:tem_index])

            mov_index = protocol.find('F', tem_index + 1, 13)
            moisture = float(protocol[tem_index + 1:mov_index])

            protocol = protocol[mov_index + 1:]
            cardon = int(protocol[0:1])

            lightnum = int(protocol[1:2])

            lighton = int(protocol[2:3])
            Light1.ChangeOn(lighton)

            lightforce = int(protocol[3:4])
            Light1.ChangeForce(lightforce)

            airon = int(protocol[4:5])
            Air.ChangeOn(airon)

            airmode = int(protocol[5:6])
            Air.ChangeMode(airmode)

            airspeed = int(protocol[6:7])
            Air.ChangeSpeed(airspeed)

            airtemperature = int(protocol[7:9])
            Air.temperature = airtemperature

            windowon = int(protocol[9:10])
            Win.ChangeOn(windowon)

            nowtime = str(protocol[10:])

            print('控制模式为', controlmode[control])
            # print('温度为：', temperature)
            # print('湿度为：', moisture)
            print('总开关状态为：', cardmode[cardon])
            print('灯光数量为：', lightnum)
            print('灯光状态为：', MechineMode[lighton])
            print('灯光强度为：', lightforce)
            print('空调状态为：', MechineMode[airon])
            print('空调模式为：', Air.mode)
            print('空调风速为', Air.speed)
            print('空调温度为:', Air.temperature)
            print('窗户状态为:', MechineMode[windowon])
            print('时间为：', nowtime)


def Main():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.connect((host, port))
    # s.send('I\'m open now'.encode())

    # Thread(target=SendData(s, Tem, Moi)).start()
    # Thread(target=ReceiveData(s)).start()
    thread_list = []
    t3 = Thread(target=HandControl)
    thread_list.append(t3)
    t1 = Thread(target=SendData)
    thread_list.append(t1)
    t2 = Thread(target=SendHeart)
    thread_list.append(t2)

    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join()

    print("success")


if __name__ == '__main__':
    Tem = TemperatureSensor()
    Moi = MoistureSensor()
    Car = HomeCard()
    Light1 = Light()
    Air = AirCondition()
    Win = Window()
    global control
    control = 1
    Main()

