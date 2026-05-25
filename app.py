import streamlit as st
from google import genai
import datetime
import time

# =========================================================================
# CONFIGURAÇÃO DE PÁGINA (Aparência)
# =========================================================================
st.set_page_config(
    page_title="Sincro App - Portal do Tempo",
    page_icon="🔮",
    layout="centered"
)

# Puxa a chave de API salva nos Secrets do Streamlit
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# =========================================================================
# 1. FUNÇÕES DE CÁLCULO (CÉREBRO MATEMÁTICO CORRIGIDO)
# =========================================================================
def calcular_dados_portais(nome, dia, mes, ano):
    """
    Realiza os cálculos exatos de confluência (Maia Oficial, Numerologia e Astrologia).
    """
    # 1.1 Astrologia (Signo) e Anjo Cabalístico
    signos = [
        ("Capricórnio", "Asariel"), ("Aquário", "Uriel"), ("Peixes", "Asariel"),
        ("Áries", "Samuel"), ("Touro", "Anael"), ("Gêmeos", "Rafael"),
        ("Câncer", "Gabriel"), ("Leão", "Miguel"), ("Virgem", "Rafael"),
        ("Libra", "Aniel"), ("Escorpião", "Azrael"), ("Sagitário", "Saquiel")
    ]
    datas_signos = [20, 19, 20, 20, 21, 21, 22, 23, 23, 23, 22, 21]
    
    idx = mes - 1 if dia <= datas_signos[mes - 1] else (mes % 12)
    signo, anjo = signos[idx]

    # 1.2 Numerologia: Caminho de Vida (Data)
    ano_calc = ano if ano != 0 else 2026
    str_data = f"{dia:02d}{mes:02d}{ano_calc}"
    soma_vida = sum(int(digito) for digito in str_data if digito.isdigit())
    
    while soma_vida > 9 and soma_vida not in [11, 22]:
        soma_vida = sum(int(d) for d in str(soma_vida))

    # 1.3 Numerologia: Expressão (Nome)
    tabela_pitagorica = {
        'A':1,'I':9,'J':1,'Q':8,'Y':7, 'B':2,'K':2,'R':9,'Z':8,
        'C':3,'L':3,'S':1, 'D':4,'M':4,'T':2, 'E':5,'N':5,'U':3,
        'F':6,'O':6,'V':4, 'G':7,'P':7,'W':5, 'H':8,'X':6
    }
    soma_nome = 0
    for letra in nome.upper():
        if letra in tabela_pitagorica:
            soma_nome += tabela_pitagorica[letra]
            
    while soma_nome > 9 and soma_nome not in [11, 22]:
        soma_nome = sum(int(d) for d in str(soma_nome))

    # 1.4 Sincronário Maia Corrigido (Sequência Arquetípica de José Argüelles)
    selos_maias = [
        "Dragão", "Vento", "Noite", "Semente", "Serpente", 
        "Enlaçador de Mundos", "Mão", "Estrela", "Lua", "Cachorro", 
        "Macaco", "Humano", "Caminhante do Céu", "Mago", "Águia", 
        "Guerreiro", "Terra", "Espelho", "Tormenta", "Sol"
    ]
    
    # Cálculo absoluto com base juliana simplificada para sincronia do Tzolkin
    yc = ano_calc - 1
    data_usuario = datetime.date(ano_calc, mes, dia)
    dia_do_ano = data_usuario.timetuple().tm_yday
    
    # Fórmula de posicionamento absoluto de dias na linha do tempo mística
    base_dias = (ano_calc * 365) + (yc // 4) - (yc // 100) + (yc // 400) + dia_do_ano
    
    # Alinhamento constante (Garante 22/03/1979 como KIN 248)
    kin_calculado = (base_dias + 214) % 260
    if kin_calculado == 0:
        kin_calculado = 260
        
    tom_calculado = kin_calculado % 13
    if tom_calculado == 0:
        tom_calculado = 13
        
    # Índice correspondente na matriz (0 a 19)
    selo_idx = (kin_calculado - 1) % 20
    selo_calculado = selos_maias[selo_idx]

    return {
        "kin": kin_calculado,
        "tom": tom_calculado,
        "selo": selo_calculado,
        "signo": signo,
        "anjo": anjo,
        "num_vida": soma_vida,
        "num_expressao": soma_nome
    }

# =========================================================================
# 2. MOTOR DO GEMINI (CHAMADAS INDIVIDUAIS SOB DEMANDA)
# =========================================================================
def chamar_gemini_ia(nome, dia, mes, ano, dados_calculados, idioma, tipo_leitura):
    """
    Envia os dados calculados para o Gemini com tratamento de erro exposto para diagnóstico.
    """
    time.sleep(2)  # Respiro protetor anti-bloqueio
    
    # Extração segura usando .get() para evitar KeyError
    kin = dados_calculados.get("kin", 1)
    tom = dados_calculados.get("tom", 1)
    selo = dados_calculados.get("selo", "Sol")
    signo = dados_calculados.get("signo", "Áries")
    anjo = dados_calculados.get("anjo", "Miguel")
    num_vida = dados_calculados.get("num_vida", 7)
    num_expressao = dados_calculados.get("num_expressao", 7)
    
    if tipo_leitura == "geral":
        prompt = f"Gere uma leitura de autoconhecimento geral profunda e magnética para {nome}, nascido em {dia}/{mes}/{'2026' if ano == 0 else ano}. Idioma: {idioma}. Dados: KIN {kin}, Tom {tom}, Selo {selo}, Signo {signo}, Anjo {anjo}, Caminho de Vida {num_vida}, Expressão {num_expressao}. Escreva de forma fluida e mística. Termine com a saudação tradicional 'In Lak'ech'."
    elif tipo_leitura == "vocacao":
        prompt = f"Gere uma análise focada em MISSÃO, PROPÓSITO E VOCAÇÃO PROFISSIONAL para {nome}. Idioma: {idioma}. Dados: KIN {kin}, Signo {signo}, Números {num_vida} e {num_expressao}. Revele talentos ocultos e caminhos de prosperidade baseados nessa frequência cósmica."
    elif tipo_leitura == "amor":
        prompt = f"Gere um alinhamento sobre AMOR, RELACIONAMENTOS E AFETIVIDADE para {nome}. Idioma: {idioma}. Dados: KIN {kin}, Signo {signo}, Anjo {anjo}, Caminho de Vida {num_vida}. Explique o comportamento afetivo, desafios e magnetismo de atração."

    try:
        client = genai.Client(api_key=API_KEY)
        resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return resposta.text
    except Exception as e:
        return f"🌌 Os portais de {tipo_leitura} estão temporariamente indisponíveis (Limite diário do Google atingido). Erro Técnico: {str(e)}"

# =========================================================================
# 3. INTERFACE VISUAL DO USUÁRIO (WEB APP)
# =========================================================================
st.title("🔮 Sincro App")
st.subheader("A Geometria Sagrada do Tempo")
st.markdown("> *In Lak'ech. Digite seu nome completo e data de nascimento. Prepare-se para espelhar sua alma no tempo...*")
st.markdown("---")

# Preserva os dados salvos entre as interações do navegador
if "dados_calculados" not in st.session_state:
    st.session_state.dados_calculados = None
    st.session_state.texto_geral = None

idioma_opcao = st.selectbox("🌐 Escolha seu idioma / Choose language", ["Português", "English", "Español"])
idioma_map = {"Português": "pt", "English": "en", "Español": "es"}
idioma = idioma_map[idioma_opcao]

nome_input = st.text_input("✨ Nome Completo:")

col1, col2, col3 = st.columns(3)
with col1:
    dia = st.number_input("📅 Dia de Nascimento", min_value=1, max_value=31, value=15)
with col2:
    mes = st.number_input("📅 Mês de Nascimento", min_value=1, max_value=12, value=6)
with col3:
    ano_input = st.number_input("📅 Ano (Deixe 0 se não souber)", min_value=0, max_value=2026, value=1995)

st.markdown("<br>", unsafe_allow_html=True)

# BOTÃO PRINCIPAL (Gera estritamente o conteúdo da primeira aba aberta)
if st.button("🔮 Ativar o Portal do Tempo", use_container_width=True):
    if not nome_input.strip():
        st.warning("Por favor, digite seu nome para abrir o portal.")
    elif not API_KEY:
        st.error("Configure a chave GEMINI_API_KEY nos Secrets do Streamlit.")
    else:
        with st.spinner("🌌 Sincronizando frequências cósmicas e gerando sua leitura gratuita..."):
            st.session_state.dados_calculados = calcular_dados_portais(nome_input, dia, mes, ano_input)
            st.session_state.texto_geral = chamar_gemini_ia(nome_input, dia, mes, ano_input, st.session_state.dados_calculados, idioma, "geral")
            st.success("✨ Alinhamento Concluído!")

# Exibição Condicional das Abas Inteligentes
if st.session_state.dados_calculados is not None:
    st.markdown("---")
    aba1, aba2, aba3 = st.tabs(["🔮 Portal Geral (Aberto)", "💼 Missão & Vocação", "💖 Confluência Amorosa"])
    
    with aba1:
        st.write(st.session_state.texto_geral)
        
    with aba2:
        st.markdown("### 🔒 Portal de Vocação & Prosperidade")
        st.info("Deseja destravar as previsões de carreira, finanças e caminhos de sucesso do seu KIN?")
        st.markdown("---")
        
        # Só consome requisição se clicar aqui (Simula fluxo após pagamento do Mercado Pago)
        if st.button("💳 Testar Desbloqueio: Gerar Missão & Vocação", key="btn_pay_voc"):
            with st.spinner("🔮 Conectando ao módulo premium..."):
                texto_premium_voc = chamar_gemini_ia(nome_input, dia, mes, ano_input, st.session_state.dados_calculados, idioma, "vocacao")
                st.write(texto_premium_voc)
                
    with aba3:
        st.markdown("### 🔒 Portal do Magnetismo Afetivo")
        st.info("Descubra os mistérios das suas conexões amorosas, carmas e compatibilidades de alma.")
        st.markdown("---")
        
        if st.button("💳 Testar Desbloqueio: Gerar Confluência Amorosa", key="btn_pay_amo"):
            with st.spinner("🔮 Conectando ao módulo premium..."):
                texto_premium_amo = chamar_gemini_ia(nome_input, dia, mes, ano_input, st.session_state.dados_calculados, idioma, "amor")
                st.write(texto_premium_amo)
                
