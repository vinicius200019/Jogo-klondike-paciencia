# main.py
import pygame
import random
import sys
import time

# Inicializar Pygame
pygame.init()
pygame.display.set_caption("Paciência Klondike (Python)")

# Configurações da tela
LARGURA, ALTURA = 1000, 700
tela = pygame.display.set_mode((LARGURA, ALTURA))

# Fontes
fonte = pygame.font.SysFont("arial", 20)
fonte_pequena = pygame.font.SysFont("arial", 14)
fonte_botao = pygame.font.SysFont("arial", 16)
fonte_grande = pygame.font.SysFont("arial", 32, bold=True)
fonte_titulo = pygame.font.SysFont("arial", 24, bold=True)
fonte_subtitulo = pygame.font.SysFont("arial", 18, bold=True)

# Cores
VERDE_MESA = (0, 128, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 0, 0)
AZUL_SELECAO = (0, 0, 255)
CINZA_ESCURO = (80, 80, 80)
CINZA_BOTAO = (180, 180, 180)
CINZA_BOTAO_HOVER = (200, 200, 200)
CINZA_CLARO = (220, 220, 220)
HINT_FILL = (255, 255, 0, 100)
HINT_BORDER = (255, 200, 0)
DOURADO = (255, 215, 0)
VERDE_CLARO = (144, 238, 144)

# Posições
pos_tableau = [(100 + i * 120, 300) for i in range(7)]  # Ajustado para baixo
pos_fundacoes = [(400 + i * 120, 150) for i in range(4)]  # Ajustado para baixo
pos_estoque = (100, 150)  # Ajustado para baixo
pos_descarte = (220, 150)  # Ajustado para baixo

# Dimensões
LARG_CARTA, ALT_CARTA = 80, 120
LARG_BOTAO, ALT_BOTAO = 120, 40
LARG_INFO, ALT_INFO = 140, 35

class Carta:
    def __init__(self, naipe, valor, virada=True):
        self.naipe = naipe
        self.valor = valor
        self.virada = virada
    
    def eh_vermelha(self):
        return self.naipe in ["♥", "♦"]
    
    @property
    def texto(self):
        if self.virada:
            return "[XX]"
        valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        return f"{valores[self.valor-1]}{self.naipe}"
    
    @property
    def texto_superior(self):
        if self.virada:
            return "XX"
        valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        if self.valor == 10:
            return "10"
        return f"{valores[self.valor-1]}{self.naipe}"
    
    def to_dict(self):
        return {
            'naipe': self.naipe,
            'valor': self.valor,
            'virada': self.virada,
            'eh_vermelha': self.eh_vermelha(),
            'texto': self.texto,
            'texto_superior': self.texto_superior
        }

    def clone(self):
        return Carta(self.naipe, self.valor, self.virada)

