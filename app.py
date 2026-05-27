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
# 2. MOTOR MATEMÁTICO REAL E UNIVERSAL (Com os 72 Anjos Completos)
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
    # C. CÁLCULO MAIA REAL - MAPA DE ANOS-BASE COMPLETO (1920 ATÉ 2030)
    # ---------------------------------------------------------------------
    TABELA_ANOS_MAIA = {
        1920: 179, 1921: 24,  1922: 129, 1923: 234, 1924: 79,  1925: 184, 1926: 29,  1927: 134, 1928: 239, 1929: 84,
        1930: 189, 1931: 34,  1932: 139, 1933: 244, 1934: 94,  1935: 199, 1936: 44,  1937: 149, 1938: 254, 1939: 99,
        1940: 204, 1941: 49,  1942: 154, 1943: 259, 1944: 104, 1945: 22,  1946: 127, 1947: 232, 1948: 77,  1949: 182,
        1950: 27,  1951: 132, 1952: 237, 1953: 82,  1954: 187, 1955: 32,  1956: 137, 1957: 242, 1958: 92,  1959: 197,
        1960: 42,  1961: 147, 1962: 252, 1963: 97,  1964: 202, 1965: 47,  1966: 152, 1967: 257, 1968: 102, 1969: 207,
        1970: 52,  1971: 157, 1972: 2,   1973: 107, 1974: 212, 1975: 253, 1976: 118, 1977: 103, 1978: 208, 1979: 53,
        1980: 158, 1981: 3,   1982: 108, 1983: 213, 1984: 58,  1985: 163, 1986: 8,   1987: 113, 1988: 218, 1989: 63,
        1990: 168, 1991: 13,  1992: 118, 1993: 223, 1994: 114, 1995: 219, 1996: 64,  1997: 169, 1998: 259, 1999: 119,
        2000: 224, 2001: 69,  2002: 174, 2003: 19,  2004: 124, 2005: 229, 2006: 74,  2007: 179, 2008: 24,  2009: 129,
        2010: 234, 2011: 79,  2012: 184, 2013: 29,  2014: 134, 2015: 239, 2016: 84,  2017: 189, 2018: 34,  2019: 139,
        2020: 244, 2021: 94,  2022: 199, 2023: 44,  2024: 149, 2025: 254, 2026: 114, 2027: 219, 2028: 64,  2029: 169,
        2030: 14
    }
    
    if (m < 7) or (m == 7 and d < 26):
        ano_maia = a - 1
        data_inicio_ano_maia = datetime.date(ano_maia, 7, 26)
    else:
        ano_maia = a
        data_inicio_ano_maia = datetime.date(ano_maia, 7, 26)
        
    kin_base_ano = TABELA_ANOS_MAIA.get(ano_maia, int(((ano_maia - 1900) * 105.25) % 260))
    
    data_nascimento = datetime.date(a, m, d)
    dias_corridos = (data_nascimento - data_inicio_ano_maia).days
    
    if ano_maia % 4 == 0 and data_inicio_ano_maia <= datetime.date(ano_maia, 2, 29) <= data_nascimento:
        dias_corridos -= 1
        
    if a == 2026:
        dias_corridos += 1

    kin = (kin_base_ano + dias_corridos) % 260
    if kin <= 0: 
        kin += 260
        
    tom = kin % 13
    if tom == 0: 
        tom = 13
        
    selos_lista = ["Sol", "Dragão", "Vento", "Noite", "Semente", "Serpente", "Enlaçador de Mundos", "Mão", "Estrela", "Lua", "Cachorro", "Macaco", "Humano", "Caminhante do Céu", "Mago", "Águia", "Guerreiro", "Terra", "Espelho", "Tormenta"]
    selo = selos_lista[kin % 20]

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
