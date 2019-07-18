
import serial
import pygame
from pygame.locals import *


class RCTest(object):

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((250, 250))
        background = pygame.image.load('上下左右.png')
        screen.blit(background, (0, 0))
        pygame.display.update()
        self.ser = serial.Serial("COM22", 9600, timeout=1)    # mac
        # self.ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)           # linux
        self.send_inst = True
        self.steer()

    def steer(self):

        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        self.ser.write(b'6')

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        self.ser.write(b'7')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        self.ser.write(b'8')

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        self.ser.write(b'9')

                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        self.ser.write(b'1')

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        self.ser.write(b'2')

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        self.ser.write(b'3')

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        self.ser.write(b'4')

                    # exit
                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        self.send_inst = False
                        self.ser.write(b'0')
                        self.ser.close()
                        break

                elif event.type == pygame.KEYUP:
                    self.ser.write(b'0')


if __name__ == '__main__':
    RCTest()
