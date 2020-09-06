"""
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

"""
import tkinter as tk        # mejor esta forma, evita solapamiento de nombres
import tkinter.ttk as ttk   # Para el Progressbar widget
import pygame.mixer         # Para los sonidos

# Para el TTS:
# se para la cuenta del tiempo con cada TTS desde countdown...
# import win32com.client as wincl
# speak=wincl.Dispatch("SAPI.SpVoice")


def reset_all() -> None:
    """ Reset de todas las cosas que se muestran en pantalla:
        Botón de pausa: Etiqueta y estado
        Terminar evento de reloj activo y reset del id
        reset de progressbars
        reset de sgs transcurridos
        reset del tábata
        cálculo de totales
    """

    def reset_pausa() -> None:
        """ Forzar la etiqueta del botón de Pausa y su estado"""
        global pausa
        pausa = False
        b_pausa.config(text='Pausa', bg='yellow')
    
    def reset_countdown() -> None:
        """ Si tengo un evento de reloj activo..."""
        global cd_id
        if cd_id != 0:
            # cancelarlo y resetear el id del evento
            l_reloj.after_cancel(cd_id)
            cd_id = 0

    def reset_progress_bars() -> None:
        """ Reset the Progressbars"""
        pg_total['value'] = 0
        pg_actual['value'] = 0

    def reset_seg_transcurridos() -> None:
        """ Reset de los segundos transcurridos"""
        global seg_trans
        seg_trans = 0

    def reset_tabata() -> None:
        """ resetear el Tábata"""
        global tabata
        tabata = []
    
    reset_pausa()
    reset_countdown()
    reset_progress_bars()
    reset_seg_transcurridos()
    reset_tabata() 
    # Calcular los totales de nuevo "Just in case"
    make_tot(None)


def actu_labels(ant: str, actu: str, sig: str, 
                sgs: int, tot_actu: int, seg_trans: int, 
                color_rlj: str=None) ->None:
    """ Actualizar las etiquetas de ejercicios anterior, actual y siguiente.
        ant, actu, sig : labels a mostrar
        sgs: segundos transcurridos del ejercicio actual
        tot_actu: totales del ejercicio actual
        seg_trans: segundos transcurridos del total de la sesión
        color: Opcional: color del bg del reloj
    """
    def set_color(tipo: str, label: tk.Label) -> None:
        t_tipo = tipo
        if tipo not in l_color:
            tipo = 'Otro'
        label.config(text=t_tipo, bg=l_color[tipo])

    def por_que_serie_voy() -> 'Label':
        # Etiqueta de por cuál serie voy
        q_s = n_seri.get()
        # q_s = 0
        for paso in tabata:
            if paso['label'] == 'Preparados':
                q_s -= 1
        serie_str = 'Serie {}/{}'
        if len(tabata) == 0:
            l_que_serie.config(text='Serie 0/n')
        else:
            l_que_serie.config(text=serie_str.format(q_s, n_seri.get()))

    global seg_total
    # Colores etiquetas
    l_color = dict()
    l_color['Descanso'] = 'cyan'
    l_color['Preparados'] = 'yellow'
    l_color['Otro'] = 'lawn green'
    # Etiquetas
    set_color(ant, l_ant)
    set_color(actu, l_actu)
    set_color(sig, l_sig)
    # Color del reloj
    if color_rlj is None:
        color_rlj = 'white'
    # Reloj
    l_reloj.config(bg=color_rlj)
    reloj.set(mmss(int(sgs)))
    # print('---------' + str(seg_total) + '+++++++++' + str(tot_actu))
    pg_total['value'] = (int(seg_trans) * 100) / seg_total
    if tot_actu == 0:
        tot_actu = sgs = 1
    pg_actual['value'] = 100 - ((int(sgs) * 100) / tot_actu)
    por_que_serie_voy()


def switch_pausa() -> None:
    """ Switch el label, text y bg, del botón de pausa: Pausa/Continuar
        y también switch del estado de 'pausa'
    """
    global cd_id
    global pausa
    # Si no estoy en un tabata no puedo pausar
    if len(tabata) == 0 : return
    # Únicamente si se puede pedir una pausa (cd_id != 0), la pedimos
    if cd_id != 0:
        # cancelarlo y resetear el id del evento
        l_reloj.after_cancel(cd_id)
        cd_id = 0
    pausa = not(pausa)
    if pausa:
        b_pausa.config(text='Continuar', bg='orange')
    else:
        b_pausa.config(text='Pausa', bg='yellow')
    cd_id = l_reloj.after(10, countdown, tabata)
    # con esta forma de pausa me 'como' un segundo cada vez que la uso.


