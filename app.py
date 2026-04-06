from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

stok = []
hareketler = []

HTML = """
<h1>Çiftçiler İHLAS</h1>

<h2>Mal Girişi</h2>
<form method="post" action="/giris">
<input name="urun" placeholder="Ürün">
<input name="kg" placeholder="Kg">
<input name="oda" placeholder="Oda">
<button>Kaydet</button>
</form>

<h2>Satış</h2>
<form method="post" action="/satis">
<input name="musteri" placeholder="Müşteri">
<input name="kg" placeholder="Kg">
<button>Satış Yap</button>
</form>

<h2>Stok</h2>
{% for s in stok %}
<p>{{s}}</p>
{% endfor %}
"""

@app.route("/")
def home():
    return render_template_string(HTML, stok=stok)

@app.route("/giris", methods=["POST"])
def giris():
    veri = request.form
    stok.append(f"{veri['urun']} - {veri['kg']}kg - Oda {veri['oda']}")
    return redirect("/")

@app.route("/satis", methods=["POST"])
def satis():
    veri = request.form
    hareketler.append(veri["musteri"])
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
