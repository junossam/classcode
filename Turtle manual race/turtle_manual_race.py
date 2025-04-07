import turtle  # 터틀 그래픽 모듈을 가져옴

# 스크린 설정
scr = turtle.Screen()  # 터틀 그래픽 화면 생성
scr.title("Turtle Race")  # 화면 제목 설정

# 결승선 그리기
finishline = turtle.Turtle()  # 결승선을 그릴 터틀 객체 생성
finishline.hideturtle()  # 결승선을 그리는 터틀을 숨김

# 왼쪽 결승선 그리기
finishline.penup()  # 펜을 들어서 이동 중 선이 그려지지 않도록 설정
finishline.color('red')  # 결승선 색상을 빨간색으로 설정
finishline.goto(-200, 200)  # 결승선 시작 위치로 이동
finishline.pendown()  # 펜을 내려 선을 그릴 준비
finishline.goto(-200, -200)  # 결승선 아래쪽 끝까지 선을 그림

# 오른쪽 결승선 그리기
finishline.penup()  # 펜을 들어서 이동 중 선이 그려지지 않도록 설정
finishline.color('blue')  # 결승선 색상을 파란색으로 설정
finishline.goto(200, 200)  # 결승선 시작 위치로 이동
finishline.pendown()  # 펜을 내려 선을 그릴 준비
finishline.goto(200, -200)  # 결승선 아래쪽 끝까지 선을 그림

# 거북이 초기화 함수 정의
def create_turtle(color, x, y):
    """
    주어진 색상과 위치를 기반으로 거북이를 생성하고 초기화하는 함수.
    :param color: 거북이 색상
    :param x: 거북이의 초기 x 좌표
    :param y: 거북이의 초기 y 좌표
    :return: 초기화된 거북이 객체
    """
    t = turtle.Turtle()  # 새로운 터틀 객체 생성
    t.shape('turtle')  # 거북이 모양으로 설정
    t.color(color)  # 거북이 색상 설정
    t.penup()  # 이동 중 선이 그려지지 않도록 설정
    t.goto(x, y)  # 초기 위치로 이동
    return t  # 초기화된 거북이 객체 반환

# 거북이 초기 설정 값
colors = ['red', 'blue', 'green']  # 거북이 색상 리스트
positions = [(-200, 150), (-200, 0), (-200, -150)]  # 거북이 초기 위치 리스트

# 순서대로 거북이 정보 가져와서 초기화
turtles = []  # 초기화된 거북이 객체를 저장할 리스트
for color, position in zip(colors, positions):  # 색상과 위치를 묶어서 반복
    t = create_turtle(color, *position)  # 거북이 생성 및 초기화
    turtles.append(t)  # 생성된 거북이를 리스트에 추가

# 거북이들이 움직일 거리 설정
move_x = 10  # 한 번 움직일 때 거북이가 이동할 거리 (픽셀 단위)

# 승자를 결정하는 변수 초기화
winner = None  # 아직 승자가 없으므로 None으로 초기화

# 거북이를 움직이는 함수
def move_t(t):
    """
    주어진 거북이를 앞으로 이동시키고, 결승선에 도달했는지 확인하는 함수.
    :param t: 이동할 거북이 객체
    """
    global winner  # 전역 변수 winner를 사용
    if winner is None:  # 아직 승자가 없을 경우에만 이동
        t.forward(move_x)  # 거북이를 앞으로 이동
    if t.xcor() >= 200 and winner is None:  # 거북이가 결승선에 도달했는지 확인
        print(f"The winner is the {t.color()[0]} turtle!")  # 승자 출력
        winner = t  # 승자를 현재 거북이로 설정

# 키보드 이벤트 처리 (각각 함수 만들어서 처리)
"""
# 첫 번째 거북이를 움직이는 함수
def move_t1():
    move_t(turtles[0])
    
# 두 번째 거북이를 움직이는 함수
def move_t2():
    move_t(turtles[1])
    
# 세 번째 거북이를 움직이는 함수
def move_t3():
    move_t(turtles[2])

# 키보드 이벤트 설정
scr.onkey(move_t1, 'q')  # 'q' 키를 누르면 첫 번째 거북이가 움직임
scr.onkey(move_t2, 't')  # 't' 키를 누르면 두 번째 거북이가 움직임
scr.onkey(move_t3, 'o')  # 'o' 키를 누르면 세 번째 거북이가 움직임
"""

# 키보드 이벤트 처리 (람다식을 이용하여 함수 생성)
# 각 키보드 이벤트를 특정 거북이의 움직임에 바인딩
scr.onkey(lambda: move_t(turtles[0]), 'q')  # 'q' 키를 누르면 첫 번째 거북이가 움직임
scr.onkey(lambda: move_t(turtles[1]), 't')  # 't' 키를 누르면 두 번째 거북이가 움직임
scr.onkey(lambda: move_t(turtles[2]), 'o')  # 'o' 키를 누르면 세 번째 거북이가 움직임

scr.listen()  # 키보드 입력을 기다림

# 경주 끝
turtle.done()  # 터틀 그래픽 창이 닫히지 않도록 유지
