import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib
from calendar import month_name

month_lookup = list(month_name)



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
data_ventas['Fecha'] = pd.to_datetime(data_ventas['FECHA'])
data_ventas['month'] = data_ventas['FECHA'].dt.month
# data_ventas['VENTA'] = data_ventas['VENTA'].astype(int)
# data_ventas.options.display.float_format = {}

# ventas totales por mes
# print(data_ventas.columns)
ventas_total_por_mes = pd.pivot_table(data_ventas,
                                      values='VENTA',
                                      index='month',
                                      aggfunc='sum')
ventas_total_por_mes['VENTA'] = ventas_total_por_mes['VENTA'].astype(int)

# ventas cierre de trato
cierre_trato_df = data_ventas[data_ventas['TIPO VENTA'] == 'CIERRE DE TRATO']
ventas_cierre_trato = cierre_trato_df['VENTA'].sum() # obteniendo total de ventas por cierre de trato
ventas_cierre_trato_pivot = pd.pivot_table(cierre_trato_df, 
                                           values='VENTA', 
                                           index='month', 
                                           aggfunc="sum",)
ventas_cierre_trato_pivot['VENTA'] = ventas_cierre_trato_pivot['VENTA'].astype(int)

# ventas diseño entrega a cliente
entrega_diseño_df = data_ventas[data_ventas['TIPO VENTA'] == 'ENTREGA DISEÑO']
ventas_entrega_diseño = entrega_diseño_df['VENTA'].sum()
ventas_entrega_diseño_pivot = pd.pivot_table(entrega_diseño_df,
                                             values='VENTA',
                                             index='month',
                                             aggfunc="sum")
ventas_entrega_diseño_pivot['VENTA'] = ventas_entrega_diseño_pivot['VENTA'].astype(int)

# ventas inicio producción
inicio_prod_df = data_ventas[data_ventas['TIPO VENTA'] == 'INICIO PRODUCCIÓN']
ventas_inicio_prod = inicio_prod_df['VENTA'].sum() # obteniendo total de ventas por inicio producción
ventas_inicio_prod_pivot = pd.pivot_table(inicio_prod_df,
                                          values='VENTA',
                                          index='month',
                                          aggfunc='sum')
ventas_inicio_prod_pivot['VENTA'] = ventas_inicio_prod_pivot['VENTA'].astype(int)

# ventas inicio instalación
inicio_instal_df = data_ventas[data_ventas['TIPO VENTA'] == 'INICIO INSTALACIÓN']
ventas_inicio_instal = inicio_instal_df['VENTA'].sum()
ventas_inicio_instal_pivot = pd.pivot_table(inicio_instal_df,
                                            values='VENTA',
                                            index='month',
                                            aggfunc='sum')
ventas_inicio_instal_pivot['VENTA'] = ventas_inicio_instal_pivot['VENTA'].astype(int)

