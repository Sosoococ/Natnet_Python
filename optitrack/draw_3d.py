from multiprocessing import Process, Queue, Event
from queue import Empty
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class RealTimePlot3D(Process):
    def __init__(self, optitrack_queue, frequency, stop_event):
        super(RealTimePlot3D, self).__init__()
        self.optitrack_queue = optitrack_queue
        self.frequency = frequency
        self.stop_event = stop_event

        # initialize figure
        self.fig = plt.figure()

        # 子图1：显示场景
        self.ax_scene = self.fig.add_subplot(121, projection='3d')
        self.ax_scene.set_xlim([-1, 1])
        self.ax_scene.set_ylim([-1, 1])
        self.ax_scene.set_zlim([-1, 1])
        self.ax_scene.set_xlabel('X')
        self.ax_scene.set_ylabel('Y')
        self.ax_scene.set_zlabel('Z')
        self.ax_scene.set_title('3D Scene')

        # 子图2：显示箭头
        self.ax_arrow = self.fig.add_subplot(122, projection='3d')
        self.quiver = self.ax_arrow.quiver(0, 0, 0, 1, 0, 0, color='r', label='Rotated Point')
        self.ax_arrow.set_xlim([-1, 1])
        self.ax_arrow.set_ylim([-1, 1])
        self.ax_arrow.set_zlim([-1, 1])
        self.ax_arrow.set_xlabel('X')
        self.ax_arrow.set_ylabel('Y')
        self.ax_arrow.set_zlabel('Z')
        self.ax_arrow.set_title('Arrow Motion')

        # 初始化数据
        self.x, self.y, self.z = 0.0, 0.0, 0.0
        self.roll, self.pitch, self.yaw = 0.0, 0.0, 0.0

    def update_scene(self, frame):
        try:
            # 从队列获取数据
            data = self.optitrack_queue.get(timeout=(1 / (1 * self.frequency)))

            # 解析数据
            robot_id, (x, y, z), (roll, pitch, yaw), time = data
            print(x,y,z)

            # 清空原有的点
            self.ax_scene.cla()

            # 绘制新的点，假设每个机器人用不同的颜色表示
            self.ax_scene.scatter(x, y, z, c=f'C{robot_id}', marker='o', label=f'Robot {robot_id}')

            # 设置坐标轴范围
            self.ax_scene.set_xlim([-1, 1])
            self.ax_scene.set_ylim([-1, 1])
            self.ax_scene.set_zlim([-1, 1])

            # 设置坐标轴标签
            self.ax_scene.set_xlabel('X')
            self.ax_scene.set_ylabel('Y')
            self.ax_scene.set_zlabel('Z')

            # 设置子图标题
            self.ax_scene.set_title('3D Scene')

            # 添加图例
            self.ax_scene.legend()

            # 显示时间信息
            self.ax_scene.text(-0.9, 0.9, f'Time: {time}', color='black')

        except Empty:
            pass  # Ignore empty queue and check for the stop event

    def update_arrow(self, frame):
        # 更新箭头数据，替换为你的实际输入方法
        self.x += np.random.uniform(-0.1, 0.1)
        self.y += np.random.uniform(-0.1, 0.1)
        self.z += np.random.uniform(-0.1, 0.1)
        self.roll += np.random.uniform(-1.0, 1.0)
        self.pitch += np.random.uniform(-1.0, 1.0)
        self.yaw += np.random.uniform(-1.0, 1.0)

        # 计算旋转矩阵
        rotation_matrix = np.array([
            [np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
             np.cos(np.radians(self.yaw)) * np.sin(np.radians(self.pitch)) * np.sin(np.radians(self.roll)) - np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.roll)),
             np.cos(np.radians(self.yaw)) * np.sin(np.radians(self.pitch)) * np.cos(np.radians(self.roll)) + np.sin(np.radians(self.yaw)) * np.sin(np.radians(self.roll))],
            [np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
             np.sin(np.radians(self.yaw)) * np.sin(np.radians(self.pitch)) * np.sin(np.radians(self.roll)) + np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.roll)),
             np.sin(np.radians(self.yaw)) * np.sin(np.radians(self.pitch)) * np.cos(np.radians(self.roll)) - np.cos(np.radians(self.yaw)) * np.sin(np.radians(self.roll))],
            [-np.sin(np.radians(self.pitch)),
             np.cos(np.radians(self.pitch)) * np.sin(np.radians(self.roll)),
             np.cos(np.radians(self.pitch)) * np.cos(np.radians(self.roll))]
        ])

        # 计算旋转后的点
        rotated_point = np.dot(rotation_matrix, np.array([self.x, self.y, self.z]))

        # 更新箭头数据
        self.quiver.set_UVC(rotated_point[0], rotated_point[1], rotated_point[2])

    def animate(self):
        # 创建场景动画
        ani_scene = FuncAnimation(self.fig, self.update_scene, frames=range(100), interval=100)

        # 创建箭头动画
        ani_arrow = FuncAnimation(self.fig, self.update_arrow, frames=range(100), interval=100)

        # 显示图形
        plt.show()

    def run(self):
        self.animate()
        while not self.stop_event.is_set():
            try:
                # Retrieve data from the optitrack_queue
                # data = self.optitrack_queue.get()
                data = self.optitrack_queue.get(timeout=(1 / (1 * self.frequency)))  # Use timeout to periodically check for the stop event
                self.update_scene(data)
                self.update_arrow(data)
            except Empty:
                pass  # Ignore empty queue and check for the stop event

    def stop(self):
        self.stop_event.set()
        