import pandas as pd
import streamlit as st

st.title("Comercializadora Integral :red[Vori Vost], S.A. de C.V.")
st.header('Reporte de Resultados', divider='red')

datos_vorivost = ['Datos Financieros', 'Datos Operativos']
page = st.radio('Menu', datos_vorivost, index=None, label_visibility='collapsed')

# diccionario de meses en español
meses_español = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

## datos de diseño
# diseño entrega a cliente
data_diseño = pd.read_excel('./datasets/diseño.xlsx') # leyenfo archivo Excel
filtro_entrega_cliente = data_diseño['Proceso'] == 'Entregable a Cliente' # filtro de Entregable a cliente
data_diseño_entrega_cliente = data_diseño.loc[filtro_entrega_cliente]
data_diseño_entrega_cliente['Fecha'] = pd.to_datetime(data_diseño_entrega_cliente['Fecha'])
data_diseño_entrega_cliente_24 = data_diseño_entrega_cliente[data_diseño_entrega_cliente['Fecha'].dt.year == 2024]
# data_diseño_entrega_cliente_24 = data_diseño_entrega_cliente_24.sort_values(by='Fecha')
data_diseño_entrega_cliente_24['month'] = data_diseño_entrega_cliente_24['Fecha'].dt.month.map(meses_español)
diseño_pivot = pd.pivot_table(data_diseño_entrega_cliente_24, values='ML Realizados', index='month', aggfunc=sum)

# diseño entrega a producción
filtro_entrega_produccion = data_diseño['Proceso'] == 'Producción'
data_diseño_entrega_produccion = data_diseño.loc[filtro_entrega_produccion]
data_diseño_entrega_produccion['Fecha'] = pd.to_datetime(data_diseño_entrega_produccion['Fecha'])
data_diseño_entrega_produccion_24 = data_diseño_entrega_produccion[data_diseño_entrega_produccion['Fecha'].dt.year == 2024]
data_diseño_entrega_produccion_24
data_diseño_entrega_produccion_24['month'] = data_diseño_entrega_produccion_24['Fecha'].dt.month.map(meses_español)
diseño_pivot_prod = pd.pivot_table(data_diseño_entrega_produccion_24, values='ML Realizados', index='month', aggfunc='sum')


if page == 'Datos Financieros':
    financieros = ['Ventas', 'Control de gastos', 'Estado de Resultados']
    st.subheader(page)
    financial_option = st.radio('Menu' ,financieros, label_visibility='collapsed', index=None)
    if financial_option == 'Ventas':
        st.subheader('Ventas', divider='blue')
        st.write('Ventas por **Cierre de Trato**:')
        st.write('Ventas por **Entrega de Diseño**:')
        st.write('Ventas por **Inicio de Producción**:')
        st.write('Ventas por **Inicio de Instalación**:')
        st.write('Ventas por **Finalización**:')
    if financial_option == 'Control de gastos':
        cat_gastos = ['Administrativos', 'Operativos']
        cat = st.radio('Gastos:', cat_gastos, index=None)
        if cat == 'Administrativos':
            st.subheader('Gastos: Administrativos', divider='rainbow')
            st.write('Comisiones MP:')
            st.write('IMSS/INFONAVIT:')
            st.write('Finiquitos/Primas:')
            st.write('Oficinas:')
            st.write('Bonos:')
        if cat == 'Operativos':
            st.subheader('Gastos: Operativos', divider='green')
            st.write('Destajo')
            st.write('Horas Extras')
            st.write('Gasolina')
            st.write('Servicios Autos')
            st.write('Costos de Retrabajos')
    if financial_option == 'Estado de Resultados':
        st.subheader('Estado de Resultados', divider='red')
if page == 'Datos Operativos':
    st.subheader(page)
    operativas = ['Diseño', 'Producción', 'Instalación']
    operation_option = st.radio('Menu', operativas, index=None, label_visibility='collapsed')
    if operation_option == 'Diseño':
        st.subheader('ML Entregados a Clientes', divider='green')
        diseño_clientes_chart = st.line_chart(diseño_pivot)
        diseño_pivot
        st.subheader('ML Entregados a Producción', divider='rainbow')
        diseño_prod_chart = st.line_chart(diseño_pivot_prod)
        diseño_pivot_prod