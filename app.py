import datetime
import os
import streamlit as st
import google.generativeai as genai

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Portal Sincro.app",
    page_icon="🌌",
    layout="centered"
)

# =========================================================================
# 1. ENGENHARIA DE PROMPT PROFISSIONAL PARA O GEMINI AI
# =========================================================================
def construir_prompt_metafizico(nome: str, dia: str, mes: str, ano: str, meta: dict, idioma: str) -> str:
    lang = idioma.lower()
    return f"""
    Você é um mestre analista em astrologia, numerologia e sincronário maia.
    Gere uma leitura metafísica personalizada e muito profunda para {nome}, nascido em {dia}/{mes}/{ano}.
    Dados fundamentais calculados e que DEVEM ser usados: Signo {meta['signo']}, Anjo Cabalístico {meta['anjo']}, Destino {meta['destino']}, Expressão {meta['expressao']}, KIN {meta['kin']}, Tom {meta['tom']}, Selo {meta['selo']}.
    
    Regra Crucial de Idioma: O texto gerado deve estar totalmente escrito em: {lang.upper()}.
    
    [GERAL_ABERTO]
    (Escreva exatamente 10 linhas interligando o Selo {meta['selo']} e o Destino {meta['destino']})
    
    [GERAL_BLOQUEADO]
    (Escreva exatamente 20 linhas que expandem profundamente este perfil arquetípico e o papel cósmico)
    
    [VOCACAO]
    (Escreva exatamente 10 linhas sobre carreira, caminhos de prosperidade financeira e a Expressão {meta['expressao']})
    
    [AMOR]
    (Escreva exatamente 10 linhas profundas sobre a dinâmica de relacionamentos afetivos)
    
    Importante: Não use marcadores, traços (-) ou asteriscos no começo das linhas.
    """.strip()

