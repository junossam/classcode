import turtle
import time

# 미로 데이터: 1은 벽, 0은 길
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 스크린 설정
win = turtle.Screen()  # 터틀 스크린 생성
win.bgcolor('black')   # 스크린 배경 색을 검정으로 설정

# 벽을 그리는 터틀 설정
wall = turtle.Turtle()  # 벽을 그릴 터틀 객체 생성
wall.color('white')     # 벽의 색을 흰색으로 설정
wall.hideturtle()       # 벽 그릴 때 터틀을 숨김
wall.speed(0)           # 터틀 속도를 최대로 설정하여 빠르게 그림

# 미로 크기 계산
x_len = len(maze[0])  # 미로의 가로 길이 (열의 개수)
y_len = len(maze)     # 미로의 세로 길이 (행의 개수)

# 미로를 그리기
for y in range(y_len):                                                      # for 미로의 행을 반복
    for x in range(x_len):                                                      # for 각 행의 열을 반복
        if maze[y][x] == 1:                                                         # if 현재 위치가 벽(1)인지 확인
            wall.penup()                                                                # 터틀을 들어 올려 선을 그리지 않음
            wall.goto((x - (x_len // 2)) * 24, ((y_len // 2) - y) * 24)                 # 벽의 좌표로 이동, 미로의 중심을 (0,0)으로 설정
            wall.pendown()                                                              # 터틀을 내려 선을 그리기 시작
            wall.begin_fill()                                                           # 벽을 채우기 시작
            for _ in range(4):                                                          # for 사각형의 네 변을 반복
                wall.forward(24)                                                            # 각 변의 길이만큼 앞으로 이동
                wall.right(90)                                                              # 오른쪽으로 90도 회전
            wall.end_fill()                                                             # 벽 채우기 완료

# 플레이어 설정
player = turtle.Turtle()  # 플레이어를 위한 터틀 객체 생성
player.shape('turtle')    # 플레이어 모양을 거북이로 설정
player.color('blue')      # 플레이어 색을 파란색으로 설정
player.penup()            # 선을 그리지 않도록 플레이어 터틀을 들어 올림

# 초기 플레이어 위치
player_x = 1  # 플레이어의 초기 x 좌표
player_y = 1  # 플레이어의 초기 y 좌표

# 플레이어 이동 함수
def player_move(set_h):
    # 플레이어의 새로운 좌표 계산
    move_x = (player_x - (x_len // 2)) * 24 + 12
    move_y = ((y_len // 2) - player_y) * 24 - 12
    # 플레이어의 방향 설정
    player.setheading(set_h)
    # 플레이어를 새로운 좌표로 이동
    player.goto(move_x, move_y)

def move(move_x, move_y, set_h):
    global player_x, player_y, start_time, end_time
    if maze[player_y + move_y][player_x + move_x] == 0:                         # 플레이어가 이동할 위치가 길(0)인지 확인
        if start_time is None:
            start_time = time.time()                                                # 처음 이동 시 시작 시간 기록
        player_x += move_x                                                          # 플레이어의 x 좌표를 이동
        player_y += move_y                                                          # 플레이어의 y 좌표를 이동
        player_move(set_h)                                                          # 플레이어를 새로운 위치로 이동
        if (player_x, player_y) == (x_len - 2, y_len - 2):                      # 목표 위치에 도달했는지 확인
            end_time = time.time()                                                  # 도착 시 종료 시간 기록
            elapsed_time = end_time - start_time                                    # 경과 시간 계산
            text_turtle.write(f"Elapsed time:\n   {elapsed_time:.2f} seconds", align='left', font=('Arial', 16, 'normal'))

# 방향별 이동 함수
def move_up():
    move(0, -1, 90)  # 위쪽으로 이동, 방향은 90도

def move_down():
    move(0, 1, 270)  # 아래쪽으로 이동, 방향은 270도

def move_left():
    move(-1, 0, 180)  # 왼쪽으로 이동, 방향은 180도

def move_right():
    move(1, 0, 0)    # 오른쪽으로 이동, 방향은 0도

# 키보드 이벤트 바인딩
win.onkey(move_up, 'Up')            # 'Up' 키를 누르면 위로 이동
win.onkey(move_down, 'Down')        # 'Down' 키를 누르면 아래로 이동
win.onkey(move_left, 'Left')        # 'Left' 키를 누르면 왼쪽으로 이동
win.onkey(move_right, 'Right')      # 'Right' 키를 누르면 오른쪽으로 이동

start_time = None  # 게임 시작 시간 초기화
end_time = None  # 게임 종료 시간 초기화

text_turtle = turtle.Turtle()           # 시간을 표시할 터틀 객체 생성
text_turtle.hideturtle()                # 시간을 표시할 때 터틀을 숨김
text_turtle.penup()                     # 선을 그리지 않도록 터틀을 들어 올림
text_turtle.color('red')                # 텍스트 색상을 빨간색으로 설정
text_turtle.goto((0 - (x_len // 2)) * 24, ((y_len // 2) - 0) * 24 + 15)  # 텍스트를 화면의 상단 중앙으로 이동

# 키보드 입력을 기다림
win.listen()

# 초기 플레이어 위치로 이동
player_move(0)

# 터틀 이벤트 루프 시작
turtle.done()
