from Robotic_Arm.rm_robot_interface import *
ROBOT_IP = "169.254.128.18"
ROBOT_PORT = 8080
# 实例化机械臂并创建连接
arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
handle = arm.rm_create_robot_arm(ROBOT_IP, ROBOT_PORT)
print(f"连接句柄 ID: {handle.id}")
# 读取当前 6 个关节角（单位：°，RealMan 接口直接用角度，无需弧度转换）
ret, state = arm.rm_get_current_arm_state()
if ret != 0:
    print(f"获取机械臂状态失败，错误码: {ret}")
    arm.rm_delete_robot_arm()
    exit(1)
current_q = state["joint"]
print("当前关节角(°):", current_q)
# 仅让第 6 关节在当前位置基础上增加 5°
target_q = current_q.copy()
target_q[5] += 5.0
print("目标关节角(°):", target_q)
input("确认机械臂周围安全后按 Enter 执行关节运动...")
# 低速执行关节空间运动（v 为速度百分比 1~100，取较小值；block=1 阻塞等待到位）
ret = arm.rm_movej(target_q, 10, 0, 0, 1)
if ret != 0:
    print(f"关节运动失败，错误码: {ret}")
else:
    ret, state = arm.rm_get_current_arm_state()
    if ret == 0:
        print("运动后关节角(°):", state["joint"])

# 断开连接
arm.rm_delete_robot_arm()
