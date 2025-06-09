# proyecto-final-ada
Proyecto Final Análisis y Diseño de  Algoritmos

## Pasos para bajar y ejecutar el proyecto
1. En la terminal ir a una carpeta para proyectos
2. Bajar el código: `git clone https://github.com/isaac-chido-one/proyecto-final-ada.git`
3. Ir a la carpeta del código: `cd proyecto-final-ada`
4. Iniciar el ambiente python: `python3 -m venv venv`
5. En linux entrar al ambiente python: `source venv/bin/activate`
6. En windows entrar al ambiente python: `venv\Scripts\activate`
7. Instalar dependencias: `pip install -r requirements.txt`
8. Ejecutar la aplicación: `python app.py`

Al finalizar la aplicación se guarda la información en formato json en el archivo `storage/vacancies.json`
Para visualizar la información guarda: `cat storage/vacancies.json | jq`
Listar dependencias: `pip freeze > requirements.txt`
