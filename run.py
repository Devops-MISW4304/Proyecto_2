import os
from app import create_app, db

app = create_app()

@app.cli.command('init_db')
def init_db_command():
    """Crea las tablas de la base de datos."""
    print("Creando tablas...")
    db.create_all()
    print("Tablas creadas.")
    
@app.route('/init_db')
def init_db_route():
    db.create_all()
    return "Tablas creadas."


