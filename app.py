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
# 2. MOTORES MATEMÁTICOS CONCEITUAIS (CALIBRADOS E HOMOLOGADOS)
# =========================================================================

def obter_anjo_cabalistico(dia: int, mes: int) -> str:
    tabela_anjos = [
        {"nome": "Vehuiah", "num": 1, "inicio": (20, 3), "fim": (24, 3)},
        {"nome": "Jeliel", "num": 2, "inicio": (25, 3), "fim": (29, 3)},
        {"nome": "Sitael", "num": 3, "inicio": (30, 3), "fim": (3, 4)},
        {"nome": "Elemiah", "num": 4, "inicio": (4, 4), "fim": (8, 4)},
        {"nome": "Mahasiah", "num": 5, "inicio": (9, 4), "fim": (13, 4)},
        {"nome": "Haaiah", "num": 26, "inicio": (14, 4), "fim": (18, 4)}, 
        {"nome": "Achaiah", "num": 7, "inicio": (19, 4), "fim": (23, 4)},
        {"nome": "Cahethel", "num": 8, "inicio": (24, 4), "fim": (28, 4)},
        {"nome": "Haziel", "num": 9, "inicio": (29, 4), "fim": (3, 5)},
        {"nome": "Aladiah", "num": 10, "inicio": (4, 5), "fim": (8, 5)},
        {"nome": "Lauviah", "num": 11, "inicio": (9, 5), "fim": (13, 5)},
        {"nome": "Hahaiah", "num": 12, "inicio": (14, 5), "fim": (18, 5)},
        {"nome": "Iezalel", "num": 13, "inicio": (19, 5), "fim": (23, 5)},
        {"nome": "Mebahel", "num": 14, "inicio": (24, 5), "fim": (28, 5)},
        {"nome": "Hariel", "num": 15, "inicio": (29, 5), "fim": (2, 6)},
        {"nome": "Hakamiah", "num": 16, "inicio": (3, 6), "fim": (7, 6)},
        {"nome": "Lauviah", "num": 17, "inicio": (8, 6), "fim": (12, 6)},
        {"nome": "Caliel", "num": 18, "inicio": (13, 6), "fim": (17, 6)},
        {"nome": "Leuviah", "num": 19, "inicio": (18, 6), "fim": (22, 6)},
        {"nome": "Pahaliah", "num": 20, "inicio": (23, 6), "fim": (27, 6)},
        {"nome": "Nelchael", "num": 21, "inicio": (28, 6), "fim": (2, 7)},
        {"nome": "Yeiayel", "num": 22, "inicio": (3, 7), "fim": (7, 7)},
        {"nome": "Melahel", "num": 23, "inicio": (8, 7), "fim": (12, 7)},
        {"nome": "Haheuiah", "num": 24, "inicio": (13, 7), "fim": (17, 7)},
        {"nome": "Nith-Haiah", "num": 25, "inicio": (18, 7), "fim": (22, 7)},
        {"nome": "Lelahel", "num": 6, "inicio": (23, 7), "fim": (27, 7)}, 
        {"nome": "Yerathel", "num": 27, "inicio": (28, 7), "fim": (1, 8)},
        {"nome": "Seheiah", "num": 28, "inicio": (2, 8), "fim": (6, 8)},
        {"nome": "Reyiel", "num": 29, "inicio": (7, 8), "fim": (12, 8)},
        {"nome": "Omael", "num": 30, "inicio": (13, 8), "fim": (17, 8)},
        {"nome": "Lecabel", "num": 31, "inicio": (18, 8), "fim": (23, 8)},
        {"nome": "Vasariah", "num": 32, "inicio": (24, 8), "fim": (28, 8)},
        {"nome": "Yehuiah", "num": 33, "inicio": (29, 8), "fim": (2, 9)},
        {"nome": "Lehahiah", "num": 34, "inicio": (3, 9), "fim": (7, 9)},
        {"nome": "Chavakhiah", "num": 35, "inicio": (8, 9), "fim": (12, 9)},
        {"nome": "Menadel", "num": 36, "inicio": (13, 9), "fim": (17, 9)},
        {"nome": "Aniel", "num": 37, "inicio": (18, 9), "fim": (22, 9)},
        {"nome": "Haamiah", "num": 38, "inicio": (23, 9), "fim": (27, 9)},
        {"nome": "Rehael", "num": 39, "inicio": (28, 9), "fim": (2, 10)},
        {"nome": "Ieiazel", "num": 40, "inicio": (3, 10), "fim": (7, 10)},
        {"nome": "Hahahel", "num": 41, "inicio": (8, 10), "fim": (12, 10)},
        {"nome": "Mikael", "num": 42, "inicio": (13, 10), "fim": (17, 10)},
        {"nome": "Veuliah", "num": 43, "inicio": (18, 10), "fim": (22, 10)},
        {"nome": "Yelaiah", "num": 44, "inicio": (23, 10), "fim": (27, 10)},
        {"nome": "Sealiah", "num": 45, "inicio": (28, 10), "fim": (1, 11)},
        {"nome": "Ariel", "num": 46, "inicio": (2, 11), "fim": (6, 11)},
        {"nome": "Asaliah", "num": 47, "inicio": (7, 11), "fim": (11, 11)},
        {"nome": "Mihael", "num": 48, "inicio": (12, 11), "fim": (16, 11)},
        {"nome": "Vehuel", "num": 49, "inicio": (17, 11), "fim": (21, 11)},
        {"nome": "Daniel", "num": 50, "inicio": (22, 11), "fim": (26, 11)},
        {"nome": "Hahasiah", "num": 51, "inicio": (27, 11), "fim": (1, 12)},
        {"nome": "Imamiah", "num": 52, "inicio": (2, 12), "fim": (6, 12)},
        {"nome": "Nanael", "num": 53, "inicio": (7, 12), "fim": (11, 12)},
        {"nome": "Nithael", "num": 54, "inicio": (12, 12), "fim": (16, 12)},
        {"nome": "Mebahiah", "num": 55, "inicio": (17, 12), "fim": (21, 12)},
        {"nome": "Poyel", "num": 56, "inicio": (22, 12), "fim": (26, 12)},
        {"nome": "Nemamiah", "num": 57, "inicio": (27, 12), "fim": (31, 12)},
        {"nome": "Yeialel", "num": 58, "inicio": (1, 1), "fim": (5, 1)},
        {"nome": "Harahel", "num": 59, "inicio": (6, 1), "fim": (10, 1)},
        {"nome": "Mitzrael", "num": 60, "inicio": (11, 1), "fim": (15, 1)},
        {"nome": "Umabel", "num": 61, "inicio": (16, 1), "fim": (20, 1)},
        {"nome": "Iah-Hel", "num": 62, "inicio": (21, 1), "fim": (25, 1)},
        {"nome": "Anauel", "num": 63, "inicio": (26, 1), "fim": (30, 1)},
        {"nome": "Mehiel", "num": 64, "inicio": (31, 1), "fim": (4, 2)},
        {"nome": "Damabiah", "num": 65, "inicio": (5, 2), "fim": (9, 2)},
        {"nome": "Manakel", "num": 66, "inicio": (10, 2), "fim": (14, 2)},
        {"nome": "Eyael", "num": 67, "inicio": (15, 2), "fim": (19, 2)},
        {"nome": "Habuhiah", "num": 68, "inicio": (20, 2), "fim": (24, 2)},
        {"nome": "Rochel", "num": 69, "inicio": (25, 2), "fim": (29, 2)},
        {"nome": "Jabamiah", "num": 70, "inicio": (1, 3), "fim": (5, 3)},
        {"nome": "Haiaiel", "num": 71, "inicio": (6, 3), "fim": (10, 3)},
        {"nome": "Mumiah", "num": 72, "inicio": (11, 3), "fim": (15, 3)}
    ]
    
    for anjo_alvo in tabela_anjos:
        in_m, fi_m = anjo_alvo["inicio"][1], anjo_alvo["fim"][1]
        in_d, fi_d = anjo_alvo["inicio"][0], anjo_alvo["fim"][0]
        
        if in_m == fi_m and mes == in_m and in_d <= dia <= fi_d:
            return f"{anjo_alvo['nome']} ({anjo_alvo['num']}º Gênio)"
        elif in_m != fi_m:
            if (mes == in_m and dia >= in_d) or (mes == fi_m and dia <= fi_d):
                return f"{anjo_alvo['nome']} ({anjo_alvo['num']}º Gênio)"
                
    return "Gênio da Humanidade"


