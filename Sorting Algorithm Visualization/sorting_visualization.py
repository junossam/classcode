#######################################################################
# 파일명: sorting_visualization_v0.4.py
# 프로그램설명: 정렬 알고리즘 학습을 위한 시각화 프로그램입니다.
# 개발자: 성서고등학교 교사 강준호
# E-mail: junh048@dge.go.kr
# 
# 형상관리
# - v0.3(2024. 9. 25.) : 초기 버전 완성
# - v0.4(2024. 10. 15.) : 키보드 기능 추가
#######################################################################

"""
프로그램 설명
  - 추를 이동하여 저울에 2개 올리면 더 무거운 것이 표시됩니다.
  - 저울에 무게를 측정할 때마다 카운트가 증가합니다.
  - 왼쪽 위의 5가지 색상의 원은 자유롭게 이동 가능하며, 변수 i, j 등의 역할을 수행할 때 사용할 수 있습니다.
  - 오른쪽 아래 확인 버튼을 누르면 추의 무게가 표시됩니다.
  - 추가적으로 '초기화 - 랜덤' 버튼과 '초기화 - 오름차순' 버튼이 추가되어 무게추의 초기 상태를 설정할 수 있습니다.
"""

import pygame
import sys
import random

# 1. pygame 초기화 및 화면 설정
pygame.init()
screen_width = 1200  # 화면의 가로 크기
screen_height = 800  # 화면의 세로 높이
screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 생성
pygame.display.set_caption("Sorting Algorithm Visualization v1.0(2024. 9. 24.) - 성서고등학교 정보 교사 강준호")  # 윈도우 제목 설정

# 2. 색상 정의
WHITE = (255, 255, 255)  # 흰색 (배경색)
BLACK = (0, 0, 0)  # 검정색 (선 색상)
RED = (255, 0, 0)  # 빨간색 (무게 표시 및 스티커 색상)
GREEN = (0, 255, 0)  # 초록색 (버튼 색상 및 스티커 색상)
BLUE = (0, 0, 255)  # 파란색 (스티커 색상)
ORANGE = (255, 165, 0)  # 주황색 (스티커 색상)
PURPLE = (128, 0, 128)  # 보라색 (스티커 색상)

# 3. 폰트 설정
font_path = './font/NanumGothic.ttf'  # 나눔 고딕 파일 경로 지정
font_size = 26  # 폰트 크기 설정
button_font = pygame.font.Font(font_path, font_size)  # 확인 버튼을 그릴 때 사용할 폰트
scale_font = pygame.font.Font(font_path, 36)  # 저울 값 표시 폰트

# 4. 무게추와 관련된 설정
weight_area_width = 50  # 무게추 공간의 가로 너비
weight_area_height = 80  # 무게추 공간의 세로 높이
weight_area_spacing = 10  # 무게추 공간 사이의 간격
weight_area_start_x = screen_width - 10 * (weight_area_width + weight_area_spacing) - 20  # 무게추 공간의 시작 x 좌표
weight_area_start_y = 20  # 무게추 공간의 시작 y 좌표

# 5. 무게추 이미지 로드 및 크기 조정
weight_image = pygame.image.load('./images/weight_image.png')  # 무게추 이미지 파일 불러오기
weight_image = pygame.transform.scale(weight_image, (weight_area_width, weight_area_height))  # 무게추 이미지를 (50, 80) 크기로 조정

# 6. 저울 이미지 로드 및 크기 조정
scale_image_normal = pygame.image.load('./images/scale_normal.png')  # 수평 저울 이미지
scale_image_left = pygame.image.load('./images/scale_left.png')  # 왼쪽 기울어진 저울 이미지
scale_image_right = pygame.image.load('./images/scale_right.png')  # 오른쪽 기울어진 저울 이미지
scale_image_size = (300, 250)  # 저울 이미지 크기
scale_image_normal = pygame.transform.scale(scale_image_normal, scale_image_size)  # 이미지 크기 조정
scale_image_left = pygame.transform.scale(scale_image_left, scale_image_size)  # 이미지 크기 조정
scale_image_right = pygame.transform.scale(scale_image_right, scale_image_size)  # 이미지 크기 조정

