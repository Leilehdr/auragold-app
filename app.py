import os
import json
from datetime import datetime
import pandas as pd
import streamlit as st

# Configuração da Página do App
st.set_page_config(
    page_title="Aura Gold — Gestão Executiva", page_icon="⚜️", layout="wide"
)

# Arquivo para salvamento local no notebook
DB_FILE = "auragold_database.json"

def carregar_dados():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if "emprestimos" not in st.session_state:
    st.session_state["emprestimos"] = carregar_dados()

# Estilo Visual: Preto Absoluto e Dourado Luxo (#D4AF37) com Alertas em Vermelho Vivo
st.markdown("""
    <style>
    .stApp {
        background-color: #080808;
        color: #e6e6e6;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #D4AF37 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #997d22 100%);
        color: #080808;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #f3d06c 0%, #D4AF37 100%);
        box-shadow: 0px 0px 12px rgba(212, 175, 55, 0.4);
    }
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #222222;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #D4AF37 !important;
    }
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
        border: 1px solid #D4AF37;
        background-color: #141414;
    }
    .atraso-card {
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 8px;
        background-color: #1f0505;
        border-left: 6px solid #ff2222;
        border: 1px solid #551111;
    }
    .normal-card {
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 8px;
        background-color: #141414;
        border-left: 6px solid #D4AF37;
        border: 1px solid #222222;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #161616;
        color: #f2f2f2;
        border: 1px solid #333333;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚜️ AURA GOLD — Gestão e Crédito Executivo")
st.write("Painel operacional para controle diário de carteira, fluxo de caixa e mitigação de riscos.")

# Menu Lateral (Botões de Funcionalidade)
menu = st.sidebar.radio(
    "⚡ Painel de Controle",
    [
        "📅 Consulta Diária",
        "➕ Alimentar (Cadastrar)",
        "📊 Desempenho & Dashboard",
        "⚙️ Gerenciar e Atualizar Status"
    ]
)

# ==========================================
# 1. ALIMENTAR (CADASTRAR)
# ==========================================
if menu == "➕ Alimentar (Cadastrar)":
    st.header("➕ Alimentar Nova Operação de Crédito")
    
    with st.form("form_emprestimo"):
        nome_cliente = st.text_input("Nome Completo do Cliente")
        col1, col2 = st.columns(2)
        with col1:
            valor_emprestado = st.number_input("Valor Emprestado / Saída (R$)", min_value=0.0, format="%.2f")
            taxa_juros = st.number_input("Taxa de Juros Total (%)", min_value=0.0, format="%.2f")
        with col2:
            num_parcelas = st.number_input("Número de Parcelas", min_value=1, step=1, value=1)
            data_vencimento = st.date_input("Data do Vencimento / Pedido", value=datetime.today().date())
        
        status_pagamento = st.selectbox("Status Inicial", ["Pendente", "Pago", "Atrasado"])
        
        submitted = st.form_submit_button("💾 Salvar Informações no Sistema")
        
        if submitted:
            if nome_cliente and valor_emprestado > 0:
                valor_total = valor_emprestado + (valor_emprestado * (taxa_juros / 100))
                
                novo_registro = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "cliente": nome_cliente,
                    "valor_emprestado": valor_emprestado,
                    "juros": taxa_juros,
                    "parcelas": int(num_parcelas),
                    "valor_total": valor_total,
                    "data": data_vencimento.strftime("%Y-%m-%d"),
                    "status": status_pagamento
                }
                
                st.session_state["emprestimos"].append(novo_registro)
                salvar_dados(st.session_state["emprestimos"])
                st.success(f"Operação de {nome_cliente} registrada e salva com segurança no seu notebook!")
            else:
                st.warning("Preencha o nome do cliente e um valor válido.")

# ==========================================
# 2. CONSULTA DIÁRIA
# ==========================================
elif menu == "📅 Consulta Diária":
    st.header("📅 Consulta Diária de Vencimentos")
    
    data_selecionada = st.date_input("Selecione a data para auditar:", value=datetime.today().date())
    data_str = data_selecionada.strftime("%Y-%m-%d")
    
    dados = st.session_state["emprestimos"]
    
    if not dados:
        st.info("Nenhuma operação registrada no banco de dados local.")
    else:
        filtrados = [e for e in dados if e["data"] == data_str]
        
        st.subheader(f"Vencimentos previstos para: {data_selecionada.strftime('%d/%m/%Y')}")
        
        if filtrados:
            for item in filtrados:
                if item["status"] == "Atrasado":
                    st.markdown(f"""
                        <div class="atraso-card">
                            <h3 style="color: #ff4d4d !important; margin: 0;">🚨 CLIENTE EM ATRASO: {item['cliente']}</h3>
                            <p style="margin: 6px 0 0 0; color: #ffcccc;"><b>Valor Devido:</b> R$ {item['valor_total']:.2f} | <b>Parcelas:</b> {item['parcelas']}x | <b>Juros:</b> {item['juros']}%</p>
                            <p style="margin: 4px 0 0 0; color: #ff3333;"><b>Status:</b> ATRASADO (Requer Cobrança)</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="normal-card">
                            <h3 style="color: #D4AF37 !important; margin: 0;">👤 Cliente: {item['cliente']}</h3>
                            <p style="margin: 6px 0 0 0;"><b>Valor a Pagar:</b> R$ {item['valor_total']:.2f} | <b>Parcelas:</b> {item['parcelas']}x | <b>Juros:</b> {item['juros']}%</p>
                            <p style="margin: 4px 0 0 0;"><b>Status:</b> <span style="color: #D4AF37;">{item['status']}</span></p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum cliente agendado para esta data específica.")

# ==========================================
# 3. DESEMPENHO E DASHBOARD
# ==========================================
elif menu == "📊 Desempenho & Dashboard":
    st.header("📊 Painel de Desempenho e Indicadores")
    
    dados = st.session_state["emprestimos"]
    
    if not dados:
        st.info("Alimente dados no sistema para gerar o relatório de desempenho.")
    else:
        df = pd.DataFrame(dados)
        
        total_saidas = df["valor_emprestado"].sum()
        total_retorno_previsto = df["valor_total"].sum()
        
        pago_df = df[df["status"] == "Pago"]
        atrasado_df = df[df["status"] == "Atrasado"]
        
        total_recebido = pago_df["valor_total"].sum()
        total_prejuizo = atrasado_df["valor_emprestado"].sum()
        
        taxa_inadimplencia = (total_prejuizo / total_saidas) * 100 if total_saidas > 0 else 0
        
        if taxa_inadimplencia <= 10:
            status_diag = "EXCELENTE / SAUDÁVEL (Retornos sólidos e baixo risco)"
            cor_diag = "#2e7d32"
        elif taxa_inadimplencia <= 30:
            status_diag = "⚠️ MEIO-TERMO / ATENÇÃO (Monitorar cobranças de perto)"
            cor_diag = "#f57f17"
        else:
            status_diag = "🚨 RISCO ALTO / PREJUÍZO (Rever concessão e cobrar inadimplentes)"
            cor_diag = "#c62828"
            
        st.markdown(f"""
            <div class="metric-card" style="border-color: {cor_diag};">
                <h3 style="color: {cor_diag} !important; margin:0;">DIAGNÓSTICO: {status_diag}</h3>
                <p style="margin: 5px 0 0 0;">Taxa de Inadimplência da Carteira: {taxa_inadimplencia:.1f}%</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Emprestado (Saídas)", f"R$ {total_saidas:.2f}")
        col2.metric("Retorno Previsto", f"R$ {total_retorno_previsto:.2f}")
        col3.metric("Entrada Realizada", f"R$ {total_recebido:.2f}")
        col4.metric("Prejuízos / Atrasados", f"R$ {total_prejuizo:.2f}", delta=f"-{taxa_inadimplencia:.1f}%", delta_color="inverse")
        
        st.subheader("Gráfico Comparativo de Fluxo")
        chart_data = pd.DataFrame({
            "Métrica": ["Saídas (Investido)", "Retorno Previsto", "Entradas (Recebido)", "Atrasos / Prejuízo"],
            "Valores (R$)": [total_saidas, total_retorno_previsto, total_recebido, total_prejuizo]
        })
        st.bar_chart(chart_data.set_index("Métrica"))

# ==========================================
# 4. GERENCIAR E ATUALIZAR STATUS
# ==========================================
elif menu == "⚙️ Gerenciar e Atualizar Status":
    st.header("⚙️ Atualização Diária e Gestão de Clientes")
    
    dados = st.session_state["emprestimos"]
    
    if not dados:
        st.info("Nenhum registro para gerenciar.")
    else:
        for idx, item in enumerate(dados):
            prefixo = "🚨 [ATRASADO] " if item["status"] == "Atrasado" else ""
            with st.expander(f"{prefixo}Cliente: {item['cliente']} | Data: {item['data']} | Status: {item['status']}"):
                novo_status = st.selectbox(
                    "Atualizar Status",
                    ["Pendente", "Pago", "Atrasado"],
                    index=["Pendente", "Pago", "Atrasado"].index(item["status"]),
                    key=f"status_up_{idx}"
                )
                
                if st.button("💾 Salvar Alteração", key=f"btn_up_{idx}"):
                    dados[idx]["status"] = novo_status
                    st.session_state["emprestimos"] = dados
                    salvar_dados(dados)
                    st.success("Status atualizado com sucesso!")
                    st.rerun()
