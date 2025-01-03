import pygame
from time import sleep, time
from gpiozero import Button

class Player(pygame.sprite.Sprite):

    def __init__(self, playerNum, x_pos, upBTN, downBTN , rightBTN, leftBTN):
        super().__init__()
        self.x_pos = x_pos
        self.playerNum = playerNum
        self.up_key = up_key
        self.right_key = right_key
        self.down_key = down_key
        self.left_key = left_key
        self.limits = set()
        self.clock = pygame.time.Clock()
        self.last_time = 0

        if self.playerNum == 1:
            self.originalPointer = pygame.image.load('assets/p1PointerUp.png').convert_alpha()
            y_pos = 300
        else:
            self.originalPointer = pygame.image.load('assets/p2PointerUp.png').convert_alpha()
            y_pos = 600

        self.image = self.originalPointer
        self.rect = self.image.get_rect(center=(self.x_pos, y_pos))

        self.angle = 0
        self.rotationSpeed = 10
        self.rotation_index = 0


    def get_input(self):

        # switch match case
        #replace line 35 and each if statement with if self.upButton.is_pressed 
        angle = None
        if self.upButton.is_pressed:
            angle = 0
        elif keys[self.right_key]:
            angle = -90
        elif keys[self.down_key]:
            angle = 180
        elif self.leftButton.is_pressed:
            angle = 90
        return angle

    def update(self, guesses):
        # Continuous rotation
        if 90 in guesses and 180 in guesses:
            self.image = pygame.transform.rotate(self.originalPointer, self.angle - 90)
        elif -90 in guesses and 180 in guesses:
            self.image = pygame.transform.rotate(self.originalPointer, self.angle)

        elif 0 in guesses or -90 in guesses:
            self.image = pygame.transform.rotate(self.originalPointer, 180 + self.angle)
        else:
            self.image = pygame.transform.rotate(self.originalPointer, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle += self.rotationSpeed
        self.angle %= 360


        for x in guesses:
            self.limits.add((x + 90) % 360)
            self.limits.add((x - 90) % 360)

        if 0 in guesses and 180 in guesses:

            rotation_images1 = [pygame.transform.rotate(self.originalPointer, 270), pygame.transform.rotate(self.originalPointer, 90)]

            self.image = rotation_images1[self.rotation_index]
            self.rect = self.image.get_rect(center=self.rect.center)

            delay = 300

            current_time = pygame.time.get_ticks()
            if current_time - self.last_time >= delay:
                self.rotation_index = (self.rotation_index + 1) % len(rotation_images1)
                self.last_time = current_time



        elif -90 in guesses and 90 in guesses:
            rotation_images2 = [pygame.transform.rotate(self.originalPointer, 0), pygame.transform.rotate(self.originalPointer, 180)]

            self.image = rotation_images2[self.rotation_index]
            self.rect = self.image.get_rect(center=self.rect.center)

            delay = 300

            current_time = pygame.time.get_ticks()
            if current_time - self.last_time >= delay:
                self.rotation_index = (self.rotation_index + 1) % len(rotation_images2)
                self.last_time = current_time

        elif self.limits:
            if -90 in guesses and 0 in guesses:
                if self.angle == (list(self.limits)[-2] + 80) or self.angle == (list(self.limits)[-3] - 80):
                    self.rotationSpeed *= -1
            elif -90 in guesses and 180 in guesses:
                if self.angle == list(self.limits)[-3] or self.angle == list(self.limits)[-4]:
                    self.rotationSpeed *= -1
            elif 90 in guesses and 0 in guesses:
                if self.angle == (list(self.limits)[-2] - 80) or self.angle == (list(self.limits)[-1] + 80):
                    self.rotationSpeed *= -1
            elif 90 in guesses and 180 in guesses:
                if self.angle == (list(self.limits)[-1] + 80) or self.angle == (list(self.limits)[-4] + 100):
                    self.rotationSpeed *= -1
            elif 0 in guesses:
                if self.angle == (list(self.limits)[-1] - 40) or self.angle == (list(self.limits)[-2]):
                    self.rotationSpeed *= -1
            elif -90 in guesses:
                if self.angle == (list(self.limits)[-1] - 15) or self.angle == (list(self.limits)[-2] + 5):
                    self.rotationSpeed *= -1
            else:
                if self.angle == (max(self.limits) - 40) or self.angle == (min(self.limits) + 20):
                    self.rotationSpeed *= -1


    def update_end(self, angle):
        self.image = pygame.transform.rotate(self.originalPointer, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
