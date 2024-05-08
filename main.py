import random
import matplotlib.pyplot as plt

import localization

# 좌표 리스트 생성
sensors = [(-3, 3), (-3, -3), (3, -3)]
n_0 = 1 # amount of leakage
D = 1 # Diffusion constant
t = 1

# 랜덤으로 한 점 선택
random_x = random.choice(range(-5, 6))
random_y = random.choice(range(-5, 6))

leakage_point =[random_x, random_y]
leakage_amount = localization.diffusion_function(sensors, leakage_point, n_0, D, t)

estimated_point, r = localization.localization(sensors, leakage_amount, n_0, D, t)

print("Randomly selected point:", (random_x, random_y))
print('Estimated point :',estimated_point)

# 좌표 시각화
plt.figure(figsize=(6, 6))
for point in sensors:
    plt.scatter(point[0], point[1], color='blue')

# 랜덤으로 선택된 점 시각화
plt.scatter(random_x, random_y, color='black', label='Random Point', marker='x', s=100)

circle1 = plt.Circle((sensors[0][0], sensors[0][1]), r[0], color='r', fill=False)
circle2 = plt.Circle((sensors[1][0], sensors[1][1]), r[1], color='g', fill=False)
circle3 = plt.Circle((sensors[2][0], sensors[2][1]), r[2], color='b', fill=False)

fig, ax = plt.subplots()

# 원 그리기
ax.add_artist(circle1)
ax.add_artist(circle2)
ax.add_artist(circle3)

# 원의 중심점 표시
for i, (sensor, radius, color) in enumerate(zip(sensors, r, ['r', 'g', 'b'])):
    plt.scatter(sensor[0], sensor[1], color=color, label=f"Sensor {i+1}")

# leakage_point 표시
plt.scatter(leakage_point[0], leakage_point[1], color='black', label='Leakage Point', marker='x', s=100)

# 축과 라벨, 타이틀 추가
plt.axhline(0, color='black', linewidth=0.5)  # x 축
plt.axvline(0, color='black', linewidth=0.5)  # y 축
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.xticks(range(-5, 6))
plt.yticks(range(-5, 6))
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Randomly Selected Point and Blue Points')
plt.grid(True)
plt.legend()
plt.show()