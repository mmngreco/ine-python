import requests
import pandas as pd
import numpy as np
from pandas.io import json


class INE:
    def __init__(self):
        """
        https://servicios.ine.es/wstempus/js/{idioma}/{función}/{input}[?parámetros]
        https://www.ine.es/dyngs/DataLab/manual.html?cid=47
        """
        idioma = "ES"
        self.endpoint = f"https://servicios.ine.es/wstempus/js/{idioma}"

    def set_language(self, language):
        """Set language.

        Parameters
        ----------
        language : str, {"ES", "EN"}
        """
        self.endpoint = f"https://servicios.ine.es/wstempus/js/{language}"

    def get_functions(self, function="OPERACIONES_DISPONIBLES"):
        """Get functions availables.
 
        Parameters
        ----------
        function : str
            Function can take below values:
            * Operaciones: OPERACIONES_DISPONIBLES, OPERACIÓN...
            * Variables: VARIABLES, VARIABLES_OPERACION...
            * Valores: VALORES_VARIABLES, VALORES_VARIABLEOPERACION...
            * Tablas: TABLAS_OPERACION, GRUPOS_TABLA...
            * Series: SERIE, SERIES_OPERACION...
            * Publicaciones: PUBLICACIONES, PUBLICACIONES_OPERACION...
            * Datos: DATOS_SERIE, DATOS_TABLA...

        Returns
        -------
        function : pandas.DataFrame
        """
        endpoint_function = f"{self.endpoint}/{function}"
        r = requests.get(endpoint_function, verify=False)
        r_dict = json.loads(r.text)
        return pd.DataFrame(r_dict)

    def get_input(self, input_str, **kwargs):
        """Get inputs.

        Principales identificadores de la base de datos Tempus3.

        * Ejemplo 1: Identificador del elemento operación estadística.
        Existen tres códigos para la identificación de la operación estadística
        "Índice de Precios de Consumo (IPC)":
            - código alfabético Tempus3 interno (IPC)
            - código numérico Tempus3 interno (Id=25)
            - código de la operación estadística en el Inventario de
              Operaciones Estadísticas (IOE30138)
            (Ver operaciones disponibles:
            https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES)
        * Ejemplo 2: Identificador de la variable "Provincias":
            - código numérico Tempus3 interno (Id=115)
            (Ver Variables: https://servicios.ine.es/wstempus/js/ES/VARIABLES)

        Identificador de las tablas PcAxis

        * Ejemplo 1: Identificador de la tabla "Gastos internos totales en
        actividades de I+D por años y sectores/unidad"
            - código alfanumérico PcAxis interno (Id=/t14/p057/a2016/l0/01001.px)
            (Ver Obtención del identificador de una tabla utilizando INEbase )

        Parameters
        ----------
        inputs : str
        kwargs : dict, optional

        See Also
        --------
        get_function
        """
        endpoint_input = f"{self.endpoint}/{input_str}"
        r = requests.get(endpoint_input, params=kwargs, verify=False)
        r_dict = json.loads(r.text)
        return r_dict

    def get_series(self, series, date=None, last=None, geo=None):
        """
        Parameters
        ----------
        input : str
        date : str, list or slice, optional
            Must pass a date in YYYYMMDD format.
        last : int
            Retrive the `last` values.
        geo : int, {1, 0}, optional
            To retrive geographical results.
        """
        params = dict()

        if isinstance(date, slice):
            init = date.start if date.start is not None else ""
            end = date.stop if date.stop is not None else ""
            date = f"{init}:{end}"
        elif isinstance(date, list):
            date = "&".join(["date={d}" for d in date])

        if date is not None:
            params.update(dict(date=date))
        if last is not None:
            params.update(dict(last=last))
        if geo is not None:
            params.update(dict(geo=geo))

        series_dict = self.get_input(f"DATOS_SERIE/{series}", **params)
        data = pd.DataFrame(series_dict["Data"])[["Fecha", "Valor"]]
        dtype = dict(Fecha="datetime64[ms]", Valor="float64")
        return data.astype(dtype).set_index("Fecha")



    def get_ipc(self, date=None, last=None, geo=None):
        if date is None:
            date = slice("20000101", None)
        return self.get_series("IPC206449", date, last, geo)

    def get_cntr2010(self, date=None, last=None, geo=None):
        return self.get_series(30024, date, last, geo)

    def get_tables():
        raise NotImplementedError