# 7. 전역 변수 초기화
weight_areas = []  # 무게추를 놓을 수 있는 공간 리스트
weights = []  # 무게추 객체 리스트
stickers = []  # 스티커 리스트
left_offset_y = 0  # 왼쪽 접시의 y축 오프셋
right_offset_y = 0  # 오른쪽 접시의 y축 오프셋
scale_value = 0  # 저울의 값
previous_left_weight = None  # 이전에 왼쪽 접시에 놓였던 무게추
previous_right_weight = None  # 이전에 오른쪽 접시에 놓였던 무게추
scale_rect = pygame.Rect(50, screen_height - 300, 300, 200)  # 저울의 전체 영역
button_rect = pygame.Rect(screen_width - 350, screen_height - 100, 300, 50)  # 확인 버튼의 사각형 영역
reset_random_button_rect = pygame.Rect(screen_width - 350, screen_height - 170, 300, 50)  # 초기화 - 랜덤 버튼의 사각형 영역
reset_sorted_button_rect = pygame.Rect(screen_width - 350, screen_height - 240, 300, 50)  # 초기화 - 오름차순 버튼의 사각형 영역
reset_descending_button_rect = pygame.Rect(screen_width - 350, screen_height - 310, 300, 50)  # 초기화 - 내림차순 버튼의 사각형 영역
left_plate_weight = None  # 왼쪽 접시에 놓인 무게추
right_plate_weight = None  # 오른쪽 접시에 놓인 무게추
show_weights = False  # 무게를 표시할지 여부
dragging_sticker = None  # 드래그 중인 스티커
last_click_time = 0  # 마지막 클릭 시간을 저장하기 위한 변수
double_click_threshold = 400  # 더블 클릭 인식 시간 (밀리초 단위)
FPS = 60  # 초당 프레임 수 설정
clock = pygame.time.Clock()  # FPS 설정

# 8. 무게추 공간 설정
for i in range(10):  # 10개의 빈 공간 생성
    x = weight_area_start_x + i * (weight_area_width + weight_area_spacing)  # 각 공간의 x 좌표 계산
    y = weight_area_start_y  # y 좌표는 동일
    weight_areas.append({
        'rect': pygame.Rect(x, y, weight_area_width, weight_area_height),  # 무게추를 놓을 수 있는 사각형 영역 생성
        'occupied': False  # 해당 공간이 비어있음을 표시
    })

# 9. 무게추 생성 및 초기화 함수
def initialize_weights(randomize=True, descending=False):
    """
    무게추의 초기 상태를 설정하는 함수입니다.
    :param randomize: True이면 무게추를 랜덤한 무게로 설정하고, False이면 정렬순으로 설정합니다.
    :param descending: False 오름차순, True 내림차순
    """
    global weights, scale_value, left_plate_weight, right_plate_weight, previous_left_weight, previous_right_weight
    weights = []  # 무게추 객체 리스트 초기화
    scale_value = 0  # 카운트 값 초기화
    left_plate_weight = None  # 왼쪽 접시의 무게추 초기화
    right_plate_weight = None  # 오른쪽 접시의 무게추 초기화
    previous_left_weight = None  # 이전 무게추 상태 초기화
    previous_right_weight = None  # 이전 무게추 상태 초기화
    
    for area in weight_areas:
        area['occupied'] = False  # 모든 무게추 공간 비우기

    weight_values = random.sample(range(1, 1001), 10)  # 0~1000 까지 숫자 중에 랜덤의 10개
    if randomize:
        random.shuffle(weight_values)  # 랜덤한 무게 값
    elif descending:
        weight_values.sort(reverse=True)  # 내림차순 정렬
    else:
        weight_values.sort()  # 오름차순 정렬

    for i in range(10):  # 10개의 무게추 생성
        x = weight_areas[i]['rect'].x  # 무게추의 초기 x 좌표
        y = weight_areas[i]['rect'].y  # 무게추의 초기 y 좌표
        weights.append({
            'rect': pygame.Rect(x, y, weight_area_width, weight_area_height),  # 무게추의 사각형 영역 생성
            'image_pos': [x, y],  # 무게추 이미지의 현재 위치 설정
            'dragging': False,  # 무게추가 드래그되고 있는지 여부
            'weight': weight_values[i]  # 무게추의 무게 값
        })
        weight_areas[i]['occupied'] = True  # 해당 공간이 차있음을 표시

# 초기화 - 랜덤 버튼 기능 추가
initialize_weights()  # 초기 실행 시 랜덤 값으로 초기화

