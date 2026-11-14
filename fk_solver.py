import numpy as np
import math
import matplotlib.pyplot as plt

def transMatrix(length, angle):
    theta = math.radians(angle)

    T = np.array([
        [math.cos(theta), -math.sin(theta), length * math.cos(theta)],
        [math.sin(theta), math.cos(theta), length * math.sin(theta)],
        [0, 0, 1]
    ])
    return T

dof = int(input("Enter your Degree of Freedom(int): "))
T_total = np.eye(3)

joints = [[0, 0]]
arms = [T_total.copy()]

for i in range (dof):
    print(f"\nJoint {i+1}")
    length = float(input("Enter arm length: "))
    angle = float(input("enter joint angle: "))

    T = transMatrix(length, angle)
    T_total = T_total @ T
    joints.append([T_total[0, 2], T_total[1, 2]])
    arms.append(T_total.copy())

x = T_total[0, 2]
y = T_total[1, 2]
orientation = math.degrees(
    math.atan2(T_total[1, 0], T_total[0,0])
)

print(f"X coordinates: {x:.3f}")
print(f"Y coordinates: {y:.3f}")
print(f"Final coordinates: ({x:.3f}, {y:.3f})")
print(f"arm orientation: ({orientation:.3f}) degrees")
print("\nthe transformation matrix: ")
print(T_total)


#plotting
joints = np.array(joints)
plt.figure(figsize=(9,9))

plt.plot(
    joints[:, 0],
    joints[:, 1],
    'o-',
    linewidth=4,
    markersize=9
)
for i, joint in enumerate(joints):
    plt.annotate(
        f"J{i}",
        (joint[0], joint[1]),
        xytext=(7, 7),
        textcoords="offset points"
    )

axis_length = max(
    np.linalg.norm(joints[i+1] - joints[i])
    for i in range(dof)
) * 0.25

for i, T in enumerate(arms):
    origin = T[:2, 2]
    x_axis = T[:2, 0] * axis_length
    y_axis = T[:2, 1] * axis_length

    plt.quiver(
        origin[0], origin[1],
        x_axis[0], x_axis[1],
        angles='xy',
        scale_units='xy',
        scale=1
    )
    plt.quiver(
    origin[0], origin[1],
    y_axis[0], y_axis[1],
    angles='xy',
    scale_units='xy',
    scale=1
    )
    
    plt.text(
        origin[0], origin[1] - axis_length * 0.2,
        f"Frame {i}"
    )

plt.scatter(x, y, s=100, marker='*')
reach = np.sum([
    np.linalg.norm(joints[i+1] - joints[i])
    for i in range(dof)
])
margin = reach * 0.2
plt.xlim(-reach - margin, reach + margin)
plt.ylim(-reach - margin, reach + margin)
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title(f"{dof}-DOF Robot Arm - Forward Kinematics")
plt.grid(True)
plt.axis("equal")
plt.show()