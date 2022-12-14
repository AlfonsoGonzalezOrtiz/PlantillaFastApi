## Instalación

Ejecutar en un cmd en el directorio donde tenemos la carpeta del proyecto descomprimida:

```sh
code .
```

Utilizar python version 3.10.6


Una vez que tenemos el Visual Studio Code cont todas las carpetas del proyecto abiertas, 
Abrimos un terminal dentro de Visual Studio Code y ejecutamos el siguiente comando:

```sh
pip install -r requirements.txt
```
## Ejecución  

Dentro del terminal de VSC:

```sh
python.exe -m uvicorn app:app --reload
```

## OPCIONAL entorno virtual


```sh
C:\Users\Cate\Desktop\EXAMEN-IW>activate

(base) C:\Users\Cate\Desktop\EXAMEN-IW>conda activate "c:\Users\Cate\Desktop\EXAMEN-IW\.conda"
``` 
El comando -> conda activate "c:\Users\Cate\Desktop\Template\.conda" va entre comillas
Donde c:\Users\Cate\Desktop\EXAMEN-IW es la ruta donde hemos descargado el fichero 

```sh
(c:\Users\Cate\Desktop\EXAMEN-IW\.conda) C:\Users\Cate\Desktop\EXAMEN-IW>pip install -r requirements.txt

(c:\Users\Cate\Desktop\EXAMEN-IW\.conda) C:\Users\Cate\Desktop\EXAMEN-IW>python.exe -m uvicorn app:app --reload
```

## Enlaces
https://examen-iw.vercel.app
https://examen-iw-jose-tapia-catena.vercel.app
https://examen-iw-git-main-jose-tapia-catena.vercel.app
