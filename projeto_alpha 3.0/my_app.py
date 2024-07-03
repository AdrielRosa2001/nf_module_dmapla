import PySimpleGUI as sg
from databse import db_session, init_db
from models import Pedido, Pedido_Emitido, Pedido_Falho
from sql_conexao import ServerDB
from operacoes import Comandos
from datetime import date, datetime
import time


def generate_tabel_data():
    headings = [' ID ', 'PEDIDO']
    pedidos = []
    for pedido in Pedido.query.all():
            pedidos.append([pedido.id, pedido.numero_pedido])
    data = pedidos
    return headings, data

sg.theme('Reddit')   # Add a touch of color
# All the stuff inside your window.
headings, data = generate_tabel_data()

layout = [  
            [sg.Text("Digite o Mês/Ano abaixo (ex: 08/2023):")],
            [sg.Text("Mês"), sg.InputText(f'{date.today().month}/{date.today().year}' , size=(10, 1), key=('input_data')), sg.Button('Buscar Notas cartão', key=('search_notes'))],
            [sg.Text("Mês"), sg.InputText(f'{date.today().month}/{date.today().year}' , size=(10, 1), key=('input_data')), sg.Text('Quantidade:'), sg.InputText('15', size=(10, 1), key='quanttity'), sg.Button('Buscar TOP Dinheiro', key=('search_notes_top_15'))],
            [sg.Button('Emitir NFc-e auto', size=(25,1), button_color='green', key=('auto_emissao')), sg.Button('Limpar notas no banco', size=(25,1), button_color='red', key=('clear_pedidos'))],
            [sg.Text("Notas pendentes:")],
            [sg.Table(values=data, headings=headings, key='table_pedidos')],
            [sg.Button('Ver notas que estão faltando no XML das NFc-e', size=(52,1), key=('view_notes_lost'))],
            [sg.Button('Gerar arquivos para o contador', size=(52,1), key=('generate_files'))] ]


