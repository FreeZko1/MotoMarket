from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from WEB import create_app
app = create_app()

# Nastavení úrovně logování
app.logger.setLevel(logging.INFO)

# Vytvoření handleru, který zapíše logy do souboru. Upravte cestu podle potřeby.
handler = RotatingFileHandler('application.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)

# Formát logování
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Přidání handleru do loggeru aplikace
app.logger.addHandler(handler)



if __name__ == '__main__':
    app.logger.info("unguje")
    app.run(debug=True,host='0.0.0.0',port=80)
