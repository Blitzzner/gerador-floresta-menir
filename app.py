import random
import streamlit as st
from typing import Dict, List, Tuple

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Gerador - Floresta do Menir",
    page_icon="🌲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# DADOS BASE DA FLORESTA DO MENIR
# ==========================================
ASSENTAMENTOS = {
    "Buraco Roto": [(12, "Humano"), (15, "Méerme"), (17, "Elfo"), (19, "Musgueiro"), (20, "Mûr")],
    "Dreg": [(10, "Humano"), (14, "Méerme"), (18, "Musgueiro"), (19, "Mûr"), (20, "Cattus")],
    "Tosacurta": [(8, "Méerme"), (11, "Humano"), (16, "Cattus"), (19, "Elfo"), (20, "Mûr")],
    "Altonó": [(8, "Méerme"), (14, "Humano"), (16, "Mûr"), (19, "Cattus"), (20, "Elfo")],
    "Prigwort": [(9, "Humano"), (13, "Méerme"), (17, "Musgueiro"), (18, "Elfo"), (20, "Mûr")],
    "Castelo Campina da Samambaia": [(10, "Humano"), (15, "Méerme"), (20, "Elfo")]
}

CLASSES_INFO = {
    "Bardo": {"dv": 6, "ataque": "+0", "attr": ["DES", "CAR"]}, 
    "Clérigo": {"dv": 6, "ataque": "+0", "attr": ["SAB"]},
    "Encantador": {"dv": 6, "ataque": "+0", "attr": ["INT", "CAR"]}, 
    "Guerreiro": {"dv": 8, "ataque": "+1", "attr": ["FOR", "CON"]},
    "Frade": {"dv": 4, "ataque": "+0", "attr": ["SAB"]}, 
    "Caçador": {"dv": 8, "ataque": "+1", "attr": ["FOR", "DES"]},
    "Cavaleiro": {"dv": 8, "ataque": "+1", "attr": ["FOR", "CON"]}, 
    "Mago": {"dv": 4, "ataque": "+0", "attr": ["INT"]},
    "Ladrão": {"dv": 4, "ataque": "+0", "attr": ["DES"]}
}

SALVAGUARDAS = {
    "Bardo": (13, 14, 13, 15, 15), "Clérigo": (11, 13, 12, 16, 14),
    "Encantador": (11, 12, 13, 16, 14), "Guerreiro": (12, 13, 14, 15, 16),
    "Frade": (11, 12, 13, 16, 14), "Caçador": (12, 14, 13, 15, 16),
    "Cavaleiro": (12, 13, 12, 15, 15), "Mago": (14, 14, 13, 16, 14),
    "Ladrão": (13, 14, 13, 15, 15)
}

ARMADURAS = {
    "Sem armadura": {"ca": 10, "peso": 0}, "Couro": {"ca": 12, "peso": 200},
    "Casca de árvore": {"ca": 13, "peso": 300}, "Cota de malha": {"ca": 14, "peso": 400},
    "Pinha": {"ca": 15, "peso": 400}, "Escamas": {"ca": 16, "peso": 500},
    "Placas": {"ca": 17, "peso": 700}
}

ARMAS = {
    "Machado de batalha": {"dano": "1d8", "peso": 100}, "Porrete": {"dano": "1d4", "peso": 20},
    "Besta": {"dano": "1d8", "peso": 50}, "Adaga": {"dano": "1d4", "peso": 10},
    "Machadinha": {"dano": "1d6", "peso": 20}, "Lança Justa": {"dano": "1d6", "peso": 100},
    "Arco longo": {"dano": "1d6", "peso": 40}, "Espada Longa": {"dano": "1d8", "peso": 30},
    "Maça": {"dano": "1d6", "peso": 40}, "Alabarda": {"dano": "1d10", "peso": 140},
    "Arco curto": {"dano": "1d6", "peso": 20}, "Espada curta": {"dano": "1d6", "peso": 20},
    "Funda": {"dano": "1d4", "peso": 10}, "Lança": {"dano": "1d6", "peso": 30},
    "Cajado": {"dano": "1d4", "peso": 40}, "Espada larga": {"dano": "1d10", "peso": 140},
    "Martelo de guerra": {"dano": "1d6", "peso": 40}
}

