from Robotic_Arm.rm_robot_interface import *

ROBOT_IP = "169.254.128.18"
ROBOT_PORT = 8080
LIMIT = 0.03  # 相对起始点的实验限位：±3 cm

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


def within_limit(target, start, limit):
    for i in range(3):
        if abs(target[i] - start[i]) > limit:
            return False
    return True


# 安全目标：Z + 2 cm
safe_target = start.copy()
safe_target[2] += 0.02

# 超限目标：X + 5 cm（只用于验证，不执行运动）
out_target = start.copy()
out_target[0] += 0.05

print("安全目标检查:", within_limit(safe_target, start, LIMIT))
print("超限目标检查:", within_limit(out_target, start, LIMIT))

if not within_limit(out_target, start, LIMIT):
    print("目标超出实验安全限位，禁止发送运动指令。")

# 断开连接
arm.rm_delete_robot_arm()
