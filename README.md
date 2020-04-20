# Human-Robot-Interaction

## Message Definition
### Main_Sub (Send by) -> Main_Pub (Send to)
+ 'Init' -> Turtle_start (SimNode)
+ Turtle_reach_human1 (SimNode) -> Human_detect (TcpNode)
+ Human1 (TcpNode) -> Human_find2 (SimNode)
+ Human2 (TcpNode) -> Human_find3 (SimNode)
+ Human3 (TcpNode) -> Turtle_go (SimNode)
+ Turtle_reach_goods (SimNode) -> Object_detect (ObjNode)
+ Object_detected (ObjNode) -> Turtle_back (SimNode)
+ Turtle_reach_human2 (SimNode) -> Send_object (TcpNode) 

(Remote Host do face comparision after receiving object) 