class JogoKlondike:
    def __init__(self):
        self.tableau = [[] for _ in range(7)]
        self.fundacoes = [[] for _ in range(4)]
        self.estoque = []
        self.descarte = []
        self.historico = []
        self.MAX_HISTORICO = 50
        self.iniciar_jogo()
    
    def salvar_estado(self):
        if len(self.historico) >= self.MAX_HISTORICO:
            self.historico.pop(0)
        
        estado = {
            'tableau': [[carta.clone() for carta in coluna] for coluna in self.tableau],
            'fundacoes': [[carta.clone() for carta in fundacao] for fundacao in self.fundacoes],
            'estoque': [carta.clone() for carta in self.estoque],
            'descarte': [carta.clone() for carta in self.descarte]
        }
        self.historico.append(estado)
    
    def desfazer(self):
        if len(self.historico) > 0:
            estado_anterior = self.historico.pop()
            self.tableau = estado_anterior['tableau']
            self.fundacoes = estado_anterior['fundacoes']
            self.estoque = estado_anterior['estoque']
            self.descarte = estado_anterior['descarte']
            return True
        return False
    
    def iniciar_jogo(self):
        self.tableau = [[] for _ in range(7)]
        self.fundacoes = [[] for _ in range(4)]
        self.estoque = []
        self.descarte = []
        self.historico = []
        self.criar_baralho()
        self.distribuir_cartas()
        self.salvar_estado()
    
    def criar_baralho(self):
        naipes = ["♠", "♣", "♥", "♦"]
        baralho = []
        
        for naipe in naipes:
            for valor in range(1, 14):
                baralho.append(Carta(naipe, valor, True))
        
        random.shuffle(baralho)
        self.estoque = baralho
    
    def distribuir_cartas(self):
        idx = 0
        for col in range(7):
            for row in range(col + 1):
                carta = self.estoque[idx]
                carta.virada = (row != col)
                self.tableau[col].append(carta)
                idx += 1
        del self.estoque[:idx]
    
    def virar_estoque(self):
        self.salvar_estado()
        
        if len(self.estoque) == 0 and len(self.descarte) > 0:
            for carta in reversed(self.descarte):
                carta.virada = True
                self.estoque.append(carta)
            self.descarte.clear()
            return
        
        qtd = min(3, len(self.estoque))
        for _ in range(qtd):
            carta = self.estoque.pop(0)
            carta.virada = False
            self.descarte.append(carta)
    
    def pode_mover_para_fundacao(self, origem, indice_origem, fundacao_idx):
        if origem == "descarte" and self.descarte:
            carta = self.descarte[-1]
        elif origem == "tableau" and self.tableau[indice_origem]:
            carta = self.tableau[indice_origem][-1]
        else:
            return False
        
        if len(self.fundacoes[fundacao_idx]) == 0:
            return carta.valor == 1
        
        topo = self.fundacoes[fundacao_idx][-1]
        return (carta.naipe == topo.naipe and carta.valor == topo.valor + 1)
    
    def mover_carta(self, origem, indice_origem, destino, indice_destino):
        self.salvar_estado()
        
        if origem == "descarte" and self.descarte:
            carta = self.descarte.pop()
        elif origem == "tableau" and self.tableau[indice_origem]:
            carta = self.tableau[indice_origem].pop()
        else:
            return False
        
        if destino == "fundacao":
            self.fundacoes[indice_destino].append(carta)
        elif destino == "tableau":
            self.tableau[indice_destino].append(carta)
        
        self.virar_ultima_carta_tableau()
        return True
    
    def virar_ultima_carta_tableau(self):
        for coluna in self.tableau:
            if coluna:
                ultima_carta = coluna[-1]
                if ultima_carta.virada:
                    ultima_carta.virada = False
    
    def verificar_vitoria(self):
        return all(len(fundacao) == 13 for fundacao in self.fundacoes)
    
    def obter_tableau(self):
        return [[carta.to_dict() for carta in coluna] for coluna in self.tableau]
    
    def obter_fundacoes(self):
        return [[carta.to_dict() for carta in fundacao] for fundacao in self.fundacoes]
    
    def obter_estoque(self):
        return [carta.to_dict() for carta in self.estoque]
    
    def obter_descarte(self):
        return [carta.to_dict() for carta in self.descarte]
    
    def pode_mover_tableau_tableau(self, col_origem, row_origem, col_destino):
        if not self.tableau[col_origem] or self.tableau[col_origem][row_origem].virada:
            return False
        
        carta_movida = self.tableau[col_origem][row_origem]
        
        if not self.tableau[col_destino]:
            return carta_movida.valor == 13

        topo_destino = self.tableau[col_destino][-1]
        
        cor_oposta = carta_movida.eh_vermelha() != topo_destino.eh_vermelha()
        valor_menor = carta_movida.valor == topo_destino.valor - 1
        
        return cor_oposta and valor_menor
    
    def mover_cartas(self, origem, idx_origem, idx_origem_row, destino, idx_destino):
        self.salvar_estado()
        
        if origem == 'tableau':
            cartas_a_mover = self.tableau[idx_origem][idx_origem_row:]
            del self.tableau[idx_origem][idx_origem_row:]
        elif origem == 'descarte':
            if idx_origem_row != len(self.descarte) - 1:
                return False
            cartas_a_mover = [self.descarte.pop()]
        else:
            return False
            
        if destino == 'tableau':
            self.tableau[idx_destino].extend(cartas_a_mover)
            self.virar_ultima_carta_tableau()
            return True
        elif destino == 'fundacao' and len(cartas_a_mover) == 1:
            self.fundacoes[idx_destino].append(cartas_a_mover[0])
            self.virar_ultima_carta_tableau()
            return True
            
        if origem == 'tableau':
            self.tableau[idx_origem].extend(cartas_a_mover)
        elif origem == 'descarte':
            self.descarte.extend(cartas_a_mover)
            
        return False

