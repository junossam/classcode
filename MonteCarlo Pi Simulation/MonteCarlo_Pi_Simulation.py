import turtle
import random

# 스크린 설정
win = turtle.Screen()                           # 터틀 스크린 생성
win.bgcolor('white')                            # 배경 색을 흰색으로 설정

# 원을 그리는 터틀 설정
circle = turtle.Turtle()                        # 원을 그릴 터틀 객체 생성
circle.hideturtle()                             # 터틀을 숨김 (그림만 표시)
circle.penup()                                  # 선을 그리지 않도록 터틀을 들어 올림
circle.goto(0, -200)                            # 원의 하단을 (0, -200)으로 이동
circle.pendown()                                # 터틀을 내려 선을 그리기 시작
circle.circle(200)                              # 반지름이 200인 원을 그림

# 정사각형을 그리는 터틀 설정
square = turtle.Turtle()                        # 정사각형을 그릴 터틀 객체 생성
square.hideturtle()                             # 터틀을 숨김 (그림만 표시)
square.penup()                                  # 선을 그리지 않도록 터틀을 들어 올림
square.goto(-200, -200)                         # 정사각형의 하단 좌측 모서리 위치로 이동
square.pendown()                                # 터틀을 내려 선을 그리기 시작
for _ in range(4):                              # 4번 반복하여 정사각형의 네 변을 그림
    square.forward(400)                         # 400만큼 앞으로 이동
    square.left(90)                             # 왼쪽으로 90도 회전

# 점을 찍는 터틀 설정
point = turtle.Turtle()                         # 점을 찍을 터틀 객체 생성
point.hideturtle()                              # 터틀을 숨김 (점만 표시)
point.penup()                                   # 선을 그리지 않도록 터틀을 들어 올림

# 결과를 표시하는 터틀 설정
result = turtle.Turtle()                        # 결과를 표시할 터틀 객체 생성
result.hideturtle()                             # 터틀을 숨김 (텍스트만 표시)
result.penup()                                  # 선을 그리지 않도록 터틀을 들어 올림
result.goto(-200, 220)                          # 결과를 (좌측 상단)으로 이동

# 점의 개수와 원 내부의 점의 개수 초기화
total_points = 0                                # 전체 점의 개수
circle_points = 0                               # 원 내부에 위치한 점의 개수

# 점을 무작위로 생성하고 원 내부 여부를 확인하는 반복문
for _ in range(10000):                          # 10000개의 점을 생성
    x = random.uniform(-200, 200)               # -200에서 200 사이의 랜덤 x 좌표 생성
    y = random.uniform(-200, 200)               # -200에서 200 사이의 랜덤 y 좌표 생성
    point.goto(x, y)                            # 생성된 점으로 이동

    total_points += 1                           # 전체 점 개수 증가
    if x**2 + y**2 <= 200**2:                   # 점이 원 내부에 있는지 확인
        circle_points += 1                      # 원 내부 점 개수 증가
        point.dot(2, 'blue')                    # 원 내부 점은 파란색으로 표시
    else:
        point.dot(2, 'red')                     # 원 외부 점은 빨간색으로 표시
        
    # 원주율(pi) 추정값 계산 및 표시
    pi = 4 * circle_points / total_points       # 원주율 추정값 계산
    result.clear()                              # 이전 결과를 지움
    result.write("Estimated value of pi: {}".format(pi), font=("Arial", 16, "normal"))  # 결과를 텍스트로 표시
    
# 터틀 그래픽스 종료
turtle.done()
