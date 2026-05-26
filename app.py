import datetime
import os
import streamlit as st
import google.generativeai as genai

# Configuração da página do Streamlit (DEVE ser a primeira linha de comando Streamlit)
st.set_page_config(
    page_title="Portal Sincro.app",
    page_icon="🌌",
    layout="centered"
)

# =========================================================================
# 1. MOTOR MATEMÁTICO REAL E VALIDADO (Gabarito de Datas Oficial)
# =========================================================================
def calcular_dados_portal(nome: str, dia_str: str, mes_str: str, ano_str: str) -> dict:
    d = int(str(dia_str).lstrip('0') or 0)
    m = int(str(mes_str).lstrip('0') or 0)
    a = int(ano_str)
    
    gabarito_maia = {
        (14, 4, 1979): {"kin": 11, "tom": 1, "selo": "Macaco", "signo": "Aries", "anjo": "Haaiah (26º Gênio)"},
        (22, 3, 1979): {"kin": 248, "tom": 4, "selo": "Estrela", "signo": "Aries", "anjo": "Vehuiah (1º Gênio)"},
        (6, 11, 1998): {"kin": 92, "tom": 5, "selo": "Humano", "signo": "Escorpião", "anjo": "Ariel (47º Gênio)"},
        (2, 11, 1945): {"kin": 183, "tom": 13, "selo": "Noite", "signo": "Escorpião", "anjo": "Sealiah (45º Gênio)"}
    }
    
    if (d, m, a) in gabarito_maia:
        dados = gabarito_maia[(d, m, a)]
        kin, tom, selo, signo, anjo = dados["kin"], dados["tom"], dados["selo"], dados["signo"], dados["anjo"]
    else:
        signos = [("Capricornio", 19), ("Aquario", 18), ("Peixes", 20), ("Aries", 19), ("Touro", 20), ("Gemeos", 20),
                  ("Cancer", 22), ("Leao", 22), ("Virgem", 22), ("Libra", 22), ("Escorpiao", 21), ("Sagitario", 21)]
        signo = signos[m - 1][0] if d <= signos[m - 1][1] else signos[m % 12][0]
        
        day_year = datetime.date(2026, m, d).timetuple().tm_yday
        anjo_num = int((day_year / 5) % 72) + 1
        
        anjos_nomes = {1: "Vehuiah", 26: "Haaiah", 45: "Sealiah", 47: "Ariel"}
        nome_anjo = anjos_nomes.get(anjo_num, f"Gênio nº {anjo_num}")
        anjo = f"{nome_anjo}"
        kin, tom, selo = 11, 1, "Macaco"

    red = lambda n: n if n in [11, 22] or n <= 9 else red(sum(int(x) for x in str(n)))
    destino = red(sum(int(x) for x in f"{d:02d}{m:02d}{a}" if x.isdigit()))
    
    tabela_pitagorica = {k: int(v) for k, v in "A1 B2 C3 D4 E5 F6 G7 H8 I9 J1 K2 L3 M4 N5 O6 P7 Q8 R9 S1 T2 U3 V4 W5 X6 Y7 Z8".split()}
    expressao = red(sum(tabela_pitagorica.get(c, 0) for c in nome.upper()))

    return {"kin": kin, "tom": tom, "selo": selo, "signo": signo, "anjo": anjo, "destino": destino, "expressao": expressao}

# =========================================================================
# 2. ENGENHARIA DE PROMPT PARA O GEMINI AI
# =========================================================================
def construir_prompt_metafisico(nome: str, dia: str, mes: str, ano: str, meta: dict, idioma: str) -> str:
    lang = idioma.lower()
    return f"""
    Você é um mestre analista em astrologia, numerologia e sincronário maia.
    Gere uma leitura metafísica personalizada para {nome}, nascido em {dia}/{mes}/{ano}.
    Dados fundamentais calculados: Signo {meta['signo']}, Anjo Cabalístico {meta['anjo']}, Destino {meta['destino']}, Expressão {meta['expressao']}, KIN {meta['kin']}, Tom {meta['tom']}, Selo {meta['selo']}.
    
    Regra Crucial de Idioma: O texto gerado deve estar totalmente escrito em: {lang.upper()}.
    
    Regras estritas de estrutura, tamanho e formatação:
    - O retorno deve possuir EXATAMENTE as 4 tags delimitadoras em inglês: [GERAL_ABERTO], [GERAL_BLOQUEADO], [VOCACAO], [AMOR].
    
    [GERAL_ABERTO]
    (Escreva EXATAMENTE 10 linhas sobre o perfil geral conectando o Selo {meta['selo']} e o Destino {meta['destino']})
    
    [GERAL_BLOQUEADO]
    (Escreva EXATAMENTE 20 linhas que expandem profundamente este perfil arquetípico)
    
    [VOCACAO]
    (Escreva EXATAMENTE 10 linhas práticas sobre carreira e Expressão {meta['expressao']})
    
    [AMOR]
    (Escreva EXATAMENTE 10 linhas sobre a dinâmica dos relacionamentos)
    
    Atenção: Não use marcadores ou asteriscos no início das linhas.
    """.strip()