def calcular_kin_maia(dia: int, mes: int, ano: int) -> tuple:
    if mes == 2 and dia == 29:
        dia = 28

    data_alvo = datetime.date(ano, mes, dia)
    data_ancora = datetime.date(2013, 7, 26)
    kin_ancora = 164

    dias_gregorianos = (data_alvo - data_ancora).days

    qtd_bissextos = 0
    ano_min = min(ano, 2013)
    ano_max = max(ano, 2013)
    
    for a in range(ano_min, ano_max + 1):
        if (a % 4 == 0 and (a % 100 != 0 or a % 400 == 0)):
            data_29_fev = datetime.date(a, 2, 29)
            if min(data_alvo, data_ancora) <= data_29_fev <= max(data_alvo, data_ancora):
                qtd_bissextos += 1

    if data_alvo < data_ancora:
        dias_reais = dias_gregorianos + qtd_bissextos
    else:
        dias_reais = dias_gregorianos - qtd_bissextos

    kin = (kin_ancora + dias_reais) % 260
    if kin <= 0:
        kin += 260

    tom = kin % 13
    if tom == 0: tom = 13

    selos_lista = [
        "Dragão Vermelho", "Vento Branco", "Noite Azul", "Semente Amarela", 
        "Serpente Vermelha", "Enlaçador de Mundos Branco", "Mão Azul", "Estrela Amarela", 
        "Lua Vermelha", "Cachorro Branco", "Macaco Azul", "Humano Amarelo", 
        "Caminhante do Céu Vermelho", "Mago Branco", "Águia Azul", "Guerreiro Amarelo", 
        "Terra Vermelha", "Espelho Branco", "Tormenta Azul", "Sol Amarelo"
    ]
    selo = selos_lista[(kin - 1) % 20]

    return kin, tom, selo


