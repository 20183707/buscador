import ast
from math import atan2, degrees

from flask import Flask, render_template, request
import mysql.connector # importando la libreria para la base de datos

import cv2
from joblib._multiprocessing_helpers import mp

import webbrowser
import time
from math import atan2, radians, degrees
import cv2
import mediapipe as mp
import numpy as np


texto = []

app = Flask(__name__)




#----------------------------------------------------- Inicia la funcion para buscar en el indice invertido
def buscarURL(palabra):

    with open('miInvertido.txt', "r", encoding="utf8") as f:
        data = f.read()

        diccionario = ast.literal_eval(data)

    recuperar = []
    print("\n\n")
    for key, values in diccionario.items():
        if palabra in key:
            recuperar.append([key, values])

    return recuperar
#------------------------------------------------------------ Fin de la funcion buscar





def clasificar():
    indice_x = []
    indice_y = []

    diccionario = {0: ["10000", "r", "a.png"],
                   1: ["01000", "e", "b.png"],
                   2: ["00100", "d", "c.png"],
                   3: ["00010", "d", "pepino.png"],
                   4: ["00001", "e", "pepino.png"],

                   5: ["01100", "f", "b.png"],
                   6: ["01010", "g", "c.png"],
                   7: ["01001", "h", "pepino.png"],
                   8: ["00110", "i", "pepino.png"],
                   9: ["00111", "j", "b.png"],

                   10: ["00011", "k", "c.png"],
                   11: ["00111", "l", "pepino.png"],
                   12: ["01111", "m", "pepino.png"],
                   13: ["11111", "n", "b.png"],

                   }

    f = " "
    g = []
    palabra = ""

    # INICIAR SISTEMA DE DETECCIÓN.
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # INICIAR CAMARA
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

        # COMPROBAR ENTRADA
        success, image = cap.read()
        #image = cv2.imread('b.png')

        # CONVERTIR IMAGEN A RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        # DIBUJAR PUNTOS DE DETECCIÓN
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        inicio = 5
        fin = 9
        cont = 2

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                x = [landmark.x for landmark in hand_landmarks.landmark]
                y = [landmark.y for landmark in hand_landmarks.landmark]

                binario = ""
                palabra = ""
                pulgar_x = x[1:5]
                pulgar_y = y[1:5]

                angle = atan2(pulgar_y[2] - pulgar_y[3], pulgar_x[2] - pulgar_x[3])
                angle = degrees(angle)

                if results.multi_handedness:
                    for hand in results.multi_handedness:
                        # if hand.classification[0].label == "Left":
                        #   if angle < 120:
                        # print("1.0 ", end="")
                        #       binario += "1"
                        if hand.classification[0].label == "Right":
                            if angle > 120:
                                # print("1 ", end="")
                                binario += "1"
                        binario += "0"

            for i in range(4):
                # ---------------------------------- Para todos los dedos
                dedos_x = x[inicio:fin]
                dedos_y = y[inicio:fin]

                if dedos_y[1] < dedos_y[3]:
                    # print(cont,end=" ")
                    binario += "1"
                else:
                    binario += "0"
                cont += 1
                inicio += 4
                fin += 4

                # Ciclo para quitar los signos de puntuacion

                for values in diccionario.values():
                    if values[0] == binario:
                        # print("La palabra: ", binario, "La clave: ", values, "0:", values[0], "\t1:", values[1], "\t2:", values[2])
                        f = values[1]
                        palabra += values[1]
                        g.append(values[1])



        cv2.imshow('MediaPipe Hands', image)

        cv2.imwrite("static/css/foto.png", image)

    dd = []


    buscar = ''.join(palabra)

    cap.release()

    return buscar


#------------------------------------------------------------ Funcion para tomar la foto
def tomarFoto():

    cap = cv2.VideoCapture(0)
    leido, frame = cap.read()

    if leido == True:
        cv2.imwrite("static/css/foto.png", frame)
        print("Foto tomada correctamente")
    else:
        print("Error al acceder a la cámara")

    cap.release()



#------------------------------------------------------------ Funcion para dirigise al archivo .html
@app.route('/')
def inicio():
    return render_template("mostrarAlumnos.html")

#------------------------------------------------------------




#------------------------------------------------------------ Funcion que controla todo el programa
@app.route('/procesarAlumnos', methods=['POST'])
def procesarAlumnos():

    nombre = request.form.get("nombre")
    texto = request.form.get("texto")
    borrar = request.form.get("borrar")
    #texto.append(request.form.get("texto"))

    if borrar == 1 or borrar == "1":
        buscar = ""
        texto = ""
        print("Borrarrrrrrrrrr")
        return render_template("mostrarAlumnos.html", buscar=buscar, texto=texto)

    else:
        #tomarFoto()
        buscar = clasificar() + texto

        recuperar = buscarURL(buscar)
        return render_template("mostrarAlumnos.html",buscar = buscar, texto = texto,recuperar = recuperar)


if __name__=='__main__':
    app.run(debug=True)