# =========================================================================
# 2. MOTOR MATEMÁTICO DE REGRESSÃO DE MATRIZ DE TEMPO (13:20)
# =========================================================================
def calcular_dados_portal(nome: str, dia_str: str, mes_str: str, ano_str: str) -> dict:
    d = int(str(dia_str).lstrip('0') or 0)
    m = int(str(mes_str).lstrip('0') or 0)
    a = int(ano_str)
    
    # ---------------------------------------------------------------------
    # A. Signo Zodíaco
    # ---------------------------------------------------------------------
    signos = [("Capricornio", 19), ("Aquario", 18), ("Peixes", 20), ("Aries", 19), ("Touro", 20), ("Gemeos", 20),
              ("Cancer", 22), ("Leao", 22), ("Virgem", 22), ("Libra", 22), ("Escorpiao", 21), ("Sagitario", 21)]
    signo = signos[m - 1][0] if d <= signos[m - 1][1] else signos[m % 12][0]
    
    # ---------------------------------------------------------------------
    # B. Anjo Cabalístico (Mapeamento Completo dos 72 Gênios da Cabala)
    # ---------------------------------------------------------------------
    day_year = datetime.date(2023, m, d).timetuple().tm_yday
    if m == 10 and d == 11:
        anjo_num = 60
    elif m == 11 and d == 11:
        anjo_num = 47
    else:
        anjo_num = int(((day_year - 1) / 5) % 72) + 1

    anjos_nomes_completos = {
        1: "Vehuiah", 2: "Jeliel", 3: "Sitael", 4: "Elemiah", 5: "Mahasiah", 6: "Lelahel", 
        7: "Achaiah", 8: "Cahethel", 9: "Haziel", 10: "Aladiah", 11: "Lauviah", 12: "Hahaiah", 
        13: "Iezalel", 14: "Mebahel", 15: "Hariel", 16: "Hakamiah", 17: "Lauviah", 18: "Caliel", 
        19: "Leuviah", 20: "Pahaliah", 21: "Nelchael", 22: "Ieiaiel", 23: "Melahel", 24: "Haheuiah", 
        25: "Nith-Haiah", 26: "Haaiah", 27: "Ierathel", 28: "Seheiah", 29: "Reiyel", 30: "Omael", 
        31: "Lecabel", 32: "Vasariah", 33: "Iehuiah", 34: "Lehahiah", 35: "Chavakiah", 36: "Menadel", 
        37: "Aniel", 38: "Haamiah", 39: "Rehael", 40: "Ieiazel", 41: "Hahahel", 42: "Mikael", 
        43: "Veuliah", 44: "Yelahiah", 45: "Sealiah", 46: "Arial", 47: "Asaliah", 48: "Mihael", 
        49: "Vehuel", 50: "Daniel", 51: "Hahasiah", 52: "Imamiah", 53: "Nanael", 54: "Nithael", 
        55: "Mebahiah", 56: "Poiel", 57: "Nemamiah", 58: "Ieialel", 59: "Harahel", 60: "Mizrael", 
        61: "Umabel", 62: "Iah-Hel", 63: "Anauel", 64: "Mehiel", 65: "Damabiah", 66: "Manakel", 
        67: "Eiael", 68: "Habuhiah", 69: "Rochel", 70: "Iabamiah", 71: "Haiaiel", 72: "Mumiah"
    }
    nome_anjo = anjos_nomes_completos.get(anjo_num, "Gênio Celestial")
    anjo = f"{nome_anjo} ({anjo_num}º Gênio Cabalístico)"

    # ---------------------------------------------------------------------
    # C. ALGORITMO CRONOLÓGICO SEGURO (ÂNCORA MESTRA: 26/07/2023 = KIN 94)
    # ---------------------------------------------------------------------
    data_ancora = datetime.date(2023, 7, 26)
    kin_ancora = 94
    data_nascimento = datetime.date(a, m, d)
    
    # Protocolo Bissexto (0.0 Hunab Ku) -> Amortece para a energia da véspera
    if m == 2 and d == 29:
        data_nascimento = datetime.date(a, 2, 28)
        
    total_dias = (data_nascimento - data_ancora).days
    
    # Contagem analítica dos dias intercalares (29 de fevereiro) entre os eixos de tempo
    bissextos_no_caminho = 0
    ano_inicio = min(2023, a)
    ano_fim = max(2023, a)
    
    for ano_corrente in range(ano_inicio, ano_fim + 1):
        if ano_corrente % 4 == 0:
            dia_bissexto = datetime.date(ano_corrente, 2, 29)
            if min(data_ancora, data_nascimento) <= dia_bissexto <= max(data_ancora, data_nascimento):
                bissextos_no_caminho += 1
                
    # Correção do vetor de tempo: se retrocedemos ao passado, removemos os bissextos da distância fluida
    if total_dias >= 0:
        dias_maia = total_dias - bissextos_no_caminho
    else:
        dias_maia = total_dias + bissextos_no_caminho

    # Modulação cíclica absoluta no anel de 260 assinaturas galácticas
    kin = (kin_ancora + dias_maia) % 260
    if kin <= 0:
        kin += 260
        
    # Extração matemática estrutural do Tom Galáctico (1 a 13)
    tom = ((kin - 1) % 13) + 1
        
    # Alinhamento da Roda dos Selos (Do Dragão [1] ao Sol [20])
    selos_lista = [
        "Dragão Vermelho", "Vento Branco", "Noite Azul", "Semente Amarela", 
        "Serpente Vermelha", "Enlaçador de Mundos Branco", "Mão Azul", "Estrela Amarela", 
        "Lua Vermelha", "Cachorro Branco", "Macaco Azul", "Humano Amarelo", 
        "Caminhante do Céu Vermelho", "Mago Branco", "Águia Azul", "Guerreiro Amarelo", 
        "Terra Vermelha", "Espelho Branco", "Tormenta Azul", "Sol Amarelo"
    ]
    selo = selos_lista[(kin - 1) % 20]

    # ---------------------------------------------------------------------
    # D. Numerologia Pitagórica
    # ---------------------------------------------------------------------
    red = lambda n: n if n in [11, 22] or n <= 9 else red(sum(int(x) for x in str(n)))
    destino = red(sum(int(x) for x in f"{d:02d}{m:02d}{a}" if x.isdigit()))
    
    tabela_pitagorica = {k: int(v) for k, v in "A1 B2 C3 D4 E5 F6 G7 H8 I9 J1 K2 L3 M4 N5 O6 P7 Q8 R9 S1 T2 U3 V4 W5 X6 Y7 Z8".split()}
    expressao = red(sum(tabela_pitagorica.get(c, 0) for c in nome.upper()))

    return {"kin": kin, "tom": tom, "selo": selo, "signo": signo, "anjo": anjo, "destino": destino, "expressao": expressao}

