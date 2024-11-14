from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from flask_security import current_user
from flask import redirect, url_for, request, render_template
from functools import wraps
from .db import db
from app.models.user import User, Role

# Create the Admin instance with the secure index view
class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not any(role.name == 'admin' for role in current_user.roles):
            return redirect(url_for('security.login'))

        # Get statistics for dashboard
        stats = {
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(active=True).count(),
            'total_roles': Role.query.count()
        }
        return self.render('admin/index.html', stats=stats)

# Initialize Admin with SecureAdminIndexView
admin = Admin(
    name='Admin Dashboard',
    template_mode='bootstrap4',
    index_view=SecureAdminIndexView(),
    base_template='admin/master.html'
)

# Custom ModelView with authentication
class SecureModelView(ModelView):
    def __init__(self, model, session, **kwargs):
        super(SecureModelView, self).__init__(model, session, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

    def render(self, template, **kwargs):
        # Add AdminLTE specific values
        kwargs['adminlte_theme'] = True
        return super(SecureModelView, self).render(template, **kwargs)

# Custom dashboard view
class DashboardView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/dashboard.html')

    def is_accessible(self):
        return current_user.is_authenticated and any(role.name == 'admin' for role in current_user.roles)

# User admin view
class UserAdmin(SecureModelView):
    column_list = ('username', 'email', 'active', 'roles', 'created_at', 'last_login_at')
    column_searchable_list = ('username', 'email')
    column_filters = ('active', 'roles', 'created_at', 'last_login_at')
    form_excluded_columns = ('password_hash', 'fs_uniquifier')
    can_create = True
    can_edit = True
    can_delete = True

# Role admin view
class RoleAdmin(SecureModelView):
    column_list = ('name', 'description')
    form_excluded_columns = ('users',)

def init_admin(app):
    admin.init_app(app)

    # Add views with unique endpoints
    admin.add_view(DashboardView(name='Dashboard', endpoint='admin_dashboard'))
    admin.add_view(UserAdmin(User, db.session, name='Users'))
    admin.add_view(RoleAdmin(Role, db.session, name='Roles'))
