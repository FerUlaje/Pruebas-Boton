import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Comercializadora Integral :red[Vori Vost], S.A. de C.V.")
st.header('Reporte de Resultados', divider='red')

datos_vorivost = ['Datos Financieros', 'Datos Operativos']
page = st.radio('Menu', datos_vorivost, index=None, label_visibility='collapsed')

# diccionario de meses en español
meses_español = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

## Ventas
data_ventas = pd.read_excel('./datasets/Ventas_Vori_Vost_2024.xlsx') # leyendo archivo ventas
# ventas cierre de trato
cierre_trato_df = data_ventas[data_ventas['TIPO VENTA'] == 'CIERRE DE TRATO']
ventas_cierre_trato = cierre_trato_df['VENTA'].sum() # obteniendo total de ventas por cierre de trato
ventas_cierre_trato_pivot = pd.pivot_table(cierre_trato_df, 
                                           values='VENTA', 
                                           index='MES', 
                                           aggfunc="sum")
ventas_cierre_trato_pivot['VENTA'] = ventas_cierre_trato_pivot['VENTA'].astype(int)

# ventas diseño entrega a cliente
entrega_diseño_df = data_ventas[data_ventas['TIPO VENTA'] == 'ENTREGA DISEÑO']
ventas_entrega_diseño = entrega_diseño_df['VENTA'].sum()
ventas_entrega_diseño_pivot = pd.pivot_table(entrega_diseño_df,
                                             values='VENTA',
                                             index='MES',
                                             aggfunc="sum")
ventas_entrega_diseño_pivot['VENTA'] = ventas_entrega_diseño_pivot['VENTA'].astype(int)

# ventas inicio producción
inicio_prod_df = data_ventas[data_ventas['TIPO VENTA'] == 'INICIO PRODUCCIÓN']
ventas_inicio_prod = inicio_prod_df['VENTA'].sum() # obteniendo total de ventas por inicio producción
ventas_inicio_prod_pivot = pd.pivot_table(inicio_prod_df,
                                          values='VENTA',
                                          index='MES',
                                          aggfunc='sum')
ventas_inicio_prod_pivot['VENTA'] = ventas_inicio_prod_pivot['VENTA'].astype(int)

# ventas inicio instalación
inicio_instal_df = data_ventas[data_ventas['TIPO VENTA'] == 'INICIO INSTALACIÓN']
ventas_inicio_instal = inicio_instal_df['VENTA'].sum()
ventas_inicio_instal_pivot = pd.pivot_table(inicio_instal_df,
                                            values='VENTA',
                                            index='MES',
                                            aggfunc='sum')
ventas_inicio_instal_pivot['VENTA'] = ventas_inicio_instal_pivot['VENTA'].astype(int)

# ventas finalización
finalizacion_df = data_ventas[data_ventas['TIPO VENTA'] == 'FINALIZACIÓN']
ventas_finalizacion = finalizacion_df['VENTA'].sum()
ventas_finalizacion_pivot = pd.pivot_table(finalizacion_df,
                                           values='VENTA',
                                           index='MES',
                                           aggfunc='sum')
ventas_finalizacion_pivot['VENTA'] = ventas_finalizacion_pivot['VENTA'].astype(int)


## datos de diseño
# diseño entrega a cliente
data_diseño = pd.read_excel('./datasets/diseño.xlsx') # leyenfo archivo Excel
filtro_entrega_cliente = data_diseño['Proceso'] == 'Entregable a Cliente' # filtro de Entregable a cliente
data_diseño_entrega_cliente = data_diseño.loc[filtro_entrega_cliente]
data_diseño_entrega_cliente['Fecha'] = pd.to_datetime(data_diseño_entrega_cliente['Fecha'])
data_diseño_entrega_cliente_24 = data_diseño_entrega_cliente[data_diseño_entrega_cliente['Fecha'].dt.year == 2024]
# data_diseño_entrega_cliente_24 = data_diseño_entrega_cliente_24.sort_values(by='Fecha')
data_diseño_entrega_cliente_24['month'] = data_diseño_entrega_cliente_24['Fecha'].dt.month.map(meses_español)
diseño_pivot = pd.pivot_table(data_diseño_entrega_cliente_24, values='ML Realizados', index='month', aggfunc="sum")

