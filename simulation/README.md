# 仿真部分说明

## 前言
src下的turtlebot包来自于上学期移动机器人实验；
编译本部分时把包放在ros工作空间中；
各个节点之间数据交流类型都是 UInt16

## 编译完成后：
运行 $ roslaunch robot_sim_demo turtlebot_world.launch 即可打开仿真环境，
其中robot_sim_demo在/src/ourHRI下；
之后打开新的终端运行 $ roslaunch turtlebot_rviz_launchers view_navigation.launch 即可打开rviz；
再打开一个新的终端运行 $ roslaunch turtlebot_gazebo amcl_demo.launch map_file:=/filepath/mymap.yaml，
其中mymap.yaml在/src/mymap下；
这时候就可以看到在rviz中的地图了

## 实现本项目所需功能的部分：
本项目关于turtlebot仿真控制部分在HRI_sim.py文件中，
再打开一个新的终端，进入HRI_sim.py文件所在目录，
输入 $ python HRI_sim.py，
这时仿真环境中的turtlebot会等待其他部分(如主流程、人脸识别语音交互部分、物体识别部分等)的指令信号；

talk.py和adjust.py文件是模拟其他部分传输指令以测试本部分的功能，
其中talk.py模拟主流程，用来给turtlebot下达去指定房间位置的信号，
而adjust.py用来下达turtlebot位姿调整信号，
打开两个新的终端分别输入 $ python talk.py  以及 $ python adjust.py

## 接下来是实现功能的流程：
在talk.py所在终端输入 0 ，即给turtlebot下达第一次去有三个客人的房间的指令，
此时在HRI_sim.py终端可以看到turtlebot执行去有客人的房间的特定点的动作，
在仿真环境下也可以看到turtlebot在运动，
在turtlebot第一次到达了有客人房间的指定点后，会发出 4 的信号，然后会等待下一个指令，
之后如果在adjust.py所在终端输入turtlebot应该调整的角度信息，
（目前turtlebot只实现了逆时针转，所以给的角度信息是0°-360°，0°为发出指令时turtlebot面向的正前方），
在HRI_sim.py所在终端可以看到turtlebot正在调整的信息，调整完成后会发出 7 的信号，
进行完3次调整后，在talk.py终端输入 1 ，turtlebot执行去另一个房间取物品的动作，
此时可以在HRI_sim.py终端可以看到相关信息，
取完物品后，在talk.py终端输入 2 ，turtlebot就会执行取有客人的房间送物品的动作，
之后再经过3次的和上面相同的姿态调整后，即完成了任务
