from mcpi.minecraft import Minecraft
import time
import math
import board
from PIL import Image
import adafruit_ssd1306
import digitalio
import time

# Define the Reset Pin 
reset_pin = digitalio.DigitalInOut(board.D4)

# Display Size
WIDTH = 128
HEIGHT = 64

i2c = board.I2C()

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH,HEIGHT,i2c,addr=0x3c,reset=reset_pin)

oled.fill(0)
oled.show()

# ========================================================================
# ★ 하드웨어 출력은 맨 아래 시작점(Starting Point)에서 적용하면 됨
# ========================================================================

# 1 깨끗한 돌 2 풀흙 3 흙 4 제련된 돌 8,9 물 10,11 용암 12 모래  17나무 18나뭇잎
# 67 제련된 계단 108 벽돌 계단 109 깨끗한 계단 128 흙 계단 134,135,136 나무 계단 156 석영 계단 114 계단
stairs=(67,108,109,128,134,135,136,156,114)

# time.sleep() 주기
TIME_SLEEP_CYCLE = 0.5

mc = Minecraft.create()
sleep_cnt = 0.0     # 연속해서 움직이지 않은 시간(초)
fly_cnt = 0.0       # 연속해서 공중에 떠 있은 시간(초)

# ========================================================================

# 걷고 있는 상태인지 확인
def is_walking(x1, z1):
    x2, _, z2 = mc.player.getPos()
    if (abs(x1-x2) >= 0.5) or (abs(z1-z2) >= 0.5):
        return True
    return False

# 점프하고 있는 상태인지 확인
def is_jumping(y1, block_foot):
    y2 = mc.player.getPos().y
    if (0 < abs(y1-y2) <= 1.5) and block_foot == 0:
        return True
    return False

# 공중에 떠 있은 시간 업데이트
def increase_flying_cnt(block_foot, block_under):
    global fly_cnt
    if block_foot == 0 and block_under == 0:
        fly_cnt += TIME_SLEEP_CYCLE
    else:
        fly_cnt = 0

# 움직이지 않은 시간 초기화
def init_sleep_cnt():
    global sleep_cnt
    sleep_cnt = 0.0

# 움직이지 않은 시간 업데이트
def increase_sleep_cnt(x1, y1, z1):
    global sleep_cnt
    x2, y2, z2 = mc.player.getPos()
    if ((x1, y1, z1) == (x2, y2, z2)):
        sleep_cnt += TIME_SLEEP_CYCLE
    else:
        sleep_cnt = 0.0

# ========================================================================

# Input Mode >> 1
def minecraft_func():
    time.sleep(TIME_SLEEP_CYCLE)

    # 캐릭터 및 블록의 좌표 계산
    px, py, pz = mc.player.getPos()
    block_head = mc.getBlock(px, math.ceil(py+1), pz)
    block_body = mc.getBlock(px, math.ceil(py), pz)
    block_foot = mc.getBlock(px, math.ceil(py-1), pz)
    block_under = mc.getBlock(px, math.ceil(py-2), pz)

    # 공격 이벤트(철 검을 들고 마우스 우클릭)
    hit_blocks = tuple(mc.events.pollBlockHits())
    hit_times = len(hit_blocks) 

    # 1회 공격 시
    if hit_times == 1:
        init_sleep_cnt()
        return "Attacked"

    # 2회 이상 공격 시
    if hit_times > 2:
        init_sleep_cnt()
        # 공격한 블럭들을 모두 철 블록으로 변환
        for block in hit_blocks:
            mc.setBlock(block.pos.x, block.pos.y, block.pos.z, 42)
        return "Transformed into Iron"
        
    increase_sleep_cnt(px, py, pz)
    
    if sleep_cnt >= 5.0:
        return "Sleeping"   # 잠자기(5초동안 이동 없음)

    if (block_body in (10, 11)) or (block_foot in (10, 11)):
        return "Burning in Lava"   # 용암 안에서 타고 있음

    if block_head in (8, 9):
        return "Diving"     # 잠수(머리가 물 속에 있음)

    if (block_body in (8, 9)) or (block_foot in (8, 9)):
        return "Swimming"   # 수영(몸 또는 발이 물 속에 있음)

    if (block_body == 65) or (block_foot == 65):
        return "On Ladder"  # 사다리를 타고 있음

    if (block_body in stairs) or (block_foot in stairs) or (block_under in stairs):
        return "On Stairs"  # 계단 위에 있음
    
    increase_flying_cnt(block_foot, block_under)

    if (fly_cnt > 0.5) and (block_under == 0):
        return "Flying"     # 비행

    if is_jumping(py, block_foot):
        return "Jumping"    # 점프

    if is_walking(px, pz):
        return "Walking"    # 걷기

    if round(float(py) - int(py), 1) in (0.8, -0.2) :
        return "Sitting Down"   # 앉기(Shift 키)

    return ""

# Input Mode >> 2
def what_under_block():
        time.sleep(0.5)
        px,py,pz = mc.player.getPos()
        under_block = mc.getBlock(px,math.ceil(py-2),pz)
        return str(under_block)

# Input Mode >> 3
def what_under_blocks():
        user_in = int(input("block code input : "))
        time.sleep(1.0)
        px,py,pz = mc.player.getPos()
        tx = (-1,0,1)
        for x in tx:
                for z in tx:
                        under_block = mc.getBlock(px+x,math.ceil(py-2),pz+z)
                        if under_block == user_in:
                                return "O"
                        else:
                                answer = "X"
        return answer

# ========================================================================

# 실행할 모드 입력
def input_mode():
    print("1 = 캐릭터 행동 감지 + 연금술 모드")
    print("2 = 캐릭터 2칸 아래에 있는 블록의 종류를 확인함")
    print("3 = 입력한 블록 코드가 캐릭터 2칸 아래 3*3 범위에 존재하는지 확인함")
    print("※ 그 외의 값을 입력하면 프로그램 종료\n")

    try:
        selected_mode = int(input("Input Mode >> "))
    except:
        exit()

    return selected_mode


# 이미지 코드(문자열) 반환받기
def get_image_code(mode):
    if mode == 1:
        return minecraft_func()
    elif mode == 2:
        return what_under_block()
    elif mode == 3:
        return what_under_blocks()
    return ""

# ========================================================================



# ========================================================================
# 시작점 (Starting Point)
# ========================================================================

# 실행할 모드 입력
main_mode = input_mode()

# 반복 실행
while True:
    image_code = get_image_code(main_mode)  # 이미지 코드(문자열) 반환받기
    if image_code != "":            # 공백이 아닐 경우
        mc.postToChat(image_code)   # 메시지 출력
        # OLED에 이미지 출력
        try:
            image = Image.open(image_code+".png").convert('1')
            oled.image(image)
            oled.show()
        except:
            pass

# ========================================================================
