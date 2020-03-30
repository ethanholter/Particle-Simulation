import pygame
from random import randint, random
from math import *

WIDTH = 600
HEIGHT = 600
BACKGROUND = (10, 10, 30)
GRAVITY = .5
particles = []

pygame.init()
done = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def map(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

def dist(coord1, coord2):
    return sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)

def normalize(vector):
    magnitude = sqrt(vector[0]**2 + vector[1]**2)
    if magnitude != 0:
        return (vector[0]/magnitude, vector[1]/magnitude)
    else:
        return (vector[0]/.01, vector[1]/.01)

class Particle:
    def __init__(self):
        self.location = [randint(1, WIDTH - 1), randint(1, HEIGHT - 1)]
        tempv = normalize((map(random(),0,1,-2,2), map(random(),0,1,-2,2)))
        self.velocity = [tempv[0], tempv[1]]
        self.acceleration = [0, 0]
        self.color = (255, 255, 255)

        self.FRICTION = .98
        self.GRUMPYNESS = 5
        self.DISTANCE = 100
        self.MAXSPEED = 10

    def show(self):
        pygame.draw.circle(screen, self.color, (round(self.location[0]), round(self.location[1])), 2)

    def update(self):
        #movement
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.velocity[0] *= self.FRICTION
        self.velocity[1] *= self.FRICTION
        self.acceleration = [0, 0]

        # wallbounce
        if self.location[0] > WIDTH:
            self.velocity[0] *= -1
            self.location[0] = WIDTH - 3
        if self.location[0] < 0:
            self.velocity[0] *= -1
            self.location[0] = 3
        if self.location[1] > HEIGHT:
            self.velocity[1] *= -1
            self.location[1] = HEIGHT - 3
        if self.location[1] < 0:
            self.velocity[1] *= -1
            self.location[1] = 3

        if self.location[0] < 0 + self.DISTANCE:
            self.acceleration[0] += (1/dist(self.location, [0, self.location[1]])) * self.GRUMPYNESS
        if self.location[0] > WIDTH - self.DISTANCE:
            self.acceleration[0] += -(1/dist(self.location, [WIDTH, self.location[1]])) * self.GRUMPYNESS
        if self.location[1] < 0 + self.DISTANCE:
            self.acceleration[1] += (1/dist(self.location, [self.location[0], 0])) * self.GRUMPYNESS
        if self.location[1] > HEIGHT - self.DISTANCE:
            self.acceleration[1] += -(1/dist(self.location, [self.location[0], HEIGHT])) * self.GRUMPYNESS

        #interaction with other particles
        self.color = (255, 255, 255)
        for particle in particles:
            distance = dist((particle.location[0], particle.location[1]), (self.location[0], self.location[1]))
            if particle is self:
                 continue
            elif distance < self.DISTANCE:
                acelVector = normalize((self.location[0] - particle.location[0], self.location[1] - particle.location[1]))
                self.acceleration[0] += acelVector[0] * (1/dist(self.location, particle.location)) * self.GRUMPYNESS
                self.acceleration[1] += acelVector[1] * (1/dist(self.location, particle.location)) * self.GRUMPYNESS
        if sqrt(self.velocity[0]**2 + self.velocity[1]**2) > self.MAXSPEED:
            self.velocity = list(normalize((self.velocity[0], self.velocity[1])) * self.MAXSPEED)

        mousePos = pygame.mouse.get_pos()
        mouseDistance = dist(mousePos, (self.location[0], self.location[1]))
        if mouseDistance < self.DISTANCE * 2:
            mouseVect = normalize((self.location[0] - mousePos[0], self.location[1] - mousePos[1]))
            self.acceleration[0] += mouseVect[0] * (1/dist(self.location, mousePos)) * self.GRUMPYNESS * 10
            self.acceleration[1] += mouseVect[1] * (1/dist(self.location, mousePos)) * self.GRUMPYNESS * 10
for i in range(100):
    particle = Particle()
    particles.append(particle)

def draw():
    screen.fill(BACKGROUND)
    for particle in particles:
        particle.show()
        particle.update()

while not done:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pygame.display.flip()
