from Robotic_Arm.rm_robot_interface import *

ROBOT_IP = "169.254.128.18"
ROBOT_PORT = 8080

# 实例化机械臂并创建连接
arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
handle = arm.rm_create_robot_arm(ROBOT_IP, ROBOT_PORT)
print(f"连接句柄 ID: {handle.id}")

# 读取当前末端位姿（[x, y, z, rx, ry, rz]，位置单位 m，姿态单位 rad）
ret, state = arm.rm_get_current_arm_state()
if ret != 0:
    print(f"获取机械臂状态失败，错误码: {ret}")
    arm.rm_delete_robot_arm()
    exit(1)

current = state["pose"]
print(f"当前位置: x={current[0]:.3f}, y={current[1]:.3f}, z={current[2]:.3f}")

# 沿 Z 轴上移 2 cm
target = current.copy()
target[2] += 0.04
print(f"目标位置: x={target[0]:.3f}, y={target[1]:.3f}, z={target[2]:.3f}")

input("确认安全后按 Enter 执行移动（低速）...")

# 低速直线运动（v 为速度百分比 1~100，取较小值；block=1 阻塞等待到位）
ret = arm.rm_movel(target, 10, 0, 0, 1)
if ret != 0:
    print(f"直线运动失败，错误码: {ret}")
else:
    ret, state = arm.rm_get_current_arm_state()
    if ret == 0:
        new_pose = state["pose"]
        print(f"移动后: x={new_pose[0]:.3f}, y={new_pose[1]:.3f}, z={new_pose[2]:.3f}")

# 断开连接
arm.rm_delete_robot_arm()
