from datetime import datetime
def mensajeEntity(mensaje) -> dict:
    return {
        "timestamp" : datetime.fromtimestamp(mensaje["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
        "origen" : mensaje["origen"],
        "destino" : mensaje["destino"],
        "texto" : mensaje["texto"],
    }


def mensajesEntity(mensajes) -> list:
    return [mensajeEntity(mensaje) for mensaje in mensajes ]


def convertirFecha(fecha: str):
    strDatetime = fecha.split("T");
    hora = strDatetime[1].split('.')[0]
    string = (strDatetime[0] + " " + hora)
    dt_object = datetime.strptime(string,"%Y-%m-%d %H:%M:%S") 

    return datetime.timestamp(dt_object)