def stop() -> None:
    """ Botón de stop """
    reset_all()
    actu_labels('-', '-Stop-', '-', 0, 0, 0)


def make_tot(aux) -> None:
    """ Calcular el total de segundos de todo el ejercicio y actualizar el
        Label en cada 'focusout'.
        Hace falta el arg 'aux' porque el bind llama a la función con
        un argumento: el evento .
    """
    global seg_total
    secs = int(n_seri.get()) * (int(t_prep.get()) + (int(n_ejer.get()) *
                                                     (int(t_trab.get()) +
                                                      int(t_desc.get()))))
    total.set(mmss(secs))
    seg_total = secs


def mmss(n_secs: int) -> str:
    """ Saco la cuenta de minutos y segundos y retorno en formato mm:ss """
    mins, secs = divmod(n_secs, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    return timeformat


def countdown(tabata: list) -> None:
    """ Cuenta atrás de los sgs del ejercicio
        Toca los sonidos que correspondan
        Actualiza las etiquetas según toca """
    
    def get_cd_data() -> tuple:
        return (l_ant.cget('text'), l_actu.cget('text'), 
                l_sig.cget('text'), tabata[0]['num'], 
                tabata[0]['bg'], tabata[0]['tiempo'])

    def order_labels(ant: str, act: str, sig: str) -> tuple:
        inicio = False
        if act != tabata[0]['label']:
            inicio = True
            ant = act
            act = tabata[0]['label']
            if len(tabata) == 1:
                sig = '-'
            else:
                sig = tabata[1]['label']
        return (ant, act, sig, inicio)

    def play_sound_fxs(inicio: bool, color: str) -> str:
        # play -3 sgs.
        if n_sgs <= 3:
            menos_tres_s.play()
            color = 'magenta'
        if tabata[0]['num'] > 1:
            tabata[0]['num'] -= 1
        else:
            # Pasamos al siguiente ejercicio
            tabata.pop(0)
        # play other sounds
        if inicio:
            if t_act == 'Descanso':
                fin_ej_s.play()
            elif t_act == 'Preparados':
                pass
            else:
                inicio_ej_s.play()
        return color

    global cd_id, seg_trans
    empezamos = False
    # Si estoy en pausa, paro
    if pausa:
        return
    # ¿He terminado?
    if tabata == []:
        actu_labels('-', '-Fin-', '-', 0, 1, seg_trans)
        final_s.play()
        # speak.Speak("Hemos terminado. Enhorabuena.")
        return
    t_ant, t_act, t_sig, n_sgs, color, tot_actu = get_cd_data()
    t_ant, t_act, t_sig, empezamos = order_labels(t_ant, t_act, t_sig)
    color = play_sound_fxs(empezamos, color)
    seg_trans += 1
    actu_labels(t_ant, t_act, t_sig, n_sgs, tot_actu, seg_trans, color)
    cd_id = l_reloj.after(1000, countdown, tabata)
    # if empezamos and (t_act == 'Trabajo'):
    #     speak.Speak("Empezamos con Sentadillas")


def crear_tabata() -> None:
    """ Crea la estructura de todo el ejercicio: Lista de eventos -
        diccionario - a ejecutar
        Para cada 'evento' - ejercico o descanso - agrega un elemento a la
        lista con su información
    """

    def crear_evento_tabata(etiqueta: str, num: int, color: str) -> dict:
        """ Devuelve el siguiente evento tábata -> diccionario"""
        paso = {}
        paso['label'] = str(etiqueta)
        paso['num'] = int(num)
        paso['bg'] = color
        paso['tiempo'] = int(num)
        return paso

    def inicializa_datos() -> set:
        """ Saca los datos para crear el tabata"""
        return (int(e_series.get()), int(e_preparacion.get()), 
                int(e_ejercicios.get()), int(e_trabajo.get()), 
                int(e_descanso.get()))

    def get_ejercicio(ej) -> str:
        """ Devuelve el ejercicio ej de la lista de ejercicios"""
        pos = str(int(ej) + 1)+'.0'
        end_pos = str(int(ej) + 1) + '.end'
        return t_lista_ej.get(pos, end_pos)

    global tabata
    reset_all()
    series, prepare_t, ejercicios, work_t, rest_t = inicializa_datos()
    # Series
    for _ in range(series):
        # Prepare ------------
        tabata.append(crear_evento_tabata('Preparados', prepare_t, 'yellow'))
        # Ejercicios
        trabajo = ''
        for ej in range(ejercicios):
            trabajo = get_ejercicio(ej)
            # Si el siguiente ejercicio no está definido en la lista lo llamo "Trabajo"
            if trabajo == '':
                trabajo = 'Trabajo'
            # Append work
            tabata.append(crear_evento_tabata(trabajo, work_t, 'lawn green'))
            # Append rest
            tabata.append(crear_evento_tabata('Descanso', rest_t, 'cyan'))
    l_actu.config(text='-Inicio-')
    countdown(tabata)


""" Inicializamos algunas variables """
tabata = []
print(tabata)
cd_id = 0
pausa = False

#
# Sounds
#

# Objeto sonidos de pygame.mixer
sounds = pygame.mixer
sounds.init()

# Sonidos disponibles
final_s = sounds.Sound('Final.wav')
menos_tres_s = sounds.Sound('En_3_2_1.wav')
inicio_ej_s = sounds.Sound('Inicio_ejercicio.wav')
fin_ej_s = sounds.Sound('Fin_ejercicio.wav')

# Lista de sonidos para controlar el volumen de TODOS
track = []
track.append(final_s)
track.append(menos_tres_s)
track.append(inicio_ej_s)
track.append(fin_ej_s)

#
# GUI...
#

app = tk.Tk()
app.title('Tábata Timer JFB')
# No usamos la geometría, que el grid de tkinter haga su magia
# app.geometry('300x110+300+300')

# .......... Frame TÁBATA, el del reloj ..........
lf_tabata = tk.LabelFrame(app, text='Tábata Timer')
lf_tabata.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

reloj = tk.IntVar()
reloj.set('00:00')

total = tk.IntVar()
n_seri = tk.IntVar()
t_prep = tk.IntVar()
n_ejer = tk.IntVar()
t_trab = tk.IntVar()
t_desc = tk.IntVar()

n_seri.set(2)
t_prep.set(30)
n_ejer.set(8)
t_trab.set(20)
t_desc.set(10)

seg_total = 0
seg_trans = 0

# Ejercicios
# ROW: 00. COL: 00, COLUMNSPAN: 3
l_sig = tk.Label(lf_tabata, text='vvv Siguiente vvv', font=('bold', 48))
l_sig.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

# ROW: 01. COL: 00, COLUMNSPAN: 3
l_actu = tk.Label(lf_tabata, text='Tábata', font=('bold', 64))
l_actu.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

# ROW: 02. COL: 00, COLUMNSPAN: 3
l_ant = tk.Label(lf_tabata, text='Anterior', font=('bold', 16))
l_ant.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

# Reloj cuenta atrás
l_reloj = tk.Label(lf_tabata, text='Countdown', textvariable=reloj,
                   font=('bold', 128))
l_reloj.grid(row=3, column=0, padx=10, pady=10, columnspan=3)

# Botones de control del reloj
b_stop = tk.Button(lf_tabata, text='Stop', command=stop, bg='red')
b_stop.grid(row=4, column=2, pady=10)

b_inicio = tk.Button(lf_tabata, text='Inicio', command=crear_tabata,
                     bg='lawn green')
b_inicio.grid(row=4, column=1, pady=10)

b_pausa = tk.Button(lf_tabata, text='Pausa', command=switch_pausa, bg='yellow')
b_pausa.grid(row=4, column=0, pady=10)

# Label Serie x/n
l_que_serie = tk.Label(lf_tabata, text='Serie 0/n', font=('bold', 16))
l_que_serie.grid(row=5, column=0, padx=10, pady=10, columnspan=3)

# Progressbar Total
pg_total = ttk.Progressbar(lf_tabata,
                           orient='horizontal',
                           mode='determinate',
                           maximum=100,
                           value=0,
                           length=500)
pg_total.grid(row=6,
              column=0,
              padx=10,
              pady=10,
              columnspan=3)

# Progressbar de este ejercicio
pg_actual = ttk.Progressbar(lf_tabata,
                            orient='horizontal',
                            mode='determinate',
                            maximum=100,
                            value=0,
                            length=500)
pg_actual.grid(row=7,
               column=0,
               padx=10,
               pady=10,
               columnspan=3)

# .......... Frame CONFIGURACIÓN ..........
lf_config = tk.LabelFrame(app, text='Configuración del tábata')
lf_config.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

# Total de tiempo
l_tot = tk.Label(lf_config, textvariable=total, font=('bold', 32))
l_tot.grid(row=0, column=0, padx=10, pady=10, columnspan=5)

# series, prepare_t, ejercicios, work_t, rest_t
l_series = tk.Label(lf_config, text='# Series')
l_preparacion = tk.Label(lf_config, text='*   ( T. Prep.')
l_ejercicios = tk.Label(lf_config, text='+   ( # Ejercicios')
l_trabajo = tk.Label(lf_config, text='*   ( T. Ejercicio')
l_descanso = tk.Label(lf_config, text='+   T. Descanso ) ) )')

l_series.grid(row=1, column=0, padx=10, pady=10)
l_preparacion.grid(row=1, column=1, padx=10, pady=10)
l_ejercicios.grid(row=1, column=2, padx=10, pady=10)
l_trabajo.grid(row=1, column=3, padx=10, pady=10)
l_descanso.grid(row=1, column=4, padx=10, pady=10)

e_series = tk.Entry(lf_config, textvariable=n_seri, width=3)
e_preparacion = tk.Entry(lf_config, textvariable=t_prep, width=3)
e_ejercicios = tk.Entry(lf_config, textvariable=n_ejer, width=3)
e_trabajo = tk.Entry(lf_config, textvariable=t_trab, width=3)
e_descanso = tk.Entry(lf_config, textvariable=t_desc, width=3)

# Binds para hacer el cálculo del total de minutos on focusout
e_series.bind('<FocusOut>', make_tot)
e_preparacion.bind('<FocusOut>', make_tot)
e_ejercicios.bind('<FocusOut>', make_tot)
e_trabajo.bind('<FocusOut>', make_tot)
e_descanso.bind('<FocusOut>', make_tot)

e_series.grid(row=2, column=0, padx=10, pady=10)
e_preparacion.grid(row=2, column=1, padx=10, pady=10)
e_ejercicios.grid(row=2, column=2, padx=10, pady=10)
e_trabajo.grid(row=2, column=3, padx=10, pady=10)
e_descanso.grid(row=2, column=4, padx=10, pady=10)

# .......... Frame VOLUMEN ..........


def change_volume(v) -> None:
    """ Para regular el volumen de TODOS los sonidos del Tábata Timer
        por eso el for """
    for t in track:
        t.set_volume(volume.get())


lf_vol = tk.LabelFrame(app, text='Volumen')
lf_vol.grid(row=1, column=1, padx=10, pady=10)

volume = tk.DoubleVar()

volume.set(track[0].get_volume())

volume_scale = tk.Scale(lf_vol,
                        variable=volume,
                        from_=1.0, to=0.0,
                        resolution=0.1,
                        command=change_volume,
                        orient=tk.VERTICAL)
# label="Volume", # no hace falta, ya está el label del Frame
volume_scale.grid(row=0, column=0, padx=10, pady=10)

# .......... Frame EJERCICIOS ..........
lf_ejerci = tk.LabelFrame(app, text='Lista de ejercicios')
lf_ejerci.grid(row=1, column=2, padx=10, pady=10)

t_lista_ej = tk.Text(lf_ejerci, height=12, width=30)
t_lista_ej.grid(row=3, column=5, padx=10, pady=10, rowspan=4)

# Rellenamos con una lista de ejercicios de ejemplo para ilustrar al usuario
for l in range(1, 9):
    pos = str(l)+'.0'
    ej = 'Ejercicio ' + str(l) + '\n'
    t_lista_ej.insert(pos, ej)

# Para forzar el que se haga el primer cálculo y la ventana aparezca con datos
make_tot(None)


if __name__ == '__main__':
    app.mainloop()
