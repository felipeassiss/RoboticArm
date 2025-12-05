import numpy as np
import cv2 as cv
import time
from picamera2 import Picamera2
import pigpio

pi = pigpio.pi()

BASE = 17
OMBRO = 18
GARRA = 22
COTOVELO = 23

def set_angle(pin, angle):
pulse = 500 + (angle / 180) * 2000
pi.set_servo_pulsewidth(pin, pulse)
time.sleep(0.5)

def abrir_garra():
set_angle(GARRA, 170)

def fechar_garra():
set_angle(GARRA, 60)

def posicao_descanso():
set_angle(BASE, 90)
set_angle(OMBRO, 90)
set_angle(COTOVELO, 90)
abrir_garra()

def abaixar_para_pegar():
set_angle(OMBRO, 120)
set_angle(COTOVELO, 60)

def levantar_objeto():
set_angle(OMBRO, 60)
set_angle(COTOVELO, 110)

def colocar_na_caixa_vermelha():
set_angle(BASE, 150)
set_angle(OMBRO, 60)
abrir_garra()

def colocar_na_caixa_azul():
set_angle(BASE, 40)
set_angle(OMBRO, 60)
abrir_garra()

def colocar_na_caixa_verde():
set_angle(BASE, 180)
set_angle(OMBRO, 60)
abrir_garra()


def get_contours(mask, frame, color_name, draw_color):
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

for cnt in contours:
area = cv.contourArea(cnt)

if area > 1000:
x, y, w, h = cv.boundingRect(cnt)
cv.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
cv.putText(frame, color_name, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.7, draw_color, 2)
return True

return False

picam2 = Picamera2()
config = picam2.create_preview_configuration(
main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(config)
picam2.start()

kernel = np.ones((5, 5), np.uint8)

frozen = False
last_frame = None

freeze_delay = 5 # <-- TEMPO EM SEGUNDOS ANTES DE CONGELAR
detected_time = None # quando detectou

while True:
posicao_descanso()
time.sleep(0.5)

if not frozen:
frame = picam2.capture_array()
last_frame = frame.copy()
else:
frame = last_frame

imgHsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

# --- FAIXAS DE CORES ---
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])
mask_red = cv.inRange(imgHsv, lower_red1, upper_red1) + cv.inRange(imgHsv, lower_red2, upper_red2)

lower_green = np.array([40, 70, 70])
upper_green = np.array([80, 255, 255])
mask_green = cv.inRange(imgHsv, lower_green, upper_green)

lower_blue = np.array([100, 100, 100])
upper_blue = np.array([130, 255, 255])
mask_blue = cv.inRange(imgHsv, lower_blue, upper_blue)

mask_red = cv.dilate(mask_red, kernel, iterations=1)
mask_green = cv.dilate(mask_green, kernel, iterations=1)
mask_blue = cv.dilate(mask_blue, kernel, iterations=1)

detected = False
cor = ""

if not frozen:
# Detecta cores
if not detected:
detected = get_contours(mask_red, frame, "Vermelho", (0, 0, 255))
cor = "Vermelho"
if not detected:
detected = get_contours(mask_green, frame, "Verde", (0, 255, 0))
cor = "Verde"
if not detected:
detected = get_contours(mask_blue, frame, "Azul", (255, 0, 0))
cor = "Azul"

if detected and detected_time is None:
detected_time = time.time() # marca momento em que detectou

# Se já detectou, espera o tempo antes de congelar
if detected_time is not None:
if time.time() - detected_time >= freeze_delay:
frozen = True
picam2.stop()

abaixar_para_pegar()
time.sleep(1)

fechar_garra()
time.sleep(0.5)

levantar_objeto()
time.sleep(1)

if cor == "Vermelho":
colocar_na_caixa_vermelha()
time.sleep(0.5)
elif cor == "Azul" :
colocar_na_caixa_azul()
time.sleep(0.5)

else
colocar_na_caixa_verde()
time.sleep(0.5)

posicao_descanso()
time.sleep(0.2)
frozen = False
picam2.start()
detected_time = None

cv.imshow("Monitor de Cores", frame)

if cv.waitKey(1) == ord('q'):
break

cv.destroyAllWindows()

pi.stop()
