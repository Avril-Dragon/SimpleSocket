protocol = '6C-16F0.2F1101000250'
print('测试协议:', protocol)
top = protocol[0:2]
print('首部为：', top)
tem_index = protocol.find('F', 2, 6)
print(tem_index)
temperature = protocol[2:tem_index]
print('温度为：', temperature)
mov_index = protocol.find('F', tem_index+1, 11)
print(mov_index)
moisture = protocol[tem_index+1:mov_index]
print('湿度：', moisture)
protocol = protocol[mov_index + 1:]
cardon = protocol[0:1]
print('开关状态为：', cardon)
lightnum = protocol[1:2]
print('灯光数量为：', lightnum)

lighton = protocol[2:3]
print('灯光状态为：', lighton)
lightforce = protocol[3:4]
print('灯光强度为：', lightforce)

airon = protocol[4:5]
print('空调状态为：', airon)
airmode = protocol[5:6]
print('空调模式为：', airmode)
airspeed = protocol[6:7]
print('空调风速为', airspeed)
airtemperature = protocol[7:9]
print('空调温度为:', airtemperature)

windowon = protocol[9:]
print('窗户状态为:', windowon)