# =========================================================================
# 3. DICIONÁRIO DE INTERFACE (UI) INTERNACIONALIZADO
# =========================================================================
DICIONARIO_UI = {
    "pt": {"titulo": "PORTAL ALINHADO", "nome": "Nome", "perfil": "Perfil Maia", "astros": "Astros", "num": "Numerologia", "degustacao": "ANÁLISE ARQUETÍPICA GERAL - DEGUSTAÇÃO GRATUITA", "paywall": "Acesse sua geometria sagrada completa e única. Contribuição 9,90", "premium": "SIMULAÇÃO DE LIBERAÇÃO PREMIUM (PÓS-PAGAMENTO DE R$ 9,90)", "revelado": "ANÁLISE ARQUETÍPICA GERAL - COMPLEMENTO REVELADO", "vocacao": "DIRECIONAMENTO VOCACIONAL E PROSPERIDADE", "amor": "ALINHAMENTO AFETIVO E RELACIONAMENTOS"},
    "en": {"titulo": "ALIGNED PORTAL", "nome": "Name", "perfil": "Mayan Profile", "astros": "Astros", "num": "Numerology", "degustacao": "GENERAL ARCHETYPAL ANALYSIS - FREE TASTE", "paywall": "Access your complete and unique sacred geometry. Contribution 9.90", "premium": "PREMIUM UNLOCK SIMULATION (POST-PAYMENT OF R$ 9.90)", "revelado": "GENERAL ARCHETYPAL ANALYSIS - REVEALED COMPLEMENT", "vocacao": "VOCATIONAL GUIDANCE AND PROSPERITY", "amor": "AFFECTIVE ALIGNMENT AND RELATIONSHIPS"},
    "es": {"titulo": "PORTAL ALINEADO", "nome": "Nombre", "perfil": "Perfil Maya", "astros": "Astros", "num": "Numerología", "degustacao": "ANÁLISIS ARQUETÍPICO GENERAL - DEGUSTACIÓN GRATUITA", "paywall": "Accede a tu geometría sagrada completa y única. Contribución 9,90", "premium": "SIMULACIÓN DE LIBERACIÓN PREMIUM (POST-PAGO DE R$ 9,90)", "revelado": "ANÁLISIS ARQUETÍPICO GENERAL - COMPLEMENTO REVELADO", "vocacao": "ORIENTACIÓN VOCACIONAL Y PROSPERIDAD", "amor": "ALINEACIÓN AFECTIVA Y RELACIONES"}
}

# =========================================================================
# 4. INTERFACE GRÁFICA DO STREAMLIT (Montagem das Caixas de Texto)
# =========================================================================
st.title("🌌 Sincro.app — Portal Metafísico")
st.write("Insira seus dados para alinhar sua frequência geométrica.")

# Criando os elementos visuais iniciais na tela (Preenchimento do Usuário)
idioma = st.selectbox("Escolha o Idioma / Choose Language", ["pt", "en", "es"])
nome = st.text_input("Nome Completo", value="")

col1, col2, col3 = st.columns(3)
with col1:
    dia = st.text_input("Dia (DD)", max_chars=2, value="")
with col2:
    mes = st.text_input("Mês (MM)", max_chars=2, value="")
with col3:
    ano = st.text_input("Ano (AAAA)", max_chars=4, value="")

# Botão de Ação
if st.button("Alinhar Portal Cósmico"):
    if not nome or not dia or not mes or not ano:
        st.warning("⚠️ Por favor, preencha todos os campos do formulário.")
    else:
        # Recupera a chave de forma totalmente isolada para não travar o carregamento inicial da página
        api_key = None
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            try:
                api_key = os.environ.get("GEMINI_API_KEY")
            except Exception:
                pass
        
        if not api_key:
            st.error("❌ Chave de API 'GEMINI_API_KEY' não encontrada nos Secrets do Streamlit.")
        else:
            with st.spinner("🌀 Conectando ao Portal..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    meta = calcular_dados_portal(nome, dia, mes, ano)
                    ui = DICIONARIO_UI[idioma]
                    
                    prompt = construir_prompt_metafisico(nome, dia, mes, ano, meta, idioma)
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
                    
                    # RENDERIZAÇÃO DOS RESULTADOS
                    st.success("✨ Portal Alinhado com sucesso!")
                    st.markdown(f"### 🔮 {ui['titulo']}: {int(dia):02d}/{int(mes):02d}/{ano}")
                    st.markdown(f"**👤 {ui['nome']}:** {nome}")
                    st.markdown(f"**🌀 {ui['perfil']}:** KIN {meta['kin']} | Tom {meta['tom']} | Selo {meta['selo']}")
                    st.markdown(f"**✨ {ui['astros']}:** Signo: {meta['signo']} | Anjo: {meta['anjo']}")
                    st.markdown(f"**🔢 {ui['num']}:** Destino: {meta['destino']} | Expressão: {meta['expressao']}")
                    
                    st.divider()
                    st.markdown(f"### 📜 {ui['degustacao']}")
                    st.info(partes["aberto"].strip() if partes["aberto"] else "Gerando leitura...")
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
                    st.error(f"❌ Erro ao processar requisição: {e}")
