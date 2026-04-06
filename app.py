from flask import Flask, request, redirect, render_template_string
from datetime import datetime

app = Flask(__name__)

stok = []
musteriler = {}
hareketler = []
odemeler = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Çiftçiler İHLAS</title>
<style>
body { font-family:Arial; background:#f5f5f5; padding:10px;}
h1 { color:#1F7A4C;}
.box { background:white; padding:15px; margin:10px 0; border-radius:10px;}
input { padding:10px; width:100%; margin:5px 0;}
button { background:#1F7A4C; color:white; padding:10px; border:none;}
</style>
</head>

<body>

<h1>Çiftçiler İHLAS</h1>

<div class="box">
<h3>📦 Mal Girişi</h3>
<form method="post" action="/giris">
<input name="urun" placeholder="Ürün">
<input name="cins" placeholder="Cins">
<input name="kg" placeholder="Kg">
<input name="oda" placeholder="Oda">
<button>Kaydet</button>
</form>
</div>

<div class="box">
<h3>📤 Satış</h3>
<form method="post" action="/satis">
<input name="musteri" placeholder="Müşteri">
<input name="urun" placeholder="Ürün">
<input name="kg" placeholder="Kg">
<input name="fiyat" placeholder="Fiyat">
<button>Satış Yap</button>
</form>
</div>

<div class="box">
<h3>💰 Ödeme</h3>
<form method="post" action="/odeme">
<input name="musteri" placeholder="Müşteri">
<input name="tutar" placeholder="Tutar">
<button>Ödeme Al</button>
</form>
</div>

<div class="box">
<h3>👤 Cari</h3>
{% for m, bakiye in musteriler.items() %}
<p>{{m}} : {{bakiye}} TL</p>
{% endfor %}
</div>

<div class="box">
<h3>📊 Stok</h3>
{% for s in stok %}
<p>{{s}}</p>
{% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, stok=stok, musteriler=musteriler)

@app.route("/giris", methods=["POST"])
def giris():
    v = request.form
    stok.append(f"{v['urun']} {v['cins']} - {v['kg']}kg (Oda {v['oda']})")
    return redirect("/")

@app.route("/satis", methods=["POST"])
def satis():
    v = request.form
    toplam = float(v["kg"]) * float(v["fiyat"])
    musteriler[v["musteri"]] = musteriler.get(v["musteri"], 0) + toplam
    hareketler.append(v)
    return redirect("/")

@app.route("/odeme", methods=["POST"])
def odeme():
    v = request.form
    musteriler[v["musteri"]] = musteriler.get(v["musteri"], 0) - float(v["tutar"])
    odemeler.append(v)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
