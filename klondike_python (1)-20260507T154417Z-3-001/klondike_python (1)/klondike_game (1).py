import random
import json

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
        """Retorna apenas o número/naipe para mostrar na parte superior da carta"""
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
        """Cria uma cópia da carta"""
        return Carta(self.naipe, self.valor, self.virada)

tableau = []
fundacoes = []
estoque = []
descarte = []
historico = []  # Lista para armazenar estados anteriores
MAX_HISTORICO = 50  # Limite de ações no histórico

def salvar_estado():
    """Salva o estado atual do jogo no histórico"""
    if len(historico) >= MAX_HISTORICO:
        historico.pop(0)
    
    estado = {
        'tableau': [[carta.clone() for carta in coluna] for coluna in tableau],
        'fundacoes': [[carta.clone() for carta in fundacao] for fundacao in fundacoes],
        'estoque': [carta.clone() for carta in estoque],
        'descarte': [carta.clone() for carta in descarte]
    }
    historico.append(estado)

def desfazer():
    """Desfaz a última ação"""
    if len(historico) > 0:
        estado_anterior = historico.pop()
        
        global tableau, fundacoes, estoque, descarte
        tableau = estado_anterior['tableau']
        fundacoes = estado_anterior['fundacoes']
        estoque = estado_anterior['estoque']
        descarte = estado_anterior['descarte']
        return True
    return False

def iniciar_jogo():
    global tableau, fundacoes, estoque, descarte, historico
    
    tableau = [[] for _ in range(7)]
    fundacoes = [[] for _ in range(4)]
    estoque = []
    descarte = []
    historico = []
    
    criar_baralho()
    distribuir_cartas()
    salvar_estado()  # Salva estado inicial

def criar_baralho():
    global estoque
    naipes = ["♠", "♣", "♥", "♦"]
    baralho = []
    
    for naipe in naipes:
        for valor in range(1, 14):
            baralho.append(Carta(naipe, valor, True))
    
    random.shuffle(baralho)
    estoque = baralho

def distribuir_cartas():
    global tableau, estoque
    idx = 0
    
    for col in range(7):
        for row in range(col + 1):
            carta = estoque[idx]
            carta.virada = (row != col)
            tableau[col].append(carta)
            idx += 1
    
    del estoque[:idx]

def virar_estoque():
    salvar_estado()  # Salva estado antes da ação
    
    global estoque, descarte
    
    if len(estoque) == 0 and len(descarte) > 0:
        for carta in reversed(descarte):
            carta.virada = True
            estoque.append(carta)
        descarte.clear()
        return
    
    qtd = min(3, len(estoque))
    for _ in range(qtd):
        carta = estoque.pop(0)
        carta.virada = False
        descarte.append(carta)

def pode_mover_para_fundacao(origem, indice_origem, fundacao_idx):
    if origem == "descarte" and descarte:
        carta = descarte[-1]
    elif origem == "tableau" and tableau[indice_origem]:
        carta = tableau[indice_origem][-1]
    else:
        return False
    
    if len(fundacoes[fundacao_idx]) == 0:
        return carta.valor == 1
    
    topo = fundacoes[fundacao_idx][-1]
    return (carta.naipe == topo.naipe and carta.valor == topo.valor + 1)

def mover_carta(origem, indice_origem, destino, indice_destino):
    salvar_estado()  # Salva estado antes da ação
    
    if origem == "descarte" and descarte:
        carta = descarte.pop()
    elif origem == "tableau" and tableau[indice_origem]:
        carta = tableau[indice_origem].pop()
    else:
        return False
    
    if destino == "fundacao":
        fundacoes[indice_destino].append(carta)
    elif destino == "tableau":
        tableau[indice_destino].append(carta)
    
    virar_ultima_carta_tableau()
    return True

def virar_ultima_carta_tableau():
    for coluna in tableau:
        if coluna:
            ultima_carta = coluna[-1]
            if ultima_carta.virada:
                ultima_carta.virada = False

def verificar_vitoria():
    return all(len(fundacao) == 13 for fundacao in fundacoes)

def obter_tableau():
    return [[carta.to_dict() for carta in coluna] for coluna in tableau]

def obter_fundacoes():
    return [[carta.to_dict() for carta in fundacao] for fundacao in fundacoes]

def obter_estoque():
    return [carta.to_dict() for carta in estoque]

def obter_descarte():
    return [carta.to_dict() for carta in descarte]

def pode_mover_tableau_tableau(col_origem, row_origem, col_destino):
    if not tableau[col_origem] or tableau[col_origem][row_origem].virada: return False
    
    carta_movida = tableau[col_origem][row_origem]
    
    if not tableau[col_destino]:
        return carta_movida.valor == 13

    topo_destino = tableau[col_destino][-1]
    
    cor_oposta = carta_movida.eh_vermelha() != topo_destino.eh_vermelha()
    valor_menor = carta_movida.valor == topo_destino.valor - 1
    
    return cor_oposta and valor_menor
    
def mover_cartas(origem, idx_origem, idx_origem_row, destino, idx_destino):
    salvar_estado()  # Salva estado antes da ação
    
    if origem == 'tableau':
        cartas_a_mover = tableau[idx_origem][idx_origem_row:]
        del tableau[idx_origem][idx_origem_row:]
    elif origem == 'descarte':
        if idx_origem_row != len(descarte) - 1: return False
        cartas_a_mover = [descarte.pop()]
    else:
        return False
        
    if destino == 'tableau':
        tableau[idx_destino].extend(cartas_a_mover)
        virar_ultima_carta_tableau()
        return True
    elif destino == 'fundacao' and len(cartas_a_mover) == 1:
        fundacoes[idx_destino].append(cartas_a_mover[0])
        virar_ultima_carta_tableau()
        return True
        
    if origem == 'tableau':
        tableau[idx_origem].extend(cartas_a_mover)
    elif origem == 'descarte':
        descarte.extend(cartas_a_mover)
        
    return False

iniciar_jogo()