from app import init_app
from flask import render_template, request, redirect, make_response, session, url_for, flash
from app.forms.forms import  LoginForm
import unittest

app = init_app()
todos = ['Actualizar software', 'Leer documentacion', 'Listar requerimientos']




@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('app/tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/inicio'))
    session['user_ip'] = user_ip
    return response


@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    username = session.get('username')
    user_ip = session.get('user_ip')
    login_form = LoginForm()

    context = {
        'todos': todos,
        'user_ip': user_ip,
        'login_form': login_form,
        'username': username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Usuario registrado con exito')
        return redirect(url_for('index'))

    return render_template('home.html', **context)


if __name__ == '__main__':
    app.run()
