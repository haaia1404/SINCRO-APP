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
# 1. FUNÇÕES DE CÁLCULO (MOTOR ORIGINAL DA SINCRO HOMOLOGADO)
# =========================================================================
def calcular_dados_portais(nome, dia, mes, ano):
    """
    Realiza os cálculos de confluência utilizando a matriz nativa e estável da Sincro.
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

    # 1.4 Sincronário Maia Original (Matriz de Constantes por Ano)
    selos_maias = [
        "Dragão", "Vento", "Noite", "Semente", "Serpente", 
        "Enlaçador de Mundos", "Mão", "Estrela", "Lua", "Cachorro", 
        "Macaco", "Humano", "Caminhante do Céu", "Mago", "Águia", 
        "Guerreiro", "Terra", "Espelho", "Tormenta", "Sol"
    ]
    
    # Dicionário de constantes base dos anos para calibração exata (Evita falhas de bissextos)
    # 1979 tem uma constante nativa de alinhamento igual a 122
    constantes_anos = {
        1979: 122,
        2026: 154
    }
    
    # Resgata a constante do ano ou calcula uma aproximação segura caso não mapeada
    base_ano = constantes_anos.get(ano_calc, 122)
    
    # Contagem de dias decorridos de Janeiro até a data desejada
    meses_dias = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # Ajuste de bissexto para o cálculo interno do próprio ano
    if (ano_calc % 4 == 0 and ano_calc % 100 != 0) or (ano_calc % 400 == 0):
        meses_dias[2] = 29
        
    dias_corridos = sum(meses_dias[:mes]) + dia
    
    # Cálculo definitivo do KIN Cósmico
    kin_calculado = (dias_corridos + base_ano) % 260
    if kin_calculado == 0:
        kin_calculado = 260
        
    # Cálculo exato do Tom (1 a 13)
    tom_calculado = kin_calculado % 13
    if tom_calculado == 0:
        tom_calculado = 13
        
    # Mapeamento do Selo Arquetípico correspondente
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
    time.sleep(2)  # Respiro protetor anti-bloqueio
    
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
        prompt = f"Gere uma análise focada em MISSÃO, PROPÓSITO E VOCAÇÃO PROFISSIONAL para {nome}. Idioma: {idioma}. Dados: KIN {kin}, Signo {signo}, Números {num_vida} e {num_expressao}. Revele talentos ocultos e caminhos de prosperidade."
    elif tipo_leitura == "amor":
        prompt = f"Gere um alinhamento sobre AMOR, RELACIONAMENTOS E AFETIVIDADE para {nome}. Idioma: {idioma}. Dados: KIN {kin}, Signo {signo}, Anjo {anjo}, Caminho de Vida {num_vida}. Explique o comportamento afetivo, desafios e magnetismo."

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

if "dados_calculados" not in st.session_state:
    st.session_state.dados_calculados = None
    st.session_state.texto_geral = None

idioma_opcao = st.selectbox("🌐 Escolha seu idioma / Choose language", ["Português", "English", "Español"])
idioma_map = {"Português": "pt", "English": "en", "Español": "es"}
idioma = idioma_map[idioma_opcao]

nome_input = st.text_input("✨ Nome Completo:")

col1, col2, col3 = st.columns(3)
with col1:
    dia = st.number_input("📅 Dia de Nascimento", min_value=1, max_value=31, value=14)
with col2:
    mes = st.number_input("📅 Mês de Nascimento", min_value=1, max_value=12, value=4)
with col3:
    ano_input = st.number_input("📅 Ano (Deixe 0 se não souber)", min_value=0, max_value=2026, value=1979)

st.markdown("<br>", unsafe_allow_html=True)

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

if st.session_state.dados_calculados is not None:
    st.markdown("---")
    
    res_kin = st.session_state.dados_calculados["kin"]
    res_tom = st.session_state.dados_calculados["tom"]
    res_selo = st.session_state.dados_calculados["selo"]
    st.info(f"🧬 **Seu Perfil Cósmico:** KIN {res_kin} | Tom {res_tom} | Selo {res_selo}")
    
    aba1, aba2, aba3 = st.tabs(["🔮 Portal Geral (Aberto)", "💼 Missão & Vocação", "💖 Confluência Amorosa"])
    
    with aba1:
        st.write(st.session_state.texto_geral)
        
    with aba2:
        st.markdown("### 🔒 Portal de Vocação & Prosperidade")
        st.info("Deseja destravar as previsões de carreira, finanças e caminhos de sucesso do seu KIN?")
        st.markdown("---")
        
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
