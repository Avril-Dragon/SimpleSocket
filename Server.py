import socket
import time
import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        c = self.request
        Flag = True
        while Flag:
            protocol = c.recv(1024).decode()
            pro_tocol = protocol
            print('测试协议:', protocol)
            top = protocol[0:2]
            print('首部为：', top)
            heart = int(protocol[2:3])
            print('心跳为：', heart)
            control = int(protocol[3:4])
            print('控制模式为', control)
            tem_index = protocol.find('F', 4, 8)
            temperature = int(protocol[4:tem_index])
            print('温度为：', temperature)
            mov_index = protocol.find('F', tem_index + 1, 13)
            moisture = float(protocol[tem_index + 1:mov_index])
            print('湿度为：', moisture)
            protocol = protocol[mov_index + 1:]
            cardon = int(protocol[0:1])
            print('总开关状态为：', cardon)
            lightnum = int(protocol[1:2])
            print('灯光数量为：', lightnum)

            lighton = int(protocol[2:3])
            print('灯光状态为：', lighton)
            lightforce = int(protocol[3:4])
            print('灯光强度为：', lightforce)

            airon = int(protocol[4:5])
            print('空调状态为：', airon)
            airmode = int(protocol[5:6])
            print('空调模式为：', airmode)
            airspeed = int(protocol[6:7])
            print('空调风速为', airspeed)
            airtemperature = int(protocol[7:9])
            print('空调温度为:', airtemperature)

            windowon = int(protocol[9:10])
            print('窗户状态为:', windowon)

            if cardon == 1 and heart == 0:
                print('通电，可以调控')

                if control == 1:
                    print('自动模式，根据温度和湿度自动控制')
                    # 温度调整
                    if temperature > 30:
                        print('温度过高，空调设置制冷，中速，目标温度为25度，关闭窗户')
                        airon = 1
                        airmode = 0
                        airspeed = 1
                        airtemperature = 25
                        windowon = 0
                    elif temperature < 10:
                        print('温度过低，空调设置制热，中速，目标温度为20度，关闭窗户')
                        airon = 1
                        airmode = 1
                        airspeed = 1
                        airtemperature = 20
                        windowon = 0

                    else:
                        print('温度正常，空调保持现有状态')

                    # 湿度调整
                    if moisture > 0.65:
                        print('湿度过高，空调设置送风，高速，开启窗户')
                        airon = 1
                        airmode = 2
                        airspeed = 2
                        windowon = 1
                    elif moisture < 0.4:
                        print('湿度过低，空调设置制冷，中速，目标温度为25度，关闭窗户')
                        airon = 1
                        airmode = 0
                        airspeed = 1
                        airtemperature = 25
                        windowon = 0
                    else:
                        print('湿度正常，空调保持现有状态')

                    # 灯光调节
                    lighton = 1
                    lightforce = 3

                    SendData = '6C01' + str(temperature) + 'F' + str(moisture) + 'F' + str(cardon) + str(
                        lightnum) + str(lighton) \
                               + str(lightforce) + str(airon) + str(airmode) + str(airspeed) + str(
                        airtemperature) + str(windowon) \
                               + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    c.send(SendData.encode())

                if control == 0:
                    print('手动控制，根据用户提供数据调节')
                    SendData = pro_tocol + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    c.send(SendData.encode())

            elif cardon == 0 and heart == 0:
                print('断电，不进行调整')
                SendData = '6C1' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                c.send(SendData.encode())

            if heart == 1:
                print('心跳测试，不进行调整')
                SendData = '6C1' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                c.send(SendData.encode())


if __name__ == '__main__':
    host = socket.gethostname()
    port = 12345
    server = socketserver.ThreadingTCPServer((host, port), MyServer)
    server.serve_forever()


"""
s = socket.socket()

s.bind((host, port))
s.listen(5)
CardOn = 0      # 0表示没人，1表示有人
TemUp = 0       # 0表示降温，1表示升温，2表示维持
MoiUp = 0       # 0表示加湿，1表示去湿，2表示维持

while True:
    c, address = s.accept()
    print('连接地址：', address)
    #c.send('Welcome to use'.encode())
    Flag = True
    Flag1 = False
    while Flag1:
        protocol = c.recv(1024).decode()
        print('测试协议:', protocol)
        top = protocol[0:2]
        print('首部为：', top)
        SendData = '6C0'
        equipment = protocol[2]
        if equipment == '0':
            EquName = '温度传感器'
            print('设备是', EquName)
            data = int(protocol[3:])
            print('接收数据,温度为:', data)

            if CardOn == 1:
                if data == 'exit':
                    Flag = False
                elif data > 25:
                    print('温度过高，需要降温')
                    SendData = SendData + ''
                    c.send('降温！'.encode())
                    print('温度指令下发成功')
                else:
                    print('温度正常')
                    c.send('温度正常。'.encode())
                    print('温度指令下发成功')
            else:
                print('房间无人，不发送指令')
                SendData = SendData + str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
                c.send(SendData.encode())
        elif equipment == '1':
            EquName = '湿度传感器'
            print('设备是', EquName)
            data = float(protocol[3:])
            print('接收数据,湿度为:', data)
            if CardOn == 1:
                if data == 'exit':
                    Flag = False
                elif data > 0.65:
                    print('湿度过高！')
                    c.send('干燥！'.encode())
                    print('湿度指令下发成功')
                elif data < 0.45:
                    print('湿度过低')
                    c.send('加湿！'.encode())
                    print('湿度指令下发成功')
                else:
                    print('湿度正常')
                    c.send('适度正常。'.encode())
                    print('湿度指令下发成功')
            else:
                print('房间无人，不发送指令')
                SendData = SendData + str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
                c.send(SendData.encode())
        else:
            EquName = '门卡'
            print('设备是', EquName)
            data = int(protocol[3:])
            # print('接收数据,开关状态为:', data)

            if data == 'exit':
                Flag = False
            elif data == 1:
                print('家里有人！')
                CardOn = 1
                c.send('有人！'.encode())
                # print('指令下发成功')
            elif data == 0:
                print('家里无人')
                CardOn = 0
                c.send('无人！'.encode())
                # print('指令下发成功')
"""


