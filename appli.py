from flask import Flask , render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Configurer SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'      # Spécifie l'URL de connexion à la base de données (ici SQLite)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False            # Désactive le suivi des modifications pour optimiser les performances
db = SQLAlchemy(app)

# Définir un modèle
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)                # Définit les colonnes de la table. db.Integer : Pour les nombres entiers.
    title = db.Column(db.String(100), nullable=False)           # db.String(100) : Pour les chaînes de caractères (limitées ici à 100 caractères).
    completed = db.Column(db.Boolean, default=False)            # db.Boolean : Pour les valeurs booléennes.

    def __repr__(self):
        return f'<Task {self.title}>'

# Ajouter la page d’accueil 
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# -----------------------------------------------TERMINAL--------------------------------------------------------------- 
# Créer la base de données
# Sur le terminal :
# python
# >>> from app import db, app(si le fichier est autre que app)
# >>> with app.app_context():
# >>> ....db.create_all()                                        # /!\ bien mettre 4 espace pour bien indenter
# >>> ....print("Toutes les tables ont été crées avec succès !")
# -----------------------------------------------TERMINAL--------------------------------------------------------------- 

# # Opérations CRUD (Créer, Lire, Mettre à jour, Supprimer)

# Ajouter des données
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()
    return redirect('/')

# Lire des données (Récupère toutes les tâches)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return {task.id : task.title for task in tasks}

# Mettre à jour des données (Met à jour le statut d'une tâche)
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
    return redirect('/')

# Supprimer des données (supprime une tâche)
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

# finaliser l'app (pour run)
if __name__ == '__main__':
    app.run(debug=True)