ITENS_AVENTURA = [
    "Vara 3m", "Giz (10 pedaços)", "Cinzel", "Panelas", "Pé de cabra",
    "Roupa de inverno", "Arpeu", "Tinta, pena e papel", "Cravos de ferro (12)",
    "Lanterna", "Bolinhas de gude", "Ânfora de óleo", "Corda (15m)",
    "Sacos grandes", "Pá", "Marreta", "Martelo", "Tenda", "Estrepes", "Barbante (50m)"
]

SIGNOS_LUNARES = [
    (3, "Sorridente (Crescente)", "50% chance de um guardião morto-vivo ignorar a presença do personagem, se não provocado."),
    (4, "Sorridente (Cheia)", "+1 bônus em salvaguarda contra poderes de mortos-vivos."),
    (7, "Sorridente (Minguante)", "+1 ataque contra mortos-vivos."),
    (10, "Morta (Crescente)", "+1 em ataque e rolagem de dano na rodada subsequente a matar um inimigo."),
    (11, "Morta (Cheia)", "Se morto por meios não mágicos, retorna à morte após 1 turno com 1 PV. CON e SAB permanentemente reduzidas à metade. Numa 2ª morte, sem efeito."),
    (14, "Morta (Minguante)", "Mortos-vivos atacam este personagem por último."),
    (17, "Besta (Crescente)", "+2 bônus em Carisma (máx. 18) quando interagir com animais domesticados."),
    (18, "Besta (Cheia)", "Animais selvagens atacam este personagem por último."),
    (21, "Besta (Minguante)", "+1 ataque contra animais selvagens."),
    (24, "Escamosa (Crescente)", "Efeitos de venenos são atrasados em 1 turno."),
    (25, "Escamosa (Cheia)", "+2 bônus em Salvaguarda contra ataques de sopro e poderes mágicos de serpes e dragões."),
    (29, "Escamosa (Minguante)", "+1 ataque contra serpentes e serpes."),
    (33, "do Cavaleiro (Crescente)", "+2 bônus em Carisma (máx. 18) quando interagir com nobres."),
    (34, "do Cavaleiro (Cheia)", "+1 CA defendendo ataques de armas de metais."),
    (38, "do Cavaleiro (Minguante)", "Em um empate de iniciativa contra cavaleiros ou soldados, o personagem age primeiro."),
    (42, "Apodrecida (Crescente)", "+2 em Carisma (máx. 18) quando interagir com fungos sencientes."),
    (43, "Apodrecida (Cheia)", "+2 CA contra ataques de criaturas fúngicas."),
    (47, "Apodrecida (Minguante)", "Na presença do personagem, monstros fúngicos sofrem -1 de penalidade em ataques e rolagens de dano."),
    (51, "da Donzela (Crescente)", "+2 bônus em Carisma (máx. 18) quando interagir com semi-fadas."),
    (52, "da Donzela (Cheia)", "+2 bônus em salvaguarda contra encantamentos e glamours."),
    (56, "da Donzela (Minguante)", "+1 bônus em ataque e dano contra criaturas metamorfas ou recoberta por ilusões."),
    (60, "da Feiticeira (Crescente)", "Quando recebe cura mágica, cura 1 PV adicional (Aplica-se uma vez ao dia por tipo de cura mágica)."),
    (61, "da Feiticeira (Cheia)", "+1 bônus em salvaguarda contra magia sagrada (milagres)."),
    (65, "da Feiticeira (Minguante)", "+1 bônus em ataques contra feiticeiras e conjuradores divinos."),
    (69, "do Ladrão (Crescente)", "+2 bônus em Carisma (máx. 18) quando interagir com mortais caóticos."),
    (70, "do Ladrão (Cheia)", "+1 CA defendendo ataques de mortais, fadas e semi-fadas caóticos."),
    (74, "do Ladrão (Minguante)", "+1 ataque contra mortais, fadas e semi-fadas caóticos."),
    (78, "Bode (Crescente)", "+2 bônus em Carisma (máx. 18) quando interagir com méermes (incluindo chifres retorcidos)."),
    (79, "Bode (Cheia)", "Méermes (incluindo chifres retorcidos) atacam o personagem por último."),
    (83, "Bode (Minguante)", "+1 ataque contra méermes (incluindo chifres retorcidos)."),
    (87, "Estreita (Crescente)", "+2 bônus em Carisma (Máx. 18) interagindo com fadas, mas sofre -1 em salvaguarda contra magias faéricas."),
    (88, "Estreita (Cheia)", "Se afligido por maldição/Tabu, há 1-em-4 chance do conjurador também ser afligido pela mesma magia."),
    (92, "Estreita (Minguante)", "+1 bônus em ataque contra fadas e semi-fadas."),
    (96, "Preta (Crescente)", "+1 bônus em reações de NPCs e criaturas."),
    (97, "Preta (Cheia)", "+2 bônus em CA e salvaguarda quando surpreso."),
    (100, "Preta (Minguante)", "+ 2 bônus em salvaguarda contra ilusões e glamours.")
]

