import pygame
import random as rand
from pygame.locals import *
from nn import *

class Player:
    def __init__(self, coords, neural_net):
        self.coords = coords
        self.neural_net = neural_net
        self.velocity = [0,0]
        self.acceleration = 2
        self.p_size = 10

    def on_loop(self, step_size, food_coords):
        self.update_velocity(self.get_move(food_coords), step_size)
        self.update_coords(step_size)


    def update_coords(self, step_size):
        self.coords[0] += self.velocity[0] * step_size
        self.coords[1] += self.velocity[1] * step_size

    def update_velocity(self, move_string, step_size):
        if 'up' in move_string:
            self.velocity[1] -= self.acceleration * step_size
        if 'down' in move_string:
            self.velocity[1] += self.acceleration * step_size
        if 'left' in move_string:
            self.velocity[0] -= self.acceleration * step_size
        if 'right' in move_string:
            self.velocity[0] += self.acceleration * step_size

    def get_move(self, food_coords):
        move_string = ''
        if self.neural_net is None:
            keys = pygame.key.get_pressed()
            if keys[K_w] or keys[K_UP]:
                move_string += 'up'
            if keys[K_s] or keys[K_DOWN]:
                move_string += 'down'
            if keys[K_a] or keys[K_LEFT]:
                move_string += 'left'
            if keys[K_d] or keys[K_RIGHT]:
                move_string += 'right'
        else:
            self.neural_net.input[0].set_value(self.coords[0] - food_coords[0])
            self.neural_net.input[1].set_value(self.coords[1] - food_coords[1])
            self.neural_net.input[2].set_value(self.velocity[0])
            self.neural_net.input[3].set_value(self.velocity[1])

            if self.neural_net.output[0].get_value() > 0:
                move_string += 'up'
            if self.neural_net.output[1].get_value() > 0:
                move_string += 'down'
            if self.neural_net.output[2].get_value() > 0:
                move_string += 'left'
            if self.neural_net.output[3].get_value() > 0:
                move_string += 'right'
        return move_string

    def on_render(self, display):
        pygame.draw.circle(display,(0, 150, 255), self.coords, self.p_size)

class Food():
    def __init__(self, coords):
        self.coords = coords
        self.f_size = 15

    def on_render(self, display):
        pygame.draw.rect(display, (255, 0, 0), (self.coords, (self.f_size, self.f_size)))

class Game:
    def __init__(self, playable, neural_net, total_ticks):
        self.playable = playable
        self.total_ticks = total_ticks
        self.tick = 0
        self._running = True
        self.size = self.width, self.height = 1280, 720
        if self.playable:
            self._display_surf = pygame.display.set_mode(self.size)

        

        self.score = 0
        if self.playable:
            self.font = pygame.font.SysFont(None, 24)

        
        self.player = Player([self.width / 2, self.height / 2], neural_net)
        self.food = Food([rand.uniform(0, self.width), rand.uniform(0, self.height)])

        if self.playable:
            self.step_size = 0.01
        else:
            self.step_size = 0.5

    #check if player is intersecting with food
    def check_food(self):
        distance = (((self.player.coords[0] - (self.food.coords[0] + self.food.f_size / 2)) ** 2) + ((self.player.coords[1] - (self.food.coords[1] + self.food.f_size / 2)) ** 2)) ** 0.5
        return distance < (self.player.p_size) + (self.food.f_size / 2)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.player.on_loop(self.step_size, self.food.coords)
        if self.check_food():
            self.food = Food([rand.uniform(0, self.width), rand.uniform(0, self.height)])
            self.score += 1

    def on_render(self):
        self._display_surf.fill((255, 255, 255))

        self.player.on_render(self._display_surf)
        self.food.on_render(self._display_surf)

        score_txt = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        self._display_surf.blit(score_txt, (20, 20))

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while( self._running ):
            if self.playable:
                for event in pygame.event.get():
                    self.on_event(event)
            self.on_loop()
            if(self.playable):
                self.on_render()
            if self.total_ticks is not None and self.tick == self.total_ticks:
                self._running = False
            self.tick += 1
        self.on_cleanup()
        return self.score

if __name__ == "__main__" :
    pygame.init()
    theApp = Game(True, NeuralNet([4, 10, 10, 4], linear), 10000)
    theApp.on_execute()