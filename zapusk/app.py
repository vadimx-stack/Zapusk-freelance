from flask import Flask, render_template, url_for, redirect, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zapusk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    about = db.Column(db.Text, nullable=True)
    specialization = db.Column(db.String(200), nullable=True)
    rating = db.Column(db.Float, default=0)
    skills = db.relationship('Skill', secondary='user_skills', backref='users')
    reviews = db.relationship('Review', backref='freelancer', lazy=True, foreign_keys='Review.freelancer_id')
    avg_completion_time = db.Column(db.Float, default=0)
    projects = db.relationship('Project', backref='client', lazy=True, foreign_keys='Project.client_id')
    proposals = db.relationship('Proposal', backref='freelancer', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    freelancer = db.relationship('User', foreign_keys=[freelancer_id], backref='assigned_projects')
    project_skills = db.relationship('ProjectSkill', backref='project', lazy=True)
    proposals = db.relationship('Proposal', backref='project', lazy=True)
    files = db.relationship('ProjectFile', backref='project', lazy=True)
    
    @property
    def skills(self):
        return [ps.skill.name for ps in self.project_skills]

class ProjectSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    skill = db.relationship('Skill')

class ProjectFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project = db.relationship('Project', backref='reviews')
    client = db.relationship('User', foreign_keys=[client_id], backref='client_reviews')

@app.route('/')
def index():
    projects = Project.query.filter_by(status='open').order_by(Project.created_at.desc()).limit(6).all()
    return render_template('index.html', projects=projects)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user_exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if user_exists:
            flash('Пользователь с таким именем или email уже существует')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна! Теперь вы можете войти')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Проверьте свой email и пароль')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'client':
        projects = Project.query.filter_by(client_id=current_user.id).all()
        return render_template('client_dashboard.html', user=current_user, projects=projects)
    else:
        proposals = Proposal.query.filter_by(freelancer_id=current_user.id).all()
        projects = Project.query.filter_by(status='open').all()
        return render_template('freelancer_dashboard.html', user=current_user, proposals=proposals, projects=projects)

