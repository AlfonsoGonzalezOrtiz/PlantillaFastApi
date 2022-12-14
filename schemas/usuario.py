def usuarioEntity(usuario) -> dict:
    return {
        "telefono" : usuario["telefono"],
        "alias" : usuario["alias"],
        "contactos" : usuario["contactos"]
    }

def usuariosEntity(usuarios) -> list:
    if usuarios != None:
        return [usuarioEntity(usuario) for usuario in usuarios ]
    return None

