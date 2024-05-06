# Error en las órdenes

## Estructura del repo
```
│   README.md
│   .gitignore
|  build.sh
|  requirements.txt
|  config.py
|  utils.py
|  app.py
|  modeling.ipynb
└──/data
└──/venv
```

3. Levantar la aplicación
```console
    # Descargar python 3.8 
    $brew install python@3.8
    # Crear el ambiente virtual
    $ python3.8 -m venv venv
    # Activar el ambiente virtual
    $ source venv/bin/activate
    # Instalar las dependencias
    $ sh build.sh
    # Ejecutar la app
    $ streamlit run app.py --server.port 5000
```

4. Levantar la aplicación utilizando Docker
```console
    # Crear imagen
    $ docker build -t app_streamlit:1.0 .
    # Levantar aplicación
    $ docker run --name container -p 8500:8500 -it -v "(pwd):/app" app_streamlit:1.0
```    
