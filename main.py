import pygame
import random
import tkinter as tk
from tkinter import messagebox

# Inicializando o Pygame
pygame.init()

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (0, 0, 255)

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Definindo a tela de jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Steven Universe Memory Game")

# Carregar a música tema
pygame.mixer.music.load("Steven Universe_256k.mp3")  # Certifique-se de que o arquivo esteja no diretório correto

# Imagens de Steven Universe (substitua pelos ícones do tema)
icon_paths = ["src/garnet.jpg", "src/perola.jpg", "src/Steven-Universe.jpg", "src/connie.jpg", "src/ametista.jpg", "src/pai steven.jpg"]
icons = [pygame.image.load(path) for path in icon_paths]

# Função para embaralhar as cartas
def shuffle_icons():
    icons_pair = icons * 2  # Como é um jogo de memória, precisamos de pares de cada imagem
    random.shuffle(icons_pair)
    return icons_pair

# Classe do jogo
class MemoryGame:
    def __init__(self):
        self.grid = [[None for _ in range(4)] for _ in range(3)]  # Grid de 4x3
        self.selected = []
        self.matched = []
        self.reset_grid()

    def reset_grid(self):
        shuffled_icons = shuffle_icons()
        index = 0
        for i in range(3):
            for j in range(4):
                self.grid[i][j] = shuffled_icons[index]
                index += 1

    def draw_grid(self):
        screen.fill(WHITE)
        for i in range(3):
            for j in range(4):
                x = j * 150 + 25
                y = i * 125 + 25
                if (i, j) in self.matched or (i, j) in self.selected:
                    screen.blit(self.grid[i][j], (x, y))
                else:
                    pygame.draw.rect(screen, PINK, (x, y, 100, 100))
        pygame.display.flip()

    def check_match(self):
        if len(self.selected) == 2:
            if self.grid[self.selected[0][0]][self.selected[0][1]] == self.grid[self.selected[1][0]][self.selected[1][1]]:
                self.matched.extend(self.selected)
            self.selected = []

# Função para iniciar o jogo
def start_game():
    pygame.mixer.music.play(-1)  # Tocar a música tema repetidamente
    game = MemoryGame()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(game.selected) < 2:
                    mouse_x, mouse_y = event.pos
                    row = mouse_y // 125
                    col = mouse_x // 150
                    if (row, col) not in game.selected and (row, col) not in game.matched:
                        game.selected.append((row, col))

        game.draw_grid()
        game.check_match()
        clock.tick(30)

    pygame.quit()

# Função para a interface inicial usando tkinter
def main_menu():
    root = tk.Tk()
    root.title("Steven Universe Memory Game")

    def on_start_click():
        root.destroy()  # Fecha a janela inicial
        start_game()

    # Criando o botão para iniciar o jogo
    start_button = tk.Button(root, text="Iniciar Jogo", command=on_start_click, height=2, width=20)
    start_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
