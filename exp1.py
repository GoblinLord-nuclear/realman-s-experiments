from Robotic_Arm.rm_robot_interface import *

ROBOT_IP = "169.254.128.18"
ROBOT_PORT = 8080

# 实例化机械臂并创建连接
arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
handle = arm.rm_create_robot_arm(ROBOT_IP, ROBOT_PORT)
print(f"连接句柄 ID: {handle.id}")

# 读取末端位姿和关节角度
ret, state = arm.rm_get_current_arm_state()
if ret != 0:
    print(f"获取机械臂状态失败，错误码: {ret}")
else:
    tcp = state["pose"]   # [x, y, z, rx, ry, rz]
    q = state["joint"]    # [q1, q2, q3, q4, q5, q6]

    print(f"末端位姿 [x, y, z, rx, ry, rz]: {tcp}")
    print(f"关节角度 [q1, q2, q3, q4, q5, q6]: {q}")
    print("连接成功！")

# 断开连接
arm.rm_delete_robot_arm()