# 10. 스티커 생성 및 초기화
sticker_radius = 15  # 스티커의 반지름 설정
sticker_spacing = 20  # 스티커 사이의 간격
sticker_colors = [RED, GREEN, BLUE, ORANGE, PURPLE]  # 스티커 색상 리스트
for i in range(5):  # 5개의 스티커 생성
    x = 50 + i * (sticker_radius * 2 + sticker_spacing)  # 스티커의 초기 x 좌표
    y = 50  # 스티커의 초기 y 좌표
    stickers.append({
        'pos': [x, y],  # 스티커의 중심 좌표
        'color': sticker_colors[i],  # 스티커의 색상 설정
        'dragging': False  # 스티커가 드래그 중인지 여부
    })

# 11. 무게추 공간에 번호를 표시하는 함수 추가
def draw_weight_area_numbers(screen, weight_areas):
    """
    무게추 공간에 번호를 표시합니다.
    :param screen: pygame 화면 객체
    :param weight_areas: 무게추를 놓을 수 있는 공간 리스트
    """
    font = pygame.font.SysFont(None, 24)  # 폰트 설정
    for index, area in enumerate(weight_areas):
        text_surface = font.render(str(index), True, BLACK)  # 번호 텍스트 렌더링
        text_rect = text_surface.get_rect(center=(area['rect'].centerx, area['rect'].bottom + 15))  # 번호를 공간 하단에 위치
        screen.blit(text_surface, text_rect)  # 텍스트를 화면에 그리기

