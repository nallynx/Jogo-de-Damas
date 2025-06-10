import pygame

# CONSTANTES DE CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (214, 222, 224)
ROXO = (140, 82, 255)
LARANJA = (255, 165, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
COR_FUNDO = (54, 54, 54)
COR_TABULEIRO = (0, 31, 0)

# CONSTANTES DE DIMENSÕES
largura = 800
altura= 600

class Interface:
    """Classe responsável por toda a interface gráfica do jogo"""
    
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('Damas')
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.logo = pygame.image.load("assets/logo.png")
        self.fundo_roxo = pygame.image.load("assets/Roxo.png")
        self.fundo_laranja = pygame.image.load("assets/Laranja.png")
        self.fundo_verde = pygame.image.load("assets/Empate.png")

    def desenha_tabuleiro_e_pecas(self, jogo):
        """Desenha o tabuleiro e todas as peças"""
        # Desenhar tabuleiro
        matriz = []
        for i in range(8):
            if i % 2 == 0:
                matriz.append(['#','-','#','-','#','-','#','-'])
            else:
                matriz.append(['-','#','-','#','-','#','-', '#'])

        y = 0
        for l in range(len(matriz)):
            x = 0
            for c in range(len(matriz[l])):
                if matriz[l][c] == '#':
                    pygame.draw.rect(self.display, COR_TABULEIRO, (x, y, 75, 75))
                else:
                    pygame.draw.rect(self.display, BRANCO, (x, y, 75, 75))
                x += 75
            y += 75

        # Destacar célula selecionada e movimentos possíveis
        if jogo.cedula_selecionada:
            obrigatorios = jogo.todos_obrigatorios()
            movs = jogo.movimentos_possiveis(jogo.cedula_selecionada)

            if obrigatorios != {}:
                if (jogo.cedula_selecionada[0], jogo.cedula_selecionada[1]) not in obrigatorios:
                    x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                    y_vermelho = altura / 8 * jogo.cedula_selecionada[0]

                    pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                else:
                    if movs[0] == []:
                        x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                        y_vermelho = altura / 8 * jogo.cedula_selecionada[0]

                        pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                    else:
                        for i in range(len(movs[0])):
                            x_possivel = altura / 8 * movs[0][i][1]
                            y_possivel = altura / 8 * movs[0][i][0]

                            pygame.draw.rect(self.display, VERDE, (x_possivel, y_possivel, 75, 75))
            else:
                if jogo.pulando:
                    x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                    y_vermelho = altura / 8 * jogo.cedula_selecionada[0]
                    pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                else:
                    if movs[0] == []:
                        x_vermelho = altura / 8 * jogo.cedula_selecionada[1]
                        y_vermelho = altura / 8 * jogo.cedula_selecionada[0]
                        pygame.draw.rect(self.display, VERMELHO, (x_vermelho, y_vermelho, 75, 75))
                    else:
                        for i in range(len(movs[0])):
                            x_possivel = altura / 8 * movs[0][i][1]
                            y_possivel = altura / 8 * movs[0][i][0]
                            pygame.draw.rect(self.display, VERDE, (x_possivel, y_possivel, 75, 75))

        # Desenhar peças
        matriz_jogo = jogo.get_matriz_para_desenho()
        for l in range(len(matriz_jogo)):
            for c in range(len(matriz_jogo[l])):
                elemento = matriz_jogo[l][c]
                if elemento != '-':
                    x = altura / 8 * c + altura / 16
                    y = altura / 8 * l + altura / 16

                    if elemento.lower() == 'x':
                        pygame.draw.circle(self.display, ROXO, (int(x), int(y)), 20, 0)
                        if elemento == 'X':  # Dama
                            pygame.draw.circle(self.display, PRETO, (int(x), int(y)), 10, 0)
                            pygame.draw.circle(self.display, AZUL, (int(x), int(y)), 5, 0)
                    else:
                        pygame.draw.circle(self.display, LARANJA, (int(x), int(y)), 20, 0)
                        if elemento == 'O':  # Dama
                            pygame.draw.circle(self.display, PRETO, (int(x), int(y)), 10, 0)
                            pygame.draw.circle(self.display, AZUL, (int(x), int(y)), 5, 0)

    def desenha_interface_jogo(self, jogo):
        """Desenha as informações da interface durante o jogo"""
        fonte = pygame.font.Font(None, 30)
        fonte_pequena = pygame.font.Font(None, 20)
        
        x = jogo.tabuleiro.contar_pecas('x')
        o = jogo.tabuleiro.contar_pecas('o')

        if jogo.status != 'Game Over':

            # Contador de peças
            surface_texto, rect_texto = self.text_objects(f"{jogo.jogador_x.nome}: {12 - o}", fonte, BRANCO)
            rect_texto.center = (700, 30)
            self.display.blit(surface_texto, rect_texto)

            surface_texto, rect_texto = self.text_objects(f"{jogo.jogador_o.nome}: {12 - x}", fonte, BRANCO)
            rect_texto.center = (700, altura - 30)
            self.display.blit(surface_texto, rect_texto)

            # Indicador de turno
            if jogo.turno % 2 == 1:
                nome = jogo.jogador_o.nome
                cor = jogo.jogador_o.cor
            else:
                nome = jogo.jogador_x.nome
                cor = jogo.jogador_x.cor

            surface_texto, rect_texto = self.text_objects(f"Vez de {nome}", fonte, cor)
            rect_texto.center = (700, altura / 2)
            self.display.blit(surface_texto, rect_texto)

            # Dica para voltar ao menu
            surface_texto, rect_texto = self.text_objects("ESC - Voltar ao Menu", fonte_pequena, CINZA)
            rect_texto.center = (700, 330)
            self.display.blit(surface_texto, rect_texto)

            # Dica para resetar
            surface_texto, rect_texto = self.text_objects("R - Reiniciar Jogo", fonte_pequena, CINZA)
            rect_texto.center = (700, 350)
            self.display.blit(surface_texto, rect_texto)

    def tela_menu(self, loop_jogo, regras, sair):
        """Desenha o menu principal"""
        self.display.fill(PRETO)

        logo_rect = self.logo.get_rect(center=(largura // 2, altura // 2))
        self.display.blit(self.logo, logo_rect)
        
        self.cria_botao("INICIAR",(largura - 650, altura / 2, 120, 60), BRANCO, AZUL, PRETO, loop_jogo)
        self.cria_botao("REGRAS",(largura - 450, altura / 2, 120, 60),BRANCO, AZUL, PRETO, regras)
        self.cria_botao("SAIR",(largura - 250, altura / 2, 120, 60), BRANCO, AZUL, PRETO, sair)

    def tela_regras(self):
        self.display.fill(PRETO)
    
        fonte = pygame.font.SysFont('comicsansms', 20)

        info1 = fonte.render('Regras do Jogo de Damas', False, AZUL)
        info2 = fonte.render('Objetivo: Capturar ou bloquear todas as peças do oponente.', False, BRANCO)
        info3 = fonte.render('Cada jogador tem 12 peças. Jogam-se nas casas escuras.', False, BRANCO)
        info4 = fonte.render('Peças movem-se na diagonal, 1 casa por vez, para frente.', False, BRANCO)
        info5 = fonte.render('Ao chegar à última linha, a peça vira dama (maiúscula).', False, BRANCO)
        info6 = fonte.render('Damas se movem na diagonal, para frente e para trás, por várias casas.', False, BRANCO)
        info7 = fonte.render('Captura é obrigatória, inclusive múltiplas, se possível.', False, BRANCO)
        info8 = fonte.render('Empate se nenhum jogador puder se mover ou por regra.', False, BRANCO)
        info9 = fonte.render('Se não houver destaque, não há jogada ou não é seu turno.', False, BRANCO)
        info10 = fonte.render('Tanto peças quanto dama podem capturar para frente e para trás', False, BRANCO)
        info11 = fonte.render('Clique em uma peça para ver suas jogadas válidas (verde).', False, VERDE)
        voltar = fonte.render('Pressione ESC para voltar ao menu.', False, BRANCO)

        self.display.blit(info1, (10, 50))
        self.display.blit(info2, (10, 80))
        self.display.blit(info3, (10, 110))
        self.display.blit(info4, (10, 140))
        self.display.blit(info5, (10, 170))
        self.display.blit(info6, (10, 200))
        self.display.blit(info7, (10, 230))
        self.display.blit(info8, (10, 260))
        self.display.blit(info9, (10, 290))
        self.display.blit(info10, (10, 320))
        self.display.blit(info11, (10, 350))
        self.display.blit(voltar, (10, 550))

    def tela_vencedor_display(self, vencedor, jogo):
        """Exibe a tela do vencedor com fundo temático"""
        fonte = pygame.font.SysFont('comicsansms', 50)

        if vencedor == "x":
            nome = jogo.jogador_x.nome
            self.display.blit(self.fundo_roxo, (0, 0))
            surface_texto, rect_texto = self.text_objects(f"{nome} Venceu!", fonte, PRETO)
        elif vencedor == "o":
            nome = jogo.jogador_o.nome
            self.display.blit(self.fundo_laranja, (0, 0))
            surface_texto, rect_texto = self.text_objects(f"{nome} Venceu!", fonte, PRETO)
        else:  # Empate
            self.display.blit(self.fundo_verde, (0, 0))
            surface_texto, rect_texto = self.text_objects("Empate!", fonte, PRETO)

        rect_texto.center = ((largura / 2), altura / 2)
        self.display.blit(surface_texto, rect_texto)

    def tela_nomes(self, nick1, nick2, ativo1, ativo2):
        """Desenha apenas a interface da tela de nomes"""
        fonte = pygame.font.Font(None, 36)
        
        # Configurações visuais
        input_box1 = pygame.Rect(200, 200, 300, 50)
        input_box2 = pygame.Rect(200, 300, 300, 50)
        cor_inativo = (180, 180, 180)
        cor_ativo = (0, 255, 0)
        fundo_input = (30, 30, 30)
        
        self.limpar_tela()
        
        # Desenhar caixas de input
        pygame.draw.rect(self.display, fundo_input, input_box1, border_radius=8)
        pygame.draw.rect(self.display, cor_ativo if ativo1 else cor_inativo, input_box1, 2, border_radius=8)

        pygame.draw.rect(self.display, fundo_input, input_box2, border_radius=8)
        pygame.draw.rect(self.display, cor_ativo if ativo2 else cor_inativo, input_box2, 2, border_radius=8)

        # Texto nos inputs
        txt1 = nick1 if nick1 else "Nome Player 1"
        txt2 = nick2 if nick2 else "Nome Player 2"
        cor_txt1 = (255, 255, 255) if nick1 else (150, 150, 150)
        cor_txt2 = (255, 255, 255) if nick2 else (150, 150, 150)

        surface1 = fonte.render(txt1, True, cor_txt1)
        surface2 = fonte.render(txt2, True, cor_txt2)

        self.display.blit(surface1, (input_box1.x + 10, input_box1.y + 10))
        self.display.blit(surface2, (input_box2.x + 10, input_box2.y + 10))

        # Instruções
        info_titulo = fonte.render("Escolha os nomes dos jogadores", True, (255, 255, 255))
        self.display.blit(info_titulo, (200, 100))
        
        info_enter = fonte.render("Pressione ENTER para começar", True, (0, 255, 0))
        self.display.blit(info_enter, (200, 400))
        
        return input_box1, input_box2

    def text_objects(self, text, font, color):
        """Cria objetos de texto para exibição"""
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def cria_botao(self, msg, sqr, cor1, cor2, cor_texto, acao=None):
        """Cria um botão interativo"""
        mouse = pygame.mouse.get_pos()
        clique = pygame.mouse.get_pressed()

        if sqr[0] + sqr[2] > mouse[0] > sqr[0] and sqr[1] + sqr[3] > mouse[1] > sqr[1]:
            pygame.draw.rect(self.display, cor2, sqr)
            if clique[0] == 1 and acao != None:
                acao()
        else:
            pygame.draw.rect(self.display, cor1, sqr)

        fontePequena = pygame.font.SysFont('comicsansms', 20)
        surface_texto, rect_texto = self.text_objects(msg, fontePequena, cor_texto)
        rect_texto.center = (sqr[0] + 60, sqr[1] + 20)
        self.display.blit(surface_texto, rect_texto)

    def atualizar_display(self):
        """Atualiza a tela"""
        pygame.display.update()

    def tick(self, fps=60):
        """Controla o FPS"""
        self.clock.tick(fps)

    def limpar_tela(self, cor=PRETO):
        """Limpa a tela com uma cor"""
        self.display.fill(cor)
        
def capturar_nomes():
    """Captura os nomes dos jogadores com lógica separada"""
    interface = Interface()
    nick1 = ""
    nick2 = ""
    ativo1 = ativo2 = False
    
    sair_input = False
    while not sair_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obter as caixas de input da interface
                input_box1, input_box2 = interface.tela_nomes(nick1, nick2, ativo1, ativo2)
                
                ativo1 = input_box1.collidepoint(event.pos)
                ativo2 = input_box2.collidepoint(event.pos) and not ativo1
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and nick1 and nick2:
                    return nick1, nick2
                if ativo1:
                    if event.key == pygame.K_BACKSPACE:
                        nick1 = nick1[:-1]
                    elif len(nick1) < 10 and event.unicode.isprintable():
                        nick1 += event.unicode
                elif ativo2:
                    if event.key == pygame.K_BACKSPACE:
                        nick2 = nick2[:-1]
                    elif len(nick2) < 10 and event.unicode.isprintable():
                        nick2 += event.unicode

        # Desenhar a tela
        interface.tela_nomes(nick1, nick2, ativo1, ativo2)
        interface.atualizar_display()
        interface.tick(30)