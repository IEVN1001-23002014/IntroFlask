import math
from flask import Flask, render_template , request
app=Flask(__name__)
@app.route('/')
def index():
    titulo="PWA"
    lista=["pedro","luis","pedro"]
    return render_template("index.html", titulo=titulo,lista=lista)
@app.route('/operasBas', methods=["GET","POST"])
def operasBas():
    n1=0
    n2=0
    res=0
    operacion=''
    if request.method== 'POST':
        n1=request.form.get('n1')
        n2=request.form.get('n2')
        operacion=request.form.get('operacion')
        if request.form.get('operacion')=='sumar':
            res=float(n1)+float(n2)
        elif request.form.get('operacion')=='restar':
            res=float(n1)-float(n2)
        elif request.form.get('operacion')=='multiplicar':
            res=float(n1)*float(n2)
    return render_template("operasBas.html",n1=n1,n2=n2,res=res)
@app.route("/distancia", methods=['GET', 'POST'])
def distancia():
    res = None
    if request.method == 'POST':
        x1 = request.form.get('x1')
        y1 = request.form.get('y1')
        x2 = request.form.get('x2')
        y2 = request.form.get('y2')

        # Imprime en la consola del CMD para verificar qué llega
        print(f'Recibido: x1={x1}, y1={y1}, x2={x2}, y2={y2}')

    if x1 and y1 and x2 and y2:
        try:
            x1, y1 = float(x1), float(y1)
            x2, y2 = float(x2), float(y2)
            res = round(math.hypot(x2 - x1, y2 - y1), 4)
            print(f'Resultado calculado: {res}')
        except ValueError:
            res = 'Error en los valores ingresados'

    return render_template("distancia.html",res=res)
@app.route("/hola")
def func():
    return "Hello ..."
@app.route("/user/<string:user>")
def func2(user):
    return "Hola: " + user
@app.route("/numero/<int:n>")
def func3(n):
    return "asies: {}".format(n)
@app.route("/user/<int:id>/<string:username>")
def func4(id,username):
    return "ID: {} nombre: {}".format(id,username)
@app.route("/suma/<float:n1>/<float:n2>")
def func5(n1,n2):
    return "la suma es: {}".format(n1+n2)

if __name__=="__main__":
    app.run(debug=True)