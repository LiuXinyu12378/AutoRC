
import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import socket
import time
import os


class CollectTrainingData(object):
    def __init__(self, host, port, serial_port, input_size):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)

        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # connect to a seral port
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.send_inst = True

        self.input_size = input_size

        # create labels
        self.k = np.zeros((3, 3), 'float')
        for i in range(3):
            self.k[i, i] = 1

        pygame.init()
        screen = pygame.display.set_mode((250, 250))
        background = pygame.image.load('上下左右.png')
        screen.blit(background, (0, 0))
        pygame.display.update()

    def collect(self):

        saved_frame = 0
        total_frame = 0
        forward_num = 0
        left_num = 0
        right_num = 0
        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        X = np.empty((0, self.input_size))
        y = np.empty((0, 3))

        # stream video frames one by one
        try:
            stream_bytes = b' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024*6)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    # 阈值下界
                    lowerb = (55, 55, 55)
                    # 阈值上界
                    upperb = (255, 255, 255)

                    # 图像二值化
                    mask = cv2.inRange(image, lowerb, upperb)
                    # select lower half of the image
                    height, width = gray.shape
                    roi = mask[int(height / 2):height, :]

                    cv2.imshow('image', image)
                    cv2.imshow('roi', roi)
                    # reshape the roi image into a vector
                    # temp_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                    frame += 1
                    total_frame += 1

                    # get input from human driver
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
                                forward_num += 1
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

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print("exit")
                                self.send_inst = False
                                self.ser.write(b'0')
                                self.ser.close()
                                break

                        elif event.type == pygame.KEYUP:
                            self.ser.write(b'0')

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            # # save data as a numpy file
            # file_name = str(int(time.time()))
            # directory = "training_data"
            # if not os.path.exists(directory):
            #     os.makedirs(directory)
            # try:
            #     np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
            # except IOError as e:
            #     print(e)
            #
            # end = cv2.getTickCount()
            # # calculate streaming duration
            # print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))
            #
            # print(X.shape)
            # print(y.shape)
            # print("Total frame: ", total_frame)
            # print("Saved frame: ", saved_frame)
            # print("Dropped frame: ", total_frame - saved_frame)

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p = "0.0.0.0", 8000

    # serial port
    sp = "COM22"

    # vector size, half of the image
    s = 120 * 320

    ctd = CollectTrainingData(h, p, sp, s)
    ctd.collect()