LINGUAS_PARENTESCO = {
    "Humano": ["Campinês"], "Méerme": ["Campinês", "Gaffe", "Caprês"],
    "Elfo": ["Campinês", "Silvânico", "Alto Élfico"], "Musgueiro": ["Campinês", "Mulchês"],
    "Mûr": ["Campinês", "Silvânico"], "Cattus": ["Campinês", "Miau"]
}
LINGUAS_EXTRAS = ["Drûnico", "Subterrânico", "Bogin", "Deorlíngua", "Serpês"]

NOMES = {
    "Elfo": {
        "Rústico": ["Mãe-Que-Bebe-Champagne", "Flerte-ao-Ver-Te", "Caipira-Pira-e-Espirra", "Torresmo-Resmungando", "Pato-e-Sapato-Empatado", "Óculos-Verde-Perto", "Sibila-na-camomila", "Uma-Banda-de-Maçã", "Acorda-Bem-Abóbora", "E-Se-Tu-Pedir-Quadrúpede", "Papelada-Pá-Vestida", "Triste-Como-Lápis-Desapontado", "Juntos-Mió-Que-Só", "Janta-Antes-do-Meio-Dia", "Rapte-me-Capte-me", "Titã-de-Rolimã", "Nome-de-Perfume", "Tramela-Sem-Janela", "Despudorada-Dada-é-Danada", "Juventude-Agora-Coagulada"],
        "Cortês": ["Concebe-apenas-sonhos", "Sopro-sobre-luz-de-velas", "Cálice-de-violeta", "Sonho-de-recordações", "Luminescência-dos-dias-perdidos", "Pacto-selado-com-besouros", "Imprudência-tem-suas-conquistas", "Indigo-e-artesanato", "Não-case-com-homens", "Última-névoa-matinal", "Assassinato-das-gralhas", "Trepidação-da-noite", "Cheiro-doce-da-vingança", "Sete-passos-no-amanhecer", "Tom-de-traição-invernal", "Fino-gemido-do-vento", "Lamento-raso-do-espírito", "Desliza-atrás-das-sombras", "Arrogância-da-Primavera", "Violeta-e-Clementina"]
    },
    "Méerme": {
        "Homem": ["Aele", "Broob", "Crump", "Drerdil", "Frennig", "Grerg", "Gripe", "Llerg", "Llerod", "Lope", "Mashker", "Olledg", "Rheg", "Xandgara", "Xandbem", "Xandtir", "Xandor", "Xank", "Snerd"],
        "Mulher": ["Braembel", "Berrilda", "Bredhir", "Draed", "Fannigril", "Frandorup", "Grendilore", "Grendel", "Gretch", "Hildrup", "Hraigl", "Hwendel", "Maybel", "Myrkla", "Nannigril", "Pettigril", "Rrhimbir", "Shord", "Smethra", "Whelda"],
        "Unissex": ["Aedel", "Addle", "Blocke", "Clover", "Crewwin", "Curlip", "Eleye", "Ellip", "Frannidore", "Ghrend", "Grennigara", "Gwendil", "Hrannick", "Hwoldrup", "Lindor", "Merril", "Smenthard", "Snerg", "Wendil", "Windor"],
        "Sobrenome": ["Tagarelalto", "Mechazul", "Cascoval", "Cascopaco", "Cotoveloliso", "Cachoscurtos", "Cachoslongos", "Tosacurta", "Chifrepontudo", "Barbalonga", "Canelalonga", "Canelacurta", "Cervinho", "Cócegasleve", "Balidomalicioso", "Laceiro", "Balidobaixo", "Cervão", "Campineiro", "Saltacampina"]
    },
    "Cattus": {
        "Primeiro Nome": ["Laranja", "Pretinho(a)", "Ruivinho(a)", "Zeca", "Faísca", "Jasqueline", "Miau", "Pequeno(a)", "Lorde/Lady", "Vovô", "Mamã", "Monsieur/Madame", "Neném", "Mingau", "Pisspiss", "Príncipe/Princesa", "Pitoco/Pituca", "Barão/Baronesa", "Luna", "Tomtom"],
        "Sobrenome": ["Bichano", "Meia-branca", "Cauda torta", "Felpudo", "Fofura", "Caçador", "Sete-vidas", "Lambida", "Língua-de-leite", "Gatuno", "Malhado", "Pega-rato", "de Botas", "Glutão", "Tricolor", "Petisco", "Tigrado", "Arranhador", "Ronron", "Bigode-molhado"]
    },
    "Humano": {
        "Homem": ["Fubá", "Tostão", "Nono", "Alquimino", "Toupera", "Santo", "Vespasiano", "Coriolano", "Scipião", "Dúlio", "Tibério", "Radomir", "Piu", "Pomba", "Pintado", "Canhoto", "Pirão", "Anzol", "Patota", "Cumbuca"],
        "Mulher": ["Arenosa", "Mamona", "Cuca", "Emelda", "Noemi", "Vermelha", "Ardida", "Broa", "Pintada", "Ilabel", "Irene", "Lillibeth", "Naná", "Nirvana", "Teté", "Marilda", "Delfina", "Celestina", "Mirna", "Odete"],
        "Unissex": ["Açaí", "Cacá", "Nove", "Abelha", "Broa", "Garoa", "Tilápia", "Neon", "Acerola", "Sal", "Tonté", "Tizil", "Anú", "Formiga", "Dindin", "Pirauê", "Gal", "Sol", "Nanquim", "Tesourinha"],
        "Sobrenome": ["Cascais", "Campinazul", "Dourados", "Alagados", "Boagente", "Santos", "Salgado", "Dançante", "Corrente", "Queimada", "Estrela", "Queixada", "Curado", "Cervinho", "Cervão", "Campineiro", "Arqueiro", "Pontadelança", "Onze", "Lamaçal"]
    },
    "Musgueiro": {
        "Homem": ["Dombo", "Brimbul", "Gobulom", "Odobaldo", "Gremo", "Tototo", "Esporo", "Terracio", "Semente", "Micose", "Lonlom", "Odaíris", "Nyoma", "Cheirosa", "Oglom", "Omb", "Ximofo", "Soneca", "Otano", "Ferrugem"],
        "Mulher": ["Liqueno", "Bendiom", "Eblis", "Boloris", "Golim", "Guema", "Ivis", "Anaero", "Espiga", "Blibli", "Álmiscar", "Libibi", "Micélio", "Momba", "Milica", "Xirlimi", "Xodózi", "Ssivi", "Laranja", "Hifas"],
        "Unissex": ["Bilibom", "Blobu", "Guento", "Glob", "Tézin", "Greblim", "Azedim", "Penicilin", "Imbiuí", "Pólipo-roxo", "Lambó", "Marrombe", "Limimbi", "Olob", "Oop", "Lasão", "Smodron", "Tofa", "Tomumchá", "Birroso"],
        "Sobrenome": ["Casca-de-árvore", "Fungo-liso", "Umidade", "Samambaia", "Espumante", "Corcunda-suja", "Pé-suíno", "Barba-de-musgo", "Levedura", "Bolorento", "Dedo-mofado", "Pé-de-lama", "Caneca-de-espuma", "Verdinho", "Compostador", "Orelha-de-pau", "Probiótico", "Queijo-pequeno", "Cogu", "Galho-seco"]
    },
    "Mûr": {
        "Homem": ["Bagna", "Barcudel", "Blumf", "Biriba", "Caracoles", "Chimm", "Delgodan", "Dundum", "Eosvaldo", "Grumo", "Gilbinho", "Guiano", "Ilano", "Kungus", "Londus", "Lubbal", "Olpipo", "Pirilampo", "Rungel", "Wumpus"],
        "Mulher": ["Amendoim", "Canana", "Cherufi", "Dula", "Frutinha", "Gruga", "Hooool", "Malina", "Mogmo", "Melinha", "Munmil", "Munmun", "Netacla", "Orvalho", "Pailufi", "Pimpopuc", "Purun", "Risada", "Sasserpifi", "Wipsi"],
        "Unissex": ["Bonfrin", "Bisnaga", "Chanche", "Danlu", "Finis", "Gogol", "Hololo", "Lentidão", "Lumfris", "Mabmun", "Mungus", "Nemchance", "Ottem", "Ootem", "Piriperê", "Solsan", "Turio", "Undas", "Umpu", "Wolun"],
        "Sobrenome": ["Bola-de-catota", "Fala-molhado", "Troca-botas", "Espiga-verde", "Come-milho", "Luz-da-lua", "Atira-esterco", "Sobe-em-árvore", "Cutuca-porco", "Mergulha-fundo", "Sempre-faminto", "Magro-de-ruim", "Esnobe-do-brejo", "Beijo-azedo", "Pega-mariposa", "Pulmão-de-ouro", "Riso-alto", "Capim-queimado", "Cerca-brejo", "Barulho-no-mato"]
    }
}

