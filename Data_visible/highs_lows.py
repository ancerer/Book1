import csv
from matplotlib import pyplot as plt
from datetime import datetime

filename = 'Data_visible.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # 从文件中获取air temperature
    highs = []
    dates = []
    for row in reader:
        current_date = datetime.strptime(row[3], '%Y-%m-%dT%H:%M:%S')
        dates.append(current_date)
        high = float(row[10])
        highs.append(high)
    print(highs)

    # 绘制图形
    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(dates, highs, c='red')
    # 设置图形的格式
    plt.title("Daily air temperature", fontsize=20)
    plt.xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel("Temperature(F)", fontsize=16)
    plt.tick_params(axis="both", which='major', labelsize=16)

    plt.show()