# ventas finalización
finalizacion_df = data_ventas[data_ventas['TIPO VENTA'] == 'FINALIZACIÓN']
ventas_finalizacion = finalizacion_df['VENTA'].sum()
ventas_finalizacion_pivot = pd.pivot_table(finalizacion_df,
                                           values='VENTA',
                                           index='month',
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
data_diseño_entrega_cliente_24['month'] = data_diseño_entrega_cliente_24['Fecha'].dt.month
diseño_pivot = pd.pivot_table(data_diseño_entrega_cliente_24, values='ML Realizados', index='month', aggfunc="sum")
diseño_pivot['ML Realizados'] = diseño_pivot['ML Realizados'].astype(int)

# diseño entrega a producción
filtro_entrega_produccion = data_diseño['Proceso'] == 'Producción'
data_diseño_entrega_produccion = data_diseño.loc[filtro_entrega_produccion]
data_diseño_entrega_produccion['Fecha'] = pd.to_datetime(data_diseño_entrega_produccion['Fecha'])
data_diseño_entrega_produccion_24 = data_diseño_entrega_produccion[data_diseño_entrega_produccion['Fecha'].dt.year == 2024]
data_diseño_entrega_produccion_24['month'] = data_diseño_entrega_produccion_24['Fecha'].dt.month
diseño_pivot_prod = pd.pivot_table(data_diseño_entrega_produccion_24, values='ML Realizados', index='month', aggfunc='sum')
diseño_pivot_prod['ML Realizados'] = diseño_pivot_prod['ML Realizados'].astype(int)


## Egresos
data_egresos = pd.read_excel('./datasets/egresos_vori_vost_2024.xlsx')
data_egresos['Fecha'] = pd.to_datetime(data_egresos['Fecha'])
data_egresos['mes'] = data_egresos['Fecha'].dt.month.map(meses_español)

filtro_egresos_admin = data_egresos['Categoría'] == 'GTO_ADMON'
data_egresos_gto_admin = data_egresos.loc[filtro_egresos_admin]

filtro_egresos_gto_oper = data_egresos['Categoría'] == 'GTO_OPERATIVO'
data_egresos_gto_oper = data_egresos.loc[filtro_egresos_gto_oper]

gto_oper_pivot = pd.pivot_table(data_egresos_gto_oper,
                                values='Monto',
                                index='Subcategoría',
                                columns='mes',
                                aggfunc='sum')

gto_admon_pivot = pd.pivot_table(data_egresos_gto_admin,
                                 values='Monto',
                                 index='Subcategoría',
                                 columns='mes',
                                 aggfunc='sum')


## Comisiones MP

filtro_gto_oper_comisiones_mp = data_egresos_gto_admin['Subcategoría'] == 'COMISIONES OTRO MP'
data_egresos_gto_admin_comisiones_mp = data_egresos_gto_admin.loc[filtro_gto_oper_comisiones_mp]
data_egresos_gto_admin_comisiones_mp['month'] = data_egresos_gto_admin_comisiones_mp['Fecha'].dt.month

## IMSS/INFONAVIT/FONACOT
filtro_imss = data_egresos_gto_admin['Subcategoría'] == 'IMSS/INFONAVIT/FONACOT'
egresos_admin_imss = data_egresos_gto_admin.loc[filtro_imss]
egresos_admin_imss['month'] = egresos_admin_imss['Fecha'].dt.month

## Finiquito/PrimaVacacional
filtro_finiquito = data_egresos_gto_admin['Subcategoría'] == 'FINIQUITO/PRIMA VACACIONAL'
egresos_finiquitos = data_egresos_gto_admin.loc[filtro_finiquito]
egresos_finiquitos['month'] = egresos_finiquitos['Fecha'].dt.month

## Oficinas
filtro_oficinas = data_egresos_gto_admin['Subcategoría'] == 'OFICINAS'
egresos_oficinas = data_egresos_gto_admin.loc[filtro_oficinas]
egresos_oficinas['month'] = egresos_oficinas['Fecha'].dt.month

## Bonos
filtro_bonos_admin = data_egresos_gto_admin['Subcategoría'] == 'BONOS'
bonos_admin = data_egresos_gto_admin.loc[filtro_bonos_admin]
bonos_admin['month'] = bonos_admin['Fecha'].dt.month

## Gasolina
filtro_gasolina = data_egresos_gto_oper['Subcategoría'] == 'GASOLINA'
gasolina = data_egresos_gto_oper.loc[filtro_gasolina]
gasolina['month'] = gasolina['Fecha'].dt.month

## Servicio autos
filtro_servicio_autos = data_egresos_gto_oper['Subcategoría'] == 'SERVICIOS AUTOS'
servicio_autos = data_egresos_gto_oper.loc[filtro_servicio_autos]
servicio_autos['month'] = servicio_autos['Fecha'].dt.month
## horas extras
horas_extras = pd.read_excel('./datasets/horas_extras_2024.xlsx')

## Función para aplicar formato condicional
def apply_color(val):
    color = 'background-color: {}'.format('#ff9999') if val < 200 else ('background-color: {}'.format('#99ff99') if val > 400 else 'background-color: {}'.format('#ffff99'))
    return color

# aplicar el formato condicional por filas
def magnify():
    return [dict(selector="th",
                 props=[("font-size", "4pt")]),
            dict(selector="td",
                 props=[('padding', "0em 0em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '12pt')])
]

## Producción
data_prod = pd.read_excel('./datasets/produccion.xlsx')
data_prod['Fecha'] = pd.to_datetime(data_prod['Fecha'])
data_prod_2024 = data_prod[data_prod['Fecha'].dt.year == 2024]
data_prod_2024['month'] = data_prod_2024['Fecha'].dt.month
data_prod_2024_real = data_prod_2024[data_prod_2024['Fecha'].dt.month >= 4]

if page == 'Datos Financieros':
    financieros = ['Ventas', 'Control de gastos', 'Estado de Resultados']
    st.subheader(page)
    financial_option = st.radio('Menu' ,financieros, label_visibility='collapsed', index=None)
    if financial_option == 'Ventas':
        st.subheader('Ventas', divider='blue')
        fig6 = px.bar(ventas_total_por_mes, 
                      y = 'VENTA',
                      title='Total Ventas 2024', 
                      text='VENTA',
                      labels={ 'VENTA': 'ventas',
                              'month': 'mes'},)
        fig6.update_layout(yaxis=dict(showgrid=False))
        fig6.update_traces(textposition='outside')
        st.plotly_chart(fig6)
        ventas_total_por_mes

        st.write('Ventas por **Cierre de Trato**: ', ventas_cierre_trato.astype(int))
        fig = px.line(ventas_cierre_trato_pivot, 
                      y='VENTA', 
                      title='Ventas Cierre Trato', 
                      markers=True, 
                      line_shape='spline', 
                      text='VENTA',
                      labels={'month': 'mes',
                              'VENTA': 'ventas'})
        fig.update_layout(yaxis=dict(showgrid=False))
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig)
        ventas_cierre_trato_pivot

        st.write('Ventas por **Entrega de Diseño**:', ventas_entrega_diseño.astype(int))
        fig2 = px.line(ventas_entrega_diseño_pivot, 
                       y='VENTA', 
                       title='Ventas Entrega Diseño', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig2.update_layout(yaxis=dict(showgrid=False))
        fig2.update_traces(textposition='top center')
        st.plotly_chart(fig2)
        ventas_entrega_diseño_pivot

        st.write('Ventas por **Inicio de Producción**:', ventas_inicio_prod.astype(int))
        fig3 = px.line(ventas_inicio_prod_pivot, 
                       y='VENTA', 
                       title='Ventas Inicio Producción', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig3.update_layout(yaxis=dict(showgrid=False))
        fig3.update_traces(textposition='top center')
        st.plotly_chart(fig3)
        ventas_inicio_prod_pivot

        st.write('Ventas por **Inicio de Instalación**:', ventas_inicio_instal.astype(int))
        fig4 = px.line(ventas_inicio_instal_pivot, 
                       y='VENTA', 
                       title='Ventas Inicio Instalación', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig4.update_layout(yaxis=dict(showgrid=False))
        fig4.update_traces(textposition='top center')
        st.plotly_chart(fig4)
        ventas_inicio_instal_pivot

        st.write('Ventas por **Finalización**:', ventas_finalizacion.astype(int))
        fig5 = px.line(ventas_finalizacion_pivot, 
                       y='VENTA', 
                       title='Ventas Finalización', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig5.update_layout(yaxis=dict(showgrid=False))
        fig5.update_traces(textposition='top center')
        st.plotly_chart(fig5)
        ventas_finalizacion_pivot
    if financial_option == 'Control de gastos':
        cat_gastos = ['Administrativos', 'Operativos']
        cat = st.radio('Gastos:', cat_gastos, index=None)
        if cat == 'Administrativos':
            # aplicar formato condicional por filas
            st.subheader('Gastos: Administrativos', divider='rainbow')
            st.dataframe(gto_admon_pivot, column_order=('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'))
            st.write('Comisiones MP:')
            comisiones_admin_mp = pd.pivot_table(data_egresos_gto_admin_comisiones_mp,
                                                 values='Monto',
                                                 index='month',
                                                 aggfunc='sum')
            fig8 = px.line(comisiones_admin_mp,
                           y='Monto',
                           title='Comisiones Otro MP',
                           markers=True,
                           line_shape='spline',
                           text='Monto')
            fig8.update_layout(yaxis=dict(showgrid=False))
            fig8.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig8)
            # mostrar tabla dinámica con totales
            comisiones_admin_mp_1 = pd.pivot_table(data_egresos_gto_admin_comisiones_mp,
                                                 values='Monto',
                                                 index='month',
                                                 aggfunc='sum',
                                                 margins=True,
                                                 margins_name='Total')
            comisiones_admin_mp_1
            st.write('IMSS/INFONAVIT:')
            imss_pivot = pd.pivot_table(egresos_admin_imss,
                                        values='Monto',
                                        index='month',
                                        aggfunc='sum')
            fig9 = px.line(imss_pivot,
                           y='Monto',
                           title='IMSS, INFONAVIT y FONACOT',
                           markers=True,
                           line_shape='spline',
                           text='Monto')
            fig9.update_layout(yaxis=dict(showgrid=False))
            fig9.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig9)
            # mostrar tabla dinámica con totales
            imss_pivot_1 = pd.pivot_table(egresos_admin_imss,
                                        values='Monto',
                                        index='month',
                                        aggfunc='sum',
                                        margins=True,
                                        margins_name='Total')
            imss_pivot_1
            st.write('Finiquitos/Primas:')
            finiquitos_pivot = pd.pivot_table(egresos_finiquitos,
                                              values='Monto',
                                              index='month',
                                              aggfunc='sum')
            fig10 = px.line(finiquitos_pivot,
                            y='Monto',
                           markers=True,
                           line_shape='spline',
                           text='Monto')
            fig10.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Finiquitos y Primas Vacacionales",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig10.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig10)
            # mostrar tabla dinámica con totales
            finiquitos_pivot_1 = pd.pivot_table(egresos_finiquitos,
                                              values='Monto',
                                              index='month',
                                              aggfunc='sum',
                                              margins=True,
                                              margins_name='Total')
            finiquitos_pivot_1
            st.write('Oficinas:')
            oficinas_pivot = pd.pivot_table(egresos_oficinas,
                                            values='Monto',
                                            index='month',
                                            aggfunc='sum')
            fig11 = px.line(oficinas_pivot,
                            y='Monto',
                            markers=True,
                            line_shape='spline',
                            text='Monto')
            fig11.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Gastos Oficinas",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig11.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig11)
            # mostrando tabla dinámica con totales totales
            oficinas_pivot_1 = pd.pivot_table(egresos_oficinas,
                                            values='Monto',
                                            index='month',
                                            aggfunc='sum',
                                            margins=True,
                                            margins_name='Total')
            oficinas_pivot_1
            st.write('Bonos:')
            bonos_admin_pivot = pd.pivot_table(bonos_admin,
                                               values='Monto',
                                               index='month',
                                               aggfunc='sum')
            fig12 = px.line(bonos_admin_pivot,
                            y='Monto',
                            markers=True,
                            line_shape='spline',
                            text='Monto')
            fig12.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Bonos Administrativos",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig12.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig12)
            # mostrando tabla dinámica con totales
            bonos_admin_pivot_1 = pd.pivot_table(bonos_admin,
                                               values='Monto',
                                               index='month',
                                               aggfunc='sum',
                                               margins=True,
                                               margins_name='Total')
            st.dataframe(bonos_admin_pivot_1)
        if cat == 'Operativos':
            st.dataframe(gto_oper_pivot, column_order=('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'))
            st.subheader('Gastos: Operativos', divider='green')
            st.write('Destajo')
            st.write('Horas Extras')
            horas_extras_pivot = pd.pivot_table(horas_extras,
                                                values='costo',
                                                index='semana',
                                                aggfunc='sum')
            fig7 = px.line(horas_extras_pivot,
                           y='costo',
                           markers=True, 
                           line_shape='spline')
            fig7.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Costo Horas Extras",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig7.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig7)
            horas_extras_pivot
            st.write('Gasolina')
            gasolina_pivot = pd.pivot_table(gasolina,
                                            values='Monto',
                                            index='month',
                                            aggfunc='sum')
            fig13 = px.line(gasolina_pivot,
                            y='Monto',
                            markers=True,
                            line_shape='spline',
                            text='Monto')
            fig13.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Gasolina",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig13.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig13)
            gasolina_pivot_1 = pd.pivot_table(gasolina,
                                              index='month',
                                              values='Monto',
                                              aggfunc='sum',
                                              margins=True,
                                              margins_name='Total')
            st.dataframe(gasolina_pivot_1)
            st.write('Servicios Autos')
            servicio_autos_pivot = pd.pivot_table(servicio_autos,
                                                  index='month',
                                                  values='Monto',
                                                  aggfunc='sum')
            fig14 = px.line(servicio_autos_pivot,
                            y='Monto',
                            markers=True,
                            line_shape='spline',
                            text='Monto')
            fig14.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Servicios de Autos",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig14.update_traces(textposition='top center', line=dict(color='#FF0000'))
            st.plotly_chart(fig14)
            # mostrando tabla dinámica con totales
            servicio_autos_pivot_1 = pd.pivot_table(servicio_autos,
                                              index='month',
                                              values='Monto',
                                              aggfunc='sum',
                                              margins=True,
                                              margins_name='Total')
            st.dataframe(servicio_autos_pivot_1)
            st.subheader('Costos de Retrabajos')
            st.write('No se puede obtener el costo de retrabajos')
    if financial_option == 'Estado de Resultados':
        st.subheader('Estado de Resultados', divider='red')
        st.image('./edo_resultados/edo_resultados_acum_mayo.png', caption='Estado de Resultados Mayo 2024')
if page == 'Datos Operativos':
    st.subheader(page)
    operativas = ['Diseño', 'Producción', 'Instalación']
    operation_option = st.radio('Menu', operativas, index=None, label_visibility='collapsed')
    if operation_option == 'Diseño':
        st.subheader('ML Entregados a Clientes', divider='green')
        fig15 = px.line(diseño_pivot,
                        y='ML Realizados',
                        markers=True,
                        line_shape='spline',
                        text='ML Realizados')
        fig15.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Metros Lineales Entregados a Clientes",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
        fig15.update_traces(textposition='top center', line=dict(color='#FF0000'))
        st.plotly_chart(fig15)
        diseño_pivot
        st.subheader('ML Entregados a Producción', divider='rainbow')
        fig16 = px.line(diseño_pivot_prod,
                        y='ML Realizados',
                        markers=True,
                        line_shape='spline',
                        text='ML Realizados')
        fig16.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Metros Lineales Entregados a Producción",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
        fig16.update_traces(textposition='top center', line=dict(color='#FF0000'))
        st.plotly_chart(fig16)
        diseño_pivot_prod
    if operation_option == 'Producción':
        st.subheader('Total Metros Lineales Producidos', divider='red')
        prod_pivot = pd.pivot_table(data_prod_2024_real,
                                    values='PRODUCIDOS',
                                    index='month',
                                    columns='Área',
                                    aggfunc='sum')
        fig17 = px.bar(prod_pivot,
                       y=['Entregable', 'Extras', 'Retrabajos'])
        fig17.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Total de ML Producidos",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
        fig17.update_traces(texttemplate='%{value}', textposition='inside')
        st.plotly_chart(fig17)
        # mostrando los totales de la tabla dinámica
        prod_pivot_1 = pd.pivot_table(data_prod_2024_real,
                                    values='PRODUCIDOS',
                                    index='month',
                                    columns='Área',
                                    aggfunc='sum',
                                    margins=all,
                                    margins_name='Total')
        st.dataframe(prod_pivot_1)
        st.write()
    if operation_option == 'Instalación':
        st.subheader('Datos de Instalación', divider='rainbow')