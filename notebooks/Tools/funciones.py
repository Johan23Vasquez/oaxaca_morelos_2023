import pandas as pd 
import matplotlib.pyplot as plt 
import xarray as xr 
from datetime import datetime, date, timedelta
import plotly.graph_objects as go


def inicializar_datasets(ruta):
    f = ruta
    
    return xr.open_dataset(f) 


def convertir_a_celsius(ds, variable="t2m"):
    """
    Agrega una nueva variable en grados Celsius
    al Dataset de ERA5.
    """
    
    ds = ds.copy()
    
    ds[f"{variable}_Celsius"] = ds[variable] - 273.15
    
    return ds



def grafica_promedio_std(ds, variable="t2m_Celsius"):
    """Esta función grafica el promedio, desviación estandar, mínimos y máximos de una variable en específico

    Args:
        ds (.nc): Archivo para extraer los datos a explorar
        variable (str, optional): Variable que se mostrará dentro de la gráfica. Defaults to "t2m_Celsius".
    """

    promedio = ds[variable].mean(
        dim=["latitude", "longitude"]
    )

    std = ds[variable].std(
        dim=["latitude", "longitude"]
    )

    minimo = ds[variable].min(
        dim=["latitude", "longitude"]
    )

    maximo = ds[variable].max(
        dim=["latitude", "longitude"]
    )

    # datos = ds[variable].stack(
    #     punto=("latitude", "longitude")
    # )

    fig = go.Figure()

    # for i in range(datos.sizes["punto"]):
    #     fig.add_trace(
    #         go.Scatter(
    #             x=datos.time.values,
    #             y=datos.isel(punto=i).values,
    #             mode="lines",
    #             line=dict(
    #                 color="rgba(100,100,100,0.1)",
    #                 width=1
    #             )
    #         )
    #     )

    fig.add_trace(
        go.Scatter(
            x=maximo.time.values,
            y=maximo.values,
            mode="lines",
            name="Máximo",
            line=dict(
                color="rgba(255,0,0,0.6)",
                width=1
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=minimo.time.values,
            y=minimo.values,
            mode="lines",
            name="Mínimo",
            line=dict(
                color="rgba(255,0,0,0.6)",
                width=1
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=promedio.time.values,
            y=(promedio + std).values,
            mode="lines",
            line=dict(width=0)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=promedio.time.values,
            y=(promedio - std).values,
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(0,100,255,0.3)",
            name="Desviación Estandar"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=promedio.time.values,
            y=promedio.values,
            mode="lines",
            line=dict(
                color="rgba(0,100,255,1)",
                width=3
            ),
            name="Promedio"
        )
    )

    fig.update_layout(
        title="Promedio, Mínimo, Máximo y Desviacion Estandar",
        xaxis_title="Tiempo",
        yaxis_title=variable,
    )

    fig.show()


# grafica_promedio_std(
#     oaxaca_2023,
#     "t2m_Celsius"

# )

def grafica_promedio_all(ds, variable="t2m_Celsius"):
    """Esta función grafica el promedio y todas los datos disponibles de una variable en específico

    Args:
        ds (.nc): Archivo para extraer los datos a explorar
        variable (str, optional): Variable que se mostrará dentro de la gráfica. Defaults to "t2m_Celsius".
    """

    promedio = ds[variable].mean(
        dim=["latitude", "longitude"]
    )

    datos = ds[variable].stack(
        punto=("latitude", "longitude")
    )

    fig = go.Figure()

    for i in range(datos.sizes["punto"]):
        fig.add_trace(
            go.Scatter(
                x=datos.time.values,
                y=datos.isel(punto=i).values,
                mode="lines",
                line=dict(
                    color="rgba(100,100,100,0.1)",
                    width=1
                )
            )
        )

        fig.add_trace(
        go.Scatter(
            x=promedio.time.values,
            y=promedio.values,
            mode="lines",
            line=dict(
                color="rgba(0,100,255,1)",
                width=3
            ),
            name="Promedio"
        )
    )

    fig.show()


# grafica_promedio_all(
#     oaxaca_2023,
#     "t2m_Celsius"

# )

def convertir_a_hora_local(ds, offset_utc):
    """Convierte timestamps de UTC a hora local.

    Args:
        ds (.nc): Archivo xarray para extraer la información
        offset_utc (int, optional): _description_. Defaults to -6.

    Returns:
        _type_: _description_
    """
    ds = ds.copy()
    ds = ds.assign_coords(
        time=ds.time + pd.Timedelta(hours=offset_utc)
    )
    return ds


def convertir_ssrd(ds, variable="ssrd"):
    """
    Convierte ssrd de ERA5 J/m2 a W/m2 promedio por hora.
    """
    ds = ds.copy()
    
    ds["ssrd_Wm2"] = ds["ssrd"] / 3600
    
    
    return ds



def heatmap_personalizado(ds, f1=None, f2=None, variable="t2m_Celsius", 
                titulo=None, unidad=""):
    """
    Mapa de calor horario por día para un rango de fechas.

    Args:
        ds: xarray.Dataset con coordenada time en hora local
        f1 (str): Fecha inicio. None = inicio del dataset
        f2 (str): Fecha fin . None = fin del dataset
        variable (str): Variable del dataset a graficar
        titulo (str): Título del gráfico (auto si None)
        unidad (str): Unidad para mostrar en hover
    """

    escala = [
        [0.0, "rgb(26,152,80)"],
        [0.5, "rgb(254,224,144)"],
        [1.0, "rgb(215,48,39)"]
    ]

    f1 = f1 if f1 is not None else str(ds.time.values[0])[:10]
    f2 = f2 if f2 is not None else str(ds.time.values[-1])[:10]

    if titulo is None:
        titulo = f"{variable} desde {f1} a {f2}"

    datos = ds[variable].mean(dim=["latitude", "longitude"])
    seleccion = datos.sel(time=slice(f1, f2))

    df = seleccion.to_dataframe(name="valor")

    df["fecha"] = df.index.date
    df["hora"] = df.index.hour

    heatmap = df.pivot_table(
        index="hora",
        columns="fecha",
        values="valor",
        aggfunc="mean"
    )

    fig = go.Figure(
        go.Heatmap(
            x=heatmap.columns,
            y=heatmap.index,
            z=heatmap.values,
            colorscale=escala,
            colorbar=dict(title=variable),
            hovertemplate=(
                "Día %{x}<br>"
                "Hora %{y}:00<br>"
                f"Valor %{{z:.2f}} {unidad}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=titulo,
        xaxis_title="Día del mes",
        yaxis_title="Hora del día",
        yaxis=dict(autorange="reversed")
    )

    fig.show()



def heatmap_mes(ds, mes, variable="t2m_Celsius"):
    """Esta función genera un mapa de calor que muestra la temperatura o cualquier variable
       seleccionada a lo largo de cada hora en cada dia de un mes seleccionado

    Args:
        ds (.nc): Archivo para extraer los datos a explorar
        mes (int): Número del mes que se necesita explorar 
        variable (str, optional): Variable que se mostrará en la gráfica. Defaults to "t2m_Celsius".
    """

    datos = ds[variable].mean(
        dim=["latitude", "longitude"]
    )

    seleccion_mes = datos.sel(
        time=datos.time.dt.month == mes
    )

    heatmap_diario = seleccion_mes.to_dataframe(name="temperatura")

    heatmap_diario["dia"] = heatmap_diario.index.day
    heatmap_diario["hora"] = heatmap_diario.index.hour


    heatmap = heatmap_diario.pivot(
        index="hora",
        columns="dia",
        values="temperatura"
    )

    escala_temperatura = [
        [0.0, "rgb(26,152,80)"],
        [0.5, "rgb(254,224,144)"],
        [1.0, "rgb(215,48,39)"]
    ]

    fig = go.Figure(
        go.Heatmap(
            x=heatmap.columns,
            y=heatmap.index,
            z=heatmap.values,
            colorscale=escala_temperatura,
            colorbar=dict(
                title="Temperatura"
            ),
            hovertemplate=
            "Día %{x}<br>" +
            "Hora %{y}:00<br>" +
            "Temperatura %{z:.2f} °C" +
            "<extra></extra>"
        )
    )

    fig.update_layout(
        title="Temperatura horaria por mes",
        xaxis_title="Día del mes",
        yaxis_title="Hora del día",
    )

    fig.show()





def graficar_area(ds, lat1, lat2, lon1, lon2, variable = "t2m_Celsius"):
    """Esta función grafica una variable especifica en un area seleccionada con latitud y longitud

    Args:
        ds (.nc): _description_
        lat1 (float | int): Latitud inicial (límite norte o superior del cuadro de recorte).
        lat2 (float | int): Latitud final (límite sur o inferior del cuadro de recorte).
        lon1 (float | int): Longitud inicial (límite oeste o izquierdo del cuadro de recorte).
        lon2 (float | int): Longitud final (límite este o derecho del cuadro de recorte).

        variable (str, optional): _description_. Defaults to "t2m_Celsius".
    """
    area = ds.sel(
    latitude=slice(lat1,lat2),
    longitude=slice(lon1,lon2)
    )
    

    promedio = ds[variable].mean(
        dim=["latitude", "longitude"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=promedio.time.values,
            y=promedio.values,
            mode="lines",
            line=dict(
                color="rgba(0,100,255,1)",
                width=3
            ),
            name="Promedio"
        )
    )
    
    fig.show()


def seleccionar_area(ds, lat1, lat2, lon1, lon2):
    """Esta funcion permite definir un area en especifico y guardarla como una variable para poder
       ser utilizada indepentemente del archivo del que provenga

    Args:
        ds (.nc): _description_
        lat1 (float | int): Latitud inicial (límite norte o superior del cuadro de recorte).
        lat2 (float | int): Latitud final (límite sur o inferior del cuadro de recorte).
        lon1 (float | int): Longitud inicial (límite oeste o izquierdo del cuadro de recorte).
        lon2 (float | int): Longitud final (límite este o derecho del cuadro de recorte).

    Returns:
        area: devuelve el area que engloban los puntos de latitud y longitud
    """
    area = ds.sel(
    latitude=slice(lat1,lat2),
    longitude=slice(lon1,lon2)
    )
    return area