MOD_ATRIBUTOS = (0, 0, 0, -3, -2, -2, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3)
CLASSES_FADAS = ["Bardo", "Guerreiro", "Caçador", "Mago", "Ladrão", "Encantador"]
CLASSES_MORTAIS = ["Bardo", "Guerreiro", "Caçador", "Mago", "Ladrão", "Clérigo", "Frade", "Cavaleiro"]

# ==========================================
# FUNÇÕES DO SISTEMA
# ==========================================
def rolar(qtd: int, faces: int) -> int:
    return sum(random.randint(1, faces) for _ in range(qtd))

def calc_mod(valor: int) -> int:
    return MOD_ATRIBUTOS[valor] if 0 <= valor <= 18 else 0

def format_mod(mod: int) -> str:
    return f"+{mod}" if mod > 0 else str(mod)

def gerar_atributos() -> Dict[str, int]:
    while True:
        attrs = {"FOR": rolar(3,6), "INT": rolar(3,6), "SAB": rolar(3,6), "DES": rolar(3,6), "CON": rolar(3,6), "CAR": rolar(3,6)}
        if sum(calc_mod(v) for v in attrs.values()) >= 0: return attrs

def gerar_nomes_formatados(parentesco: str) -> str:
    if parentesco == "Elfo":
        return f"- **Rústico:** {random.choice(NOMES['Elfo']['Rústico'])}\n- **Cortês:** {random.choice(NOMES['Elfo']['Cortês'])}"
    elif parentesco == "Cattus":
        return f"- {random.choice(NOMES['Cattus']['Primeiro Nome'])} {random.choice(NOMES['Cattus']['Sobrenome'])}"
    else:
        s = NOMES[parentesco]["Sobrenome"]
        return (f"- **Homem:** {random.choice(NOMES[parentesco]['Homem'])} {random.choice(s)}\n"
                f"- **Mulher:** {random.choice(NOMES[parentesco]['Mulher'])} {random.choice(s)}\n"
                f"- **Unissex:** {random.choice(NOMES[parentesco]['Unissex'])} {random.choice(s)}")

