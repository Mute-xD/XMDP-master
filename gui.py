import sys
import numpy as np
import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class GameGUI:
    def __init__(self, status):
        self.status = status
        self.screen = None
        self.width, self.height = 800, 480
        self.centerX, self.centerY = self.width // 2, self.height // 2

        pygame.font.init()
        self.font = pygame.font.SysFont('microsoftyaheiui', 20)

    def initGameWorld(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Drone')

    def eventProc(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.status.running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.status.ctlPower = 1.
                elif event.key == pygame.K_a:
                    self.status.ctlAngle = 1.
                elif event.key == pygame.K_s:
                    self.status.ctlPower = -1.
                elif event.key == pygame.K_d:
                    self.status.ctlAngle = -1.
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.status.ctlPower = 0.
                elif event.key == pygame.K_a:
                    self.status.ctlAngle = 0.
                elif event.key == pygame.K_s:
                    self.status.ctlPower = 0.
                elif event.key == pygame.K_d:
                    self.status.ctlAngle = 0.

    def statusReset(self):
        pass

    def graphRender(self):
        self.screen.fill(BLACK)
        if self.status.streamEncoded is not None:
            surface = pygame.surfarray.make_surface(self.status.streamEncoded)
            self.screen.blit(surface, (0, 0))

        lineX = self.font.render(''.join(('InputX: ', str(self.status.ctlPower))), True, WHITE)
        lineY = self.font.render(''.join(('InputY: ', str(self.status.ctlAngle))), True, WHITE)
        ping = self.font.render(''.join(('Delay: ', str(self.status.netPing))), True, WHITE)
        fps = self.font.render(''.join(('FPS: ', str(self.status.netFPS))), True, WHITE)

        compressionRate = self.font.render(''.join(('Compression: ', str(self.status.compressionRate))), True, WHITE)

        self.screen.blit(lineX, (640, 1))
        self.screen.blit(lineY, (640, 40))
        self.screen.blit(ping, (640, 80))
        self.screen.blit(compressionRate, (640, 120))
        self.screen.blit(fps, (640, 160))
        pygame.display.flip()
