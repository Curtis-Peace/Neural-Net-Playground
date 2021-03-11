import pygame
from pygame.locals import *

class Player:
    def __init__(self, coords):
        self.coords = coords
        self.velocity = [0,0]
        self.acceleration = 2

    def on_loop(self, step_size):
        self.update_velocity(self.get_move(), step_size)
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

    def get_move(self):
        keys = pygame.key.get_pressed()
        move_string = ''
        if keys[K_w] or keys[K_UP]:
            move_string += 'up'
        if keys[K_s] or keys[K_DOWN]:
            move_string += 'down'
        if keys[K_a] or keys[K_LEFT]:
            move_string += 'left'
        if keys[K_d] or keys[K_RIGHT]:
            move_string += 'right'
        return move_string

class Game:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 1280, 720
        self._display_surf = pygame.display.set_mode(self.size)

        self.player = Player([self.width / 2, self.height / 2])
        self.step_size = 0.01

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.player.on_loop(self.step_size)

    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        pygame.draw.circle(self._display_surf,(0, 150, 255), self.player.coords, 10)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = Game()
    theApp.on_execute()