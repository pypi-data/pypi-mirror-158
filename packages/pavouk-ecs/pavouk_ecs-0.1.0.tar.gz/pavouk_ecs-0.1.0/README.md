# pavouk-ecs

An Entity Component System (ECS) framework for Python.

## Installation

```bash
pip install pavouk_ecs
```

## Example

```python
import pygame
import sys

from dataclasses import dataclass
from pavouk_ecs import Manager
from pavouk_ecs.system import System


RESOLUTION = (160, 160)
BACKGROUND_COLOR = (10, 10, 10)


###
### COMPONENTS
###


@dataclass
class Area:
    w: int = 0
    h: int = 0


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0


@dataclass
class Transform:
    x: int = 0
    y: int = 0


@dataclass
class Velocity:
    x: float = 0.0
    y: float = 0.0


###
### SYSTEMS
###


class RenderSystem(System):
    def on_update(self, surface, deltatime):
        for e in self.manager.query([Transform, Area, Color]):
            t = self.manager.get(Transform, e)
            a = self.manager.get(Area, e)
            c = self.manager.get(Color, e)

            r = pygame.Rect(t.x, t.y, a.w, a.h)
            pygame.draw.rect(surface, (c.r, c.g, c.b), r)


class BouncingSystem(System):
    def on_update(self, surface, deltatime):
        for e in self.manager.query([Transform, Area, Velocity]):
            t = self.manager.get(Transform, e)
            a = self.manager.get(Area, e)
            v = self.manager.get(Velocity, e)

            if t.x <= 0 and v.x < 0 or t.x + a.w >= RESOLUTION[0]:
                v.x = -v.x
            if t.y <= 0 and v.y < 0 or t.y + a.h >= RESOLUTION[1]:
                v.y = -v.y
            
            t.x += v.x
            t.y += v.y


###
### GAME
###

class Game:
    def __init__(self):
        self.running = True

        pygame.init()
        pygame.display.set_caption("Pavouk ECS Example")

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(RESOLUTION)

        self.manager = Manager()

        player = self.manager.create_entity()
        t = self.manager.assign(Transform, player)
        t.x = 16 * 4
        t.y = 16 * 4

        a = self.manager.assign(Area, player)
        a.w = 16
        a.h = 16

        c = self.manager.assign(Color, player)
        c.r = 200
        c.g = 200
        c.b = 200

        v = self.manager.assign(Velocity, player)
        v.x = -1.0
        v.y = 2.0

        self.manager.add_system(BouncingSystem)
        self.manager.add_system(RenderSystem)
    
    def run(self):
        while self.running:
            self.screen.fill(BACKGROUND_COLOR)

            events = pygame.event.get()
            self._handle_events(events)
            
            self.manager.update_systems(self.screen, 0)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def _handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.running = False

            elif e.type == pygame.QUIT:
                self.running = False

    def quit(self):
        self.running = False


if __name__ == "__main__":
    game = Game()
    game.run()
```