def gerar_equipamento(classe: str) -> dict:
    eq = {"armadura_nome": "Sem armadura", "ca": 10, "tem_escudo": False, "armas": [], "municao": []}
    classes_pesadas = {"Guerreiro", "Clérigo", "Cavaleiro"}
    classes_leves = {"Caçador", "Bardo", "Encantador", "Ladrão"}
    
    if classe in classes_pesadas:
        rol = rolar(1, 6)
        if rol == 1: eq["armadura_nome"] = "Couro"
        elif rol == 2: eq["armadura_nome"] = "Casca de árvore"
        elif rol == 3: eq["armadura_nome"] = "Cota de malha"
        elif rol == 4: eq["armadura_nome"] = "Pinha"
        elif rol == 5: eq["armadura_nome"] = "Escamas"
        else: eq["armadura_nome"] = "Placas"
        if rolar(1, 2) == 1: eq["tem_escudo"] = True
    elif classe in classes_leves:
        rol = rolar(1, 3)
        if rol == 1: eq["armadura_nome"] = "Sem armadura"
        elif rol == 2: eq["armadura_nome"] = "Couro"
        else: eq["armadura_nome"] = "Casca de árvore"
        if classe == "Caçador" and rolar(1, 2) == 1: eq["tem_escudo"] = True
            
    eq["ca"] = ARMADURAS[eq["armadura_nome"]]["ca"]
    if eq["tem_escudo"]: eq["ca"] += 1
        
    armas_pool = ["Cajado", "Adaga", "Funda", "Porrete"] if classe in {"Frade", "Mago"} else list(ARMAS.keys())
    eq["armas"] = random.sample(armas_pool, 2)
    
    for arma in eq["armas"]:
        if arma in ["Arco longo", "Arco curto"]: eq["municao"].append(("Flechas (aljava c/ 20)", 20))
        elif arma == "Besta": eq["municao"].append(("Setas (caixa c/ 20)", 20))
        elif arma == "Funda": eq["municao"].append(("Pedras de funda (20 pedras)", 100))
    return eq

