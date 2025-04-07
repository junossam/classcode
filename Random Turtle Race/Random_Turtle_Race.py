# 이 프로그램은 거북이 그래픽 모듈을 사용하여 간단한 거북이 경주 게임을 구현한 코드입니다.
# 여러 색상의 거북이가 랜덤한 속도로 움직이며, 결승선에 가장 먼저 도달한 거북이가 승리합니다.
# 사용자는 프로그램 실행 후 콘솔에서 승리한 거북이의 색상을 확인할 수 있습니다.

import turtle
import random

# 스크린 설정
scr = turtle.Screen()  # 거북이 그래픽 화면 생성
scr.title("Turtle Race")  # 화면 제목 설정

# 결승선 그리기
finishline = turtle.Turtle()  # 결승선을 그릴 거북이 생성
finishline.hideturtle()  # 결승선을 그리는 거북이를 숨김

# 왼쪽 결승선 그리기
finishline.penup()
finishline.color('red')  # 결승선 색상 설정
finishline.goto(-200, 200)  # 시작 위치로 이동
finishline.pendown()
finishline.goto(-200, -200)  # 아래로 선을 그림

# 오른쪽 결승선 그리기
finishline.penup()
finishline.color('blue')  # 결승선 색상 설정
finishline.goto(200, 200)  # 시작 위치로 이동
finishline.pendown()
finishline.goto(200, -200)  # 아래로 선을 그림

"""
# 함수를 사용하지 않고 거북이 초기화
# 아래 코드는 주석 처리된 코드로, 각 거북이를 개별적으로 초기화하는 방식입니다.
t1 = turtle.Turtle()
t1.shape('turtle')
t1.color('red')
t1.penup()
t1.goto(-200, 150)

t2 = turtle.Turtle()
t2.shape('turtle')
t2.color('blue')
t2.penup()
t2.goto(-200, 0)

t3 = turtle.Turtle()
t3.shape('turtle')
t3.color('green')
t3.penup()
t3.goto(-200, -150)

turtles = [t1, t2, t3]
"""

# 함수를 사용한 거북이 초기화
# 거북이 초기화 함수
def create_turtle(color, x, y):
    """
    주어진 색상과 위치를 기반으로 거북이를 생성하는 함수.
    :param color: 거북이 색상
    :param x: 거북이의 초기 x 좌표
    :param y: 거북이의 초기 y 좌표
    :return: 초기화된 거북이 객체
    """
    t = turtle.Turtle()
    t.shape('turtle')  # 거북이 모양 설정
    t.color(color)  # 거북이 색상 설정
    t.penup()  # 펜을 들어서 선을 그리지 않도록 설정
    t.goto(x, y)  # 초기 위치로 이동
    return t

# 거북이 초기 설정 값
colors = ['red', 'blue', 'green']  # 거북이 색상 리스트
positions = [(-200, 150), (-200, 0), (-200, -150)]  # 거북이 초기 위치 리스트

# 순서대로 거북이 정보 가져와서 초기화
turtles = []
for color, position in zip(colors, positions):
    t = create_turtle(color, *position)  # 색상과 위치를 기반으로 거북이 생성
    turtles.append(t)  # 생성된 거북이를 리스트에 추가

# 승자를 결정하는 변수 초기화
winner = None  # 승자가 결정되기 전까지 None으로 설정

# 경주 시작
while winner is None:  # 승자가 결정될 때까지 반복
    for t in turtles:
        # 거북이들이 앞으로 나아갈 거리 랜덤 설정
        distance = random.randint(1, 10)  # 1에서 10 사이의 랜덤 거리
        t.forward(distance)  # 거북이를 앞으로 이동
        
        # 결승선에 도착했는지 확인
        if t.xcor() >= 200:  # x 좌표가 200 이상이면 결승선 도착
            winner = t  # 승자를 현재 거북이로 설정
            break  # 반복문 종료
        
# 승자 출력
print(f"The winner is the {winner.color()[0]} turtle!")  # 승리한 거북이의 색상 출력

# 경주 끝
turtle.done()  # 거북이 그래픽 창 유지