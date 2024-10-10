import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from calendar import month_name
import seaborn as sns

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

## Aplicar formato de moneda
# data_ventas['VENTA'] = data_ventas['VENTA'].apply(lambda x: '${:,.0f}'.format(x))
# data_ventas
# ventas totales por mes
# print(data_ventas.columns)
ventas_total_por_mes = pd.pivot_table(data_ventas,
                                      values='VENTA',
                                      index='month',
                                      aggfunc='sum')

ventas_total_por_mes_con_total = pd.pivot_table(data_ventas,
                                      values='VENTA',
                                      index='month',
                                      aggfunc='sum',
                                      margins=True,
                                      margins_name='Total')

# ventas cierre de trato
cierre_trato_df = data_ventas[data_ventas['TIPO VENTA'] == 'CIERRE DE TRATO']
ventas_cierre_trato = cierre_trato_df['VENTA'].sum() # obteniendo total de ventas por cierre de trato
ventas_cierre_trato_pivot = pd.pivot_table(cierre_trato_df, 
                                           values='VENTA', 
                                           index='month', 
                                           aggfunc="sum",)


# ventas diseño entrega a cliente
entrega_diseño_df = data_ventas[data_ventas['TIPO VENTA'] == 'ENTREGA DISEÑO']
ventas_entrega_diseño = entrega_diseño_df['VENTA'].sum()
ventas_entrega_diseño_pivot = pd.pivot_table(entrega_diseño_df,
                                             values='VENTA',
                                             index='month',
                                             aggfunc="sum")


# ventas inicio producción
inicio_prod_df = data_ventas[data_ventas['TIPO VENTA'] == 'INICIO PRODUCCIÓN']
ventas_inicio_prod = inicio_prod_df['VENTA'].sum() # obteniendo total de ventas por inicio producción
ventas_inicio_prod_pivot = pd.pivot_table(inicio_prod_df,
                                          values='VENTA',
                                          index='month',
                                          aggfunc='sum')


# ventas inicio instalación
inicio_instal_df = data_ventas[data_ventas['TIPO VENTA'] == 'INICIO INSTALACIÓN']
ventas_inicio_instal = inicio_instal_df['VENTA'].sum()
ventas_inicio_instal_pivot = pd.pivot_table(inicio_instal_df,
                                            values='VENTA',
                                            index='month',
                                            aggfunc='sum')


# ventas finalización
finalizacion_df = data_ventas[data_ventas['TIPO VENTA'] == 'FINALIZACIÓN']
ventas_finalizacion = finalizacion_df['VENTA'].sum()
ventas_finalizacion_pivot = pd.pivot_table(finalizacion_df,
                                           values='VENTA',
                                           index='month',
                                           aggfunc='sum')



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


## Filtrando Egresos por operativos y adminsitrativos
filtro_admon_oper = (data_egresos['Categoría'] == 'GTO_ADMON') | (data_egresos['Categoría'] == 'GTO_OPERATIVO')
data_admin_oper = data_egresos[filtro_admon_oper]
data_admin_oper['month'] = data_admin_oper['Fecha'].dt.month
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

## Destajo
destajo = pd.read_excel('./datasets/destajo.xlsx')
destajo['FECHA'] = pd.to_datetime(destajo['FECHA'])
destajo_2024 = destajo[destajo['FECHA'].dt.year == 2024]
destajo_2024['month'] = destajo['FECHA'].dt.month

## Producción
data_prod = pd.read_excel('./datasets/produccion.xlsx')
data_prod['Fecha'] = pd.to_datetime(data_prod['Fecha'])
data_prod_2024 = data_prod[data_prod['Fecha'].dt.year == 2024]
data_prod_2024['month'] = data_prod_2024['Fecha'].dt.month
data_prod_2024_real = data_prod_2024[data_prod_2024['Fecha'].dt.month >= 4]
data_prod_2024_real['PRODUCIDOS'] = data_prod_2024_real['PRODUCIDOS'].astype(int)

