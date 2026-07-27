"""
test_temporizador.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor_matematico.temporizador import Temporizador


def test_buen_desempeno_baja_poco_el_tiempo():
    temp = Temporizador(tiempo_inicial=60, d=5, tiempo_minimo=15, tiempo_maximo=120)
    t1 = temp.siguiente_tiempo(pistas_usadas=0)  # p = 4 -> resta d*(4-4) = 0
    assert t1 == 60, f"Con 0 pistas usadas el tiempo no debería bajar, dio {t1}"
    print(f"Buen desempeño (0 pistas): T1 = {t1}s  (esperado 60s)")


def test_mal_desempeno_baja_mucho_el_tiempo():
    temp = Temporizador(tiempo_inicial=60, d=5, tiempo_minimo=15, tiempo_maximo=120)
    t1 = temp.siguiente_tiempo(pistas_usadas=4)  # p = 0 -> resta d*(4-0) = 20
    assert t1 == 40, f"Con 4 pistas usadas se esperaba 40s, dio {t1}"
    print(f"Mal desempeño (4 pistas): T1 = {t1}s  (esperado 40s)")


def test_no_baja_del_minimo():
    temp = Temporizador(tiempo_inicial=20, d=10, tiempo_minimo=15, tiempo_maximo=120)
    t1 = temp.siguiente_tiempo(pistas_usadas=4)  # 20 - 10*4 = -20 -> debe quedar en el mínimo
    assert t1 == 15, f"Se esperaba el piso de 15s, dio {t1}"
    print(f"Cota mínima respetada: T1 = {t1}s  (esperado 15s)")


def test_historial_de_niveles():
    temp = Temporizador(tiempo_inicial=60, d=5)
    for pistas in [0, 1, 2, 0, 4]:
        temp.siguiente_tiempo(pistas)
    print("Historial de tiempos por nivel:", temp.historial)
    assert len(temp.historial) == 6  # T0 + 5 niveles jugados


if __name__ == "__main__":
    test_buen_desempeno_baja_poco_el_tiempo()
    test_mal_desempeno_baja_mucho_el_tiempo()
    test_no_baja_del_minimo()
    test_historial_de_niveles()
    print("Todas las pruebas del temporizador pasaron correctamente.")
