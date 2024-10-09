import streamlit as st
import pandas as pd
import plotly.express as px
from controllers.analysis_controller import get_monthly_summary, get_category_summary, generate_monthly_chart, generate_category_chart, get_financial_health

def show_analysis():
    st.title("Análise Financeira")

    # Obtendo dados
    monthly_summary = get_monthly_summary(st.session_state['username'])
    category_summary = get_category_summary(st.session_state['username'])

    # Filtros na sidebar
    st.sidebar.markdown("### Filtros")

    if not monthly_summary.empty and len(monthly_summary) > 1:
        date_range = pd.date_range(start=monthly_summary['Mês'].min(), end=monthly_summary['Mês'].max())
        start_date, end_date = st.sidebar.select_slider(
            "Selecione o período",
            options=date_range,
            value=(date_range.min(), date_range.max()),
            format_func=lambda x: x.strftime("%b %Y")
        )
    else:
        st.sidebar.warning("Período insuficiente para aplicar filtro.")
        start_date, end_date = None, None

    if not category_summary.empty:
        selected_categories = st.sidebar.multiselect(
            "Categorias",
            options=category_summary['Categoria'].tolist(),
            default=category_summary['Categoria'].tolist()
        )
    else:
        st.sidebar.warning("Nenhuma categoria disponível para aplicar filtro.")
        selected_categories = []

    # Aplicar filtros
    filtered_monthly = monthly_summary if start_date is None else monthly_summary[
        (pd.to_datetime(monthly_summary['Mês']) >= start_date) &
        (pd.to_datetime(monthly_summary['Mês']) <= end_date)
    ]
    
    filtered_category = category_summary[category_summary['Categoria'].isin(selected_categories)] if selected_categories else category_summary
    filtrado_abs = filtered_category
    filtrado_abs['Valor'] = abs(filtrado_abs['Valor'])

    # Exibir gráficos e métricas financeiras
    st.subheader("Resumo Financeiro")
    col1, col2 = st.columns(2)

    with col1:
        if not filtered_monthly.empty:
            st.plotly_chart(generate_monthly_chart(filtered_monthly), use_container_width=True)
        else:
            st.write("Nenhum dado disponível para o período selecionado.")
    
    with col2:
        if not filtrado_abs.empty:
            fig_category = px.pie(filtrado_abs, values='Valor', names='Categoria', title='Valores por Categoria')
            st.plotly_chart(fig_category, use_container_width=True)
        else:
            st.write("Nenhum dado disponível para as categorias selecionadas.")
    
    # Gráfico de dispersão para mostrar onde o dinheiro está sendo gasto
    st.subheader("Distribuição de Gastos (Dispersão)")
    if not filtered_category.empty:
        fig_scatter = px.scatter(filtered_category, x='Categoria', y='Valor', title='Dispersão dos Gastos por Categoria')
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.write("Nenhuma despesa registrada nas categorias selecionadas.")

    # Saúde financeira
    health = get_financial_health(st.session_state['username'], start_date, end_date) if start_date and end_date else get_financial_health(st.session_state['username'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Renda Total", f"R$ {health['total_income']:.2f}")
    with col2:
        st.metric("Despesas Totais", f"R$ {health['total_expenses']:.2f}")
    with col3:
        st.metric("Taxa de Poupança", f"{health['savings_rate']:.2f}%")

    # Análise comparativa de períodos
    st.subheader("Análise Comparativa de Períodos")
    if not filtered_monthly.empty:
        period1, period2 = st.columns(2)
        with period1:
            selected_period1 = st.selectbox("Selecione o primeiro período", filtered_monthly['Mês'].tolist(), key='period1')
        with period2:
            selected_period2 = st.selectbox("Selecione o segundo período", filtered_monthly['Mês'].tolist(), key='period2')

        if selected_period1 and selected_period2:
            value1 = filtered_monthly[filtered_monthly['Mês'] == selected_period1]['Valor'].values[0]
            value2 = filtered_monthly[filtered_monthly['Mês'] == selected_period2]['Valor'].values[0]
            difference = value2 - value1
            percentage_change = (difference / value1) * 100 if value1 != 0 else 0

            st.write(f"Diferença entre {selected_period1} e {selected_period2}: R$ {difference:.2f}")
            st.write(f"Variação percentual: {percentage_change:.2f}%")
    else:
        st.write("Nenhum dado disponível para comparação.")
