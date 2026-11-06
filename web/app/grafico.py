"""Gráfica PNG del panel de analítica (Matplotlib, sin JavaScript en el cliente)."""
from io import BytesIO

from matplotlib.figure import Figure


def _barras(ax, filas, clave, titulo, color):
    if not filas:
        ax.text(0.5, 0.5, "Sin datos todavía", ha="center", va="center", transform=ax.transAxes)
        ax.set_title(titulo)
        ax.set_axis_off()
        return
    etiquetas = [str(f[clave]) for f in filas]
    valores = [int(f["total"]) for f in filas]
    ax.bar(etiquetas, valores, color=color)
    ax.set_title(titulo)
    ax.set_ylabel("Peticiones")
    ax.yaxis.get_major_locator().set_params(integer=True)  # eje Y solo con enteros
    ax.tick_params(axis="x", labelrotation=25)
    ax.spines[["top", "right"]].set_visible(False)


def generar_grafico_png(estadisticas: dict) -> BytesIO:
    """Recibe el resultado de db.obtener_estadisticas() y devuelve un PNG en memoria."""
    fig = Figure(figsize=(10, 4), dpi=110)  # Figure() directa: sin estado global, segura con hilos
    ax1, ax2 = fig.subplots(1, 2)
    _barras(ax1, estadisticas.get("por_ciudad", []), "ciudad", "Peticiones por ciudad (top 5)", "#4f6bed")
    _barras(ax2, estadisticas.get("por_tipo", []), "tipo_turismo", "Peticiones por tipo de turismo", "#2bb59a")
    fig.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf