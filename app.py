import streamlit as st
from datetime import date
from google import genai
import os

# =========================================================================
# CONFIGURAÇÃO DA PÁGINA (DESIGN E INTERFACE)
# =========================================================================
st.set_page_config(
    page_title="Sincro App - Portais do Tempo",
    page_icon="🔮",
    layout="centered"
)

# Puxa a chave de forma segura do painel do Streamlit
API_KEY = st.secrets["GEMINI_API_KEY"]

# =========================================================================
# 1. MOTORES DE CÁLCULO INTERNOS
# =========================================================================
def obter_signo_e_anjo_cabalistico(dia, mes):
    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19): signo = "Áries"
    elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20): signo = "Touro"
    elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20): signo = "Gêmeos"
    elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22): signo = "Câncer"
    elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22): signo = "Leão"
    elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22): signo = "Virgem"
    elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22): signo = "Libra"
    elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21): signo = "Escorpião"
    elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21): signo = "Sagitário"
    elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19): signo = "Capricórnio"
    elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18): signo = "Aquário"
    else: signo = "Peixes"

    if mes == 4:
        if dia <= 2: anjo = "Elemiah (4º Gênio)"
        elif dia <= 6: anjo = "Mahasiah (5º Gênio)"
        elif dia <= 11: anjo = "Lelahel (6º Gênio)"
        elif dia <= 16: anjo = "Haaiah (26º Gênio Cabalístico - Amparo e Verdade)"
        elif dia <= 21: anjo = "Achaiah (7º Gênio)"
        elif dia <= 25: anjo = "Cahethel (8º Gênio)"
        else: anjo = "Haziel (9º Gênio)"
    elif mes == 3:
        if dia <= 24: anjo = "Vehuaiah (1º Gênio)"
        elif dia <= 28: anjo = "Jeliel (2º Gênio)"
        else: anjo = "Sitael (3º Gênio)"
    else:
        anjo = "Gênio Cabalístico correspondente ao ciclo solar"
        
    return signo, anjo

def reduzir_numero(n):
    while n > 9 and n != 11 and n != 22:
        n = sum(int(digito) for digito in str(n))
    return n

def calcular_numerologia_data(dia, mes, ano):
    soma = sum(int(d) for d in f"{dia:02d}{mes:02d}{ano}")
    return reduzir_numero(soma)

def calcular_numerologia_nome(nome):
    tabela = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':1,'K':2,'L':3,'M':4,'N':5,'O':6,'P':7,'Q':8,'R':9,'S':1,'T':2,'U':3,'V':4,'W':5,'X':6,'Y':7,'Z':8}
    return reduzir_numero(sum(tabela.get(l, 0) for l in nome.upper() if l in tabela))

