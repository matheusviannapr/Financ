import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Função para carregar ou criar o arquivo de dados
def load_data(filename, default_data):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(default_data)

# Função para salvar os dados no arquivo
def save_data(data, filename):
    data.to_csv(filename, index=False)

# Função para salvar mensalmente
def save_monthly_data(data, filename_prefix):
    now = datetime.now()
    filename = f"{filename_prefix}_{now.strftime('%Y_%m')}.csv"
    data.to_csv(filename, index=False)
    return filename

# Função para listar arquivos mensais salvos
def list_monthly_files(filename_prefix):
    files = [f for f in os.listdir() if f.startswith(filename_prefix) and f.endswith('.csv')]
    return sorted(files, reverse=True)

# Função para carregar histórico mensal
def load_monthly_data(filename_prefix):
    files = list_monthly_files(filename_prefix)
    if len(files) > 0:
        selected_file = st.selectbox("Selecione o mês", files)
        if selected_file:
            data = pd.read_csv(selected_file)
            st.write(f"Dados do mês: {selected_file}")
            st.dataframe(data)
            return data
    else:
        st.write("Nenhum dado mensal encontrado.")
        return None

# Função para carregar múltiplos arquivos mensais e compará-los
def load_and_compare_monthly_data(filename_prefix):
    files = list_monthly_files(filename_prefix)
    selected_files = st.multiselect("Selecione os meses para comparação", files)
    
    if len(selected_files) > 0:
        data_frames = []
        for file in selected_files:
            df = pd.read_csv(file)
            df['Mês'] = file  # Adicionar uma coluna para identificar o mês
            data_frames.append(df)
        
        # Combinar todos os DataFrames
        combined_df = pd.concat(data_frames)
        st.write("Dados combinados dos meses selecionados:")
        st.dataframe(combined_df)
        
        # Gerar gráficos comparativos
        st.write("Comparação Gráfica")
        st.bar_chart(combined_df.set_index('Mês')[['Planejado', 'Real']])
        return combined_df

# Página de Orçamento
def page_orcamento():
    st.title("Orçamento Mensal")
    
    saldo_inicial = st.number_input("Saldo Inicial", value=12000)
    saldo_final = st.number_input("Saldo Final", value=10168)
    
    st.write(f"Economia do mês: {saldo_inicial - saldo_final}")
    
    # Carregar os dados de despesas
    despesas_df = load_data('despesas.csv', {
        'Categoria': ['Alimentação', 'Saúde', 'Moradia', 'Transporte', 'Esportes', 'Outros'],
        'Planejado': [750, 412, 3500, 250, 50, 200],
        'Real': [750, 412, 3500, 250, 50, 464]
    })
    
    # Editor dinâmico para despesas
    st.write("Despesas (editáveis):")
    despesas_edit = st.data_editor(despesas_df, num_rows="dynamic")

    # Gráfico para visualizar despesas
    st.bar_chart(despesas_edit.set_index('Categoria')[['Planejado', 'Real']])

    # Salvar dados editados de despesas
    if st.button('Salvar Despesas'):
        save_data(despesas_edit, 'despesas.csv')
        st.success('Despesas salvas com sucesso!')

    # Salvar mensalmente os dados de despesas
    if st.button('Salvar Despesas Mensais'):
        filename = save_monthly_data(despesas_edit, 'despesas_mensal')
        st.success(f"Despesas salvas mensalmente em {filename}")

    # Mostrar histórico mensal de despesas
    st.write("Histórico Mensal de Despesas")
    load_monthly_data('despesas_mensal')

    # Comparação entre meses
    st.write("Comparação entre meses de Despesas")
    load_and_compare_monthly_data('despesas_mensal')

    # Carregar os dados de renda
    renda_df = load_data('renda.csv', {
        'Categoria': ['Salário', 'Bônus', 'Outros'],
        'Planejado': [8200, 0, 0],
        'Real': [8200, 0, 0]
    })

    # Editor dinâmico para renda
    st.write("Renda (editável):")
    renda_edit = st.data_editor(renda_df, num_rows="dynamic")
    
    # Gráfico para visualizar renda
    st.bar_chart(renda_edit.set_index('Categoria')[['Planejado', 'Real']])

    # Salvar dados editados de renda
    if st.button('Salvar Renda'):
        save_data(renda_edit, 'renda.csv')
        st.success('Renda salva com sucesso!')

    # Salvar mensalmente os dados de renda
    if st.button('Salvar Renda Mensal'):
        filename = save_monthly_data(renda_edit, 'renda_mensal')
        st.success(f"Renda salva mensalmente em {filename}")

    # Mostrar histórico mensal de renda
    st.write("Histórico Mensal de Renda")
    load_monthly_data('renda_mensal')

    # Comparação entre meses
    st.write("Comparação entre meses de Renda")
    load_and_compare_monthly_data('renda_mensal')

# Página de Investimentos
def page_investimentos():
    st.title("Investimentos")

    # Carregar os dados de investimento
    investimento_df = load_data('investimentos.csv', {
        'Tipo': ['Ações', 'Renda Fixa', 'Criptomoedas'],
        'Valor Investido': [10000, 5000, 2000],
        'Valor Atual': [12000, 5300, 2500]
    })

    # Editor dinâmico para investimentos
    st.write("Investimentos (editáveis):")
    investimento_edit = st.data_editor(investimento_df, num_rows="dynamic")

    # Gráfico de evolução dos investimentos
    st.bar_chart(investimento_edit.set_index('Tipo')[['Valor Investido', 'Valor Atual']])

    # Salvar dados editados de investimentos
    if st.button('Salvar Investimentos'):
        save_data(investimento_edit, 'investimentos.csv')
        st.success('Investimentos salvos com sucesso!')

    # Salvar mensalmente os dados de investimentos
    if st.button('Salvar Investimentos Mensalmente'):
        filename = save_monthly_data(investimento_edit, 'investimentos_mensal')
        st.success(f"Investimentos salvos mensalmente em {filename}")

    # Mostrar histórico mensal de investimentos
    st.write("Histórico Mensal de Investimentos")
    load_monthly_data('investimentos_mensal')

    # Comparação entre meses
    st.write("Comparação entre meses de Investimentos")
    load_and_compare_monthly_data('investimentos_mensal')

# Configurando as páginas
page = st.sidebar.selectbox("Escolha a página", ["Orçamento", "Investimentos"])

if page == "Orçamento":
    page_orcamento()
else:
    page_investimentos()
