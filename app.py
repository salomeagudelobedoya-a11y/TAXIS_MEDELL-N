from flask import Flask, render_template_string, request, redirect, url_for
import json
import os
import shutil

app = Flask(__name__)
app.secret_key = "clave_super_segura"

ARCHIVO = "taxis.json"
DATA_FILE = ARCHIVO

# -------------------------
# (Opcional) Si subiste un logo al entorno:
# archivo subido: /mnt/data/taxis_medellin_logo.avif
# Para copiarlo a tu carpeta static (ejecuta en Python si lo necesitas):
# import shutil, os
# os.makedirs("static", exist_ok=True)
# shutil.copy("/mnt/data/taxis_medellin_logo.avif", "static/logo.avif")
#
# O en Windows CMD (ejemplo si el archivo está en Descargas):
# copy "C:\Users\Salomé\Downloads\logo.avif" "C:\Users\Salomé\TAXIS_MEDELLIN\static\logo.avif"
# -------------------------


# -------------------------
# Funciones auxiliares (JSON)
# -------------------------
def cargar_taxis():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def guardar_taxis(taxis):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(taxis, f, indent=4, ensure_ascii=False)


# ================================
# Estilos base y HTML del logo
# ================================
estilo_base = """
<style>
    body {
        font-family: Arial, sans-serif;
        background: #f5f6fa;
        padding: 30px;
        text-align: center;
        margin: 0;
    }
    h1, h2 {
        color: #222;
        margin-bottom: 25px;
    }
    .btn {
        display: block;
        width: 300px;
        margin: 12px auto;
        padding: 16px;
        background: #ffd000;
        border-radius: 12px;
        color: black;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: 0.18s;
    }
    .btn:hover {
        background: #ffef66;
    }
    .form-box {
        max-width: 520px;
        margin: 18px auto;
        background: white;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        text-align: left;
    }
    label { font-weight: bold; display:block; margin-top:8px; }
    input {
        width: 100%;
        padding: 12px;
        margin-top: 6px;
        margin-bottom: 12px;
        border-radius: 8px;
        border: 1px solid #d0d6dc;
        font-size: 15px;
    }
    .card {
        background: white;
        padding: 14px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 12px;
        text-align: left;
    }
</style>
"""

# HTML + CSS for floating logo (included into every template render)
logo_flotante_html = """
<style>
.logo-flotante {
    position: fixed;
    top: 16px;
    left: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: flotar 3s infinite ease-in-out;
    z-index: 9999;
    backdrop-filter: blur(4px);
    padding: 6px 8px;
    border-radius: 10px;
}
.logo-flotante img {
    width: 78px;
    height: 78px;
    object-fit: contain;
    border-radius: 10px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    background: rgba(255,255,255,0.05);
}
.logo-float-text {
    font-size: 16px;
    line-height: 1;
    color: #FFD400;
    font-weight: 700;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.logo-float-sub {
    font-size: 13px;
    color: #ffffffcc;
    font-weight: 600;
}
@keyframes flotar {
    0% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
    100% { transform: translateY(0); }
}
</style>

<div class="logo-flotante" aria-hidden="true">
    <img src="/static/logo.avif" alt="Logo Taxi Medellín">
    <div class="logo-float-text">
        <span>Llamar ya</span>
        <span class="logo-float-sub">☎️ 604 345 45 45</span>
    </div>
</div>
"""

# Helper to combine base + logo + page content
def page(content_html):
    return render_template_string(estilo_base + logo_flotante_html + content_html)


# -------------------------
# Rutas
# -------------------------
@app.route("/")
def inicio():
    return page("""
        <div style="margin-top:20px;">
            <h1>🚕 Bienvenido al Sistema de Taxis Medellín</h1>
            <a class="btn" href="/opciones">Entrar al Menú</a>
        </div>

        <div style="margin-top: 28px; text-align:center;">
            <video width="640" controls style="border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.12);">
                <source src="/static/presentación.mp4" type="video/mp4">
                Tu navegador no soporta el video.
            </video>
        </div>
    """)


@app.route("/opciones")
def opciones():
    return page("""
        <h2>Panel de Opciones</h2>
        <a class="btn" href="/solicitar_taxi">Solicitar Taxi</a>
        <a class="btn" href="/registrar_taxi">Registrar Taxi</a>
        <a class="btn" href="/consultar_taxis">Consultar Taxis</a>
        <a class="btn" href="/editar_taxi">Editar Información</a>
        <a class="btn" href="/eliminar_taxi">Eliminar Taxi</a>
        <a class="btn" href="/">Volver al Inicio</a>
    """)


