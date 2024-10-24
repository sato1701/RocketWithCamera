import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# グラフの初期設定
fig = plt.figure()
ax1 = fig.add_subplot(222) #temp
ax2 = fig.add_subplot(224) #pressure
ax3 = fig.add_subplot(221, projection='3d') #acc
ax4 = fig.add_subplot(223) #ang

counter = 0
graph_width = 50

# リアルタイムデータ保存用リスト
temp_values = [0.0] * graph_width
pressure_values = [0.0] * graph_width
x_data = [0.0] * graph_width

ax1.set_title('Real-time Data Visualization')
ax1.set_xlabel('Time (sample index)')
ax1.set_ylabel('Templature [℃]')
ax1.set_ylim(20, 45)  # Y軸の範囲を指定 (必要に応じて調整)

ax2.set_title('Real-time Data Visualization')
ax2.set_xlabel('Time (sample index)')
ax2.set_ylabel('Pressure [hPa]')
ax2.set_ylim(970, 1020)  # Y軸の範囲を指定 (必要に応じて調整)

ax3.set_xlabel('X (down)')
ax3.set_ylabel('Y (right)')
ax3.set_zlabel('Z (back)')
ax3.set_xlim([-2, 2])
ax3.set_ylim([-2, 2])
ax3.set_zlim([-2, 2])

# 棒グラフの初期設定
ax4.set_title('Real-time Gyroscope Data')
ax4.set_xlabel('Axes')
ax4.set_ylabel('Angular Velocity [deg/s]')
ax4.set_ylim([-360, 360])
bar_colors = ['red', 'green', 'blue']
bar_container = ax4.bar(['Gyro X', 'Gyro Y', 'Gyro Z'], [0, 0, 0], color=bar_colors)

line1, = ax1.plot([], [], color='blue')
line2, = ax2.plot([], [], color='blue')

# グラフの更新関数
def update(frame):
    global counter
    line = sys.stdin.readline()  # 標準入力からデータを受け取る

    x_accel, y_accel, z_accel = 0.0, 0.0, 0.0
    gyro_x, gyro_y, gyro_z = 0.0, 0.0, 0.0

    try:
        if line:
            # CSV形式のデータを分割して最後の値を取得
            values = line.strip().split(',')
            x_accel = float(values[1])  # x方向 (下)
            y_accel = float(values[2])  # y方向 (右)
            z_accel = float(values[0])  # z方向 (奥)
            gyro_x = float(values[3])   # x方向の角速度
            gyro_y = float(values[4])   # y方向の角速度
            gyro_z = float(values[5])   # z方向の角速度

            # データ更新
            temp_values[counter % graph_width] = float(values[-2])
            pressure_values[counter % graph_width] = float(values[-3])
            x_data[counter % graph_width] = counter

            counter += 1
    
        # グラフの再描画
        line1.set_data(x_data[:min(counter, graph_width)], temp_values[:min(counter, graph_width)])
        ax1.set_xlim(max(0, counter - graph_width), counter)

        line2.set_data(x_data[:min(counter, graph_width)], pressure_values[:min(counter, graph_width)])
        ax2.set_xlim(max(0, counter - graph_width), counter)

        # 3Dベクトルの再描画
        if counter % 2 == 0: # 10回ごとにクリア
            ax3.cla()  # クリアしてから再描画
            ax3.set_xlabel('X (down)')
            ax3.set_ylabel('Y (right)')
            ax3.set_zlabel('Z (back)')
            ax3.set_xlim([-2, 2])
            ax3.set_ylim([-2, 2])
            ax3.set_zlim([-2, 2])

        # ベクトルの描画
        alr = 0.8 / np.linalg.norm([x_accel, y_accel, z_accel])
        ax3.quiver(0, 0, 0, x_accel, y_accel, z_accel, linewidth=4, arrow_length_ratio=alr)

        # 棒グラフの再描画 (角速度)
        for bar, new_value in zip(bar_container, [gyro_x, gyro_y, gyro_z]):
            bar.set_height(new_value)

    except (ValueError, IndexError):
        print("データの読み取りに失敗しました")


# アニメーションの設定
ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)  # 100msごとに更新

# グラフを表示
plt.show()

