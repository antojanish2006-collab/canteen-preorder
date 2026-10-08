from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from database.mongo import init_db
    init_db(app)

    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html'), 500

    @app.route('/')
    def index():
        from database.mongo import db
        if db is None:
            return render_template('index.html', popular_items=[], db_error=True)
            
        try:
            popular_items = list(db.menu_items.find({"is_available": True}).limit(3))
        except Exception:
            popular_items = []
        return render_template('index.html', popular_items=popular_items)

    @app.template_filter('sum')
    def sum_filter(iterable):
        return sum(iterable)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