def calcular_sincronario(dia, mes, ano):
    data_ancora, kin_ancora, data_alvo = date(2026, 4, 23), 115, date(ano, mes, dia)
    is_hunab = False
    if mes == 2 and dia == 29:
        data_alvo = date(ano, 2, 28)
        is_hunab = True

    diferenca = (data_alvo - data_ancora).days
    bissextos = sum(1 for a in range(min(ano, 2026), max(ano, 2026) + 1) if a % 4 == 0 and min(data_alvo, data_ancora) <= date(a, 2, 28) <= max(data_alvo, data_ancora))
    diferenca = (diferenca - bissextos) if diferenca > 0 else (diferenca + bissextos)

    kin_base = (kin_ancora + diferenca) % 260
    if kin_base == 0: kin_base = 260
    tom = (kin_base - 6) % 13
    if tom <= 0: tom += 13
    
    nomes_selos = ["Sol (Ajaw)","Dragão (Imix')","Vento (Ik')","Noite (Ak'b'al)","Semente (K'an)","Serpente (Chikchan)","Enlaçador de Mundos (Kimi)","Mão (Manik')","Estrela (Lamat)","Lua (Muluk)","Cachorro (Ok)","Macaco (Chuwen)","Humano (Eb')", "Caminhante do Céu (B'en)","Mago (Ix)","Águia (Men)","Guerreiro (Kib')","Terra (Kab'an)","Espelho (Etz'nab')","Tormenta (Kawak)"]
    selo = nomes_selos[kin_base % 20]

    kin_real = next(k for k in range(1, 261) if (k % 13 if k % 13 != 0 else 13) == tom and nomes_selos[k % 20] == selo)
    ano_gal = ano - 1 if (mes < 7 or (mes == 7 and dia < 26)) else ano
    dias_ano = (data_alvo - date(ano_gal, 7, 26)).days
    
    plasmas = ["Dali", "Seli", "Gama", "Kali", "Alfa", "Limi", "Silio"]
    cores = ["Vermelha (Inicia)", "Branca (Refina)", "Azul (Transforma)", "Amarela (Amadurece)"]
    luas = ["Magnética", "Lunar", "Elétrica", "Autoexistente", "Harmônica", "Rítmica", "Ressonante", "Galáctica", "Solar", "Planetária", "Espectral", "Cristal", "Cósmica"]
    
    if mes == 7 and dia == 25 and not is_hunab:
        return kin_real, tom, selo, "Dia Fora do Tempo", "Livre", "Verde"
    
    dia_sinc = (dias_ano % 365) + 1
    n_lua = min(((dia_sinc - 1) // 28) + 1, 13)
    d_lua = ((dia_sinc - 1) % 28) + 1
    return kin_real, tom, selo, f"Dia {d_lua} da Lua {luas[n_lua-1]} (Lua {n_lua})", plasmas[(d_lua-1)%7], cores[((d_lua - 1) // 7)]

# =========================================================================
# 2. INTEGRAÇÃO INTELIGENTE COM GEMINI (GERAÇÃO DOS 3 TIPOS DE TEXTO)
# =========================================================================
def chamar_gemini_ia(nome, dia, mes, ano, dados_calculados, idioma_selecionado, tipo_leitura):
    client = genai.Client(api_key=API_KEY)
    
    # Base de dados em comum que a IA vai ler
    dados_perfil = f"""
    - Nome: {nome}
    - Nascimento: {dia:02d}/{mes:02d}/{ano}
    - Energia Galáctica: KIN {dados_calculados['kin']} - Tom {dados_calculados['tom']} + Selo {dados_calculados['selo']}
    - Frequência Temporal: {dados_calculados['info_lua']} + Plasma {dados_calculados['plasma']}
    - Astrologia: Sol em {dados_calculados['signo']}
    - Guardião Espiritual: {dados_calculados['anjo']}
    - Caminho de Vida (Destino): {dados_calculados['num_data']}
    - Talentos Inatos (Expressão): {dados_calculados['num_nome']}
    """

    # Personalizando o comando de acordo com o tipo de texto escolhido
    if tipo_leitura == "geral":
        prompt = f"""
        Write strictly in {idioma_selecionado}.
        Atue como um mentor existencial profundo. Escreva um perfil revelador e inspirador (cerca de 30 linhas).
        TRADUZA os dados técnicos abaixo em força psicológica e direcionamento de vida de forma fluida.
        NÃO use listas, tópicos ou bullet points. Crie um título poético forte.
        Termine com a saudação "In Lak'ech!".
        Dados do Consultante: {dados_perfil}
        """
    elif tipo_leitura == "vocacao":
        prompt = f"""
        Write strictly in {idioma_selecionado}.
        Com base nos dados arquetípicos abaixo, escreva uma análise focada estritamente em VOCAÇÃO PROFISSIONAL, PROSPERIDADE, TALENTOS FINANCEIROS E CARREIRA.
        O texto deve ser direto, motivador e ter NO MÁXIMO 10 LINHAS.
        NÃO use tópicos. Crie um título forte focado em Propósito e Trabalho.
        Dados do Consultante: {dados_perfil}
        """
    elif tipo_leitura == "amor":
        prompt = f"""
        Write strictly in {idioma_selecionado}.
        Com base nos dados arquetípicos abaixo, escreva uma análise profunda focada em AFINIDADE AMOROSA, RELACIONAMENTOS, COMO A PESSOA AMA E SE CONECTA AFETIVAMENTE.
        O texto deve ser magnético, romântico-arquetípico e acolhedor (cerca de 15 a 20 linhas).
        NÃO use tópicos. Crie um título poético focado em Conexão de Almas e Amor.
        Dados do Consultante: {dados_perfil}
        """

    # Executa a chamada
    try:
        resposta = client.models.generate_content(model='gemini-2.5-pro', contents=prompt)
        return resposta.text
    except:
        resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return resposta.text

# =========================================================================
# 3. INTERFACE VISUAL DO USUÁRIO (WEB APP)
# =========================================================================
st.title("🔮 Sincro App")
st.subheader("O Despertar do Vórtice Sagrado através do Tempo")
st.write("Insira os dados para liberar seu portal do tempo.")

st.markdown("---")

nome_input = st.text_input("Nome Completo do Consultado:")

col1, col2 = st.columns(2)
with col1:
    data_nascimento = st.date_input("Data de Nascimento:", min_value=date(1920, 1, 1), max_value=date.today(), value=date(1990, 1, 1))
with col2:
    idioma = st.selectbox("Idioma do Relatório:", ["Português", "English", "Español"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Canalizar Leituras do Portal", use_container_width=True):
    if not nome_input.strip():
        st.warning("⚠️ Por favor, digite o nome completo antes de continuar.")
    else:
        with st.spinner("🌌 Conectando aos portais temporais e calculando suas frequências..."):
            
            dia, mes, ano = data_nascimento.day, data_nascimento.month, data_nascimento.year
            kin, tom, selo, info_lua, plasma, semana = calcular_sincronario(dia, mes, ano)
            signo, anjo = obter_signo_e_anjo_cabalistico(dia, mes)
            num_data = calcular_numerologia_data(dia, mes, ano)
            num_nome = calcular_numerologia_nome(nome_input)

            dados = {
                "kin": kin, "tom": tom, "selo": selo, "info_lua": info_lua, 
                "plasma": plasma, "semana": semana, "signo": signo, "anjo": anjo, 
                "num_data": num_data, "num_nome": num_nome
            }

            # Gerando a leitura Geral (Amostra Grátis)
            texto_geral = chamar_gemini_ia(nome_input, dia, mes, ano, dados, idioma, "geral")
            
            # Gerando as leituras Premium (que depois serão bloqueadas por pagamento)
            texto_vocacao = chamar_gemini_ia(nome_input, dia, mes, ano, dados, idioma, "vocacao")
            texto_amor = chamar_gemini_ia(nome_input, dia, mes, ano, dados, idioma, "amor")
            
            st.markdown("---")
            st.success("📜 Portais Canalizados!")
            
            # Criando Abas para organizar os 3 textos na tela de forma elegante
            aba1, aba2, aba3 = st.tabs(["🌌 Leitura Geral (Livre)", "💼 Missão & Vocação", "💖 Alinhamento Amoroso"])
            
            with aba1:
                st.write(texto_geral)
                
            with aba2:
                st.markdown("### 🔒 Módulo Premium Bloqueado")
                st.info("Adorou sua leitura? No app oficial, esta seção de Vocação Profissional (até 10 linhas) será desbloqueada via Pix automático!")
                st.markdown("---")
                st.write("*Aqui está uma prévia do seu teste atual:*")
                st.write(texto_vocacao)
                
            with aba3:
                st.markdown("### 🔒 Módulo Premium Bloqueado")
                st.info("Descubra sua dinâmica afetiva e de atração cósmica desbloqueando este módulo via Pix!")
                st.markdown("---")
                st.write("*Aqui está uma prévia do seu teste atual:*")
                st.write(texto_amor)
