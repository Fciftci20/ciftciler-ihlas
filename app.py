from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# VERİLER
stok = []
musteriler = {}
kasalar = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Çiftçiler İHLAS</title>

<style>
body {
    font-family: Arial;
    background: #f5f5f5;
    padding: 10px;
}

h1 {
    color: #1F7A4C;
}

.box {
    background: white;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
}

input {
    padding: 10px;
    width: 100%;
    margin: 5px 0;
}

button {
    background: #1F7A4C;
    color: white;
    padding: 10px;
    border: none;
}
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
<input name="oda" placeholder="Oda (1-22)">
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
<input name="kasa" placeholder="Kasa Adedi">
<canvas id="canvas" width="300" height="150" style="border:1px solid black;"></canvas>
<br>
<button type="button" onclick="temizle()">İmzayı Temizle</button>
<br><br>
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
{% for m, b in musteriler.items() %}
<p>{{m}} : {{b}} TL</p>
{% endfor %}
</div>

<div class="box">
<h3>📦 Kasa Durumu</h3>
{% for m, k in kasalar.items() %}
<p>{{m}} : {{k}} kasa</p>
{% endfor %}
</div>

<div class="box">
<h3>📊 Stok</h3>
{% for s in stok %}
<p>{{s}}</p>
{% endfor %}
</div>
<script>
let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");

let yaziyor = false;

canvas.onmousedown = () => yaziyor = true;
canvas.onmouseup = () => {
    yaziyor = false;
    ctx.beginPath();
};

canvas.onmousemove = (e) => {
    if(!yaziyor) return;
    ctx.lineWidth = 2;
    ctx.lineCap = "round";

    let rect = canvas.getBoundingClientRect();
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
};

function temizle(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, stok=stok, musteriler=musteriler, kasalar=kasalar)

@app.route("/giris", methods=["POST"])
def giris():
    v = request.form
    stok.append(f"{v['urun']} {v['cins']} - {v['kg']}kg (Oda {v['oda']})")
    return redirect("/")

@app.route("/satis", methods=["POST"])
def satis():
    v = request.form

    kg = float(v.get("kg", 0))
    fiyat = float(v.get("fiyat", 0))
    toplam = kg * fiyat

    musteri = v.get("musteri")

    # Para cari
    musteriler[musteri] = musteriler.get(musteri, 0) + toplam

    # Kasa cari
    kasa = int(v.get("kasa", 0) or 0)
    kasalar[musteri] = kasalar.get(musteri, 0) + kasa

    return redirect("/")

@app.route("/odeme", methods=["POST"])
def odeme():
    v = request.form
    musteri = v.get("musteri")
    tutar = float(v.get("tutar", 0))

    musteriler[musteri] = musteriler.get(musteri, 0) - tutar

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