# Create the Window
window = sg.Window('SPEED Fiscal automatico by: Adriel 2.0', layout)
# Event Loop to process "events" and get the "values" of the inputs
conexao = ServerDB()
init_db()
externo = Comandos

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'search_notes':
        data = str(values['input_data']).split("/")
        notas_localizadas = conexao.consultaNotas(mes=str(data[0]), ano=str(data[1]))
        if notas_localizadas != []:
            resposta = sg.popup_ok_cancel(f"Foram localizadas {len(notas_localizadas)} vendas (cartão: credito/debito/parcelado, PIX)\nDeseja adicionar a lista de emissão automatica?")
            if resposta == 'OK':
                for nota in notas_localizadas:
                    print("Nota carregada:", nota[0])
                    pedido_find = db_session.query(Pedido_Falho).filter(Pedido_Falho.numero_pedido == nota[0]).all()
                    if len(pedido_find) != 0:
                        pass
                    else:
                        pedido_novo = Pedido(nota[0])
                        db_session.add(pedido_novo)
                db_session.commit()
                quantidade = len(Pedido.query.all())
                sg.popup(f"Foram adicionadas {quantidade} notas a lista de emissão automatica!\nSe o numero deu difernte das notas localizadas não se procupe, pois notas com erro de emissão anteriores não foram adicionadas!")
                headings, data = generate_tabel_data()
                window['table_pedidos'].update(values=data)
                sg.popup("Notas carregadas com êxito!")
            else:
                pass
        else: 
            sg.popup("Notas não localizadas!")
    
    if event == "search_notes_top_15":
        quantidade = values['quanttity']
        data = str(values['input_data']).split("/")
        notas_localizadas = conexao.consultaNotasDinheiro(quanttity=quantidade, mes=str(data[0]), ano=str(data[1]))
        if notas_localizadas != []:
            resposta = sg.popup_ok_cancel(f"Foram localizadas {len(notas_localizadas)} vendas no Dinheiro!\nDeseja adicionar a lista de emissão automatica?")
            if resposta == 'OK':
                for nota in notas_localizadas:
                    pedido_novo = Pedido(nota[0])
                    db_session.add(pedido_novo)
                db_session.commit()
                headings, data = generate_tabel_data()
                window['table_pedidos'].update(values=data)
                sg.popup("Notas carregadas com êxito!")
            else:
                pass
        else: 
            sg.popup("Notas não localizadas!")
    
    if event == 'auto_emissao':
        #3 - Emitir NFc-e de forma automatica.
        pedidos = []
        for pedido in Pedido.query.all():
            """pedido_find = db_session.query(Pedido_Falho).filter(Pedido_Falho.numero_pedido == pedido.numero_pedido).all()
            if pedido_find[0].numero_pedido == pedido.numero_pedido:
                pass
            else:"""
            pedidos.append(pedido)
        if pedidos != []:
            resposta = sg.popup_ok_cancel(f"O total de {len(pedidos)} notas foram localizadas!\nDeseja emitir automaicamente?\n\nOK => Para sim!  |  Cancel => Para não!")
            if resposta == 'OK':
                retorno_nfce = externo.abrir_e_maximizar_janela_de_emissao_nfce()
                if retorno_nfce == True:
                    emitidos = []
                    nao_emitidos = []
                    for pedido in pedidos:
                        #pyautogui.alert(text='Os numeros de pedidos ja estão salvos no arquivo: notas_a_dar_baixa.txt ?\nSe sim aperte OK.', title='Emitir NFc-e', button='OK')
                        retorno_emissao = externo.dar_baixa_nas_notas_new(pedido.numero_pedido)
                        if retorno_emissao == True:
                            #peido_atual = Pedido.query.get(pedido.id)
                            pedido_emitido = Pedido_Emitido(pedido.numero_pedido)
                            db_session.add(pedido_emitido)
                            db_session.delete(pedido)
                            emitidos.append(pedido_emitido.numero_pedido)
                        elif retorno_emissao == False:
                            nao_emitidos.append(pedido.numero_pedido)
                            nao_emitido = Pedido_Falho(pedido.numero_pedido)
                            db_session.add(nao_emitido)
                            db_session.delete(pedido)
                            time.sleep(8)
                            #sg.popup("Erro ao emitir! Verifique se o programa está com alguma tela de erro aberta!")
                    #primeiro_pedido_falho = Pedido_Falho(nao_emitidos[0])
                    #db_session.add(primeiro_pedido_falho)
                    db_session.commit()
                    headings, data = generate_tabel_data()
                    window['table_pedidos'].update(values=data)
                    sg.popup(f"Emissão automatica finalizada com sucesso!\nNotas emitidas: {len(emitidos)}\nNotas NÃO emitidas: {len(nao_emitidos)}")
                elif retorno_nfce == False:
                    sg.popup("A janela do emissor de notas não foi localizada!")
        else: 
            sg.popup('Nenhum pedido pendente para dar baixa')
    
    if event == 'clear_pedidos':
        pedidos = []
        for pedido in Pedido.query.all():
                pedidos.append(pedido)
        if len(pedidos) != 0:
            resposta = sg.popup_ok_cancel(f"Foram localizadas {len(pedidos)} na base de dados do sistema\nDeseja excluir todos?")
            if resposta == 'OK':
                for pedido in pedidos:
                    db_session.delete(pedido)
                db_session.commit()
                headings, data = generate_tabel_data()
                window['table_pedidos'].update(values=data)
                sg.popup("Pedidos apagados com sucesso!")
        else:
            sg.popup("Nenhum pedido foi localizado!")

    if event == 'generate_files':
        resposta = sg.popup_ok_cancel("O total de 142 notas foram localizadas!\nDeseja emitir automaicamente?\n\nOK => Para sim!  |  Cancel => Para não!") #Ok Cancel
        print(resposta)
        
        

window.close()