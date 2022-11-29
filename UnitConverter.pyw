import PySimpleGUI as sg
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

un = ['mm','cm','th','EIA','pol']
vl = [1,10,0.0254,0.254,25.4]

def converter(numero,de,para):
    resultado = numero * vl[un.index(de)] / vl[un.index(para)]
    if para == 'EIA':
        sresultado = str(int(round(resultado,0)))
        if len(sresultado) == 1: sresultado = '0' + sresultado
    else:
        sresultado = str(resultado)[:6]
        if sresultado[-1] == '.': sresultado = sresultado[:-1]
        if resultado>float(sresultado):
            sresultado = sresultado + '…'
        #print(resultado,sresultado)
    return sresultado

sg.theme('Reddit')
sg.SetGlobalIcon(resource_path('swap.ico'))

layout = [[sg.Text('De:',(3,1),justification='right'),sg.Combo(un,'mm',(4,1),readonly=True,k='-DE-',change_submits=True),sg.Text('',(0,1)),sg.Image(resource_path('swap.png'),k='-SWAP-',enable_events=True),sg.Text('Para:',(4,1)),sg.Combo(un,'th',(4,1),readonly=True,k='-PARA-',change_submits=True),],
          [sg.Text('',(3,1),justification='right'),sg.Input(s=(8,1),k='-DE1-',change_submits=True),sg.Text('',(4,1)), sg.Input(s=(8,1),k='-PARA1-',change_submits=True)],
          [sg.Text('',(3,1),justification='right'),sg.Input(s=(8,1),k='-DE2-',change_submits=True),sg.Text('',(4,1)), sg.Input(s=(8,1),k='-PARA2-',change_submits=True)],
          [sg.Text('',(3,1),justification='right'),sg.Text('',k='-EIA1-'),sg.Text('',(11,1)), sg.Text('',k='-EIA2-')]]

window = sg.Window('Convesor de unidades', layout, size=(290,120))

while True:  # Event Loop
    event, values = window.read()   # Fica esperando um evento
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    de = values['-DE-']
    para = values['-PARA-']
    if event == '-SWAP-':
        de, para = para, de
        window['-DE-'].update(de)
        window['-PARA-'].update(para)
        window['-EIA1-'].update('')
        window['-EIA2-'].update('')
        
    if event in ['-DE1-','-DE2-','-PARA1-','-PARA2-']:
        if values[event] and values[event][-1] not in '0123456789.' or '.' in values[event][:-1] and values[event][-1] == '.' or len(values[event]) > 8:
            values[event] = values[event][:-1]
            window[event].update(values[event])
    
    if event:
        if values['-DE1-'] != '':
            para1 = converter(float(values['-DE1-']),de,para)
            window['-PARA1-'].update(para1)
        else:
            window['-PARA1-'].update('')
            
        if values['-DE2-'] != '':
            para2 = converter(float(values['-DE2-']),de,para)
            window['-PARA2-'].update(para2)
        else:
            window['-PARA2-'].update('')
            
        if values['-DE1-'] != '' and values['-DE2-'] != '' and de == 'EIA':
            window['-EIA1-'].update(values['-DE1-']+values['-DE2-'])
        else:
            window['-EIA1-'].update('')
            
        if values['-PARA1-'] != '' and values['-PARA2-'] != '' and para == 'EIA':
            window['-EIA2-'].update(para1+para2)
        else:
            window['-EIA2-'].update('')

window.close()