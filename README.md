# Human-Robot-Interaction

## Quick Start

See README.md in each folder to install the environment.

Following step is for the local host to run the system.

**Step 1:** startup roscore

```shell
roscore
```



**Step 2:** follow the simulation README.md to startup simulation interface

```shell
roslaunch robot_sim_demo turtlebot_world.launch
```

```shell
roslaunch turtlebot_rviz_launchers view_navigation.launch
```

```shell
roslaunch turtlebot_gazebo amcl_demo.launch map_file:=/home/$USERNAME$/tutorial_ws/src/mymap/mymap.yaml
```

In addition, the path in 'simulation/mymap/mymap.yaml' should be change to your own file path

**Step 3:** open a new terminal and cd to your project directory(for every step, a new terminal should be opened and cd to project directory first), then run

```shell
python tcpNode.pyshe
```



Now wait the remote client to connect.

**Step 4:** 

```shell
python objNode.py
```



**Step 5:**

```shell
cd simulation
python HRI_sim.py
```

**Step 6:**

```shell
python main.py
```


## Message **Definition**

| Main_Sub (Send by)            | Main_Pub (Send to)      |
| ----------------------------- | ----------------------- |
| 'Init'                        | Turtle_start (SimNode)  |
| Turtle_reach_human1 (SimNode) | Human_detect (TcpNode)  |
| Human1 (TcpNode)              | Human_find2 (SimNode)   |
| Human2 (TcpNode)              | Human_find3 (SimNode)   |
| Human3 (TcpNode)              | Turtle_go (SimNode)     |
| Turtle_reach_goods (SimNode)  | Object_detect (ObjNode) |
| Object_detected (ObjNode)     | Turtle_back (SimNode)   |
| Turtle_reach_human2 (SimNode) | Send_object (TcpNode)   |

(Remote Host do face comparision after receiving object) 
