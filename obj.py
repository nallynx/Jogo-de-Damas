import pygame

class Tabuleiro:
    """Classe para representar o tabuleiro de damas"""
    
    def __init__(self):
        self.matriz = [['x','-','x','-','x','-','x','-'],
                      ['-','x','-','x','-','x','-','x'],
                      ['x','-','x','-','x','-','x','-'],
                      ['-','-','-','-','-','-','-','-'],
                      ['-','-','-','-','-','-','-','-'],
                      ['-','o','-','o','-','o','-','o'],
                      ['o','-','o','-','o','-','o','-'],
                      ['-','o','-','o','-','o','-','o']]
    
    def get_peca(self, linha, coluna):
        """Retorna a peça em uma posição específica"""
        if 0 <= linha < 8 and 0 <= coluna < 8:
            return self.matriz[linha][coluna]
        return None
    
    def set_peca(self, linha, coluna, peca):
        """Define uma peça em uma posição específica"""
        if 0 <= linha < 8 and 0 <= coluna < 8:
            self.matriz[linha][coluna] = peca
    
    def esta_vazio(self, linha, coluna):
        """Verifica se uma posição está vazia"""
        return self.get_peca(linha, coluna) == '-'
    
    def contar_pecas(self, jogador):
        """Conta quantas peças um jogador tem"""
        contador = 0
        for linha in self.matriz:
            for peca in linha:
                if peca.lower() == jogador:
                    contador += 1
        return contador

class Jogador:
    """Classe para representar um jogador"""
    
    def __init__(self, simbolo, nome, cor):
        self.simbolo = simbolo  # 'x' ou 'o'
        self.nome = nome
        self.cor = cor
        self.pecas_capturadas = 0
    
    def capturar_peca(self):
        """Incrementa o contador de peças capturadas"""
        self.pecas_capturadas += 1
    
    def get_pecas_restantes(self, tabuleiro):
        """Retorna quantas peças o jogador ainda tem no tabuleiro"""
        return tabuleiro.contar_pecas(self.simbolo)