def recomendar_classes(atributos: dict, classes_disp: list) -> list:
    maior_valor = max(atributos.values())
    melhores = [k for k, v in atributos.items() if v == maior_valor]
    return [c for c in classes_disp if any(atr in melhores for atr in CLASSES_INFO[c]["attr"])] or classes_disp

# ==========================================
# CONTROLE DE ESTADO STREAMLIT
# ==========================================
if "step" not in st.session_state:
    st.session_state.step = 1

def proximo_passo(): st.session_state.step += 1
def reiniciar():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.session_state.step = 1

# ==========================================
# UI DA APLICAÇÃO
# ==========================================
st.title("🌲 Floresta do Menir")
st.markdown("*Gerador OSR de Personagens - Rápido, Elegante e Pronto para a Aventura*")
st.divider()

if st.session_state.step == 1:
    st.subheader("Etapa 1: Assentamento Inicial")
    assentamento_escolhido = st.selectbox("Onde sua jornada começa?", list(ASSENTAMENTOS.keys()))
    
    if st.button("Rolar Demografia e Atributos", type="primary"):
        st.session_state.assentamento = assentamento_escolhido
        st.session_state.rolagem_demo = rolar(1, 20)
        st.session_state.attrs = gerar_atributos()
        proximo_passo()
        st.rerun()

