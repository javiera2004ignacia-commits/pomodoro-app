import time
import os
from plyer import notification

# Función para mostrar el temporizador

def temporizador(minutos, mensaje):
    segundos = minutos * 60
    while segundos:
        mins, secs = divmod(segundos, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(timer, end="\r")
        time.sleep(1)
        segundos -= 1
    notification.notify(
        title="Pomodoro Timer",
        message=mensaje,
        timeout=5
    )
    print(f"\n🔔 ¡{mensaje}! 🔔\n")


def pomodoro(ciclos=4):
    for i in range(1, ciclos + 1):
        print(f"🍅 Pomodoro {i}")
        temporizador(25, "Fin del Pomodoro, toma un descanso")
        
        if i < ciclos:
            temporizador(5, "Descanso terminado, vuelve a trabajar")
        else:
            temporizador(15, "Ciclo completado, descansa más tiempo")

if __name__ == "__main__":
    pomodoro()
