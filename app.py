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
# 1. FUNÇÕES DE CÁLCULO (CÉREBRO MATEMÁTICO)
# =========================================================================
def calcular_dados_portais(nome, dia, mes, ano):
    """
    Realiza todos os cálculos matemáticos de confluência (Maia, Numerologia e Astrologia).
    """
    # 1.1 Astrologia (Signo) e Anjo Cabalístico (Simplificado para o motor)
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
        'A':1,'I':9,'J':1,'Q':8,'Y':7,
        'B':2,'K':2,'R':9,'Z':8,
        'C':3,'L':3,'S':1,
        'D':4,'M':4,'T':2,
        'E':5,'N':5,'U':3,
        'F':6,'O':6,'V':4,
        'G':7,'P':7,'W':5,
        'H':8,        'X':6
    }
    soma_nome = 0
    for letra in nome.upper():
        if letra in tabela_pitagorica:
            soma_nome += tabela_pitagorica[letra]
            
    while soma_nome > 9 and soma_nome not in [11, 22]:
        soma_nome = sum(int(d) for d in str(soma_nome))

    # 1.4 Sincronário Maia (Cálculo Base de KIN Dinâmico)
    selos = [
        "Sol", "Dragão", "Vento", "Noite", "Semente", "Serpente", "Enlaçador de Mundos",
        "Mão", "Estrela", "Lua", "Cachorro", "Macaco", "Humano", "Caminhante do Céu",
        "Mago", "Águia", "Guerreiro", "Terra", "Espelho", "Tormenta"
    ]
    
    # Data âncora fixa: 23 de Abril de 2026 = KIN 115
    data_usuario = datetime.date(ano_calc, mes, dia)
    data_ancora = datetime.date(2026, 4, 23)
    diferenca_dias = (data_usuario - data_ancora).days
    
    kin_calculado = (115 + diferenca_dias) % 260
    if kin_calculado <= 0:
        kin_calculado += 260
        
    tom_calculado = kin_calculado % 13
    if tom_calculado == 0:
        tom_calculado = 13
        
    selo_calculado = selos[kin_calculado % 20]

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
# 2. INTEGRAÇÃO INTELIGENTE COM GEMINI (GERAÇÃO DOS 3 TIPOS DE TEXTO)
# =========================================================================
def chamar_gemini_ia(nome, dia, mes, ano, dados_calculados, idioma, tipo_leitura):
    """
    Envia os dados calculados para o Gemini e gera as leituras com respiro anti-bloqueio.
    """
    # Respiro crucial de 2 segundos para o Google não bloquear requisições em sequência
    time.sleep(2)
    
    # Extração ultra-segura contra KeyError
    kin = dados_calculados.get("kin", 1)
    tom = dados_calculados.get("tom", 1)
    selo = dados_calculados.get("selo", "Sol")
    signo = dados_calculados.get("signo", "Áries")
    anjo = dados_calculados.get("anjo", "Miguel")
    num_vida = dados_calculados.get("num_vida", 7)
    num_expressao = dados_calculados.get("num_expressao", 7)
    
    if tipo_leitura == "geral":
        prompt = f"""
        Você é um mestre xamã maia, astrólogo cabalístico e numerólogo antigo.
        Gere uma leitura de autoconhecimento profunda e magnética para {nome}, nascido em {dia}/{mes}/{'2026' if ano == 0 else ano}.
        Idioma da resposta: {idioma}.
        
        Dados do perfil:
        - Sincronário Maia: KIN {kin}, Tom {tom}, Selo Solar {selo}.
        - Astrologia & Cabala: Signo de {signo} regido pelo Anjo Cabalístico {anjo}.
        - Numerologia: Caminho de Vida {num_vida} e Número de Expressão {num_expressao}.
        
        Esta é a LEITURA GERAL DE ORIGEM. Foque na essência da alma, na energia do tempo no dia em que nasceu. Escreva de forma fluida, misteriosa, e acolhedora. Termine com a saudação maia tradicional 'In Lak'ech'. Não use tópicos simples.
        """
        
    elif tipo_leitura == "vocacao":
        prompt = f"""
        Você é um mentor de carreira holístico e estrategista de destino.
        Gere uma análise focada em MISSÃO, PROPÓSITO E VOCAÇÃO PROFISSIONAL para {nome}.
        Idioma da resposta: {idioma}.
        
        Dados do perfil: KIN {kin}, Signo {signo}, Números {num_vida} e {num_expressao}.
        
        Esta é a aba premium de TRABALHO & VOCAÇÃO. Revele quais os talentos ocultos e caminhos de prosperidade financeira. Seja prático e profundo.
        """
        
    elif tipo_leitura == "amor":
        prompt = f"""
        Você é um conselheiro afetivo ancestral e terapeuta de alma.
        Gere um alinhamento sobre AMOR, RELACIONAMENTOS E AFETIVIDADE para {nome}.
        Idioma da resposta: {idioma}.
        
        Dados do perfil: KIN {kin}, Signo {signo}, Anjo {anjo}, Caminho de Vida {num_vida}.
        
        Esta é a aba premium de RELACIONAMENTOS & MAGNETISMO AFETIVO. Explique como essa pessoa se comporta no amor e o que sua alma busca. Seja poético e magnético.
        """

    # Bloco de segurança duplo (Try/Except) contra instabilidades da API
    try:
        client = genai.Client(api_key=API_KEY)
        resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return resposta.text
    except Exception:
        try:
            # Se falhar de primeira, espera 4 segundos extras e tenta novamente
            time.sleep(4)
            client = genai.Client(api_key=API_KEY)
            resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            return resposta.text
        except Exception:
            return f"🌌 Os portais de {tipo_leitura} estão temporariamente congestionados devido ao alto alinhamento estelar. Por favor, clique novamente no botão em alguns instantes."