elif st.session_state.step == 2:
    st.subheader("Etapa 2: Parentesco e Classe")
    
    # Processa parentescos permitidos
    opcoes_parentesco = []
    for limite, kin in ASSENTAMENTOS[st.session_state.assentamento]:
        opcoes_parentesco.append(kin)
        if st.session_state.rolagem_demo <= limite: break
            
    st.info(f"O dado demográfico de **{st.session_state.assentamento}** rolou **{st.session_state.rolagem_demo}**. Você pode escolher um dos parentescos abaixo:")
    
    col1, col2 = st.columns(2)
    with col1:
        parentesco = st.radio("Escolha seu Parentesco:", opcoes_parentesco)
    
    with col2:
        st.markdown("**Seus Atributos (Rolados):**")
        c1, c2, c3 = st.columns(3)
        attrs = st.session_state.attrs
        c1.metric("FOR", attrs["FOR"], format_mod(calc_mod(attrs["FOR"])))
        c2.metric("INT", attrs["INT"], format_mod(calc_mod(attrs["INT"])))
        c3.metric("SAB", attrs["SAB"], format_mod(calc_mod(attrs["SAB"])))
        c1.metric("DES", attrs["DES"], format_mod(calc_mod(attrs["DES"])))
        c2.metric("CON", attrs["CON"], format_mod(calc_mod(attrs["CON"])))
        c3.metric("CAR", attrs["CAR"], format_mod(calc_mod(attrs["CAR"])))

    # Processa Classes
    classes_disp = CLASSES_FADAS if parentesco in {"Elfo", "Cattus", "Mûr"} else CLASSES_MORTAIS
    classes_rec = recomendar_classes(attrs, classes_disp)
    
    def formatar_classe(c):
        return f"{c} (★ Recomendada)" if c in classes_rec else c

    classe = st.selectbox("Escolha sua Classe:", classes_disp, format_func=formatar_classe)
    
    if st.button("Finalizar Ficha", type="primary"):
        st.session_state.parentesco = parentesco
        st.session_state.classe = classe
        proximo_passo()
        st.rerun()

