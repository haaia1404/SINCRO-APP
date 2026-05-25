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
import time  # Garante que o contador de tempo está ativo para o respiro da API

def chamar_gemini_ia(nome, dia, mes, ano, dados_calculados, idioma, tipo_leitura):
    """
    Função que conecta com a API do Gemini 2.5 Flash para gerar as leituras personalizadas.
    Inclui um delay de segurança para evitar o erro de limite (ClientError).
    """
    # Dá um respiro de 2 segundos antes de chamar a API para o Google não bloquear as abas seguidas
    time.sleep(2)
    
    # Extrai os dados calculados do dicionário
    kin = dados_calculados["kin"]
    tom = dados_calculados["tom"]
    selo = dados_calculados["selo"]
    signo = dados_calculados["signo"]
    anjo = dados_calculados["anjo"]
    num_vida = dados_calculados["num_vida"]
    num_expressao = dados_calculados["num_expressao"]
    
    # Montagem do Prompt personalizado de acordo com a aba (tipo_leitura)
    if tipo_leitura == "geral":
        prompt = f"""
        Você é um mestre xamã maia, astrólogo cabalístico e numerólogo pitagórico antigo.
        Gere uma leitura de autoconhecimento profunda e magnética para {nome}, nascido em {dia}/{mes}/{anjo if ano == 0 else ano}.
        Idioma da resposta: {idioma}.
        
        Use os seguintes dados exatos do perfil dele:
        - Sincronário Maia: KIN {kin}, Tom {tom}, Selo Solar {selo}.
        - Astrologia & Cabala: Signo de {signo} guardado pelo Anjo Cabalístico {anjo}.
        - Numerologia: Caminho de Vida {num_vida} e Número de Expressão {num_expressao}.
        
        Esta é a LEITURA GERAL DE ORIGEM. Foque na essência da alma, na energia do tempo no dia em que nasceu e na sua assinatura cósmica. Escreva de forma fluida, misteriosa, "cool" e acolhedora. Termine com a saudação maia tradicional 'In Lak'ech'. Não use formatações genéricas em tópicos simples.
        """
        
    elif tipo_leitura == "vocacao":
        prompt = f"""
        Você é um mentor de carreira holístico e estrategista de destino.
        Gere uma análise focada em MISSÃO, PROPÓSITO E VOCAÇÃO PROFISSIONAL para {nome}.
        Idioma da resposta: {idioma}.
        
        Dados do perfil: KIN {kin} ({tom} + {selo}), Signo {signo}, Números {num_vida} e {num_expressao}.
        
        Esta é a aba premium de TRABALHO & VOCAÇÃO. Revele quais os talentos ocultos e caminhos de prosperidade financeira que o universo reservou para essa combinação de energias. Seja encorajador, prático e profundo.
        """
        
    elif tipo_leitura == "amor":
        prompt = f"""
        Você é um conselheiro afetivo ancestral e terapeuta de alma.
        Gere um alinhamento sobre AMOR, RELACIONAMENTOS E AFETIVIDADE para {nome}.
        Idioma da resposta: {idioma}.
        
        Dados do perfil: KIN {kin}, Signo {signo}, Anjo {anjo}, Caminho de Vida {num_vida}.
        
        Esta é a aba premium de RELACIONAMENTOS & MAGNETISMO AFETIVO. Explique como essa pessoa se comporta no amor, o que sua alma busca em um parceiro e como harmonizar seus portais afetivos. Seja poético, magnético e acolhedor.
        """

    # Bloco de segurança com tratamento de erro e re-tentativa (Retry)
    try:
        client = genai.Client(api_key=API_KEY)
        resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return resposta.text
    except Exception as e:
        # Se a API falhar ou der limite (ClientError), espera mais 4 segundos e tenta uma última vez
        try:
            time.sleep(4)
            client = genai.Client(api_key=API_KEY)
            resposta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            return resposta.text
        except Exception as erro_fatal:
            # Em vez de derrubar o app com tela vermelha, joga uma mensagem elegante na aba correspondente
            return f"🌌 Os portais do tempo estão muito congestionados neste momento. Por favor, aguarde alguns instantes e clique novamente no botão para canalizar a leitura de {tipo_leitura}."

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
