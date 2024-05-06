from flask import render_template, redirect, url_for


def init_views(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/match', methods=['POST'])
    def match_student():
        # Example of fetching data from forms, matching logic, etc.
        return redirect(url_for('index'))