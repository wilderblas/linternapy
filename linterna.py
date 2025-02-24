import subprocess
import time
import json

def obtener_luz():
    try:
        resultado = subprocess.run(['termux-sensor', '-s', 'light', '-n', '1'], 
                                  capture_output=True, text=True)
        datos = json.loads(resultado.stdout)
        if 'LIGHT' in datos and 'values' in datos['LIGHT']:
            return datos['LIGHT']['values'][0]  # Tomamos el primer valor en lux
        else:
            print("No se obtuvieron datos del sensor de luz.")
            return None
    except Exception as e:
        print(f"Error al acceder al sensor: {e}")
        return None

def encender_linterna():
    subprocess.run(['termux-torch', 'on'])

def apagar_linterna():
    subprocess.run(['termux-torch', 'off'])

def main():
    umbral_luz = 50  # Nivel de luz en lux para considerar "oscuro"
    intervalo = 5  # Revisar cada 5 segundos
    linterna_encendida = False
    
    while True:
        nivel_luz = obtener_luz()
        if nivel_luz is None:
            print("No hay datos válidos del sensor. Terminando...")
            break
        
        print(f"Nivel de luz: {nivel_luz} lux")
        
        if nivel_luz < umbral_luz and not linterna_encendida:
            print("Oscuridad detectada. Encendiendo linterna...")
            encender_linterna()
            linterna_encendida = True
        elif nivel_luz >= umbral_luz and linterna_encendida:
            print("Luz detectada. Apagando linterna...")
            apagar_linterna()
            linterna_encendida = False
        
        time.sleep(intervalo)

if __name__ == "__main__":
    main()