# 12. 무게추의 무게를 표시하는 함수
def draw_weight_text(screen, weight):
    """
    무게추 위에 무게 값을 표시합니다.
    :param screen: pygame 화면 객체
    :param weight: 현재 무게추 객체
    """
    font = pygame.font.SysFont(None, 24)  # 폰트 설정
    text_surface = font.render(str(weight['weight']), True, BLACK)  # 무게 값 텍스트 렌더링
    text_rect = text_surface.get_rect(center=(weight['rect'].centerx, weight['rect'].centery - weight_area_height // 2 - 10))  # 무게추 위에 위치
    screen.blit(text_surface, text_rect)  # 텍스트를 화면에 그리기

# 13. 저울을 그리는 함수
def draw_scale(screen, scale_rect, left_weight=None, right_weight=None):
    """
    저울과 무게추를 그리는 함수입니다.
    :param screen: pygame 화면 객체
    :param scale_rect: 저울의 전체 사각형 영역
    :param left_weight: 왼쪽 접시 위에 있는 무게추
    :param right_weight: 오른쪽 접시 위에 있는 무게추
    """
    global left_offset_y, right_offset_y  # 전역 변수로 선언하여 업데이트

    # 접시 위치 조정 값 초기화
    left_offset_y = 0
    right_offset_y = 0

    # 무게에 따라 저울 이미지 선택 및 무게추 위치 조정
    if left_weight and right_weight:
        if left_weight['weight'] > right_weight['weight']:
            scale_image = scale_image_left  # 왼쪽 기울어진 이미지
            left_offset_y = 40  # 왼쪽 접시가 내려가므로 y 축에서 아래로 이동
            right_offset_y = -20  # 오른쪽 접시는 올라가므로 y 축에서 위로 이동
        else:
            scale_image = scale_image_right  # 오른쪽 기울어진 이미지
            left_offset_y = -20  # 왼쪽 접시는 올라가므로 y 축에서 위로 이동
            right_offset_y = 40  # 오른쪽 접시가 내려가므로 y 축에서 아래로 이동
    elif left_weight:  # 왼쪽만 무게추가 있는 경우
        scale_image = scale_image_left
        left_offset_y = 40  # 왼쪽 접시가 내려가므로 y 축에서 아래로 이동
        right_offset_y = -20  # 오른쪽 접시는 올라가므로 y 축에서 위로 이동
    elif right_weight:  # 오른쪽만 무게추가 있는 경우
        scale_image = scale_image_right
        left_offset_y = -20  # 왼쪽 접시는 올라가므로 y 축에서 위로 이동
        right_offset_y = 40  # 오른쪽 접시가 내려가므로 y 축에서 아래로 이동
    else:
        scale_image = scale_image_normal  # 수평 이미지

    # 저울 이미지 그리기
    screen.blit(scale_image, (scale_rect.x, scale_rect.y))

    # 접시 위치 계산
    left_plate_center = (scale_rect.centerx - 95, scale_rect.centery - 50 + left_offset_y)  # 왼쪽 접시 위치
    right_plate_center = (scale_rect.centerx + 95, scale_rect.centery - 50 + right_offset_y)  # 오른쪽 접시 위치

    # 무게추가 있는 경우 무게추를 접시 위로 이동
    if left_weight:
        left_weight['image_pos'] = [left_plate_center[0] - weight_area_width // 2, left_plate_center[1] - weight_area_height]
        left_weight['rect'].topleft = left_weight['image_pos']
        screen.blit(weight_image, left_weight['image_pos'])

    if right_weight:
        right_weight['image_pos'] = [right_plate_center[0] - weight_area_width // 2, right_plate_center[1] - weight_area_height]
        right_weight['rect'].topleft = right_weight['image_pos']
        screen.blit(weight_image, right_weight['image_pos'])

# 14. 저울 밑에 숫자 표시 함수
def draw_scale_value(screen, scale_rect, scale_value):
    """
    저울 밑에 숫자 값을 표시합니다.
    :param screen: pygame 화면 객체
    :param scale_rect: 저울의 전체 사각형 영역
    :param scale_value: 저울에 표시할 숫자 값
    """
    value_text = scale_font.render(f"Value: {scale_value}", True, RED)  # 값 텍스트 렌더링
    value_rect = value_text.get_rect(center=(scale_rect.centerx, scale_rect.bottom + 70))  # 저울 밑에 위치
    screen.blit(value_text, value_rect)  # 텍스트를 화면에 그리기

# 15. 무게추가 저울의 접시에 놓이는지 확인하는 함수
def place_on_scale(weight, scale_rect, left_offset_y, right_offset_y):
    """
    무게추가 저울의 접시에 놓이는지 확인하고, 접시에 올려놓습니다.
    :param weight: 현재 드래그 중인 무게추 객체
    :param scale_rect: 저울의 전체 사각형 영역
    :param left_offset_y: 왼쪽 접시의 y축 오프셋
    :param right_offset_y: 오른쪽 접시의 y축 오프셋
    :return: 왼쪽 접시이면 'left', 오른쪽 접시이면 'right', 아니면 None 반환
    """
    left_plate_center = (scale_rect.centerx - 85, scale_rect.centery + 10 + left_offset_y)  # 왼쪽 접시의 중심 좌표
    right_plate_center = (scale_rect.centerx + 85, scale_rect.centery + 10 + right_offset_y)  # 오른쪽 접시의 중심 좌표

    # 무게추의 중심 좌표 계산
    weight_center = weight['rect'].center

    # 무게추가 왼쪽 접시 중심에 놓였는지 확인 (좌표 차이가 80 이하일 때)
    if abs(weight_center[0] - left_plate_center[0]) < 80 and abs(weight_center[1] - left_plate_center[1]) < 80:
        return 'left'

    # 무게추가 오른쪽 접시 중심에 놓였는지 확인 (좌표 차이가 80 이하일 때)
    elif abs(weight_center[0] - right_plate_center[0]) < 80 and abs(weight_center[1] - right_plate_center[1]) < 80:
        return 'right'
    
    return None  # 접시에 놓이지 않은 경우 None 반환

# 16. 무게추가 겹치지 않도록 근처 빈 공간으로 자동 정렬하는 함수
def snap_to_area(weight, weight_areas):
    """
    무게추가 근처 빈 공간에 있다면, 해당 공간의 중앙으로 자동 이동시킵니다.
    :param weight: 현재 무게추 객체
    :param weight_areas: 무게추를 놓을 수 있는 공간 리스트
    """
    snap_distance = 50  # 자동 정렬 거리 기준 (값을 늘려 더 쉽게 정렬되도록 조정)
    for area in weight_areas:
        if not area['occupied']:  # 해당 공간이 비어있다면
            area_center_x = area['rect'].centerx  # 공간의 중앙 x 좌표
            area_center_y = area['rect'].centery  # 공간의 중앙 y 좌표
            weight_center_x = weight['rect'].centerx  # 무게추의 중앙 x 좌표
            weight_center_y = weight['rect'].centery  # 무게추의 중앙 y 좌표

            # 무게추가 해당 공간의 중앙에 가까워지면
            if abs(area_center_x - weight_center_x) < snap_distance and abs(area_center_y - weight_center_y) < snap_distance:
                weight['image_pos'][0] = area['rect'].x  # 무게추 x 좌표를 공간의 x 좌표로 이동
                weight['image_pos'][1] = area['rect'].y  # 무게추 y 좌표를 공간의 y 좌표로 이동
                weight['rect'].topleft = (area['rect'].x, area['rect'].y)  # 무게추의 사각형 위치도 업데이트
                area['occupied'] = True  # 공간이 차있음을 표시
                break

# 17. 빈 공간을 찾는 함수
def find_nearby_empty_space(current_weight, current_rect, weight_areas, weights, screen_width, screen_height):
    """
    무게추가 놓일 때 다른 무게추와 겹치지 않는 근처의 빈 공간을 찾습니다.
    :param current_weight: 현재 드래그 중인 무게추 객체
    :param current_rect: 현재 무게추의 사각형 위치
    :param weight_areas: 무게추를 놓을 수 있는 공간 리스트
    :param weights: 모든 무게추의 리스트
    :param screen_width: 화면 너비
    :param screen_height: 화면 높이
    :return: 겹치지 않는 빈 공간의 좌표 리스트 [x, y], 찾지 못하면 None 반환
    """
    step = 5  # 무게추를 이동시킬 거리 단위 (5 픽셀씩 이동)
    max_attempts = 50  # 최대 시도 횟수
    
    for attempt in range(max_attempts):  # 최대 시도 횟수만큼 반복
        directions = [(step, 0), (-step, 0), (0, step), (0, -step), (step, step), (-step, step), (step, -step), (-step, -step)]  # 8방향 이동
        random.shuffle(directions)  # 방향을 무작위로 섞기
        for dx, dy in directions:  # 모든 방향에 대해 시도
            new_rect = current_rect.move(dx, dy)  # 현재 위치에서 새로운 위치로 이동

            # 화면을 벗어나지 않는지 확인
            if new_rect.left < 0 or new_rect.right > screen_width or new_rect.top < 0 or new_rect.bottom > screen_height:
                continue  # 화면을 벗어나면 건너뛰기

            # 다른 무게추와 겹치는지 확인 (자기 자신 제외)
            if not any(new_rect.colliderect(weight['rect']) for weight in weights if weight != current_weight):
                return [new_rect.x, new_rect.y]  # 겹치지 않는 위치를 찾으면 반환

        step += 3  # 탐색 반경을 넓히기 위해 step 증가

    return None  # 빈 공간을 찾지 못한 경우

# 18. 무게추를 겹치지 않는 빈 공간으로 이동하는 함수
def move_to_nearest_empty(current_weight, weight_areas, weights, screen_width, screen_height):
    """
    무게추가 겹치지 않는 빈 공간을 찾을 때까지 이동시킵니다.
    :param current_weight: 현재 무게추 객체
    :param weight_areas: 무게추를 놓을 수 있는 공간 리스트
    :param weights: 모든 무게추의 리스트
    :param screen_width: 화면 너비
    :param screen_height: 화면 높이
    """
    max_attempts = 20  # 최대 20번 이동 시도
    for _ in range(max_attempts):
        empty_space = find_nearby_empty_space(
            current_weight,
            pygame.Rect(current_weight['image_pos'][0], current_weight['image_pos'][1], weight_area_width, weight_area_height),
            weight_areas,
            weights,
            screen_width,
            screen_height
        )
        if empty_space:
            current_weight['image_pos'] = empty_space  # 빈 공간으로 이동
            current_weight['rect'].topleft = empty_space  # 사각형 위치도 함께 변경
        else:
            break  # 더 이상 이동할 수 있는 빈 공간이 없으면 중단

# 19. 다른 무게추와 겹치는지 확인하는 함수
def is_overlapping_with_other_weights(weight, weights):
    """
    주어진 무게추가 다른 무게추와 겹치는지 확인합니다.
    :param weight: 현재 확인할 무게추 객체
    :param weights: 모든 무게추의 리스트
    :return: 겹치면 True, 겹치지 않으면 False
    """
    current_rect = weight['rect']  # 현재 무게추의 사각형 영역
    for other_weight in weights:
        if other_weight != weight and current_rect.colliderect(other_weight['rect']):  # 자기 자신을 제외하고 겹치는지 확인
            return True  # 다른 무게추와 겹치면 True 반환
    return False  # 겹치지 않으면 False 반환

# 20. 게임 루프 및 이벤트 처리
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 윈도우 닫기 버튼을 누르면 루프 종료
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼을 눌렀을 때
            if reset_random_button_rect.collidepoint(event.pos):  # 초기화 - 랜덤 버튼 클릭 시
                initialize_weights(randomize=True)  # 무게추를 랜덤 값으로 초기화
            elif reset_sorted_button_rect.collidepoint(event.pos):  # 초기화 - 오름차순 버튼 클릭 시
                initialize_weights(randomize=False)  # 무게추를 오름차순으로 초기화
            elif reset_descending_button_rect.collidepoint(event.pos):  # 초기화 - 내림차순 버튼 클릭 시
                initialize_weights(randomize=False, descending=True)  # 무게추를 내림차순으로 초기화


            for sticker in stickers:
                distance = ((sticker['pos'][0] - event.pos[0])**2 + (sticker['pos'][1] - event.pos[1])**2)**0.5
                if distance <= sticker_radius:  # 마우스가 스티커 위에 있으면
                    sticker['dragging'] = True  # 드래그 상태로 전환
                    mouse_x, mouse_y = event.pos  # 마우스의 현재 위치
                    offset_x = sticker['pos'][0] - mouse_x  # 스티커와 마우스 사이의 x 좌표 차이
                    offset_y = sticker['pos'][1] - mouse_y  # 스티커와 마우스 사이의 y 좌표 차이
                    dragging_sticker = sticker  # 드래그 중인 스티커 설정
                    # 스티커를 리스트의 마지막으로 이동하여 가장 위에 표시되도록 함
                    stickers.remove(sticker)
                    stickers.append(sticker)
                    break

            for weight in weights:
                if weight['rect'].collidepoint(event.pos):  # 마우스가 무게추 이미지 위에 있으면
                    weight['dragging'] = True  # 드래그 상태로 전환
                    mouse_x, mouse_y = event.pos  # 마우스의 현재 위치
                    offset_x = weight['image_pos'][0] - mouse_x  # 무게추와 마우스 사이의 x 좌표 차이
                    offset_y = weight['image_pos'][1] - mouse_y  # 무게추와 마우스 사이의 y 좌표 차이

                    # 저울 위에 있는 무게추를 드래그하려면 해당 접시에서 제거
                    if weight == left_plate_weight:
                        left_plate_weight = None  # 왼쪽 접시에서 제거
                    elif weight == right_plate_weight:
                        right_plate_weight = None  # 오른쪽 접시에서 제거

                    # 무게추가 현재 위치한 공간의 occupied 상태를 False로 변경
                    for area in weight_areas:
                        if area['rect'].colliderect(weight['rect']):  # 무게추가 공간을 벗어남을 표시
                            area['occupied'] = False  # 무게추가 공간에서 빠져나왔음을 표시
                            break

            # 확인 버튼 클릭 시 무게 표시
            if button_rect.collidepoint(event.pos):
                show_weights = not show_weights  # 무게 표시 여부를 토글

        elif event.type == pygame.MOUSEBUTTONUP:  # 마우스 버튼을 놓았을 때
            for sticker in stickers:
                if sticker['dragging']:  # 드래그 중인 스티커에 대해
                    sticker['dragging'] = False  # 드래그 상태 해제
                    dragging_sticker = None  # 드래그 중인 스티커 초기화

            for weight in weights:
                if weight['dragging']:  # 드래그 중인 무게추에 대해
                    weight['dragging'] = False  # 드래그 상태 해제

                    # 무게추가 저울의 접시에 놓이는지 확인 (저울의 현재 기울기 상태에 따른 오프셋 사용)
                    scale_position = place_on_scale(weight, scale_rect, left_offset_y, right_offset_y)
                    if scale_position == 'left':
                        left_plate_weight = weight  # 왼쪽 접시에 무게추 올리기
                    elif scale_position == 'right':
                        right_plate_weight = weight  # 오른쪽 접시에 무게추 올리기

                    # 저울에 두 개의 무게추가 모두 올라가 있는 경우
                    if left_plate_weight and right_plate_weight:
                        # 저울 위의 무게추가 변경된 경우에만 값 증가
                        if (left_plate_weight != previous_left_weight or right_plate_weight != previous_right_weight):
                            scale_value += 1  # 값 1 증가
                            # 이전 상태 업데이트
                            previous_left_weight = left_plate_weight
                            previous_right_weight = right_plate_weight
                    else:
                        # 저울 위의 무게추가 하나라도 없으면 이전 상태 초기화
                        previous_left_weight = None
                        previous_right_weight = None
                        
                    # 무게추가 지정된 공간과 겹치는지 확인
                    in_area = False
                    for area in weight_areas:
                        if weight['rect'].colliderect(area['rect']) and not area['occupied']:  # 무게추가 빈 공간에 있으면
                            weight['image_pos'][0] = area['rect'].x  # 무게추의 x 좌표를 공간의 x 좌표로 이동
                            weight['image_pos'][1] = area['rect'].y  # 무게추의 y 좌표를 공간의 y 좌표로 이동
                            weight['rect'].topleft = (area['rect'].x, area['rect'].y)  # 무게추의 사각형 위치도 업데이트
                            area['occupied'] = True  # 공간이 차있음을 표시
                            in_area = True  # 공간에 배치되었음을 표시
                            break

                    # 다른 무게추와 겹치는지 확인하고, 겹치는 경우 빈 공간으로 이동
                    if not in_area and is_overlapping_with_other_weights(weight, weights):
                        move_to_nearest_empty(weight, weight_areas, weights, screen_width, screen_height)

                    # 빈 공간 근처일 경우 자동 정렬 시도
                    snap_to_area(weight, weight_areas)

        elif event.type == pygame.MOUSEMOTION:  # 마우스가 움직일 때
            for sticker in stickers:
                if sticker['dragging']:  # 드래그 중인 스티커에 대해
                    mouse_x, mouse_y = event.pos  # 마우스의 현재 위치
                    sticker['pos'][0] = mouse_x + offset_x  # 스티커의 x 위치를 마우스 위치에 따라 이동
                    sticker['pos'][1] = mouse_y + offset_y  # 스티커의 y 위치를 마우스 위치에 따라 이동

            for weight in weights:
                if weight['dragging']:  # 드래그 중인 무게추에 대해
                    mouse_x, mouse_y = event.pos  # 마우스의 현재 위치
                    weight['image_pos'][0] = mouse_x + offset_x  # 무게추의 x 위치를 마우스 위치에 따라 이동
                    weight['image_pos'][1] = mouse_y + offset_y  # 무게추의 y 위치를 마우스 위치에 따라 이동
                    weight['rect'].topleft = (weight['image_pos'][0], weight['image_pos'][1])  # 사각형 위치도 업데이트

        elif event.type == pygame.KEYDOWN:  # 키보드 키를 눌렀을 때
            if event.key == pygame.K_SPACE:  # 스페이스바가 눌렸을 때
                if left_plate_weight and right_plate_weight:  # 저울에 두 개의 무게추가 모두 있는지 확인
                    # 가벼운 무게추와 무거운 무게추 구분
                    if left_plate_weight['weight'] < right_plate_weight['weight']:
                        lighter_weight = left_plate_weight
                        heavier_weight = right_plate_weight
                    else:
                        lighter_weight = right_plate_weight
                        heavier_weight = left_plate_weight

                    # 가벼운 무게추를 빈 공간 리스트의 앞쪽으로 이동
                    for area in weight_areas:
                        if not area['occupied']:
                            lighter_weight['image_pos'] = [area['rect'].x, area['rect'].y]
                            lighter_weight['rect'].topleft = lighter_weight['image_pos']
                            area['occupied'] = True
                            break

                    # 무거운 무게추를 빈 공간 리스트의 뒤쪽으로 이동
                    for area in reversed(weight_areas):
                        if not area['occupied']:
                            heavier_weight['image_pos'] = [area['rect'].x, area['rect'].y]
                            heavier_weight['rect'].topleft = heavier_weight['image_pos']
                            area['occupied'] = True
                            break

                    # 저울의 상태를 초기화
                    left_plate_weight = None
                    right_plate_weight = None
                    previous_left_weight = None
                    previous_right_weight = None

            elif event.unicode.isdigit():  # 눌린 키가 숫자일 때
                index = int(event.unicode)
                if 0 <= index < len(weight_areas):  # 인덱스가 공간 리스트 범위 내에 있을 때
                    selected_area = weight_areas[index]
                    if selected_area['occupied']:  # 해당 공간이 비어있지 않으면
                        # 해당 공간에 있는 무게추 찾기
                        selected_weight = None
                        for weight in weights:
                            if weight['rect'].colliderect(selected_area['rect']):
                                selected_weight = weight
                                break

                        if selected_weight:  # 해당 공간에 무게추가 있다면
                            if not left_plate_weight:  # 왼쪽 접시가 비어있다면
                                left_plate_weight = selected_weight
                            elif not right_plate_weight:  # 오른쪽 접시가 비어있다면
                                right_plate_weight = selected_weight
                            else:
                                continue  # 둘 다 비어있지 않으면 아무 작업도 하지 않음

                            # 무게추를 저울의 접시에 놓기
                            scale_position = place_on_scale(selected_weight, scale_rect, left_offset_y, right_offset_y)
                            if scale_position == 'left':
                                left_plate_weight = selected_weight
                            elif scale_position == 'right':
                                right_plate_weight = selected_weight

                            # 무게추가 저울 접시에 놓이면 occupied 상태 업데이트
                            selected_area['occupied'] = False  # 무게추가 공간에서 빠져나왔음을 표시

                            # 저울에 두 개의 무게추가 모두 올라가 있는 경우
                            if left_plate_weight and right_plate_weight:
                                # 저울 위의 무게추가 변경된 경우에만 값 증가
                                if (left_plate_weight != previous_left_weight or right_plate_weight != previous_right_weight):
                                    scale_value += 1  # 값 1 증가
                                    # 이전 상태 업데이트
                                    previous_left_weight = left_plate_weight
                                    previous_right_weight = right_plate_weight
                            else:
                                # 저울 위의 무게추가 하나라도 없으면 이전 상태 초기화
                                previous_left_weight = None
                                previous_right_weight = None

    # 21. 화면 채우기 (배경 그리기)
    screen.fill(WHITE)  # 배경을 흰색으로 채움

    # 22. 저울 그리기
    draw_scale(screen, scale_rect, left_plate_weight, right_plate_weight)

    # 23. 저울 밑에 값 표시
    draw_scale_value(screen, scale_rect, scale_value)

    # 24. 무게추 공간 및 이미지 그리기
    for area in weight_areas:
        pygame.draw.rect(screen, BLACK, area['rect'], 2)  # 빈 공간을 검은색 사각형으로 표시
    draw_weight_area_numbers(screen, weight_areas)  # 무게추 공간에 번호 그리기 추가
    for weight in weights:
        screen.blit(weight_image, weight['image_pos'])  # 모든 무게추 그리기 (저울 위 포함)
        if show_weights:
            draw_weight_text(screen, weight)  # 무게추 위에 무게 표시

    # 25. 스티커 그리기 (가장 마지막에 그려서 최상단에 표시)
    for sticker in stickers:
        pygame.draw.circle(screen, sticker['color'], sticker['pos'], sticker_radius)  # 각 스티커를 원형으로 그리기

    # 26. 확인 버튼 그리기
    pygame.draw.rect(screen, GREEN, button_rect)  # 확인 버튼을 초록색으로 그리기
    if show_weights == False:
        text_surface = button_font.render("보이기", True, BLACK)  # 확인 버튼 텍스트
    else:
        text_surface = button_font.render("감추기", True, BLACK)  # 확인 버튼 텍스트
    text_rect = text_surface.get_rect(center=button_rect.center)  # 버튼의 중앙에 텍스트 중앙을 맞추기
    screen.blit(text_surface, text_rect)  # 텍스트를 버튼에 표시

    # 초기화 - 랜덤 버튼 그리기
    pygame.draw.rect(screen, BLUE, reset_random_button_rect)  # 초기화 - 랜덤 버튼을 파란색으로 그리기
    text_surface = button_font.render("초기화 - 랜덤", True, BLACK)  # 초기화 - 랜덤 버튼 텍스트
    text_rect = text_surface.get_rect(center=reset_random_button_rect.center)  # 버튼의 중앙에 텍스트 중앙을 맞추기
    screen.blit(text_surface, text_rect)  # 텍스트를 버튼에 표시

    # 초기화 - 오름차순 버튼 그리기
    pygame.draw.rect(screen, ORANGE, reset_sorted_button_rect)  # 초기화 - 오름차순 버튼을 주황색으로 그리기
    text_surface = button_font.render("초기화 - 오름차순", True, BLACK)  # 초기화 - 오름차순 버튼 텍스트
    text_rect = text_surface.get_rect(center=reset_sorted_button_rect.center)  # 버튼의 중앙에 텍스트 중앙을 맞추기
    screen.blit(text_surface, text_rect)  # 텍스트를 버튼에 표시
    
    # 초기화 - 내림차순 버튼 그리기
    pygame.draw.rect(screen, PURPLE, reset_descending_button_rect)  # 초기화 - 내림차순 버튼을 보라색으로 그리기
    text_surface = button_font.render("초기화 - 내림차순", True, BLACK)  # 초기화 - 내림차순 버튼 텍스트
    text_rect = text_surface.get_rect(center=reset_descending_button_rect.center)  # 버튼의 중앙에 텍스트 중앙을 맞추기
    screen.blit(text_surface, text_rect)  # 텍스트를 버튼에 표시


    # 27. 화면 업데이트
    pygame.display.flip()  # 화면을 새로고침

    # 28. FPS 조절
    clock.tick(FPS)  # 설정된 FPS로 화면 업데이트 속도 조절

# 29. pygame 종료
pygame.quit()
sys.exit()