@app.route("/registrar_taxi", methods=["GET", "POST"])
def registrar_taxi():
    if request.method == "POST":
        placa = request.form.get("placa","").strip()
        conductor = request.form.get("conductor","").strip()
        telefono = request.form.get("telefono","").strip()
        modelo = request.form.get("modelo","").strip()

        taxis = cargar_taxis()
        taxis.append({
            "placa": placa,
            "conductor": conductor,
            "telefono": telefono,
            "modelo": modelo
        })
        guardar_taxis(taxis)
        return page("""
            <h2>Taxi Registrado ✔</h2>
            <a class="btn" href="/opciones">Volver al Menú</a>
        """)

    return page("""
        <h2>Registrar Nuevo Taxi</h2>
        <form method="POST" class="form-box">
            <label>Placa:</label>
            <input name="placa" required>

            <label>Conductor:</label>
            <input name="conductor" required>

            <label>Teléfono:</label>
            <input name="telefono" required>

            <label>Modelo:</label>
            <input name="modelo" required>

            <button type="submit">Registrar</button>
        </form>
        <a class="btn" href="/opciones">Volver</a>
    """)


@app.route("/solicitar_taxi", methods=["GET", "POST"])
def solicitar_taxi():
    if request.method == "POST":
        direccion = request.form.get("direccion","").strip()
        return page(f"""
            <h2>Taxi solicitado a:</h2>
            <h3 style="color:#333;">{direccion}</h3>
            <a class="btn" href="/opciones">Volver al Menú</a>
        """)
    return page("""
        <h2>Solicitar Taxi</h2>
        <form method="POST" class="form-box">
            <label>Dirección de recogida:</label>
            <input name="direccion" required>
            <button type="submit">Solicitar</button>
        </form>
        <a class="btn" href="/opciones">Volver</a>
    """)


@app.route("/consultar_taxis")
def consultar_taxis():
    taxis = cargar_taxis()
    listado = ""
    if not taxis:
        listado = "<p>No hay taxis registrados.</p>"
    else:
        for t in taxis:
            listado += f"""
            <div class="card">
                <b>Placa:</b> {t.get('placa','')}<br>
                <b>Conductor:</b> {t.get('conductor','')}<br>
                <b>Teléfono:</b> {t.get('telefono','')}<br>
                <b>Modelo:</b> {t.get('modelo','')}
            </div>
            """
    return page(f"""
        <h2>Listado de Taxis 📋</h2>
        {listado}
        <a class="btn" href="/opciones">Volver</a>
    """)


@app.route("/editar_taxi", methods=["GET", "POST"])
def editar_taxi():
    taxis = cargar_taxis()
    if request.method == "POST":
        placa = request.form.get("placa","").strip()
        for taxi in taxis:
            if taxi.get("placa") == placa:
                taxi["conductor"] = request.form.get("conductor","").strip()
                taxi["telefono"] = request.form.get("telefono","").strip()
                taxi["modelo"] = request.form.get("modelo","").strip()
                guardar_taxis(taxis)
                return page("""
                    <h2>Taxi actualizado ✔</h2>
                    <a class="btn" href="/opciones">Volver</a>
                """)
        return page("""
            <h2>No existe esa placa ❌</h2>
            <a class="btn" href="/opciones">Volver</a>
        """)
    return page("""
        <h2>Editar Información del Taxi</h2>
        <form method="POST" class="form-box">
            <label>Placa:</label>
            <input name="placa" required>

            <label>Nuevo Conductor:</label>
            <input name="conductor" required>

            <label>Nuevo Teléfono:</label>
            <input name="telefono" required>

            <label>Nuevo Modelo:</label>
            <input name="modelo" required>

            <button type="submit">Actualizar</button>
        </form>
        <a class="btn" href="/opciones">Volver</a>
    """)


@app.route("/eliminar_taxi", methods=["GET", "POST"])
def eliminar_taxi():
    if request.method == "POST":
        placa = request.form.get("placa","").strip()
        taxis = cargar_taxis()
        nuevos = [t for t in taxis if t.get("placa") != placa]
        guardar_taxis(nuevos)
        return page("""
            <h2>Taxi eliminado ✔</h2>
            <a class="btn" href="/opciones">Volver</a>
        """)
    return page("""
        <h2>Eliminar Taxi</h2>
        <form method="POST" class="form-box">
            <label>Placa:</label>
            <input name="placa" required>
            <button type="submit">Eliminar</button>
        </form>
        <a class="btn" href="/opciones">Volver</a>
    """)


# -------------------------
# Ejecutar la app
# -------------------------
if __name__ == "__main__":
    # Asegúrate de tener static/logo.avif en tu carpeta de proyecto
    # Si quieres copiar el logo desde el path subido al entorno:
    # shutil.copy("/mnt/data/taxis_medellin_logo.avif", "static/logo.avif")
    app.run(debug=True)
