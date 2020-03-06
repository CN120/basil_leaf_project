import RPi.GPIO as GPIO
import time
output_pin = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(output_pin, GPIO.OUT)

GPIO.output(output_pin, GPIO.LOW)
while True:

    GPIO.output(output_pin, GPIO.HIGH)

    time.sleep(1) 

    GPIO.output(output_pin,GPIO.LOW)

    time.sleep(5) 