elif st.session_state.step == 3:
    # --- ROLAGENS FINAIS ---
    if "ficha_pronta" not in st.session_state:
        p = st.session_state.parentesco
        c = st.session_state.classe
        a = st.session_state.attrs
        
        st.session_state.alinhamento = random.choice(["Ordeiro", "Neutro"]) if c in {"Clérigo", "Frade"} else random.choice(["Ordeiro", "Neutro", "Caótico"])
        
        lim, signo_nome, signo_efeito = next(item for item in SIGNOS_LUNARES if rolar(1, 100) <= item[0])
        st.session_state.signo = f"{signo_nome} — {signo_efeito}"
        
        dv = CLASSES_INFO[c]["dv"]
        mod_con = calc_mod(a["CON"])
        st.session_state.pv = max(1, dv + mod_con)
        st.session_state.dv_str = f"1d{dv} {format_mod(mod_con)}"
        
        eq = gerar_equipamento(c)
        st.session_state.eq = eq
        
        ca_total = eq["ca"] + calc_mod(a["DES"])
        if p == "Méerme" and eq["armadura_nome"] in {"Sem armadura", "Couro"}: ca_total += 1
        st.session_state.ca_total = ca_total
        
        ouro = rolar(3, 6)
        itens_av = random.sample(ITENS_AVENTURA, 4)
        pacote_base = ["mochila (peso 80)", "6 rações perecíveis", "2 cantis", "6 tochas", "pederneira", "saco de dormir"]
        todos_equipamentos = pacote_base + [i.lower() for i in itens_av]
        str_equipamentos = ", ".join(todos_equipamentos[:-1]) + " e " + todos_equipamentos[-1] + "."
        
        peso_total = ARMADURAS[eq["armadura_nome"]]["peso"] + (100 if eq["tem_escudo"] else 0) + ouro + 80
        for arma in eq["armas"]: peso_total += ARMAS[arma]["peso"]
        for _, p_mun in eq["municao"]: peso_total += p_mun
            
        st.session_state.ouro = ouro
        st.session_state.str_equip = str_equipamentos
        st.session_state.peso_total = peso_total
        
        mod_int = calc_mod(a["INT"])
        linguas = LINGUAS_PARENTESCO[p][:]
        if mod_int > 0: linguas.extend(random.sample(LINGUAS_EXTRAS, min(mod_int, len(LINGUAS_EXTRAS))))
        st.session_state.linguas = linguas
        st.session_state.mod_int = mod_int
        
        st.session_state.ficha_pronta = True

    # --- UI DA FICHA ---
    st.success("Personagem gerado com sucesso!")
    
    with st.expander("📝 Opções de Nomes Gerados", expanded=True):
        st.markdown(gerar_nomes_formatados(st.session_state.parentesco))

    st.markdown("### Perfil do Personagem")
    col1, col2 = st.columns(2)
    col1.markdown(f"**Parentesco:** {st.session_state.parentesco}")
    col1.markdown(f"**Classe:** {st.session_state.classe}")
    col1.markdown(f"**Alinhamento:** {st.session_state.alinhamento}")
    col2.markdown(f"**Assentamento:** {st.session_state.assentamento}")
    col2.markdown(f"**Idiomas Extra:** {max(0, st.session_state.mod_int)}")
    col2.markdown(f"**Línguas Faladas:** {', '.join(st.session_state.linguas)}")
    st.markdown(f"**Signo da Lua:** {st.session_state.signo}")
    
    st.markdown("---")
    
    st.markdown("### Atributos e Combate")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    a = st.session_state.attrs
    c1.metric("FOR", a["FOR"], format_mod(calc_mod(a["FOR"])))
    c2.metric("INT", a["INT"], format_mod(calc_mod(a["INT"])))
    c3.metric("SAB", a["SAB"], format_mod(calc_mod(a["SAB"])))
    c4.metric("DES", a["DES"], format_mod(calc_mod(a["DES"])))
    c5.metric("CON", a["CON"], format_mod(calc_mod(a["CON"])))
    c6.metric("CAR", a["CAR"], format_mod(calc_mod(a["CAR"])))
    
    col_cb1, col_cb2, col_cb3 = st.columns(3)
    col_cb1.metric("PV Máximo", st.session_state.pv, st.session_state.dv_str, delta_color="off")
    col_cb2.metric("Classe de Armadura", st.session_state.ca_total, delta_color="off")
    col_cb3.metric("Ataque Base", CLASSES_INFO[st.session_state.classe]["ataque"], delta_color="off")
    
    res_mag = "+2" if st.session_state.parentesco in {"Elfo", "Cattus", "Mûr"} else "Nenhuma"
    st.caption(f"**Resistência à Magia:** {res_mag}")

    sv = SALVAGUARDAS[st.session_state.classe]
    st.markdown("##### Salvaguardas")
    sv1, sv2, sv3, sv4, sv5 = st.columns(5)
    sv1.markdown(f"**Morte:**\n## {sv[0]}")
    sv2.markdown(f"**Raio:**\n## {sv[1]}")
    sv3.markdown(f"**Paralisia:**\n## {sv[2]}")
    sv4.markdown(f"**Explosão:**\n## {sv[3]}")
    sv5.markdown(f"**Feitiço:**\n## {sv[4]}")
    
    st.markdown("---")
    
    st.markdown("### Inventário e Carga")
    eq = st.session_state.eq
    arm_nome = eq["armadura_nome"]
    arm_p = ARMADURAS[arm_nome]["peso"]
    arm_ca = ARMADURAS[arm_nome]["ca"]
    
    str_armadura = f"**{arm_nome}** (CA {arm_ca}, Peso {arm_p})"
    if eq["tem_escudo"]: str_armadura += " + **Escudo** (CA +1, Peso 100)"
    
    st.markdown(f"- **Armadura:** {str_armadura}")
    
    str_armas = []
    for arma in eq["armas"]:
        str_armas.append(f"**{arma}** (Dano {ARMAS[arma]['dano']}, Peso {ARMAS[arma]['peso']})")
    for n_mun, p_mun in eq["municao"]:
        str_armas.append(f"{n_mun} (Peso {p_mun})")
        
    st.markdown(f"- **Armas:** {', '.join(str_armas)}")
    st.markdown(f"- **Ouro Inicial:** {st.session_state.ouro} moedas (Peso {st.session_state.ouro})")
    
    # Parágrafo contínuo elegante e com quebra de linha nativa
    st.markdown(f"- **Equipamento:** {st.session_state.str_equip}")
    st.markdown(f"**📦 PESO TOTAL CARREGADO:** {st.session_state.peso_total}")
    
    st.divider()
    if st.button("🎲 Gerar Novo Personagem", type="secondary", use_container_width=True):
        reiniciar()
        st.rerun()
