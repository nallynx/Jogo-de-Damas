import pygame
from game import Jogo
from interface import Interface, capturar_nomes

class Main:
    """Classe principal que gerencia o fluxo do jogo de damas"""
    
    def __init__(self):
        self.interface = Interface()
        self.rodando = True
    
    def loop_jogo(self):
        """Loop principal do jogo de damas"""
        # Capturar nomes dos jogadores antes de iniciar o jogo
        nome1, nome2 = capturar_nomes()
        
        # Passar os nomes diretamente no construtor do jogo
        jogo = Jogo(nome_jogador_o=nome1, nome_jogador_x=nome2)
        
        rodando_jogo = True
        while rodando_jogo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando_jogo = False
                    self.sair()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Voltar ao menu principal
                        rodando_jogo = False
                        return
                    if event.key == pygame.K_r:
                        # Reiniciar o jogo com os mesmos jogadores
                        jogo = Jogo(nome_jogador_o=nome1, nome_jogador_x=nome2)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    jogo.avalia_clique(pygame.mouse.get_pos())

            self.interface.limpar_tela()
            self.interface.desenha_tabuleiro_e_pecas(jogo)
            self.interface.desenha_interface_jogo(jogo)

            vencedor = jogo.verifica_vencedor()
            if vencedor is not None:
                self.tela_vencedor(vencedor, self.interface, jogo)
                break

            self.interface.atualizar_display()
            self.interface.tick(60)

    def regras(self):
        """Exibe a tela de regras"""
        sair = False

        while sair == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sair = True
                    self.sair()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sair = True

            self.interface.tela_regras()
            self.interface.atualizar_display()
            self.interface.tick(60)

    def tela_vencedor(self, vencedor, interface, jogo):
        """Exibe a tela do vencedor"""
        sair = False

        while sair == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sair = True
                    self.sair()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sair = True

            interface.tela_vencedor_display(vencedor, jogo)
            interface.atualizar_display()
            interface.tick(60)

    def sair(self):
        """Encerra o jogo"""
        self.rodando = False
        pygame.quit()
        quit()

    def menu_jogo(self):
        """Loop do menu principal"""
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.sair()

            self.interface.tela_menu(self.loop_jogo, self.regras, self.sair)
            self.interface.atualizar_display()
            self.interface.tick(15)

    def executar(self):
        """Função principal - ponto de entrada do programa"""
        try:
            self.menu_jogo()
            
        except KeyboardInterrupt:
            print("\nJogo interrompido pelo usuário.")
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            print("Obrigado por jogar!")

if __name__ == "__main__":
    main = Main()
    main.executar()