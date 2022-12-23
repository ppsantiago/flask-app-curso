from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, validators
import mercadopago

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

class MercadoPagoClient:
    def __init__(self, access_token):
        self.access_token = access_token
        mercadopago.configure({
            'access_token': self.access_token
        })

class Usuario:
    def __init__(self, usuario, email, password):
        self.saldo = 0
        self.usuario = usuario
        self.email = email
        self.password = password

    def actualizar_saldo(self, monto):
        self.saldo += monto

class PagoForm(FlaskForm):
    email = StringField('Email del cliente', [validators.DataRequired(), validators.Email()])
    monto = FloatField('Monto del pago', [validators.DataRequired(), validators.NumberRange(min=1)])
    metodo_pago = StringField('Método de pago', [validators.DataRequired()])
    descripcion = StringField('Descripción del pago', [validators.DataRequired()])
    submit = SubmitField('Realizar pago')

@app.route('/realizar-pago', methods=['GET', 'POST'])
def realizar_pago():
    form = PagoForm()
    if form.validate_on_submit():
        # Obtener la información del formulario
        email = form.email.data
        monto = form.monto.data
        metodo_pago = form.metodo_pago.data
        descripcion = form.descripcion.data

        # Crear una instancia de MercadoPagoClient
        mercadopago_client = MercadoPagoClient('TU_CLAVE_DE_ACCESO')

        # Crear un usuario con la información del formulario
        usuario = Usuario(email, email, 'PASSWORD')

        # Procesar el pago y actualizar el saldo del usuario
        payment = procesar_pago(usuario, monto, metodo_pago, descripcion)
        if payment:
            return 'Pago realizado con éxito'
        else:
            return 'Error al realizar el pago'
    return render_template('realizar_pago.html', form=form)
