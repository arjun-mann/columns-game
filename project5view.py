import pygame
from project5mech import Columns


class ColumnsGame:
    def __init__(self):
        '''Initializes ColumnsGame'''
        self._running = True
        self._game = Columns(13, 6)
        
    def run(self) -> None:
        '''Runs a full length game of Columns in a resizable window'''
        pygame.init()
        self._resize_surface((600, 600))
        clock = pygame.time.Clock()
        self._game.p5makeboard()
        time = 0
        while self._running:
            clock.tick(30)
            time += 1
            self._handle_events()
            if time == 30:
                w = self._game.p5wait()
                if type(w) != list:
                    return
                if len(w) > 1:
                    for board in w:
                        self._redraw(board)
                        pygame.time.delay(1000)
                g = self._game.p5buildfaller()
                self._redraw(g)
                time = 0
        pygame.quit()    
    
    
    def _graph_time(self, g:list[list[str]]) -> None:
        '''Creates a graph for a list g with colored cells for jewels and empty cells for EMPTY cells'''
        surface = pygame.display.get_surface()
        cell_width = self._width // 6   #6
        cell_height = self._height // 13    #13
        for row in range(13):   #13
            for col in range(6):    #6
                color = self._color_picker(g[row][col])
                if color != (0, 0, 0):
                    pygame.draw.rect(surface, color, (col * cell_width, row * cell_height, cell_width, cell_height))
                pygame.draw.rect(surface, pygame.Color(255, 255, 255), (col * cell_width, row * cell_height, cell_width, cell_height), 1)
                if g[row][col][0] == '[':
                    pygame.draw.rect(surface, pygame.Color(172, 75, 0), (col * cell_width, row * cell_height, cell_width, cell_height), 3)
                if g[row][col][0] == '|':
                    pygame.draw.rect(surface, pygame.Color(0, 248, 251), (col * cell_width, row * cell_height, cell_width, cell_height), 3)
                if g[row][col][0] == '*':
                    pygame.draw.rect(surface, (250, 250, 250), (col * cell_width, row * cell_height, cell_width, cell_height))
    
    def _color_picker(self, jewel:str) -> tuple:
        '''Returns a specific color code for str jewel depending on its middle character'''
        if jewel == 'EMPTY':
            return (0, 0, 0)
        elif jewel[1] == 'S': #Blue
            return (0, 136, 255)
        elif jewel[1] == 'T': #Red
            return (255, 0, 0)
        elif jewel[1] == 'V': #Orange
            return (255, 111, 0)
        elif jewel[1] == 'W': #Yellow
            return (255, 249, 0)
        elif jewel[1] == 'X': #Green
            return (0, 209, 3)
        elif jewel[1] == 'Y': #Purple
            return (167, 0, 209)
        elif jewel[1] == 'Z': #Pink
            return (249, 57, 212)
    
    def _handle_events(self) -> None:
        '''Handles keypresses, quit, and resize features for the game'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    a = self._game.p5movesright()
                    self._redraw(a)
                if event.key == pygame.K_LEFT:
                    a = self._game.p5movesleft()
                    self._redraw(a)
                if event.key == pygame.K_SPACE:
                    a = self._game.p5rotates()
                    self._redraw(a)
    
    def _redraw(self, g) -> None:
        '''Redraws and updated version of the window'''
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(0, 0, 0))
        self._graph_time(g)
        pygame.display.flip()
        
    def _end_game(self) -> None:
        '''Ends the game'''
        self._running = False
        
    def _resize_surface(self, size: tuple[int, int]) -> None:
        '''Adjusts the window and measurements used when the window is resized'''
        pygame.display.set_mode(size, pygame.RESIZABLE)
        surface = pygame.display.get_surface()
        self._width = surface.get_width()
        self._height = surface.get_height()
        
if __name__ == '__main__':
    ColumnsGame().run()