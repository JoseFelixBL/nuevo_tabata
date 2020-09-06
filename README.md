# Proyecto de tábata Timer
Hasta ahora he hecho un timer que funciona.

He usado pygame para los sonidos pues hace que no se interrumpa el flujo de la cuenta atrás mientras "suena". También uso el reloj de pygame porque puedo poner que cada segundo se vuelva a pintar en pantalla mientras estoy pendiente de si se "toca" algo del interfaz.

Por otro lado uso TkInter para el interfaz... no sé si podría haber usado pygame también para el interfaz gráfico ni si eso tiene alguna ventaja.

El modelo que uso es actualizar el reloj general cada vez que salgo de focus de las variables que definen el tiempo de los ejercicios.

Otra parte del modelo es que cuando le doy a "inicio" creo una lista con todos los eventos de este tábata, y que cada vez que se acaba el tiempo del evento en curso, hago un pop de la lista para ver el siguiente, así únicamente estoy pendiente del primer elemento de la lista, y si no hay más, he terminado.

## Posibles mejoras
Creo que el proyecto ha crecido hasta el punto en el que empieza a hacerse difícil de leer, y puede que se beneficie de una reescritura con Clases, y de ser así también tengo que pensarme el modelo de cómo representar la lista de ejercicios y como seguirla pues quiero poder cambiar un tiempo, por ejemplo aumentar los descansos entre ejercicios de la serie  y que se reflejen inmediatamente en el siguiente ejercicio que empiece, o por ejemplo de quitarle una ronda, o agregar otra más... veo más fácil lo de cambiar los tiempos, ya que se pueden leer dinámicamente en cada paso, que lo de cambiar número de series que estará en un loop...

## Notas de antes a revisar

    Proyecto Tábata Timer - PEP8 compliant!
    Reescribirlo sin crear lista y eliminar elementos, hacerlo con variables de
    series, ejercicios, t_trabajo, t_descanso, t_preparación para poder
    editar tiempos dinámicamente - subir o bajar el tiempo de descanso y/o
    el número de series.
    Ponerle además otro termómetro: 1. serie, 2. ej. de esta serie, 3. tiempo_ej
    Permitir adelantar o repetir ejercicio.
    
Falta:
    Constantes:
        - definir constantes y usarlas en el programa:
            -- nombres de los audios
            -- nombres de los pasoso del tábata
    Globales:
        - evitar el uso de variables globales
    Listas Ejercicios:
        - guardar y recuperar diferentes ficheros de listas de ejercicios y
        ponerle nombre que se vea como título
    Exceptions:
        - capturar exceptions de valores en blanco cuando hago focusout
    Documentación:
        - documentar el programa de acuerdo a PEP-8
    MVC:
        - pasarlo a MVC - Model View Controler
    Formato:
        - meter widgets en Frames para ordenarlo mejor
        - Que sean de tamaño constante
Hecho:
        + arreglar el segundo que cuenta de más en cada evento tabata
        + botón pausa/continuar
        + poner los nombres de evento_tabata anterior, actual y siguiente
    Sonidos:
        + poner sonidos a -3sg: bips
        + poner sonido de final de tábata
        + Buscar otros sonidos
    Formateo:
        + que cambie el color a -3sg
        + que cambie el color entre preparación, trabajo y descanso
        + cambiar el tamaño del reloj
        + Arreglar los tamaños de los campos
        + Arreglar tamaño del campo Text
        + Que diga por qué serie va y cuántas faltan, p.e.: 3/5
    Termómetro:
        + poner un widget de termómetro de tiempo total -
        ttk.Progressbar !
        + poner un widget de termómetro de tiempo ej. actual -
        ttk.Progressbar !
    Listas Ejercicios:
        - admitir la lista de ejercicios
        # crear label de lista de ejercicios
        # crear Text de lista de ejercicios
        # Inicializar el Text
        # ??? comprobar que la lista no termina en línea vacía, y si lo
        hace, ¡quitarla!
        # Si el mum-líneas de la lista de ejercicios <> al número de
        ejercicios ??? --- de momento no hacer nadady rellenar con Trabajo
        # en crear tábata poner la etiqueta adecuada al nombre del
        ejercicio si existem si no existe o está en blanco poner TRABAJO
No haré:
        . que el tiempo total vaya disminuyendo
    Sonidos:
        x poner TTS para los nombres de los ejercicios ~ ¡No!, el tiempo
        que tarda en LEER el texto no es concurrente con countdown