def calcular_dados_portal(nome: str, dia_str: str, mes_str: str, ano_str: str) -> dict:
    d = int(str(dia_str).lstrip('0') or 0)
    m = int(str(mes_str).lstrip('0') or 0)
    a = int(ano_str)
    
    signos = [("Capricornio", 19), ("Aquario", 18), ("Peixes", 20), ("Aries", 19), ("Touro", 20), ("Gemeos", 20),
              ("Cancer", 22), ("Leao", 22), ("Virgem", 22), ("Libra", 22), ("Escorpiao", 21), ("Sagitario", 21)]
    signo = signos[m - 1][0] if d <= signos[m - 1][1] else signos[m % 12][0]
    
    anjo = obter_anjo_cabalistico(d, m)
    kin, tom, selo = calcular_kin_maia(d, m, a)

    red = lambda n: n if n in [11, 22] or n <= 9 else red(sum(int(x) for x in str(n)))
    destino = red(sum(int(x) for x in f"{d:02d}{m:02d}{a}" if x.isdigit()))
    
    tabela_pitagorica = {k: int(v) for k, v in "A1 B2 C3 D4 E5 F6 G7 H8 I9 J1 K2 L3 M4 N5 O6 P7 Q8 R9 S1 T2 U3 V4 W5 X6 Y7 Z8".split()}
    expressao = red(sum(tabela_pitagorica.get(c, 0) for c in nome.upper() if c in tabela_pitagorica))

    return {"kin": kin, "tom": tom, "selo": selo, "signo": signo, "anjo": anjo, "destino": destino, "expressao": expressao}