@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if current_user.role != 'client':
        flash('Только клиенты могут создавать проекты')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        budget = float(request.form.get('budget'))
        
        new_project = Project(
            title=title,
            description=description,
            budget=budget,
            client_id=current_user.id
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        flash('Проект успешно создан!')
        return redirect(url_for('dashboard'))
    
    return render_template('create_project.html')

@app.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_detail.html', project=project)

@app.route('/submit_proposal/<int:project_id>', methods=['GET', 'POST'])
@login_required
def submit_proposal(project_id):
    if current_user.role != 'freelancer':
        flash('Только фрилансеры могут подавать заявки')
        return redirect(url_for('dashboard'))
    
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        bid_amount = float(request.form.get('bid_amount'))
        description = request.form.get('description')
        
        new_proposal = Proposal(
            bid_amount=bid_amount,
            description=description,
            project_id=project.id,
            freelancer_id=current_user.id
        )
        
        db.session.add(new_proposal)
        db.session.commit()
        
        flash('Заявка успешно отправлена!')
        return redirect(url_for('dashboard'))
    
    return render_template('submit_proposal.html', project=project)

@app.route('/projects')
@login_required
def projects():
    projects = Project.query.filter_by(status='open').all()
    return render_template('projects.html', projects=projects)

@app.route('/view_proposals/<int:project_id>')
@login_required
def view_proposals(project_id):
    project = Project.query.get_or_404(project_id)
    
    if current_user.id != project.client_id:
        flash('У вас нет доступа к этой странице')
        return redirect(url_for('project_detail', project_id=project_id))
    
    proposals = Proposal.query.filter_by(project_id=project_id).all()
    return render_template('view_proposals.html', project=project, proposals=proposals)

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if current_user.id != project.client_id:
        flash('У вас нет доступа к редактированию этого проекта')
        return redirect(url_for('project_detail', project_id=project_id))
    
    if project.status != 'new' and project.status != 'open':
        flash('Можно редактировать только новые проекты')
        return redirect(url_for('project_detail', project_id=project_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        budget = float(request.form.get('budget'))
        
        project.title = title
        project.description = description
        project.budget = budget
        
        db.session.commit()
        
        flash('Проект успешно обновлен')
        return redirect(url_for('project_detail', project_id=project_id))
    
    return render_template('edit_project.html', project=project)

@app.route('/delete_project/<int:project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if current_user.id != project.client_id:
        flash('У вас нет доступа к удалению этого проекта')
        return redirect(url_for('project_detail', project_id=project_id))
    
    if project.status != 'new' and project.status != 'open':
        flash('Можно удалять только новые проекты')
        return redirect(url_for('project_detail', project_id=project_id))
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Проект успешно удален')
    return redirect(url_for('dashboard'))

@app.route('/mark_completed/<int:project_id>')
@login_required
def mark_completed(project_id):
    project = Project.query.get_or_404(project_id)
    
    if current_user.id != project.client_id:
        flash('У вас нет доступа к этому действию')
        return redirect(url_for('project_detail', project_id=project_id))
    
    if project.status != 'in-progress':
        flash('Только проекты в процессе выполнения можно отметить как завершенные')
        return redirect(url_for('project_details', project_id=project_id))
    
    project.status = 'completed'
    project.completed_at = datetime.utcnow()
    db.session.commit()
    
    flash('Проект успешно отмечен как завершенный')
    return redirect(url_for('project_details', project_id=project_id))

@app.route('/accept_proposal/<int:proposal_id>')
@login_required
def accept_proposal(proposal_id):
    proposal = Proposal.query.get_or_404(proposal_id)
    project = Project.query.get_or_404(proposal.project_id)
    
    if current_user.id != project.client_id:
        flash('У вас нет доступа к этому действию')
        return redirect(url_for('project_details', project_id=project.id))
    
    if project.status != 'new' and project.status != 'open':
        flash('Можно принимать заявки только на открытые проекты')
        return redirect(url_for('view_proposals', project_id=project.id))
    
    other_proposals = Proposal.query.filter(
        Proposal.project_id == project.id,
        Proposal.id != proposal.id
    ).all()
    
    for other_proposal in other_proposals:
        other_proposal.status = 'rejected'
    
    proposal.status = 'accepted'
    
    project.status = 'in-progress'
    project.freelancer_id = proposal.freelancer_id
    
    db.session.commit()
    
    flash('Заявка успешно принята, проект передан исполнителю')
    return redirect(url_for('project_details', project_id=project.id))

@app.route('/reject_proposal/<int:proposal_id>')
@login_required
def reject_proposal(proposal_id):
    proposal = Proposal.query.get_or_404(proposal_id)
    project = Project.query.get_or_404(proposal.project_id)
    
    if current_user.id != project.client_id:
        flash('У вас нет доступа к этому действию')
        return redirect(url_for('project_details', project_id=project.id))
    proposal.status = 'rejected'
    db.session.commit()
    
    flash('Заявка успешно отклонена')
    return redirect(url_for('view_proposals', project_id=project.id))

@app.route('/client/<int:user_id>')
def client_profile(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'client':
        flash('Пользователь не является заказчиком')
        return redirect(url_for('index'))
    
    projects = Project.query.filter_by(client_id=user_id).all()
    return render_template('client_profile.html', user=user, projects=projects)

@app.route('/freelancer/<int:user_id>')
def freelancer_profile(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'freelancer':
        flash('Пользователь не является фрилансером')
        return redirect(url_for('index'))
    
    proposals = Proposal.query.filter_by(freelancer_id=user_id).all()
    completed_projects = Project.query.join(Proposal).filter(
        Proposal.freelancer_id == user_id,
        Project.status == 'completed'
    ).all()
    
    return render_template('freelancer_profile.html', user=user, proposals=proposals, completed_projects=completed_projects)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)