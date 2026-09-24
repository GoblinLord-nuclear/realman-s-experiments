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

start = state["pose"]

# 在当前位姿附近构造三个安全目标点
p1 = start.copy()
p1[2] += 0.02          # Z + 2 cm

p2 = p1.copy()
p2[0] += 0.02          # 在 p1 基础上 X + 2 cm

p3 = p1.copy()         # 返回 p1

print("起点:", start)
print("P1:", p1)
print("P2:", p2)
print("P3:", p3)

input("确认 P1、P2、P3 均位于安全工作区后按 Enter 执行...")

# 低速直线运动（v 为速度百分比 1~100；block=1 阻塞等待到位）
ok = True
for point in (p1, p2, p3, start):
    ret = arm.rm_movel(point, 10, 0, 0, 1)
    if ret != 0:
        print(f"运动到 {point} 失败，错误码: {ret}")
        ok = False
        break

if ok:
    ret, state = arm.rm_get_current_arm_state()
    if ret == 0:
        print("最终位姿:", state["pose"])

# 断开连接
arm.rm_delete_robot_arm()
