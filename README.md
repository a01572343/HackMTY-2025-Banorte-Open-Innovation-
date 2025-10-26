Aliado Financiero Banorte es una aplicación con el propósito de ayudar a sus usuarios analizar su situación financiera y tomar decisiones respecto a ella. Esta hecha con el usuario y su comodidad en mente.

Al tener acceso a la información de su cuenta bancaria, la aplicación presenta sus datos de una manera de fácil comprensión y lectura, utilizando el apoyo de tablas y gráficas.

Adicionalmente, cuenta con el apoyo de un chatbot al cual el usuario puede consultar para cualquier duda que tenga respecto a su situación financiera actual y posibles decisiones futuras que considere tomar. La forma de hablar del chatbot pueden ser customizadas por el usuario escribiendole al chatbot la manera en la que deseas que este se comporte.

Por último, la aplicación cuenta con un simulador el cual permite al usuario visualizar el efecto sobre su economía que podrían tener ciertos eventos y decisiones.



GIT
El link para el repositorio github que contiene el código del programa, y cualquier posible actualización, es el siguiente.
	https://github.com/a01572343/HackMTY-2025-Banorte-Open-Innovation-.git

Para correr la aplicación, es importante configurar un entorno virtual e instalar varios paquetes y librerías. Los requerimientos de instalar son uvicorn, fastapi, pandas, google-generativeai, openpyxl, y python-dotenv. Para importarlos, ejecuta los siguientes comandos.

venv\Scripts\activate
pip install uvicorn fastapi pandas "google-generativeai" openpyxl python-dotenv

También es necesario configurar un servidor local en el sistema del entorno virtual, este debe localizarse en un servidor mcp para poder conectarse con los sistemas de IA. Para hacer esto, ejecuta los siguientes comandos, modificándolo a tu propia ubicación en el sistema.

	cd "C:\Users\name\mcp_server"
uvicorn main:app --reload

Finalmente, para ejecutar la aplicación, streamlit es necesario. Usando el sitio donde se encuentra ubicado el servidor mcp en el sistema, ejecuta el siguiente comando con tu propia ubicación.

	cd "C:\Users\name"
streamlit run app.py
