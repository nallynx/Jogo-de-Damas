from obj import Tabuleiro, Jogador
from interface import altura

class Jogo:
    """Classe principal que gerencia a lógica do jogo de damas"""
    
    def __init__(self, nome_jogador_x="Roxo", nome_jogador_o="Laranja"):
        """Inicializa o jogo com configurações padrão"""
        self._inicializar_estado_jogo()
        self._criar_jogadores(nome_jogador_x, nome_jogador_o)
        self.tabuleiro = Tabuleiro()
    
    def _inicializar_estado_jogo(self):
        """Inicializa as variáveis de estado do jogo"""
        self.status = 'Jogando'
        self.turno = 1
        self.jogadores = ('x', 'o')
        self.cedula_selecionada = None
        self.pulando = False
    
    def _criar_jogadores(self, nome_x, nome_o):
        """Cria os jogadores com suas respectivas cores"""
        self.jogador_x = Jogador('x', nome_x, (140, 82, 255))  # Roxo
        self.jogador_o = Jogador('o', nome_o, (255, 165, 0))  # Laranja
    
    # ===============================
    # MÉTODOS DE CONFIGURAÇÃO
    # ===============================
    
    def definir_nomes_jogadores(self, nome_x, nome_o):
        """Define os nomes dos jogadores após a criação do jogo"""
        self.jogador_x.nome = nome_x
        self.jogador_o.nome = nome_o
    
    def get_matriz_para_desenho(self):
        """Retorna a matriz do tabuleiro para ser desenhada pela interface"""
        return self.tabuleiro.matriz
    
    # ===============================
    # MÉTODOS DE INTERFACE/CLIQUE
    # ===============================
    
    def _clique_dentro_do_tabuleiro(self, pos):
        """Verifica se o clique foi dentro da área do tabuleiro"""
        x, y = pos
        # O tabuleiro ocupa a área de 0 a 600 (altura) tanto em x quanto em y
        # Já que o tabuleiro é quadrado de 8x8 com 75px por casa
        tamanho_tabuleiro = 8 * 75  # 600px
        return 0 <= x <= tamanho_tabuleiro and 0 <= y <= tamanho_tabuleiro
    
    def _linha_clicada(self, pos):
        """Calcula qual linha foi clicada baseada na posição do mouse"""
        y = pos[1]
        for i in range(1, 8):
            if y < i * altura / 8:
                return i - 1
        return 7
    
    def _coluna_clicada(self, pos):
        """Calcula qual coluna foi clicada baseada na posição do mouse"""
        x = pos[0]
        for i in range(1, 8):
            if x < i * altura / 8:
                return i - 1
        return 7
    
    def avalia_clique(self, pos):
        """Processa um clique do mouse e executa a ação correspondente"""
        if self.status != "Jogando":
            return
        
        if not self._clique_dentro_do_tabuleiro(pos):
            return
            
        turno_atual = self.turno % 2
        linha, coluna = self._linha_clicada(pos), self._coluna_clicada(pos)
        
        if self.cedula_selecionada:
            self._processar_clique_com_selecao(turno_atual, linha, coluna)
        else:
            self._processar_clique_sem_selecao(turno_atual, linha, coluna)
    
    def _processar_clique_com_selecao(self, turno_atual, linha, coluna):
        """Processa clique quando já há uma peça selecionada"""
        movimento = self.is_movimento_valido(
            self.jogadores[turno_atual], 
            self.cedula_selecionada, 
            linha, 
            coluna
        )
        
        if movimento[0]:
            # Movimento válido - executar jogada
            self.jogar(
                self.jogadores[turno_atual], 
                self.cedula_selecionada, 
                linha, 
                coluna, 
                movimento[1]
            )
        elif self._clicou_na_mesma_peca(linha, coluna):
            # Clicou na mesma peça selecionada
            self._processar_clique_mesma_peca()
        else:
            # Tentar selecionar nova peça
            self._tentar_selecionar_nova_peca(turno_atual, linha, coluna)
    
    def _processar_clique_sem_selecao(self, turno_atual, linha, coluna):
        """Processa clique quando não há peça selecionada"""
        if self.tabuleiro.get_peca(linha, coluna).lower() == self.jogadores[turno_atual]:
            self.cedula_selecionada = [linha, coluna]
    
    def _clicou_na_mesma_peca(self, linha, coluna):
        """Verifica se clicou na mesma peça já selecionada"""
        return (linha == self.cedula_selecionada[0] and 
                coluna == self.cedula_selecionada[1])
    
    def _processar_clique_mesma_peca(self):
        """Processa quando clica na mesma peça selecionada"""
        if self.pulando:
            # Verificar se ainda há movimentos obrigatórios
            movs = self.movimento_obrigatorio(self.cedula_selecionada)
            if not movs[0]:
                # Não há mais movimentos obrigatórios
                self.pulando = False
                self.cedula_selecionada = None
                self.proximo_turno()
            else:
                # Ainda há movimentos obrigatórios - apenas desselecionar visualmente
                self.cedula_selecionada = None
        else:
            # Não está pulando - desselecionar normalmente
            self.cedula_selecionada = None
    
    def _tentar_selecionar_nova_peca(self, turno_atual, linha, coluna):
        """Tenta selecionar uma nova peça se for válida"""
        if (self.tabuleiro.get_peca(linha, coluna).lower() == self.jogadores[turno_atual] 
            and not self.pulando):
            self.cedula_selecionada = [linha, coluna]
    
    # ===============================
    # MÉTODOS DE VALIDAÇÃO DE MOVIMENTO
    # ===============================
    
    def is_movimento_valido(self, jogador, localizacao_cedula, linha_destino, coluna_destino):
        """Verifica se um movimento é válido considerando regras do jogo"""
        linha_orig = localizacao_cedula[0]
        coluna_orig = localizacao_cedula[1]
        
        # Verificar movimentos obrigatórios
        obrigatorios = self.todos_obrigatorios()
        if obrigatorios:
            if (linha_orig, coluna_orig) not in obrigatorios:
                return False, None
            if [linha_destino, coluna_destino] not in obrigatorios[(linha_orig, coluna_orig)]:
                return False, None
        
        # Verificar movimentos possíveis
        movimento, pulo = self.movimentos_possiveis(localizacao_cedula)
        
        if [linha_destino, coluna_destino] in movimento:
            if pulo:
                return True, self._encontrar_peca_capturada(pulo, linha_destino, coluna_destino)
            
            if self.pulando:
                return False, None
                
            return True, None
        
        return False, None
    
    def _encontrar_peca_capturada(self, pulos, linha_destino, coluna_destino):
        """Encontra qual peça será capturada no pulo"""
        if len(pulos) == 1:
            return pulos[0]
        
        # Para múltiplos pulos, encontrar o correspondente ao movimento de destino
        # Isso acontece quando uma dama tem múltiplas capturas possíveis
        for pulo in pulos:
            if pulo is not None:
                return pulo
        
        return None
    
    # ===============================
    # MÉTODOS DE ANÁLISE DE MOVIMENTOS
    # ===============================
    
    def todos_obrigatorios(self):
        """Retorna todos os movimentos obrigatórios (capturas) do turno atual"""
        obrigatorios = {}
        
        for linha in range(8):
            for coluna in range(8):
                movs_obrigatorios, _ = self.movimento_obrigatorio((linha, coluna))
                if movs_obrigatorios:
                    obrigatorios[(linha, coluna)] = movs_obrigatorios
        
        return obrigatorios
    
    def existe_possivel(self):
        """Verifica se existe algum movimento possível no tabuleiro"""
        for linha in range(8):
            for coluna in range(8):
                if self.movimentos_possiveis((linha, coluna))[0]:
                    return True
        return False
    
    def movimentos_possiveis(self, localizacao_cedula):
        """Retorna todos os movimentos possíveis de uma peça"""
        # Primeiro verificar movimentos obrigatórios (capturas)
        movimentos, pulos = self.movimento_obrigatorio(localizacao_cedula)
        
        # Se não há capturas obrigatórias, verificar movimentos normais
        if not movimentos:
            movimentos = self._calcular_movimentos_normais(localizacao_cedula)
        
        return movimentos, pulos
    
    def _calcular_movimentos_normais(self, localizacao_cedula):
        """Calcula movimentos normais (sem captura) de uma peça"""
        linha_atual = localizacao_cedula[0]
        coluna_atual = localizacao_cedula[1]
        peca_atual = self.tabuleiro.get_peca(linha_atual, coluna_atual)
        movimentos = []
        
        if peca_atual.islower():
            # Peça normal
            movimentos = self._movimentos_peca_normal(peca_atual, linha_atual, coluna_atual)
        elif peca_atual.isupper():
            # Dama
            movimentos = self._movimentos_dama(linha_atual, coluna_atual)
        
        return movimentos
    
    def _movimentos_peca_normal(self, peca, linha, coluna):
        """Calcula movimentos de uma peça normal"""
        movimentos = []
        
        if peca == 'o':  # Peça laranja move para cima
            if linha > 0:
                if coluna < 7 and self.tabuleiro.get_peca(linha - 1, coluna + 1) == '-':
                    movimentos.append([linha - 1, coluna + 1])
                if coluna > 0 and self.tabuleiro.get_peca(linha - 1, coluna - 1) == '-':
                    movimentos.append([linha - 1, coluna - 1])
        
        elif peca == 'x':  # Peça roxa move para baixo
            if linha < 7:
                if coluna < 7 and self.tabuleiro.get_peca(linha + 1, coluna + 1) == '-':
                    movimentos.append([linha + 1, coluna + 1])
                if coluna > 0 and self.tabuleiro.get_peca(linha + 1, coluna - 1) == '-':
                    movimentos.append([linha + 1, coluna - 1])
        
        return movimentos
    
    def _movimentos_dama(self, linha, coluna):
        """Calcula movimentos de uma dama em todas as direções"""
        movimentos = []
        direcoes = [(-1, -1), (-1, 1), (1, 1), (1, -1)]  # Todas as diagonais
        
        for dir_linha, dir_coluna in direcoes:
            linha_atual, coluna_atual = linha, coluna
            
            while True:
                linha_atual += dir_linha
                coluna_atual += dir_coluna
                
                if not (0 <= linha_atual <= 7 and 0 <= coluna_atual <= 7):
                    break
                
                if self.tabuleiro.get_peca(linha_atual, coluna_atual) == '-':
                    movimentos.append([linha_atual, coluna_atual])
                else:
                    break
        
        return movimentos
    
    # ===============================
    # MÉTODOS DE CAPTURA/PULO
    # ===============================
    
    def movimento_obrigatorio(self, localizacao_cedula):
        """Retorna os movimentos obrigatórios (capturas) de uma peça"""
        linha, coluna = localizacao_cedula
        peca_atual = self.tabuleiro.get_peca(linha, coluna)
        jogador_atual = self.jogadores[self.turno % 2]
        
        # Verificar se a peça pertence ao jogador atual
        if not self._peca_pertence_ao_jogador(peca_atual, jogador_atual):
            return [], []
        
        if peca_atual.islower():
            return self._capturas_peca_normal(linha, coluna, jogador_atual)
        else:
            return self._capturas_dama(linha, coluna, jogador_atual)
    
    def _peca_pertence_ao_jogador(self, peca, jogador):
        """Verifica se a peça pertence ao jogador atual"""
        index_jogador = self.jogadores.index(jogador)
        return (peca.lower() == jogador and self.turno % 2 == index_jogador)
    
    def _capturas_peca_normal(self, linha, coluna, jogador):
        """Calcula capturas possíveis para uma peça normal"""
        obrigatorios = []
        pecas_capturadas = []
        
        # Verificar todas as 4 direções diagonais
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir_linha, dir_coluna in direcoes:
            linha_adj = linha + dir_linha
            coluna_adj = coluna + dir_coluna
            
            # Verificar se a posição adjacente está dentro do tabuleiro
            if not (0 <= linha_adj <= 7 and 0 <= coluna_adj <= 7):
                continue
            
            peca_adjacente = self.tabuleiro.get_peca(linha_adj, coluna_adj)
            
            # Se há uma peça inimiga adjacente
            if self._eh_peca_inimiga(peca_adjacente, jogador):
                linha_pulo = linha_adj + dir_linha
                coluna_pulo = coluna_adj + dir_coluna
                
                # Verificar se a posição de pulo está livre e dentro do tabuleiro
                if (0 <= linha_pulo <= 7 and 0 <= coluna_pulo <= 7 and
                    self.tabuleiro.get_peca(linha_pulo, coluna_pulo) == '-'):
                    
                    obrigatorios.append([linha_pulo, coluna_pulo])
                    pecas_capturadas.append((linha_adj, coluna_adj))
        
        return obrigatorios, pecas_capturadas
    
    def _capturas_dama(self, linha, coluna, jogador):
        """Calcula capturas possíveis para uma dama"""
        obrigatorios = []
        pecas_capturadas = []
        
        # Verificar todas as 4 direções diagonais
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dir_linha, dir_coluna in direcoes:
            movimentos_direcao, peca_capturada_direcao = self._capturas_dama_direcao(
                linha, coluna, dir_linha, dir_coluna, jogador
            )
            
            # Adicionar movimentos e suas respectivas capturas
            obrigatorios.extend(movimentos_direcao)
            # Para cada movimento nesta direção, a peça capturada é a mesma
            pecas_capturadas.extend([peca_capturada_direcao] * len(movimentos_direcao))
        
        return obrigatorios, pecas_capturadas
    
    def _capturas_dama_direcao(self, linha, coluna, dir_linha, dir_coluna, jogador):
        """Calcula capturas de uma dama em uma direção específica"""
        movimentos = []
        peca_capturada = None
        
        linha_atual, coluna_atual = linha, coluna
        peca_inimiga_encontrada = False
        
        while True:
            linha_atual += dir_linha
            coluna_atual += dir_coluna
            
            # Verificar limites do tabuleiro
            if not (0 <= linha_atual <= 7 and 0 <= coluna_atual <= 7):
                break
            
            peca_atual = self.tabuleiro.get_peca(linha_atual, coluna_atual)
            
            # Se encontrar peça da mesma cor, parar
            if peca_atual.lower() == jogador:
                break
            
            # Se for posição vazia
            if peca_atual == '-':
                if peca_inimiga_encontrada:
                    # Já encontrou inimigo - posição válida para captura
                    movimentos.append([linha_atual, coluna_atual])
                # Continuar procurando
                continue
            
            # Se for peça inimiga
            elif self._eh_peca_inimiga(peca_atual, jogador):
                if not peca_inimiga_encontrada:
                    # Primeira peça inimiga encontrada
                    peca_inimiga_encontrada = True
                    peca_capturada = (linha_atual, coluna_atual)
                else:
                    # Segunda peça encontrada - parar
                    break
        
        return movimentos, peca_capturada
    
    def _eh_peca_inimiga(self, peca, jogador):
        """Verifica se uma peça é inimiga do jogador atual"""
        return peca != '-' and peca.lower() != jogador
    
    # ===============================
    # MÉTODOS DE EXECUÇÃO DE JOGADA
    # ===============================
    
    def jogar(self, jogador, localizacao_cedula, linha_destino, coluna_destino, pulo):
        """Executa uma jogada completa"""
        linha_atual, coluna_atual = localizacao_cedula
        peca = self.tabuleiro.get_peca(linha_atual, coluna_atual)
        
        # Mover a peça
        self._executar_movimento(linha_atual, coluna_atual, linha_destino, coluna_destino, peca)
        
        # Processar captura se houver
        if pulo:
            self._processar_captura(pulo)
        
        # Verificar promoção para dama
        self._verificar_promocao(jogador, linha_destino, coluna_destino, peca)
        
        # Gerenciar continuação do turno
        self._gerenciar_continuacao_turno(pulo, linha_destino, coluna_destino)
        
        # Verificar condições de vitória
        self._verificar_fim_jogo()
    
    def _executar_movimento(self, linha_orig, coluna_orig, linha_dest, coluna_dest, peca):
        """Move uma peça de uma posição para outra"""
        self.tabuleiro.set_peca(linha_dest, coluna_dest, peca)
        self.tabuleiro.set_peca(linha_orig, coluna_orig, '-')
    
    def _processar_captura(self, pulo):
        """Remove a peça capturada e marca estado de pulo"""
        self.tabuleiro.set_peca(pulo[0], pulo[1], '-')
        self.pulando = True
    
    def _verificar_promocao(self, jogador, linha_destino, coluna_destino, peca_original):
        """Verifica e executa promoção para dama"""
        deve_promover = ((jogador == 'x' and linha_destino == 7) or 
                        (jogador == 'o' and linha_destino == 0))
        
        if deve_promover:
            if not self.pulando:
                # Movimento normal - sempre promove
                self.tabuleiro.set_peca(linha_destino, coluna_destino, peca_original.upper())
            else:
                # Está pulando - só promove se não há mais capturas
                movs_obrigatorios = self.movimento_obrigatorio((linha_destino, coluna_destino))[0]
                if not movs_obrigatorios:
                    self.tabuleiro.set_peca(linha_destino, coluna_destino, peca_original.upper())
    
    def _gerenciar_continuacao_turno(self, pulo, linha_destino, coluna_destino):
        """Gerencia se o turno continua ou passa para o próximo jogador"""
        if pulo:
            # Após captura, verificar se há mais capturas possíveis
            movs_obrigatorios = self.movimento_obrigatorio((linha_destino, coluna_destino))[0]
            if movs_obrigatorios:
                # Há mais capturas - manter peça selecionada
                self.cedula_selecionada = [linha_destino, coluna_destino]
            else:
                # Não há mais capturas - finalizar turno
                self._finalizar_turno()
        else:
            # Movimento normal - finalizar turno
            self._finalizar_turno()
    
    def _finalizar_turno(self):
        """Finaliza o turno atual"""
        self.cedula_selecionada = None
        self.pulando = False
        self.proximo_turno()
    
    def _verificar_fim_jogo(self):
        """Verifica se o jogo terminou"""
        vencedor = self.verifica_vencedor()
        if vencedor is not None:
            self.status = 'Game Over'
    
    # ===============================
    # MÉTODOS DE CONTROLE DO JOGO
    # ===============================
    
    def proximo_turno(self):
        """Avança para o próximo turno"""
        self.turno += 1
    
    def verifica_vencedor(self):
        """Verifica se há um vencedor ou empate"""
        pecas_x = self.tabuleiro.contar_pecas('x')
        pecas_o = self.tabuleiro.contar_pecas('o')
        
        # Vitória por eliminação
        if pecas_x == 0:
            return 'o'
        if pecas_o == 0:
            return 'x'
        
        # Empate por peças insuficientes
        if pecas_x == 1 and pecas_o == 1:
            return 'Empate'
        
        # Verificar se jogador atual não pode se mover
        if self.cedula_selecionada:
            if not self.movimentos_possiveis(self.cedula_selecionada)[0]:
                if pecas_x == 1 and self.turno % 2 == 0:
                    return 'o'
                if pecas_o == 1 and self.turno % 2 == 1:
                    return 'x'
        
        # Empate por falta de movimentos possíveis
        if not self.existe_possivel():
            return 'Empate'
        
        return None