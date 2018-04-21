# --coding:utf-8--
import matplotlib.pyplot as plt
import csv
from pylab import *
# mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'KaiTi, Times New Roman'
mpl.rcParams['axes.unicode_minus'] = False
font1 ={'family': 'KaiTi, Times New Roman',
        'size': 20}
filename = 'MHGR.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    print(header_row)

    # 从头文件中获取温度和强度
    Temps = []
    Intensitys = []
    for row in reader:
        Temp = float(row[0])
        Temps.append(Temp)
        Intensity = float(row[2])
        Intensitys.append(Intensity)

    # 绘制图形
    fig = plt.figure(dpi=600, figsize=(10,6))
    plt.plot(Temps, Intensitys, c='Blue')
    # 设置图形的格式
    plt.title('MHGR的DSC曲线', fontsize=20)
    plt.xlabel('Temperature(℃)', fontsize=16)
    plt.ylabel('Intensity(a.u.)', fontsize=16)
    # 隐藏坐标轴
    'plt.axes().get_yaxis().set_visible(False)'
    # 隐藏坐标轴刻度
    plt.yticks([])
    plt.show()