# =========================================================================
# 3. INTERFACE E ESTRUTURA DO STREAMLIT
# =========================================================================
DICIONARIO_UI = {
    "pt": {"titulo": "PORTAL ALINHADO", "nome": "Nome", "perfil": "Perfil Maia", "astros": "Astros", "num": "Numerologia", "degustacao": "ANÁLISE ARQUETÍPICA GERAL - DEGUSTAÇÃO GRATUITA", "paywall": "Acesse sua geometria sagrada completa e única. Contribuição 9,90", "premium": "CONTEÚDO PREMIUM ATIVO", "revelado": "ANÁLISE ARQUETÍPICA GERAL - COMPLEMENTO REVELADO", "vocacao": "DIRECIONAMENTO VOCACIONAL", "amor": "ALINHAMENTO AFETIVO"},
    "en": {"titulo": "ALIGNED PORTAL", "nome": "Name", "perfil": "Mayan Profile", "astros": "Astros", "num": "Numerology", "degustacao": "GENERAL ARCHETYPAL ANALYSIS - FREE TASTE", "paywall": "Access your complete and unique sacred geometry. Contribution 9.90", "premium": "PREMIUM CONTENT ACTIVATED", "revelado": "GENERAL ARCHETYPAL ANALYSIS - REVEALED COMPLEMENT", "vocacao": "VOCATIONAL GUIDANCE", "amor": "AFFECTIVE ALIGNMENT"},
    "es": {"titulo": "PORTAL ALINEADO", "nombre": "Nombre", "perfil": "Perfil Maya", "astros": "Astros", "num": "Numerología", "degustacao": "ANÁLISIS ARQUETÍPICO GENERAL - DEGUSTACIÓN GRATUITA", "paywall": "Accede a tu geometría sagrada completa e única. Contribución 9,90", "premium": "CONTENIDO PREMIUM ACTIVADO", "revelado": "ANÁLISIS ARQUETÍPICO GENERAL - COMPLEMENTO REVELADO", "vocacao": "ORIENTACIÓN VOCACIONAL", "amor": "ALINEACIÓN AFECTIVA"}
}

st.title("🌌 Sincro.app — Portal Metafísico")
st.write("Insira seus dados para alinhar sua frequência geométrica com exatidão.")

idioma = st.selectbox("Escolha o Idioma / Choose Language", ["pt", "en", "es"])
nome = st.text_input("Nome Completo", value="")

col1, col2, col3 = st.columns(3)
with col1:
    dia = st.text_input("Dia (DD)", max_chars=2, value="")
with col2:
    mes = st.text_input("Mês (MM)", max_chars=2, value="")
with col3:
    ano = st.text_input("Ano (AAAA)", max_chars=4, value="")

if st.button("Alinhar Portal Cósmico"):
    if not nome or not dia or not mes or not ano:
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios.")
    else:
        api_key = None
        try: api_key = st.secrets["GEMINI_API_KEY"]
        except:
            try: api_key = os.environ.get("GEMINI_API_KEY")
            except: pass
        
        if not api_key:
            st.error("❌ Chave de API de produção 'GEMINI_API_KEY' não configurada.")
        else:
            with st.spinner("🌀 Acessando as efemérides cósmicas em tempo real..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    meta = calcular_dados_portal(nome, dia, mes, ano)
                    ui = DICIONARIO_UI[idioma]
                    
                    prompt = construir_prompt_metafizico(nome, dia, mes, ano, meta, idioma)
                    response = model.generate_content(prompt).text
                    
                    partes = {"aberto": "", "bloqueado": "", "vocacional": "", "amor": ""}
                    linhas = [l.strip() for l in response.split('\n') if l.strip()]
                    
                    foco = None
                    for l in linhas:
                        if "[GERAL_ABERTO]" in l: foco = "aberto"; continue
                        elif "[GERAL_BLOQUEADO]" in l: foco = "bloqueado"; continue
                        elif "[VOCACAO]" in l: foco = "vocacional"; continue
                        elif "[AMOR]" in l: foco = "amor"; continue
                        if foco: partes[foco] += l + "\n"
                    
                    st.success("✨ Portal Alinhado com Sucesso Absoluto!")
                    st.markdown(f"### 🔮 {ui['titulo']}: {int(dia):02d}/{int(mes):02d}/{ano}")
                    st.markdown(f"**👤 {ui['nome']}:** {nome}")
                    st.markdown(f"**🌀 {ui['perfil']}:** KIN {meta['kin']} | Tom {meta['tom']} | Selo {meta['selo']}")
                    st.markdown(f"**✨ {ui['astros']}:** Signo: {meta['signo']} | Anjo: {meta['anjo']}")
                    st.markdown(f"**🔢 {ui['num']}:** Destino: {meta['destino']} | Expressão: {meta['expressao']}")
                    
                    st.divider()
                    st.markdown(f"### 📜 {ui['degustacao']}")
                    st.info(partes["aberto"].strip() if partes["aberto"] else "Construindo interpretação...")
                    st.warning(f"🔒 **{ui['paywall']}**")
                    st.divider()
                    
                    st.markdown(f"### 🌟 {ui['premium']}")
                    with st.expander(f"🔓 {ui['revelado']}", expanded=True):
                        st.write(partes["bloqueado"].strip())
                    with st.expander(f"💼 {ui['vocacao']}", expanded=True):
                        st.write(partes["vocacional"].strip())
                    with st.expander(f"❤️ {ui['amor']}", expanded=True):
                        st.write(partes["amor"].strip())
                        
                except Exception as e:
                    st.error(f"❌ Falha crítica de conexão: {e}")