## Costo Materia Prima
cto_mp = pd.read_excel('./datasets/materia_prima.xlsx')
cto_mp['FECHA'] = pd.to_datetime(cto_mp['FECHA'])
cto_mp['mes'] = cto_mp['FECHA'].dt.month

if page == 'Datos Financieros':
    financieros = ['Ventas', 'Control de gastos', 'Estado de Resultados']
    st.subheader(page)
    financial_option = st.radio('Menu' ,financieros, label_visibility='collapsed', index=None)
    if financial_option == 'Ventas':
        st.subheader('Ventas', divider='green')
        fig6 = px.bar(ventas_total_por_mes, 
                      y = 'VENTA',
                      title='Total Ventas 2024', 
                      text='VENTA',
                      labels={ 'VENTA': 'ventas',
                              'month': 'mes'},
                    color_discrete_sequence=['green'])
        fig6.update_layout(yaxis=dict(showgrid=False))
        fig6.update_traces(textposition='outside',
                           texttemplate='$%{text:,.0f}')
        st.plotly_chart(fig6)
        ventas_total = ventas_total_por_mes['VENTA'].sum()
        ventas_total_formato = "${:,.0f}".format(ventas_total)
        st.write('Ventas totales 2024: ', ventas_total_formato)
        fig = px.line(ventas_cierre_trato_pivot, 
                      y='VENTA', 
                      title='Ventas Cierre Trato', 
                      markers=True, 
                      line_shape='spline', 
                      text='VENTA',
                      labels={'month': 'mes',
                              'VENTA': 'ventas'})
        fig.update_layout(yaxis=dict(showgrid=False))
        fig.update_traces(textposition='top center',
                          texttemplate='$%{text:,.0f}',
                          line=dict(color='#00FF00'))
        st.plotly_chart(fig)
        ventas_cierre_trato_total = ventas_cierre_trato_pivot['VENTA'].sum()
        ventas_cierre_trato_formato = "${:,.0f}".format(ventas_cierre_trato_total)
        st.write('Ventas totales por Cierre de Trato: ', ventas_cierre_trato_formato)
        fig2 = px.line(ventas_entrega_diseño_pivot, 
                       y='VENTA', 
                       title='Ventas Entrega Diseño', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig2.update_layout(yaxis=dict(showgrid=False))
        fig2.update_traces(textposition='top center',
                           texttemplate='$%{text:,.0f}',
                          line=dict(color='#00FF00'))
        st.plotly_chart(fig2)
        ventas_entrega_diseño_total = ventas_entrega_diseño_pivot['VENTA'].sum()
        ventas_entrega_diseño_formato = "${:,.0f}".format(ventas_entrega_diseño_total)
        st.write('Ventas totales por Entrega de Diseño: ', ventas_entrega_diseño_formato)

        fig3 = px.line(ventas_inicio_prod_pivot, 
                       y='VENTA', 
                       title='Ventas Inicio Producción', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig3.update_layout(yaxis=dict(showgrid=False))
        fig3.update_traces(textposition='top center',
                           texttemplate='$%{text:,.0f}',
                          line=dict(color='#00FF00'))
        st.plotly_chart(fig3)
        ventas_inicio_prod_total = ventas_inicio_prod_pivot['VENTA'].sum()
        ventas_inicio_prod_formato = "${:,.0f}".format(ventas_inicio_prod_total)
        st.write('Ventas totales por Inicio Producción: ', ventas_inicio_prod_formato)

        fig4 = px.line(ventas_inicio_instal_pivot, 
                       y='VENTA', 
                       title='Ventas Inicio Instalación', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig4.update_layout(yaxis=dict(showgrid=False))
        fig4.update_traces(textposition='top center',
                           texttemplate='$%{text:,.0f}',
                           line=dict(color='#00FF00'))
        st.plotly_chart(fig4)
        ventas_inicio_instal_total = ventas_inicio_instal_pivot['VENTA'].sum()
        ventas_inicio_instal_formato = "${:,.0f}".format(ventas_inicio_instal_total)
        st.write('Ventas totales por Inicio Instalación: ', ventas_inicio_instal_formato)

        fig5 = px.line(ventas_finalizacion_pivot, 
                       y='VENTA', 
                       title='Ventas Finalización', 
                       markers=True, 
                       line_shape='spline', 
                       text='VENTA',
                       labels={'month': 'meses',
                               'VENTA': 'ventas'})
        fig5.update_layout(yaxis=dict(showgrid=False))
        fig5.update_traces(textposition='top center',
                           texttemplate='$%{text:,.0f}',
                           line=dict(color='#00FF00'))
        st.plotly_chart(fig5)
        ventas_finalizacion_total = ventas_finalizacion_pivot['VENTA'].sum()
        ventas_finaizacion_formato = "${:,.0f}".format(ventas_finalizacion_total)
        st.write('Ventas totales por Finalización: ', ventas_finaizacion_formato)
        # añadiendo boxplots de las ventas residenciales y en serie
        st.divider()
        # obteniendo ventas residencial
        ventas_residencial = data_ventas[data_ventas['TIPO PROYECTO'] == 'RESIDENCIAL']
        ventas_serie = data_ventas[data_ventas['TIPO PROYECTO'] == 'SERIE']
        # boxplot ventas
        st.subheader('Distribución de ventas residenciales')
        caja, ax1 = plt.subplots()
        sns.boxplot(x='TIPO VENTA', y='VENTA', data=ventas_residencial)
        st.pyplot(caja)
        st.subheader('Distribución de ventas en serie')
        caja2, ax2 = plt.subplots()
        sns.boxplot(x='TIPO VENTA', y='VENTA', data=ventas_serie)
        st.pyplot(caja2)
    if financial_option == 'Control de gastos':
        cat_gastos = ['Administrativos y Operativos Acumulados' ,'Administrativos', 'Operativos']
        cat = st.radio('Gastos:', cat_gastos, index=None)
        if cat == 'Administrativos y Operativos Acumulados':
            # Apartado para visualizar gastos administrativos y operativos juntos
            gto_admon_oper_pivot = pd.pivot_table(data_admin_oper,
                                                  index='month',
                                                  values='Monto',
                                                  aggfunc='sum')
            st.subheader('Gastos **Administrativos y Operativos**:', divider='red')
            fig22 = px.line(gto_admon_oper_pivot,
                            y='Monto',
                            title='Gastos Acumulados',
                            markers=True,
                            line_shape='spline',
                            text='Monto',
                            labels={'month': 'meses'})
            fig22.update_layout(yaxis=dict(showgrid=False))
            fig22.update_traces(textposition='top center',
                           texttemplate='$%{text:,.0f}',
                           line=dict(color='#FF0000'))
            st.plotly_chart(fig22)
            # obteniendo total de gastos administrativos y operativos con formato
            gto_admon_oper__total = gto_admon_oper_pivot['Monto'].sum()
            gto_admon_oper_formato = "${:,.0f}".format(gto_admon_oper__total)
            st.write('Total de Gastos Administrativos y Operativos: ', gto_admon_oper_formato)
            # gráfico por categoría admin y operativo
            gto_admon_oper_div_pivot = pd.pivot_table(data_admin_oper,
                                                      index='month',
                                                      columns=['Categoría'],
                                                      values='Monto',
                                                      aggfunc='sum')
            fig23 = px.line(gto_admon_oper_div_pivot,
                            labels={'month': 'mes',
                                    'value': 'monto'},
                            markers=True,
                            title='Gastos Administrativos y Operativos')
            st.plotly_chart(fig23)
            # aplicando formato de moneda
            gto_admon_oper_div_pivot['GTO_ADMON'] = gto_admon_oper_div_pivot['GTO_ADMON'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_oper_div_pivot['GTO_OPERATIVO'] = gto_admon_oper_div_pivot['GTO_OPERATIVO'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_oper_div_pivot
            # nombre del dataframe filtrado por gto admin y oper: data_admin_oper
        if cat == 'Administrativos':
            # rellenando los valores None
            gto_admon_pivot['Enero'] = gto_admon_pivot['Enero'].fillna(0)
            gto_admon_pivot['Febrero'] = gto_admon_pivot['Febrero'].fillna(0)
            gto_admon_pivot['Marzo'] = gto_admon_pivot['Marzo'].fillna(0)
            gto_admon_pivot['Abril'] = gto_admon_pivot['Abril'].fillna(0)
            gto_admon_pivot['Mayo'] = gto_admon_pivot['Mayo'].fillna(0)
            gto_admon_pivot['Junio'] = gto_admon_pivot['Junio'].fillna(0)
            gto_admon_pivot['Julio'] = gto_admon_pivot['Julio'].fillna(0)
            gto_admon_pivot['Agosto'] = gto_admon_pivot['Agosto'].fillna(0)
            gto_admon_pivot['Septiembre'] = gto_admon_pivot['Septiembre'].fillna(0)
            # cambio porcentual 1
            gto_admon_pivot['%1'] = (gto_admon_pivot['Febrero'] / gto_admon_pivot['Enero']) -1
            gto_admon_pivot['%1'] = gto_admon_pivot['%1'].fillna(0)
            # cambio porcentual 2
            gto_admon_pivot['%2'] = (gto_admon_pivot['Marzo'] / gto_admon_pivot['Febrero']) -1
            gto_admon_pivot['%2'] = gto_admon_pivot['%2'].fillna(0)
            # cambio porcentual 3
            gto_admon_pivot['%3'] = (gto_admon_pivot['Abril'] / gto_admon_pivot['Marzo']) -1
            gto_admon_pivot['%3'] = gto_admon_pivot['%3'].fillna(0)
            # cambio porcentual 4
            gto_admon_pivot['%4'] = (gto_admon_pivot['Mayo'] / gto_admon_pivot['Abril']) -1
            gto_admon_pivot['%4'] = gto_admon_pivot['%4'].fillna(0)
            # cambio porcentual 5
            gto_admon_pivot['%5'] = (gto_admon_pivot['Junio'] / gto_admon_pivot['Mayo']) -1
            gto_admon_pivot['%5'] = gto_admon_pivot['%5'].fillna(0)
            # cambio porcentual 6
            gto_admon_pivot['%6'] = (gto_admon_pivot['Julio'] / gto_admon_pivot['Junio']) -1
            gto_admon_pivot['%6'] = gto_admon_pivot['%6'].fillna(0)
            # cambio porcentual 7
            gto_admon_pivot['%7'] = (gto_admon_pivot['Agosto'] / gto_admon_pivot['Julio']) -1
            gto_admon_pivot['%7'] = gto_admon_pivot['%7'].fillna(0)
            # cambio porcentual 8
            gto_admon_pivot['%8'] = (gto_admon_pivot['Septiembre'] / gto_admon_pivot['Agosto']) -1
            gto_admon_pivot['%8'] = gto_admon_pivot['%8'].fillna(0)
            # divisor
            st.subheader('Gastos: Administrativos', divider='red')
            # aplicando formato de moneda
            gto_admon_pivot = gto_admon_pivot[['Enero', 'Febrero', '%1', 'Marzo', '%2', 'Abril', '%3', 'Mayo', '%4', 'Junio', '%5', 'Julio', '%6', 'Agosto', '%7', 'Septiembre', '%8']]
            gto_admon_pivot['Enero'] = gto_admon_pivot['Enero'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['Febrero'] = gto_admon_pivot['Febrero'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%1'] = gto_admon_pivot['%1'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot['Marzo'] = gto_admon_pivot['Marzo'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%2'] = gto_admon_pivot['%2'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot['Abril'] = gto_admon_pivot['Abril'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%3'] = gto_admon_pivot['%3'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot['Mayo'] = gto_admon_pivot['Mayo'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%4'] = gto_admon_pivot['%4'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot['Junio'] = gto_admon_pivot['Junio'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%5'] = gto_admon_pivot['%5'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot['Julio'] = gto_admon_pivot['Julio'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%6'] = gto_admon_pivot['%6'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot['Agosto'] = gto_admon_pivot['Agosto'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%7'] = gto_admon_pivot['%7'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot['Septiembre'] = gto_admon_pivot['Septiembre'].apply(lambda x: '${:,.0f}'.format(x))
            gto_admon_pivot['%8'] = gto_admon_pivot['%8'].apply(lambda x: f'{x:.0%}')
            gto_admon_pivot
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
            fig8.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig8)
            # aplicando formato de moneda
            comisiones_admin_mp_total = comisiones_admin_mp['Monto'].sum()
            comisiones_admin_mp_formato = "${:,.0f}".format(comisiones_admin_mp_total)
            st.write('Costo total por Comisiones Otro MP: ', comisiones_admin_mp_formato)

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
            fig9.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig9)
            # aplicando formato de moneda
            imss_pivot_total = imss_pivot['Monto'].sum()
            imss_pivot_formato = "${:,.0f}".format(imss_pivot_total)
            st.write('Costo toal por IMSS, INFONAVIT y FONACOT: ', imss_pivot_formato)

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
            fig10.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig10)
            # aplicando formato de monda
            finiquitos_pivot_total = finiquitos_pivot['Monto'].sum()
            finiquitos_pivot_formato = "${:,.0f}".format(finiquitos_pivot_total)
            st.write('Costo total por Finiquito y Primas Vacacionales: ', finiquitos_pivot_formato)

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
            fig11.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig11)

            oficinas_pivot_total = oficinas_pivot['Monto'].sum()
            oficinas_pivot_formato = "${:,.0f}".format(oficinas_pivot_total)
            st.write('Costo total por Gastos de Oficina: ', oficinas_pivot_formato)

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
            fig12.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig12)

            bonos_admin_total = bonos_admin_pivot['Monto'].sum()
            bonos_admin_formato = "${:,.0f}".format(bonos_admin_total)
            st.write('Costo total por Bonos Administrativos: ', bonos_admin_formato)
        if cat == 'Operativos':
            gto_oper_pivot['Enero'] = gto_oper_pivot['Enero'].fillna(0)
            gto_oper_pivot['Febrero'] = gto_oper_pivot['Febrero'].fillna(0)
            gto_oper_pivot['Marzo'] = gto_oper_pivot['Marzo'].fillna(0)
            gto_oper_pivot['Abril'] = gto_oper_pivot['Abril'].fillna(0)
            gto_oper_pivot['Mayo'] = gto_oper_pivot['Mayo'].fillna(0)
            gto_oper_pivot['Junio'] = gto_oper_pivot['Junio'].fillna(0)
            gto_oper_pivot['Julio'] = gto_oper_pivot['Julio'].fillna(0)
            gto_oper_pivot['Agosto'] = gto_oper_pivot['Agosto'].fillna(0)
            gto_oper_pivot['Septiembre'] = gto_oper_pivot['Septiembre'].fillna(0)
            # cambio porcentual 1
            gto_oper_pivot['%1'] = (gto_oper_pivot['Febrero'] / gto_oper_pivot['Enero'] -1)
            gto_oper_pivot['%1'] = gto_oper_pivot['%1'].fillna(0)
            # cambio porcentual 2
            gto_oper_pivot['%2'] = (gto_oper_pivot['Marzo'] / gto_oper_pivot['Febrero'] -1)
            gto_oper_pivot['%2'] = gto_oper_pivot['%2'].fillna(0)
            # cambio porcentual 3
            gto_oper_pivot['%3'] = (gto_oper_pivot['Abril'] / gto_oper_pivot['Marzo'] -1)
            gto_oper_pivot['%3'] = gto_oper_pivot['%3'].fillna(0)
            # cambio porcentual 4
            gto_oper_pivot['%4'] = (gto_oper_pivot['Mayo'] / gto_oper_pivot['Abril'] -1)
            gto_oper_pivot['%4'] = gto_oper_pivot['%4'].fillna(0)
            # cambio porcentual 5
            gto_oper_pivot['%5'] = (gto_oper_pivot['Junio'] / gto_oper_pivot['Mayo'] -1)
            gto_oper_pivot['%5'] = gto_oper_pivot['%5'].fillna(0)
            # cambio porcentual 6
            gto_oper_pivot['%6'] = (gto_oper_pivot['Julio'] / gto_oper_pivot['Junio'] -1)
            gto_oper_pivot['%6'] = gto_oper_pivot['%6'].fillna(0)
            # cambio porcentual 7
            gto_oper_pivot['%7'] = (gto_oper_pivot['Agosto'] / gto_oper_pivot['Julio'] -1)
            gto_oper_pivot['%7'] = gto_oper_pivot['%7'].fillna(0)
            # cambio porcentual 8
            gto_oper_pivot['%8'] = (gto_oper_pivot['Septiembre'] / gto_oper_pivot['Agosto'] -1)
            gto_oper_pivot['%8'] = gto_oper_pivot['%8'].fillna(0)
            # reordenando el DataFrame
            gto_oper_pivot = gto_oper_pivot[['Enero', 'Febrero', '%1', 'Marzo', '%2', 'Abril', '%3', 'Mayo', '%4', 'Junio', '%5', 'Julio', '%6', 'Agosto', '%7', 'Septiembre', '%8']]
            # aplicando formato de moneda y porcentaje
            gto_oper_pivot['Enero'] = gto_oper_pivot['Enero'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['Febrero'] = gto_oper_pivot['Febrero'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%1'] = gto_oper_pivot['%1'].apply(lambda x: f'{x:.0%}')
            gto_oper_pivot['Marzo'] = gto_oper_pivot['Marzo'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%2'] = gto_oper_pivot['%2'].apply(lambda x: f'{x:.0%}')
            gto_oper_pivot['Abril'] = gto_oper_pivot['Abril'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%3'] = gto_oper_pivot['%3'].apply(lambda x: f'{x:.0%}')
            gto_oper_pivot['Mayo'] = gto_oper_pivot['Mayo'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%4'] = gto_oper_pivot['%4'].apply(lambda x: f'{x:.0%}')
            gto_oper_pivot['Junio'] = gto_oper_pivot['Junio'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%5'] = gto_oper_pivot['%5'].apply(lambda x: f'{x:.0%}')
            gto_oper_pivot['Julio'] = gto_oper_pivot['Julio'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%6'] = gto_oper_pivot['%6'].apply(lambda x: f'{x:.0%}')
            gto_oper_pivot['Agosto'] = gto_oper_pivot['Agosto'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%7'] = gto_oper_pivot['%7'].apply(lambda x: f'{x:.0%}')
            gto_oper_pivot['Septiembre'] = gto_oper_pivot['Septiembre'].apply(lambda x: '${:,.0f}'.format(x))
            gto_oper_pivot['%8'] = gto_oper_pivot['%8'].apply(lambda x: f'{x:.0%}')
            # mostrando el DataFrame
            gto_oper_pivot
            st.subheader('Gastos: Operativos', divider='red')

            cto_mp_pivot = pd.pivot_table(cto_mp,
                                          index='mes',
                                          values='MONTO',
                                          aggfunc='sum')
            fig24 = px.line(cto_mp_pivot,
                            y='MONTO',
                            markers=True,
                            line_shape='spline',
                            text='MONTO')
            fig24.update_layout(yaxis=dict(showgrid=False),
                                title={'text': "Costo Materia Prima",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'})
            fig24.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig24)
            cto_mp_pivot_total = cto_mp_pivot['MONTO'].sum()
            cto_mp_pivot_formato = "${:,.0f}".format(cto_mp_pivot_total)
            st.write('Costo total de Materia Prima: ', cto_mp_pivot_formato)

            costo_destajo = pd.pivot_table(destajo_2024,
                                           values='TOTAL DESTAJO',
                                           index='SEMANA',
                                           aggfunc='sum')
            fig19 = px.line(costo_destajo,
                            y='TOTAL DESTAJO',
                            markers=True,
                            line_shape='spline',
                            text='TOTAL DESTAJO')
            fig19.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Costo Destajo",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig19.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig19)
            # pivot con totales
            costo_destajo_1 = pd.pivot_table(destajo_2024,
                                           values='TOTAL DESTAJO',
                                           index='SEMANA',
                                           aggfunc='sum',
                                           margins=True,
                                           margins_name='Total')
            costo_destajo_1['TOTAL DESTAJO'] = costo_destajo_1['TOTAL DESTAJO'].apply(lambda x: '${:,.0f}'.format(x))
            costo_destajo_1

            horas_extras_pivot = pd.pivot_table(horas_extras,
                                                values='costo',
                                                index='semana',
                                                aggfunc='sum')
            fig7 = px.line(horas_extras_pivot,
                           y='costo',
                           markers=True, 
                           line_shape='spline',
                           text='costo')
            fig7.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Costo Horas Extras",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
            fig7.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig7)
 
            horas_extras_pivot_total = horas_extras_pivot['costo'].sum()
            horas_extras_pivot_formato = "${:,.0f}".format(horas_extras_pivot_total)
            st.write('Costo total de Horas Extras: ', horas_extras_pivot_formato)

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
            fig13.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig13)

            gasolina_pivot__total = gasolina_pivot['Monto'].sum()
            gasolina_pivot_formato = "${:,.0f}".format(gasolina_pivot__total)
            st.write('Costo total de Gasolina: ', gasolina_pivot_formato)
            
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
            fig14.update_traces(textposition='top center', line=dict(color='#FF0000'), texttemplate='$%{text:,.0f}')
            st.plotly_chart(fig14)
            # mostrando tabla dinámica con totales
 
            servicio_autos_pivot_total = servicio_autos_pivot['Monto'].sum()
            servicio_autos_pivot_formato = "${:,.0f}".format(servicio_autos_pivot_total)
            st.write('Costo total por Servicios de Autos: ', servicio_autos_pivot_formato)
    if financial_option == 'Estado de Resultados':
        st.subheader('Estado de Resultados', divider='red')
        st.image('./edo_resultados/edo_resultados_acum_septiembre.png', caption='Estado de Resultados Acumulado 2024')
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
        # obteniendo el total de ML
        diseño_pivot_total = diseño_pivot['ML Realizados'].sum()
        # dando formato al total de ML
        diseño_pivot_format = "{:,.0f}".format(diseño_pivot_total)
        st.write('ML Totales Entregados a Clientes: ', diseño_pivot_format)
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
        diseño_pivot_prod_total = diseño_pivot_prod['ML Realizados'].sum()
        diseño_pivot_prod_format = "{:,.0f}".format(diseño_pivot_prod_total)
        st.write('ML Totales Entregados a Producción: ', diseño_pivot_prod_format)
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
        st.subheader('Correlación Horas Extras y ML Producidos')
        prod_sem_14 = data_prod_2024_real[data_prod_2024_real['Semana'] >= 14]
        prod_sem_14_pivot = pd.pivot_table(prod_sem_14,
                                            values='PRODUCIDOS',
                                            index='Semana',
                                            aggfunc='sum')
        prod_sem_14_pivot.rename_axis('semana', inplace=True)
        horas_extras_sem_14 = horas_extras[horas_extras['semana'] >= 14]
        horas_extras_sem_14_pivot = pd.pivot_table(horas_extras_sem_14,
                                            values='costo',
                                            index='semana',
                                            aggfunc=sum)
        correlacion_hrs_prod = pd.merge(prod_sem_14_pivot, horas_extras_sem_14_pivot, on='semana')
        correlacion_hrs_prod = correlacion_hrs_prod.rename(columns={'costo': 'Costo Hrs Extras',
                                                                    'PRODUCIDOS': 'ML Producidos'})
        #correlation_matrix = correlacion_hrs_prod.corr()
        # Selecciona las variables del DataFrame
        x_col = st.selectbox("Selecciona la columna para el eje X:", correlacion_hrs_prod.columns)
        y_col = st.selectbox("Selecciona la columna para el eje Y:", correlacion_hrs_prod.columns)
        # Creando gráfico
        fig, ax = plt.subplots()
        sns.scatterplot(x=correlacion_hrs_prod[x_col], y=correlacion_hrs_prod[y_col], ax=ax, palette='viridis')
        st.pyplot(fig)
        correlacion_hrs_prod
    if operation_option == 'Instalación':
        st.subheader('Datos de Instalación', divider='rainbow')
        destajo_3 = pd.pivot_table(destajo_2024,
                                   index='SEMANA',
                                   values=['ML', 'PZAS', 'DIA'],
                                   aggfunc='sum')
        fig21 = px.bar(destajo_3,
                       y=['ML', 'PZAS', 'DIA'],
                       barmode='group')
        fig21.update_layout(yaxis=dict(showgrid=False),
                                title={
                                    'text': "Total de Trabajo de Instalación",
                                    'y': 0.9,  # Alineación vertical
                                    'x': 0.5,  # Alineación horizontal
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                })
        fig21.update_traces( textposition='inside')
        st.plotly_chart(fig21)
        destajo_pivot_1 = pd.pivot_table(destajo_2024,
                                       index='SEMANA',
                                       values=['ML', 'PZAS', 'DIA'],
                                       aggfunc='sum',
                                       margins=all,
                                       margins_name='Total')
        destajo_pivot_1['ML'] = destajo_pivot_1['ML'].apply(lambda x: '{:,.0f}'.format(x))
        destajo_pivot_1['DIA'] = destajo_pivot_1['DIA'].apply(lambda x: '{:,.0f}'.format(x))
        destajo_pivot_1['PZAS'] = destajo_pivot_1['PZAS'].apply(lambda x: '{:,.0f}'.format(x))
        destajo_pivot_1
        destajo_3_total = destajo_3['DIA'] + destajo_3['ML'] + destajo_3['PZAS']
        destajo_3_total.name = 'total_instalado'
        costo_destajo_semana = pd.pivot_table(destajo_2024,
                                        index='SEMANA',
                                        values='TOTAL DESTAJO',
                                        aggfunc='sum')
        costo_instal_destajo = pd.merge(costo_destajo_semana, destajo_3_total, on='SEMANA')
        costo_instal_destajo = costo_instal_destajo.rename(columns={'TOTAL DESTAJO': 'Costo Destajo',
                                        'total_instalado': 'ML, Días y Pzas Instaladas'})
        x_col = st.selectbox("Selecciona la columna para el eje X:", costo_instal_destajo.columns)
        y_col = st.selectbox("Selecciona la columna para el eje Y:", costo_instal_destajo.columns)
        # Creando gráfico
        fig, ax = plt.subplots()
        sns.scatterplot(x=costo_instal_destajo[x_col], y=costo_instal_destajo[y_col], ax=ax, palette='viridis')
        st.pyplot(fig)
        costo_instal_destajo
