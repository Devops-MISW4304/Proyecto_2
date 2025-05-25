import os
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

@app.cli.command('init_db')
def init_db_command():
    """Crea las tablas de la base de datos."""
    print("Creando tablas...")
    db.create_all()
    print("Tablas creadas.")