class InterfaceJogo:
    def __init__(self):
        self.jogo = JogoKlondike()
        self.carta_selecionada = None
        self.origem_selecionada = None
        
        # Estados dos botões
        self.botao_desfazer_hover = False
        self.botao_dica_hover = False
        self.botao_novo_jogo_hover = False
        self.botao_regras_hover = False
        
        # Sistema de dicas
        self.hint_button_rect = pygame.Rect(800, 110, LARG_BOTAO, ALT_BOTAO)
        self.hint_active = False
        self.hints_expire_time = 0
        self.HINT_DURATION_MS = 4000

        # Sistema de regras
        self.mostrar_regras = False

        self.card_rects = {}
        self.move_count = 0
        self.start_ticks = pygame.time.get_ticks()
        self.paused = False
        self.pause_offset = 0
        self.game_won = False
        self.win_animation_time = 0

    def desenhar_barra_superior(self):
        """Desenha a barra superior cinza escura"""
        pygame.draw.rect(tela, CINZA_ESCURO, (0, 0, LARGURA, 80))
        
        # Desenhar botões na barra superior
        self.desenhar_botao("Desfazer (Ctrl+Z)", (20, 20), self.botao_desfazer_hover)
        self.desenhar_botao("Dica", (150, 20), self.botao_dica_hover)
        self.desenhar_botao("Novo Jogo", (280, 20), self.botao_novo_jogo_hover)
        self.desenhar_botao("Regras", (410, 20), self.botao_regras_hover)
        
        # Desenhar informações de jogo (tempo e movimentos)
        self.desenhar_info_jogo()

    def desenhar_info_jogo(self):
        """Desenha as informações de tempo e movimentos em caixas cinzas"""
        # Caixa de movimentos
        moves_rect = pygame.Rect(650, 20, LARG_INFO, ALT_INFO)
        pygame.draw.rect(tela, CINZA_BOTAO, moves_rect, border_radius=6)
        pygame.draw.rect(tela, PRETO, moves_rect, 2, border_radius=6)
        
        moves_text = fonte_botao.render(f"Movimentos: {self.move_count}", True, PRETO)
        moves_text_rect = moves_text.get_rect(center=moves_rect.center)
        tela.blit(moves_text, moves_text_rect)
        
        # Caixa de tempo
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks - self.pause_offset
        elapsed_s = max(0, elapsed_ms // 1000)
        mins = elapsed_s // 60
        secs = elapsed_s % 60
        
        time_rect = pygame.Rect(800, 20, LARG_INFO, ALT_INFO)
        pygame.draw.rect(tela, CINZA_BOTAO, time_rect, border_radius=6)
        pygame.draw.rect(tela, PRETO, time_rect, 2, border_radius=6)
        
        time_text = fonte_botao.render(f"Tempo: {mins:02d}:{secs:02d}", True, PRETO)
        time_text_rect = time_text.get_rect(center=time_rect.center)
        tela.blit(time_text, time_text_rect)

    def desenhar_botao(self, texto, pos, hover):
        cor_botao = CINZA_BOTAO_HOVER if hover else CINZA_BOTAO
        
        pygame.draw.rect(tela, cor_botao, (*pos, LARG_BOTAO, ALT_BOTAO), border_radius=6)
        pygame.draw.rect(tela, PRETO, (*pos, LARG_BOTAO, ALT_BOTAO), 2, border_radius=6)
        
        texto_render = fonte_botao.render(texto, True, PRETO)
        texto_rect = texto_render.get_rect(center=(pos[0] + LARG_BOTAO//2, pos[1] + ALT_BOTAO//2))
        tela.blit(texto_render, texto_rect)

    def desenhar_regras(self):
        """Desenha a tela de regras/estratégias"""
        # Fundo semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        tela.blit(overlay, (0, 0))
        
        # Caixa principal das regras
        caixa_rect = pygame.Rect(50, 100, LARGURA - 100, ALTURA - 200)
        pygame.draw.rect(tela, CINZA_CLARO, caixa_rect, border_radius=15)
        pygame.draw.rect(tela, PRETO, caixa_rect, 3, border_radius=15)
        
        # Título
        titulo = fonte_titulo.render("6 Estratégias de Paciência", True, PRETO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 120))
        
        # Lista de estratégias
        estrategias = [
            "1. Desbloqueie mais opções",
            "   Escolha jogadas que abram mais possibilidades futuras",
            "",
            "2. Jogue os ases e os dois cedo", 
            "   Mova para as fundações para liberar espaço",
            "",
            "3. Construa sequências longas",
            "   Não apresse as cartas para as fundações",
            "",
            "4. Prefira cartas do tabuleiro",
            "   Jogue primeiro as cartas reveladas",
            "",
            "5. Exponha colunas profundas",
            "   Revele pilhas com muitas cartas escondidas",
            "",
            "6. Use o botão desfazer",
            "   Teste jogadas mais inteligentes"
        ]
        
        y_pos = 170
        for linha in estrategias:
            if linha.startswith("1.") or linha.startswith("2.") or linha.startswith("3.") or \
               linha.startswith("4.") or linha.startswith("5.") or linha.startswith("6."):
                texto = fonte_subtitulo.render(linha, True, PRETO)
            else:
                texto = fonte_pequena.render(linha, True, PRETO)
            
            tela.blit(texto, (100, y_pos))
            y_pos += 30 if linha else 15
        
        # Botão para fechar
        self.desenhar_botao("Fechar", (LARGURA//2 - 60, ALTURA - 80), self.botao_regras_hover)

    def desenhar_carta(self, carta, x, y, mostrar_texto_superior=True):
        cor_borda = PRETO
        if (self.carta_selecionada and 
            self.carta_selecionada.get("texto") == carta.get("texto") and 
            self.carta_selecionada.get("naipe") == carta.get("naipe")):
            cor_borda = AZUL_SELECAO

        rect = pygame.Rect(x, y, LARG_CARTA, ALT_CARTA)
        key = (carta.get("texto"), carta.get("naipe"), x, y)
        self.card_rects[key] = rect

        if carta["virada"]:
            pygame.draw.rect(tela, BRANCO, rect, border_radius=8)
            pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=8)
            texto = fonte.render("XX", True, PRETO)
            tela.blit(texto, (x + 25, y + 50))
        else:
            pygame.draw.rect(tela, BRANCO, rect, border_radius=8)
            pygame.draw.rect(tela, cor_borda, rect, 2, border_radius=8)
            cor = VERMELHO if carta["eh_vermelha"] else PRETO
            
            texto = fonte.render(carta["texto"], True, cor)
            tela.blit(texto, (x + 20, y + 50))
            
            if mostrar_texto_superior:
                texto_superior = fonte_pequena.render(carta["texto_superior"], True, cor)
                tela.blit(texto_superior, (x + 5, y + 5))

    def desenhar_vitoria(self):
        if not self.game_won:
            return
            
        # Fundo semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))
        
        # Caixa de vitória
        caixa_rect = pygame.Rect(LARGURA//2 - 200, ALTURA//2 - 100, 400, 200)
        pygame.draw.rect(tela, DOURADO, caixa_rect, border_radius=15)
        pygame.draw.rect(tela, PRETO, caixa_rect, 3, border_radius=15)
        
        # Texto de vitória
        texto_parabens = fonte_grande.render("Parabéns!", True, PRETO)
        texto_movimentos = fonte.render(f"Movimentos: {self.move_count}", True, PRETO)
        
        # Calcular tempo
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks - self.pause_offset
        elapsed_s = max(0, elapsed_ms // 1000)
        mins = elapsed_s // 60
        secs = elapsed_s % 60
        texto_tempo = fonte.render(f"Tempo: {mins:02d}:{secs:02d}", True, PRETO)
        
        # Centralizar textos
        tela.blit(texto_parabens, (LARGURA//2 - texto_parabens.get_width()//2, ALTURA//2 - 60))
        tela.blit(texto_movimentos, (LARGURA//2 - texto_movimentos.get_width()//2, ALTURA//2 - 20))
        tela.blit(texto_tempo, (LARGURA//2 - texto_tempo.get_width()//2, ALTURA//2 + 10))
        
        # Botão de novo jogo na tela de vitória
        botao_novo_jogo_rect = pygame.Rect(LARGURA//2 - 60, ALTURA//2 + 50, LARG_BOTAO, ALT_BOTAO)
        cor_botao = CINZA_BOTAO_HOVER if self.botao_novo_jogo_hover else CINZA_BOTAO
        
        pygame.draw.rect(tela, cor_botao, botao_novo_jogo_rect, border_radius=6)
        pygame.draw.rect(tela, PRETO, botao_novo_jogo_rect, 2, border_radius=6)
        
        texto_render = fonte_botao.render("Novo Jogo", True, PRETO)
        texto_rect = texto_render.get_rect(center=botao_novo_jogo_rect.center)
        tela.blit(texto_render, texto_rect)

    def desenhar_estado(self):
        tela.fill(VERDE_MESA)
        self.card_rects.clear()
        
        # Desenhar barra superior
        self.desenhar_barra_superior()
        
        # Se estiver mostrando regras, desenhar e retornar
        if self.mostrar_regras:
            self.desenhar_regras()
            pygame.display.flip()
            return
        
        estado_tableau = self.jogo.obter_tableau()
        estado_fundacoes = self.jogo.obter_fundacoes()
        estado_estoque = self.jogo.obter_estoque()
        estado_descarte = self.jogo.obter_descarte()

        # Estoque
        if len(estado_estoque) > 0:
            pygame.draw.rect(tela, BRANCO, (*pos_estoque, LARG_CARTA, ALT_CARTA), border_radius=8)
            pygame.draw.rect(tela, PRETO, (*pos_estoque, LARG_CARTA, ALT_CARTA), 2, border_radius=8)
        else:
            pygame.draw.rect(tela, PRETO, (*pos_estoque, LARG_CARTA, ALT_CARTA), 2, border_radius=8)

        # Descarte
        for i, carta in enumerate(estado_descarte[-3:]):
            x = pos_descarte[0] + i * 25 
            mostrar_texto_superior = i > 0
            self.desenhar_carta(carta, x, pos_descarte[1], mostrar_texto_superior)

        # Fundações
        for i, fund in enumerate(estado_fundacoes):
            x, y = pos_fundacoes[i]
            if len(fund) > 0:
                self.desenhar_carta(fund[-1], x, y, False)
            else:
                pygame.draw.rect(tela, PRETO, (x, y, LARG_CARTA, ALT_CARTA), 2, border_radius=8)

        # Tableau
        for col, cartas in enumerate(estado_tableau):
            x, y = pos_tableau[col]
            
            if len(cartas) == 0:
                pygame.draw.rect(tela, (0, 100, 0), (x, y, LARG_CARTA, ALT_CARTA), 1)
            
            for row, carta in enumerate(cartas):
                mostrar_texto_superior = row < len(cartas) - 1
                self.desenhar_carta(carta, x, y + row * 25, mostrar_texto_superior)

        # Dicas
        if self.hint_active:
            moves = self.find_possible_moves()
            self.draw_hint_highlights(moves)

        # Vitória
        if self.game_won:
            self.desenhar_vitoria()

        pygame.display.flip()
    
    def obter_area_clicada(self, x, y):
        # Se estiver mostrando regras, só o botão fechar funciona
        if self.mostrar_regras:
            botao_fechar_x = LARGURA//2 - 60
            botao_fechar_y = ALTURA - 80
            if (botao_fechar_x <= x <= botao_fechar_x + LARG_BOTAO and
                botao_fechar_y <= y <= botao_fechar_y + ALT_BOTAO):
                return 'botao_fechar_regras', 0, 0
            return None, None, None

        # Se estiver na tela de vitória, verificar o botão "Novo Jogo"
        if self.game_won:
            botao_novo_jogo_x = LARGURA//2 - 60
            botao_novo_jogo_y = ALTURA//2 + 50
            if (botao_novo_jogo_x <= x <= botao_novo_jogo_x + LARG_BOTAO and
                botao_novo_jogo_y <= y <= botao_novo_jogo_y + ALT_BOTAO):
                return 'botao_novo_jogo_vitoria', 0, 0
            return None, None, None

        # Botões da barra superior
        if (20 <= x <= 20 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO):
            return 'botao_desfazer', 0, 0

        if (150 <= x <= 150 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO):
            return 'botao_dica', 0, 0

        if (280 <= x <= 280 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO):
            return 'botao_novo_jogo', 0, 0

        if (410 <= x <= 410 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO):
            return 'botao_regras', 0, 0

        # Áreas do jogo (só verificar se y > 80 - abaixo da barra)
        if y <= 80:
            return None, None, None

        # Ajustar coordenadas para área de jogo
        y_ajustado = y

        # Estoque
        if (pos_estoque[0] <= x <= pos_estoque[0] + LARG_CARTA and
            pos_estoque[1] <= y_ajustado <= pos_estoque[1] + ALT_CARTA):
            return 'estoque', 0, 0 

        # Descarte
        estado_descarte = self.jogo.obter_descarte()
        if estado_descarte:
            x_topo = pos_descarte[0] + min(2, len(estado_descarte) - 1) * 25
            if (x_topo <= x <= x_topo + LARG_CARTA and
                pos_descarte[1] <= y_ajustado <= pos_descarte[1] + ALT_CARTA):
                return 'descarte', 0, len(estado_descarte) - 1

        # Fundações
        for i, fund in enumerate(self.jogo.obter_fundacoes()):
            x_fund, y_fund = pos_fundacoes[i]
            if (x_fund <= x <= x_fund + LARG_CARTA and
                y_fund <= y_ajustado <= y_fund + ALT_CARTA):
                return 'fundacao', i, len(fund) - 1

        # Tableau
        estado_tableau = self.jogo.obter_tableau()
        for col, cartas in enumerate(estado_tableau):
            x_tab, y_tab = pos_tableau[col]
            
            if len(cartas) == 0:
                if (x_tab <= x <= x_tab + LARG_CARTA and
                    y_tab <= y_ajustado <= y_tab + ALT_CARTA):
                    return 'tableau', col, -1
            else:
                y_ultima = y_tab + (len(cartas) - 1) * 25
                if (x_tab <= x <= x_tab + LARG_CARTA and
                    y_ultima <= y_ajustado <= y_ultima + ALT_CARTA):
                    return 'tableau', col, len(cartas) - 1
                
                for row in range(len(cartas) - 1):
                    y_carta = y_tab + row * 25
                    if (x_tab <= x <= x_tab + LARG_CARTA and
                        y_carta <= y_ajustado < y_carta + 25):
                        return 'tableau', col, row

        return None, None, None
    
    def verificar_hover_botao(self, x, y):
        self.botao_desfazer_hover = (
            20 <= x <= 20 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO
        )
        self.botao_dica_hover = (
            150 <= x <= 150 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO
        )
        self.botao_novo_jogo_hover = (
            280 <= x <= 280 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO
        )
        self.botao_regras_hover = (
            410 <= x <= 410 + LARG_BOTAO and
            20 <= y <= 20 + ALT_BOTAO
        )

    def handle_click(self, x, y):
        # Se estiver mostrando regras, só processar o botão fechar
        if self.mostrar_regras:
            # Verificar se clicou no botão "Fechar" dentro das regras
            botao_fechar_x = LARGURA//2 - 60
            botao_fechar_y = ALTURA - 80
            if (botao_fechar_x <= x <= botao_fechar_x + LARG_BOTAO and
                botao_fechar_y <= y <= botao_fechar_y + ALT_BOTAO):
                self.mostrar_regras = False
                return
            
            # Se clicou fora do botão fechar, não fazer nada
            return

        area_clicada, idx1_clicado, idx2_clicado = self.obter_area_clicada(x, y)
        
        # Se estiver na tela de vitória, processar o botão "Novo Jogo"
        if self.game_won and area_clicada == 'botao_novo_jogo_vitoria':
            self.novo_jogo()
            return

        if area_clicada == 'botao_desfazer':
            if self.jogo.desfazer():
                self.move_count += 1
            self.carta_selecionada = None
            self.origem_selecionada = None
            return

        if area_clicada == 'botao_dica':
            moves = self.find_possible_moves()
            if moves:
                self.hint_active = True
                self.hints_expire_time = pygame.time.get_ticks() + self.HINT_DURATION_MS
            else:
                self.hint_active = True
                self.hints_expire_time = pygame.time.get_ticks() + 800
            return

        if area_clicada == 'botao_novo_jogo':
            self.novo_jogo()
            return

        if area_clicada == 'botao_regras':
            self.mostrar_regras = not self.mostrar_regras
            return

        if area_clicada == 'estoque':
            self.jogo.virar_estoque()
            self.move_count += 1
            self.carta_selecionada = None
            self.origem_selecionada = None
            return

        if self.carta_selecionada is not None:
            origem = self.origem_selecionada
            destino = (area_clicada, idx1_clicado, idx2_clicado)

            if area_clicada == 'fundacao':
                if origem[0] in ('descarte', 'tableau'):
                    if self.jogo.pode_mover_para_fundacao(origem[0], origem[1], idx1_clicado):
                        if self.jogo.mover_cartas(origem[0], origem[1], origem[2], 'fundacao', idx1_clicado):
                            self.carta_selecionada = None
                            self.origem_selecionada = None
                            self.move_count += 1
                            return

            elif area_clicada == 'tableau':
                if origem[0] == 'tableau':
                    col_origem = origem[1]
                    row_origem = origem[2]
                    col_destino = idx1_clicado

                    if self.jogo.pode_mover_tableau_tableau(col_origem, row_origem, col_destino):
                        if self.jogo.mover_cartas(origem[0], col_origem, row_origem, 'tableau', col_destino):
                            self.carta_selecionada = None
                            self.origem_selecionada = None
                            self.move_count += 1
                            return

                elif origem[0] == 'descarte':
                    col_destino = idx1_clicado
                    estado_tableau = self.jogo.obter_tableau()
                    estado_descarte = self.jogo.obter_descarte()
                    
                    if estado_descarte:
                        carta_descarte = estado_descarte[-1]
                        if estado_tableau[col_destino]:
                            topo_tableau = estado_tableau[col_destino][-1]
                            if (carta_descarte['eh_vermelha'] != topo_tableau['eh_vermelha'] and 
                                carta_descarte['valor'] == topo_tableau['valor'] - 1):
                                if self.jogo.mover_cartas(origem[0], origem[1], origem[2], 'tableau', col_destino):
                                    self.carta_selecionada = None
                                    self.origem_selecionada = None
                                    self.move_count += 1
                                    return
                        else:
                            if carta_descarte['valor'] == 13:
                                if self.jogo.mover_cartas(origem[0], origem[1], origem[2], 'tableau', col_destino):
                                    self.carta_selecionada = None
                                    self.origem_selecionada = None
                                    self.move_count += 1
                                    return

            self.carta_selecionada = None
            self.origem_selecionada = None

        # Se estiver mostrando regras ou tela de vitória, não processar outros cliques de jogo
        if self.mostrar_regras or self.game_won:
            return

        if area_clicada in ('tableau', 'descarte'):
            carta = None
            if area_clicada == 'descarte' and idx2_clicado == len(self.jogo.obter_descarte()) - 1:
                carta = self.jogo.obter_descarte()[-1]
            
            elif area_clicada == 'tableau':
                if idx2_clicado != -1:
                    carta_tab = self.jogo.obter_tableau()[idx1_clicado][idx2_clicado]
                    if not carta_tab['virada']:
                        carta = carta_tab
            
            if carta is not None:
                self.carta_selecionada = carta
                self.origem_selecionada = (area_clicada, idx1_clicado, idx2_clicado)
            else:
                self.carta_selecionada = None
                self.origem_selecionada = None

    def novo_jogo(self):
        self.jogo.iniciar_jogo()
        self.move_count = 0
        self.start_ticks = pygame.time.get_ticks()
        self.game_won = False
        self.carta_selecionada = None
        self.origem_selecionada = None
        self.mostrar_regras = False

    # Métodos de dica (mantidos do código original)
    def find_possible_moves(self):
        moves = []
        estado_tableau = self.jogo.obter_tableau()
        estado_fundacoes = self.jogo.obter_fundacoes()
        estado_descarte = self.jogo.obter_descarte()
        waste_top = estado_descarte[-1] if estado_descarte else None

        if waste_top:
            for t_idx, t_pile in enumerate(estado_tableau):
                dest_top = t_pile[-1] if t_pile else None
                if self._can_move_to_tableau_dict(waste_top, dest_top):
                    moves.append(('descarte', None, None, 'tableau', t_idx, waste_top))
            for f_idx, f in enumerate(estado_fundacoes):
                f_top = f[-1] if f else None
                if self._can_move_to_foundation_dict(waste_top, f_top):
                    moves.append(('descarte', None, None, 'fundacao', f_idx, waste_top))

        for src_idx, src in enumerate(estado_tableau):
            if not src:
                continue
            first_faceup = None
            for i, c in enumerate(src):
                if not c['virada']:
                    first_faceup = i
                    break
            if first_faceup is None:
                continue
            for i in range(first_faceup, len(src)):
                card = src[i]
                for dst_idx, dst in enumerate(estado_tableau):
                    if dst_idx == src_idx:
                        continue
                    dst_top = dst[-1] if dst else None
                    if self._can_move_to_tableau_dict(card, dst_top):
                        moves.append(('tableau', src_idx, i, 'tableau', dst_idx, card))
                if i == len(src) - 1:
                    for f_idx, f in enumerate(estado_fundacoes):
                        f_top = f[-1] if f else None
                        if self._can_move_to_foundation_dict(card, f_top):
                            moves.append(('tableau', src_idx, i, 'fundacao', f_idx, card))

        return moves

    def _can_move_to_tableau_dict(self, card_dict, dest_top_dict):
        if dest_top_dict is None:
            return card_dict['valor'] == 13
        cor_card = 'red' if card_dict['naipe'] in ['♥','♦'] else 'black'
        cor_dest = 'red' if dest_top_dict['naipe'] in ['♥','♦'] else 'black'
        return cor_card != cor_dest and card_dict['valor'] == dest_top_dict['valor'] - 1

    def _can_move_to_foundation_dict(self, card_dict, f_top_dict):
        if f_top_dict is None:
            return card_dict['valor'] == 1
        return card_dict['naipe'] == f_top_dict['naipe'] and card_dict['valor'] == f_top_dict['valor'] + 1

    def draw_hint_highlights(self, moves):
        s = pygame.Surface((LARG_CARTA, ALT_CARTA), pygame.SRCALPHA)
        s.fill(HINT_FILL)
        origem_rects = []
        destino_rects = []
        for m in moves:
            tipo_origem = m[0]
            if tipo_origem == 'descarte':
                idx = min(2, len(self.jogo.descarte)-1) if self.jogo.descarte else 0
                x = pos_descarte[0] + idx * 25
                y = pos_descarte[1]
                origem_rects.append(pygame.Rect(x, y, LARG_CARTA, ALT_CARTA))
            elif tipo_origem == 'tableau':
                src_col = m[1]
                src_row = m[2]
                x = pos_tableau[src_col][0]
                y = pos_tableau[src_col][1] + src_row * 25
                origem_rects.append(pygame.Rect(x, y, LARG_CARTA, ALT_CARTA))
            
            tipo_dest = m[3]
            dst_idx = m[4]
            if tipo_dest == 'tableau':
                x = pos_tableau[dst_idx][0]
                pilha = self.jogo.tableau[dst_idx]
                if pilha:
                    y = pos_tableau[dst_idx][1] + (len(pilha) - 1) * 25
                else:
                    y = pos_tableau[dst_idx][1]
                destino_rects.append(pygame.Rect(x, y, LARG_CARTA, ALT_CARTA))
            elif tipo_dest == 'fundacao':
                x, y = pos_fundacoes[dst_idx]
                destino_rects.append(pygame.Rect(x, y, LARG_CARTA, ALT_CARTA))
        
        for r in origem_rects:
            surf = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
            surf.fill((0,0,255,60))
            tela.blit(surf, (r.x, r.y))
            pygame.draw.rect(tela, (0,0,200), r, 2)
        
        for r in destino_rects:
            surf = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
            surf.fill(HINT_FILL)
            tela.blit(surf, (r.x, r.y))
            pygame.draw.rect(tela, HINT_BORDER, r, 2)

    def executar(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.handle_click(x, y)
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    self.verificar_hover_botao(x, y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                        if self.jogo.desfazer():
                            self.move_count += 1
                        self.carta_selecionada = None
                        self.origem_selecionada = None
                    elif event.key == pygame.K_r:
                        self.novo_jogo()
                    elif event.key == pygame.K_p:
                        if not self.paused:
                            self.paused = True
                            self.pause_start = pygame.time.get_ticks()
                        else:
                            self.paused = False
                            self.pause_offset += pygame.time.get_ticks() - self.pause_start
                    elif event.key == pygame.K_ESCAPE:
                        self.mostrar_regras = False

            if self.hint_active and pygame.time.get_ticks() > self.hints_expire_time:
                self.hint_active = False

            self.desenhar_estado()

            if not self.game_won and self.jogo.verificar_vitoria():
                self.game_won = True
                self.win_animation_time = pygame.time.get_ticks()

            clock.tick(30)

# Executar o jogo
if __name__ == "__main__":
    interface = InterfaceJogo()
    interface.executar()