# =========================================================================
# 3. INTERFACE VISUAL DO USUÁRIO (WEB APP)
# =========================================================================
st.title("🔮 Sincro App")
st.subheader("A Geometria Sagrada do Tempo")
st.markdown("> *In Lak'ech. Digite seu nome completo e data de nascimento. Prepare-se para espelhar sua alma no tempo...*")
st.markdown("---")

# Seleção de Idioma de forma elegante
idioma_opcao = st.selectbox("🌐 Escolha seu idioma / Choose your language", ["Português", "English", "Español"])
idioma_map = {"Português": "pt", "English": "en", "Español": "es"}
idioma = idioma_map[idioma_opcao]

# Campos de Entrada do Usuário
nome_input = st.text_input("✨ Nome Completo:")

col1, col2, col3 = st.columns(3)
with col1:
    dia = st.number_input("📅 Dia de Nascimento", min_value=1, max_value=31, value=15)
with col2:
    mes = st.number_input("📅 Mês de Nascimento", min_value=1, max_value=12, value=6)
with col3:
    ano_input = st.number_input("📅 Ano (Deixe 0 se não souber)", min_value=0, max_value=2026, value=1995)

st.markdown("<br>", unsafe_allow_html=True)

# Botão Único com o texto novo de impacto místico
if st.button("🔮 Ativar o Portal do Tempo", use_container_width=True):
    if not nome_input.strip():
        st.warning("Por favor, digite seu nome para abrir o portal.")
    elif not API_KEY:
        st.error("Erro: A chave GEMINI_API_KEY não foi configurada nos Secrets do Streamlit.")
    else:
        with st.spinner("🌌 Sincronizando frequências cósmicas e abrindo os portais..."):
            
            # Executa os cálculos matemáticos internamente
            dados = calcular_dados_portais(nome_input, dia, mes, ano_input)
            
            # Dispara as 3 chamadas controladas ao Gemini
            texto_geral = chamar_gemini_ia(nome_input, dia, mes, ano_input, dados, idioma, "geral")
            texto_vocacao = chamar_gemini_ia(nome_input, dia, mes, ano_input, dados, idioma, "vocacao")
            texto_amor = chamar_gemini_ia(nome_input, dia, mes, ano_input, dados, idioma, "amor")
            
            st.success("✨ Alinhamento Concluído com Sucesso!")
            st.markdown("---")
            
            # Sistema de Abas Estratégico Comercial
            aba1, aba2, aba3 = st.tabs(["🔮 Portal Geral (Aberto)", "💼 Missão & Vocação", "💖 Confluência Amorosa"])
            
            with aba1:
                st.write(texto_geral)
                
            with aba2:
                st.markdown("### 🔒 Portal de Vocação & Prosperidade")
                st.info("Deseja destravar as previsões de carreira, finanças e caminhos de sucesso do seu KIN?")
                st.markdown("---")
                # Spoiler controlado do texto gerado
                st.write(f"*{texto_vocacao[:250]}...*")
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("💳 Desbloquear Portal de Vocação por R$ 29,90", key="btn_pay_voc")
                
            with aba3:
                st.markdown("### 🔒 Portal do Magnetismo Afetivo")
                st.info("Descubra os mistérios das suas conexões amorosas, carmas e compatibilidades de alma.")
                st.markdown("---")
                # Spoiler controlado do texto gerado
                st.write(f"*{texto_amor[:250]}...*")
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("💳 Desbloquear Portal do Amor por R$ 29,90", key="btn_pay_amo")