# diseño entrega a producción
filtro_entrega_produccion = data_diseño['Proceso'] == 'Producción'
data_diseño_entrega_produccion = data_diseño.loc[filtro_entrega_produccion]
data_diseño_entrega_produccion['Fecha'] = pd.to_datetime(data_diseño_entrega_produccion['Fecha'])
data_diseño_entrega_produccion_24 = data_diseño_entrega_produccion[data_diseño_entrega_produccion['Fecha'].dt.year == 2024]
data_diseño_entrega_produccion_24['month'] = data_diseño_entrega_produccion_24['Fecha'].dt.month.map(meses_español)
diseño_pivot_prod = pd.pivot_table(data_diseño_entrega_produccion_24, values='ML Realizados', index='month', aggfunc='sum')


## Egresos
data_egresos = pd.read_excel('./datasets/egresos_vori_vost_2024.xlsx')
data_egresos['Fecha'] = pd.to_datetime(data_egresos['Fecha'])
data_egresos['mes'] = data_egresos['Fecha'].dt.month.map(meses_español)
filtro_egresos_admin = data_egresos['Categoría'] == 'GTO_ADMON'
filtro_egresos_gto_oper = data_egresos['Categoría'] == 'GTO_OPERATIVO'
data_egresos_gto_oper = data_egresos.loc[filtro_egresos_gto_oper]
gto_oper_pivot = pd.pivot_table(data_egresos_gto_oper,
                                values='Monto',
                                index='Subcategoría',
                                columns='mes',
                                aggfunc='sum')


## Función para aplicar formato condicional
def apply_color(val):
    color = 'background-color: {}'.format('#ff9999') if val < 200 else ('background-color: {}'.format('#99ff99') if val > 400 else 'background-color: {}'.format('#ffff99'))
    return color

if page == 'Datos Financieros':
    financieros = ['Ventas', 'Control de gastos', 'Estado de Resultados']
    st.subheader(page)
    financial_option = st.radio('Menu' ,financieros, label_visibility='collapsed', index=None)
    if financial_option == 'Ventas':
        st.subheader('Ventas', divider='blue')


        st.write('Ventas por **Cierre de Trato**: ', ventas_cierre_trato.astype(int))
        fig = px.line(ventas_cierre_trato_pivot, y='VENTA', title='Ventas Cierre Trato', markers=True, line_shape='spline', text='VENTA')
        fig.update_layout(yaxis=dict(showgrid=False))
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig)
        ventas_cierre_trato_pivot

        st.write('Ventas por **Entrega de Diseño**:', ventas_entrega_diseño.astype(int))
        fig2 = px.line(ventas_entrega_diseño_pivot, y='VENTA', title='Ventas Entrega Diseño', markers=True, line_shape='spline', text='VENTA')
        fig2.update_layout(yaxis=dict(showgrid=False))
        fig2.update_traces(textposition='top center')
        st.plotly_chart(fig2)
        ventas_entrega_diseño_pivot

        st.write('Ventas por **Inicio de Producción**:', ventas_inicio_prod.astype(int))
        fig3 = px.line(ventas_inicio_prod_pivot, y='VENTA', title='Ventas Inicio Producción', markers=True, line_shape='spline', text='VENTA')
        fig3.update_layout(yaxis=dict(showgrid=False))
        fig3.update_traces(textposition='top center')
        st.plotly_chart(fig3)
        ventas_inicio_prod_pivot

        st.write('Ventas por **Inicio de Instalación**:', ventas_inicio_instal.astype(int))
        fig4 = px.line(ventas_inicio_instal_pivot, y='VENTA', title='Ventas Inicio Instalación', markers=True, line_shape='spline', text='VENTA')
        fig4.update_layout(yaxis=dict(showgrid=False))
        fig4.update_traces(textposition='top center')
        st.plotly_chart(fig4)
        ventas_inicio_instal_pivot

        st.write('Ventas por **Finalización**:', ventas_finalizacion.astype(int))
        fig5 = px.line(ventas_finalizacion_pivot, y='VENTA', title='Ventas Finalización', markers=True, line_shape='spline', text='VENTA')
        fig5.update_layout(yaxis=dict(showgrid=False))
        fig5.update_traces(textposition='top center')
        st.plotly_chart(fig5)
        ventas_finalizacion_pivot
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
            styled_gto_oper = gto_oper_pivot.style.applymap(apply_color)
            st.dataframe(styled_gto_oper)
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