import streamlit as st
import oracledb
import pandas as pd
from datetime import datetime
import random

# Configuração da página
st.set_page_config(page_title="Totem de Viagens", layout="centered")


# --- FUNÇÕES DE APOIO ---
def get_connection():
    return oracledb.connect(
        user='rm567787',
        password='281083',
        dsn='oracle.fiap.com.br:1521/ORCL'
    )


def salvar_dados(dados_dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Gerar colunas e placeholders dinamicamente
        colunas = ", ".join(dados_dict.keys())
        placeholders = ", ".join([f":{k}" for k in dados_dict.keys()])
        sql = f"INSERT INTO MODELO_TOTEM ({colunas}) VALUES ({placeholders})"

        cursor.execute(sql, dados_dict)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar no banco: {e}")
        return False


# --- INÍCIO DA INTERAÇÃO ---
if 'inicio_sessao' not in st.session_state:
    st.session_state.inicio_sessao = datetime.now()
    st.session_state.toques = 0

# Simulação de contador de toques (cada interação no Streamlit recarrega o script)
st.session_state.toques += 1

st.title("✈️ Sistema de Pesquisa de Viagens")

with st.form("form_viagem"):
    st.subheader("Informações do Passageiro")
    col1, col2 = st.columns(2)
    with col1:
        celular = st.text_input("Celular")
        nome_cliente_form = st.text_input("Nome do Cliente")
        faixa_etaria = st.selectbox("Faixa Etária",
                                    ['menor 18 anos', 'entre 18 e 30 anos', 'entre 31 e 40 anos', 'entre 41 e 50 anos',
                                     'entre 51 e 60 anos', 'entre 61 e 70 anos', 'maior 70 anos'])
    with col2:
        email = st.text_input("E-mail")
        aceita_ia = st.radio("Aceita sugestão de IA?", ['sim', 'nao'], horizontal=True)

    st.divider()
    st.subheader("Detalhes do Trajeto")
    origem = st.selectbox("De (Partida)", ['Manaus', 'Rio Branco', 'Cuiabá', 'São Paulo', 'Rio de Janeiro', 'Salvador',
                                           'Belo Horizonte'])
    destino = st.selectbox("Para (Destino)",
                           ['Manaus', 'Rio Branco', 'Cuiabá', 'São Paulo', 'Rio de Janeiro', 'Salvador',
                            'Belo Horizonte'])
    trajeto = st.selectbox("Tipo de Trajeto", ['ida', 'ida-volta'])

    c1, c2, c3 = st.columns(3)
    data_partida = c1.date_input("Data Partida")
    data_retorno = c2.date_input("Data Retorno")
    qtd_assentos = c3.number_input("Qtd Assentos", min_value=1, value=1)

    st.divider()
    st.subheader("Hospedagem e Motivo")
    hospedagem = st.selectbox("Tipo de Hospedagem",
                              ['Hotel', 'Pousada', 'Resort', 'Hostel', 'Camping', 'Casa Residencial', 'Hospital'])
    contratada = st.selectbox("Hospedagem Contratada?", ['Sim', 'Não'])  # Ajustado conforme lógica de lista fornecida
    motivo = st.selectbox("Motivo da Viagem",
                          ['Turismo', 'Negocios', 'Trabalho', 'Saúde', 'Visita Familiar', 'Visita Amigos', 'Religião',
                           'Motivos Pessoais'])

    st.divider()
    operacao = st.selectbox("Operação", ['venda', 'cotacao'])
    pagamento = st.selectbox("Forma de Pagamento", ['PIX', 'Debito', 'Credito', 'cotacao'])

    submit = st.form_submit_button("Finalizar e Salvar")

if submit:
    fim_interacao = datetime.now()
    duracao_segundos = (fim_interacao - st.session_state.inicio_sessao).total_seconds()

    # Cálculos Automáticos
    tempo_viagem = (data_retorno - data_partida).days if trajeto == 'ida-volta' else 0
    valor_unitario = random.randint(300, 1000)
    fator_trajeto = 2 if trajeto == 'ida-volta' else 1
    valor_total = valor_unitario * fator_trajeto * qtd_assentos

    empresa = random.choice(['Gotijo', None, 'Cometa', 'Itamarati'])

    # Lógica de Toques (Simulada pelo tempo de resposta)
    t_alta = 1 if duracao_segundos > 600 else 0
    t_media = 1 if 300 <= duracao_segundos <= 600 else 0
    t_baixa = 1 if duracao_segundos < 300 else 0

    # Dicionário para o Banco
    dados_para_banco = {
        'INICIO_INTERACAO': st.session_state.inicio_sessao,
        'FIM_INTERACAO': fim_interacao,
        'HORA_INI': st.session_state.inicio_sessao.strftime('%H:%M:%S'),
        'HORA_FIM': fim_interacao.strftime('%H:%M:%S'),
        'TEMPO_SESSAO': int(duracao_segundos),
        'TEMPO_INTERACAO': round(duracao_segundos / 60, 2),
        'DATA_PESQUISA': datetime.now().date(),
        'DE_PARTIDA': origem,
        'PARA_DESTINO': destino,
        'TRAJETO': trajeto,
        'DATA_PARTIDA': data_partida,
        'DATA_RETORNO': data_retorno,
        'TEMPO_VIAGEM': tempo_viagem,
        'QUANT_ASSENTOS': qtd_assentos,
        'OPERACAO': operacao,
        'FAIXA_ETARIA': faixa_etaria,
        'TIPO_HOSPEDAGEM': hospedagem,
        'MOTIVO_VIAGEM': motivo,
        'HOSPEDAGEM_CONTRADADA': contratada,
        'VALOR_PASSAGEM': valor_total,
        'FORMA_PAGAMENTO': pagamento,
        'EMPRESA_PARCEIRA': empresa,
        'TOQUES_TELA': st.session_state.toques,
        'TOQUE_ALTA': t_alta,
        'TOQUE_MEDIA': t_media,
        'TOQUE_BAIXA': t_baixa,
        'CELULAR': celular,
        'EMAIL': email,
        'NOME_CLIENTE':nome_cliente_form,
        'ACEITA_SUGESTAO_IA': aceita_ia
    }

    if salvar_dados(dados_para_banco):
        st.success(f"Viagem registrada com sucesso! Valor Total: R${valor_total}")
        st.balloons()

