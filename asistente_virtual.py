import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # infromar que comenzo la grabacion
        print("ya puedes hablar")

        # guaradar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-mx")

            # prueba de que pudo ingresar
            print("dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de no comprender el audio
        except sr.UnknownValueError:
            # prueba de que no comprendio el audio
            print("Ups no entendí")

            # devolver error
            return "Sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:
            # prueba de que no comprendio el audio
            print("Ups no hay servicio")

            # devolver error
            return "Sigo esperando"

        # error inesperado
        except:
            # prueba de que no comprendio el audio
            print("Ups algo ha salido mal")

            # devolver error
            return "Sigo esperando"


# listado de voces / idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje, voz):
    # enceder el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', voz)
    # pronunciar el mensaje
    engine.say(mensaje)
    engine.runAndWait()

    # esto es para ver el listado de voces
    """
    engine = pyttsx3.init()
    for voz in engine.getProperty('voices'):
    print(voz)
    """


# informar el dia de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana
    dia_semana = dia.weekday()

    # diccionario con el nombre de los dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # decir el dia de la semana
    hablar(f"Hoy es {calendario[dia_semana]}", id1)


# informar que hora es
def pedir_hora():

    # crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora_modificada = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    hablar(hora_modificada, id1)


# funcion saludo inicial
def saludo_inicial(nombre):
    momento = ''

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour >= 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buenos dias"
    elif 13 < hora.hour < 20:
        momento = "Buenas tardes"

    # decir saludo
    saludo = f'{momento} {nombre}, soy Sabina tu asistente de voz personal. Por favor dime en que te puedo ayudar'
    hablar(saludo, id1)


# Pedir nombre
def pedir_nombre():
    saludo = "¿como te llamas?"
    hablar(saludo, id1)
    return transformar_audio_en_texto()


# funcion central del asistente
def pedir_cosas():

    # activar saludo inicial
    nombre_usuario = pedir_nombre()
    saludo_inicial(nombre_usuario)

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'cómo estás' in pedido:
            hablar('hoy me siento muy bien, ¿tu cómo estás?', id1)
            respuesta = True

            while respuesta:
                pedido = transformar_audio_en_texto().lower()
                if 'bien' in pedido:
                    hablar(f'Me alegra escucharlo, en que te puedo ayudar {nombre_usuario}', id1)
                    respuesta = False

        if 'abrir youtube' in pedido:
            hablar("Con gusto, estoy abriendo youtube", id1)
            webbrowser.open('https://www.youtube.com')
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'abrir navegador' in pedido or 'abrir google' in pedido:
            hablar("claro, estoy en eso", id1)
            webbrowser.open('https://www.google.com')
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'qué día es hoy' in pedido:
            pedir_dia()
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'qué hora es' in pedido:
            pedir_hora()
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'buscar en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia', id1)
            pedido = pedido.replace('buscar en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('wikipedia dice lo siguiente: ', id1)
            hablar(resultado, id1)
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'busca en internet' in pedido:
            hablar('ya mismo estoy en eso', id1)
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar("En la siguiente ventana puedes ver lo que encontré", id1)
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'reproducir' in pedido:
            hablar('Buena idea, ya lo reproduzco', id1)
            pedido = pedido.replace('reproducir', '')
            pywhatkit.playonyt(pedido)
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'), id1)
            hablar(f"Algo mas en lo que te pueda ayudar hoy {nombre_usuario}", id1)
            continue

        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()  # el separador de la cadena es la plabra 'de' y se queda con el ultimo objeto de la lista y eliminar espacios en blanco
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}', id1)
                continue
            except:
                hablar('perdon pero no la he encontrado', id1)

        elif 'eso es todo' in pedido:
            hablar(f"Me alegra poder ayudarte, ten un excelente resto del día {nombre_usuario}", id1)
            break


pedir_cosas()
