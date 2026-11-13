"""Pruebas de la práctica 3 (apartados b, c y e) con la API en marcha en localhost:8000.
Ejecutar:  python pruebas_p3.py
"""
import logging
from streamlit.testing.v1 import AppTest

logging.disable(logging.CRITICAL)


def run(titulo, setup=None, url=None):
    at = AppTest.from_file("streamlit_app.py", default_timeout=60).run()
    if url:
        at.sidebar.text_input[0].set_value(url)
    at.number_input[0].set_value(5.0)   # ingreso medio
    at.number_input[1].set_value(6.0)   # habitaciones
    if setup:
        setup(at)
    at.button[0].click().run()
    print(f"--- {titulo}")
    for m in at.metric:
        print(f"  {m.label}: {m.value}")
    if at.metric:
        print(f"  {at.caption[-1].value}")
    for e in at.error:
        print(f"  ERROR mostrado al usuario: {e.value}")


run("Prueba 1: petición válida")
run("Prueba 2: falta HouseAge (validación local, no se envía)",
    lambda at: at.sidebar.checkbox[0].check())
run("Prueba 3: falta HouseAge + saltar validación (la API responde 422)",
    lambda at: (at.sidebar.checkbox[0].check(), at.sidebar.checkbox[1].check()))
run("Prueba 4: URL de la API incorrecta", url="http://localhost:9999")