# =========================================================================
# 3. INTERFACE MULTILINGUE E ESTRUTURA DO STREAMLIT
# =========================================================================
DICIONARIO_UI = {
    "pt": {
        "titulo": "PORTAL ALINHADO", "nome": "Nome", "perfil": "Perfil Maia", "astros": "Astros", 
        "num": "Numerologia", "degustacao": "ANÁLISE ARQUETÍPICA GERAL - DEGUSTAÇÃO GRATUITA", 
        "paywall": "Acesse sua geometria sagrada completa e única. Contribuição 9,90", 
        "premium": "CONTEÚDO PREMIUM ATIVO", "revelado": "ANÁLISE ARQUETÍPICA GERAL - COMPLEMENTO REVELADO", 
        "vocacao": "DIRECIONAMENTO VOCACIONAL", "amor": "ALINHAMENTO AFETIVO", 
        "botao": "Alinhar Portal Cósmico", "placeholder_nome": "Nome Completo (Conforme Certidão)",
        "erro_campos": "⚠️ Por favor, preencha todos os campos obrigatórios.", "sucesso": "✨ Portal Alinhado com Sucesso Absoluto!"
    },
    "en": {
        "titulo": "ALIGNED PORTAL", "nome": "Name", "perfil": "Mayan Profile", "astros": "Astros", 
        "num": "Numerology", "degustacao": "GENERAL ARCHETYPAL ANALYSIS - FREE TASTE", 
        "paywall": "Access your complete and unique sacred geometry. Contribution 9.90", 
        "premium": "PREMIUM CONTENT ACTIVATED", "revelado": "GENERAL ARCHETYPAL ANALYSIS - REVEALED COMPLEMENT", 
        "vocacao": "VOCATIONAL GUIDANCE", "amor": "AFFECTIVE ALIGNMENT", 
        "botao": "Align Cosmic Portal", "placeholder_nome": "Full Name (As in Birth Certificate)",
        "erro_campos": "⚠️ Please fill in all required fields.", "sucesso": "✨ Portal Successfully Aligned!"
    },
    "es": {
        "titulo": "PORTAL ALINEADO", "nombre": "Nombre", "perfil": "Perfil Maya", "astros": "Astros", 
        "num": "Numerología", "degustacao": "ANÁLISIS ARQUETÍPICO GENERAL - DEGUSTACIÓN GRATUITA", 
        "paywall": "Accede a tu geometría sagrada completa e única. Contribución 9,90", 
        "premium": "CONTENIDO PREMIUM ACTIVADO", "revelado": "ANÁLISIS ARQUETÍPICO GENERAL - COMPLEMENTO REVELADO", 
        "vocacao": "ORIENTACIÓN VOCACIONAL", "amor": "ALINEACIÓN AFECTIVA", 
        "botao": "Alinear Portal Cósmico", "placeholder_nome": "Nombre Completo (Según Certificado)",
        "erro_campos": "⚠️ Por favor, complete todos los campos obligatorios.", "sucesso": "¡✨ Portal Alineado con Éxito Absoluto!"
    }
}

st.title("🌌 Sincro.app — Portal Metafísico")
st.write("Insira seus dados para alinhar sua frequência geométrica com exatidão.")

idioma = st.selectbox("Escolha o Idioma / Choose Language / Seleccione el Idioma", ["pt", "en", "es"])
ui = DICIONARIO_UI[idioma]

nome = st.text_input(ui["placeholder_nome"], value="")

col1, col2, col3 = st.columns(3)
with col1:
    dia = st.text_input("Dia / Day (DD)", max_chars=2, value="")
with col2:
    mes = st.text_input("Mês / Month (MM)", max_chars=2, value="")
with col3:
    ano = st.text_input("Ano / Year (AAAA)", max_chars=4, value="")

if st.button(ui["botao"]):
    if not nome or not dia or not mes or not ano:
        st.warning(ui["erro_campos"])
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
                    
                    st.success(ui["sucesso"])
                    st.markdown(f"### 🔮 {ui['titulo']}: {int(dia):02d}/{int(mes):02d}/{ano}")
                    st.markdown(f"**👤 {ui.get('nome', ui.get('nombre'))}:** {nome}")
                    st.markdown(f"**🌀 {ui['perfil']}:** KIN {meta['kin']} | Tom {meta['tom']} | Selo {meta['selo']}")
                    st.markdown(f"**✨ {ui['astros']}:** Signo: {meta['signo']} | Anjo: {meta['anjo']}")
                    st.markdown(f"**🔢 {ui['num']}:** Destino: {meta['destino']} | Expressão: {meta['expressao']}")
                    
                    st.divider()
                    st.markdown(f"### 📜 {ui['degustacao']}")
                    st.info(partes["aberto"].strip() if partes["aberto"] else "Generando...")
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
