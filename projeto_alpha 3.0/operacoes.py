from tkinter import Button
import pygetwindow
import pygetwindow as gw
import pyautogui
import time
import os
import shutil
#import win32clipboard




def editar_arquivo_de_notas(caminho, lista):
    arquivo = open(caminho, 'w')
    for item in lista:
        arquivo.writelines(str(item)+"\n")

def abrir_arquivo_txt(caminho):
    arquivo = open(caminho, 'r')
    lista = arquivo.readlines()
    arquivo.close()
    listan = []

    for item in lista:
        item = item.replace(f"\n", "")
        listan.append(item)

    return listan

def emitir_nfce(item):
    time.sleep(1)

    pyautogui.click(x=729, y=266) # botão Eminir NFc-e com numero de pedido
    time.sleep(1)

    #titulo janela: Emitir NFC-e
    pyautogui.write(str(item)) # entrada do numero de pedido
    time.sleep(1)

    #pyautogui.click(x=606, y=391) # botão okay da entrada no numero de pedido
    pyautogui.press('enter')
    time.sleep(2)

    cont = 0
    janela_atencao = gw.getActiveWindowTitle()
    while janela_atencao != "Atenção" or janela_atencao != "Confirmação":
        if janela_atencao == "Confirmação":
            #titulo da janela: Confirmação -> tab -> enter
            #pyautogui.click(x=491, y=451) # botão sim para confirmar emissão do NFc-e
            pyautogui.press('tab')
            time.sleep(0.4)
            pyautogui.press('enter')
            #time.sleep(9) #12 ~13 segundo de espera para aguardar o resultado da emissão

            cont = 0
            janela_ativa = gw.getActiveWindowTitle()
            saida = ""
            while janela_ativa != "NFC-e emitida com sucesso" or janela_ativa != "ERRO" or janela_ativa != "Atenção" or janela_ativa == "Alterar NCM":
                """
                Novo codigo:
                """
                janela_ativa = gw.getActiveWindowTitle()

                if janela_ativa == "NFC-e emitida com sucesso": # Sucesso ao emitir a nota fiscal
                    saida = janela_ativa
                    #print("Entrando no laço:", saida)
                    
                    #titulo da janela: NFC-e emitida com sucesso
                    janela_ativa = gw.getActiveWindowTitle()
                    if janela_ativa == "NFC-e emitida com sucesso":
                        pyautogui.press('enter')
                        janela_ativa = gw.getActiveWindowTitle()
                        
                        cont = 0
                        while janela_ativa != "Imprimir":
                            time.sleep(1)
                            cont +=1
                            janela_ativa = gw.getActiveWindowTitle()
                            if cont == 20:
                                pyautogui.alert(text='Erro na verificação da janela de impressão', button='Ok')
                                return saida
                        pyautogui.hotkey('alt', 'f4')
                        time.sleep(3)
                        return saida

                        #pyautogui.click(x=658, y=442) # botão ok para emitido com sucesso
                        
                        #pyautogui.click(x=676, y=453) # botão cancelar para impressão da NFc-e 

                elif janela_ativa == "ERRO" or janela_ativa == "Atenção" or janela_ativa == "Alterar NCM": #Erro ao tentar emitir
                    time.sleep(1)
                    janela_ativa = gw.getActiveWindowTitle()
                    while janela_ativa != "Emissão de Nota Fiscal Eletrônica para Consumidor (NFC-e)":
                        time.sleep(1)
                        pyautogui.hotkey('alt', 'f4')
                        time.sleep(6)
                        """try:
                            win_activate = gw.getWindowsWithTitle("Alterar NCM")
                            win_activate.activate()
                            print('Janela "Alterar NCM" ativada')
                        except:
                            pass"""
                        janela_ativa = gw.getActiveWindowTitle()
                        print(janela_ativa)
                        saida = "ERRO"

                    print("Entrando no laço:", saida)
                    saida = "Erro ao emitir"
                    return saida #retornando erro e fechando o laço
                    
                """
                Validação do While
                """
                time.sleep(2.5)
                janela_ativa = gw.getActiveWindowTitle()
                cont += 1
                if cont == 25:
                    print("Algum erro desconhecido ao tentar emitir NFC-e: "+item)
                    saida = "Erro ao emitir"
                    return saida
        elif janela_atencao == "Atenção":
            saida = janela_atencao
            while janela_atencao == "Atenção":
                pyautogui.press('enter')
                janela_atencao = janela_atencao = gw.getActiveWindowTitle()
                time.sleep(0.4)
            return saida
        """
        Validação do While
        """
        time.sleep(0.5)
        janela_ativa = gw.getActiveWindowTitle()
        cont += 1
        if cont == 12:
            print("Algum erro desconhecido ao tentar confirmar a emitir NFC-e: "+item)
            saida = "Erro ao emitir"
            return saida
        

        # Emissão de Nota Fiscal Eletrônica para Consumidor (NFC-e)
        # NFC-e emitida com sucesso
        # Atenção
        # ERRO

def abrir_programas_de_emissao(caminho, quantidade_de_enter):
    time.sleep(1)
    pyautogui.hotkey('win', 'r')
    time.sleep(0.4)
    pyautogui.write(caminho)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.write('009482')
    saida = 0
    while saida < quantidade_de_enter:
        time.sleep(0.4)
        pyautogui.press('enter')
        saida += 1

def emissoes_mal_sucessidas(nota):
    arquivo = open('erro_ao_emitir.txt', 'r')
    conteudo = arquivo.readlines()
    conteudo.append(nota)

    arquivo = open('erro_ao_emitir.txt', 'w')
    arquivo.writelines(conteudo)
    arquivo.close()
        
class Comandos:

    def abrir_e_maximizar_janela_de_emissao_nfce():
        count = 0
        retorno = False
        while count <= 4:
            try:
                window_get = pygetwindow.getWindowsWithTitle('Emissão de Nota Fiscal Eletrônica para Consumidor (NFC-e)')[0]
                window_get.activate()
                window_get.maximize()
                retorno = True
                count = 10
            except:
                # C:/SICNET/NFCe2/nfce.exe
                pyautogui.alert(text='O programa de Emissão de NFce não está aberto!\nAperte em OK para abrir e prosseguir com o programa!', button='Ok')
                abrir_programas_de_emissao("C:/SICNET/NFCe2/nfce.exe", 3)
                window_get = pygetwindow.getWindowsWithTitle('Emissão de Nota Fiscal Eletrônica para Consumidor (NFC-e)')[0]
                window_get.activate()
                window_get.maximize()
                retorno = True
                count = 10

        if retorno == True:
            return True
        elif retorno == False:
            return False

    def abrir_arquivo_txt(caminho):
        arquivo = open(caminho, 'r')
        lista = arquivo.readlines()
        arquivo.close()
        listan = []

        for item in lista:
            item = item.replace(f"\n", "")
            listan.append(item)

        return listan

    
    def dar_baixa_nas_notas():
        lista = abrir_arquivo_txt('notas_a_dar_baixa.txt')
        #print(lista, "\n")

        quantidade_total_de_notas = len(lista)
        notas_okay = 0
        notas_erro = 0
        notas_ja_emitidas = 0
        
        msg_de_exibicao = "QUANTIDADE DE NOTAS LOCALIZADAS: "+str(quantidade_total_de_notas)+"\n\nPRESSIONE OK PARA CONTINUAR!"
        pyautogui.alert(text=msg_de_exibicao, title='Notas Localizadas', button='Ok')

        while len(lista) != 0:
            item_da_lista = lista.pop(0)
            #print("Lista:", lista)
            print("Numero de pedido retirado da lista:", item_da_lista, "\n")
            
            retorno = emitir_nfce(item_da_lista)
            print("Tentativa de emissão com o numero:", item_da_lista)
            print("Retorno da tentativa de emissão:", retorno)

            editar_arquivo_de_notas('notas_a_dar_baixa.txt', lista)
            
            if retorno == "NFC-e emitida com sucesso":
                print("OKAY!", item_da_lista)
                notas_okay += 1
            elif retorno == "Erro ao emitir":
                tipo_de_erro = "\nERRO AO EMITIR: "+str(item_da_lista)
                emissoes_mal_sucessidas(tipo_de_erro)
                notas_erro += 1
            elif retorno == "Atenção":
                tipo_de_erro = "\nERRO - NOTA JA EMITIDA: "+str(item_da_lista)
                emissoes_mal_sucessidas(tipo_de_erro)
                notas_ja_emitidas += 1

        msg_de_exibicao = "QUANTIDADE TOTAL DE NOTAS: "+str(quantidade_total_de_notas)+"\n\nNOTAS EMITIDAS COM SUCESSO: "+str(notas_okay)+"\nNOTAS JÁ EMITIDAS: "+str(notas_ja_emitidas)+"\nNOTAS COM ERRO AO TENTAR EMITIR: "+str(notas_erro)+"\n\nPRESSIONE OK PARA CONTINUAR!"
        pyautogui.alert(text=msg_de_exibicao, title='Relatorio de Emissão', button='Ok')

    def dar_baixa_nas_notas_new(nota):
        item_da_lista = nota
        print("Numero de pedido retirado da lista:", item_da_lista, "\n")
        
        retorno = emitir_nfce(item_da_lista)
        
        if retorno == "NFC-e emitida com sucesso":
            print(f"Tentativa: {item_da_lista} | Status: {retorno}")
            return True
        elif retorno == "Erro ao emitir":
            print(f"Tentativa: {item_da_lista} | Status: {retorno} | Msg: Erro ao Emitir")
            return False
        elif retorno == "Atenção":
            print(f"Tentativa: {item_da_lista} | Status: {retorno} | Msg: Nota Já emitida!")
            return True
        else:
            return False

    def entrada_do_mes():
        mes = pyautogui.prompt(text='Escreva o mês da emissão:', title='Entrada do mês', default='')
        return mes

    def gerar_arquivos_nfce(mes):
        time.sleep(1)
        pyautogui.click(x=720, y=517)

        time.sleep(1)
        pyautogui.click(x=361, y=335)

        time.sleep(1)
        pyautogui.click(x=511, y=433)

        time.sleep(2)
        pyautogui.write(mes)

        time.sleep(1)
        pyautogui.click(x=666, y=393)

        time.sleep(1)
        pyautogui.click(x=589, y=391)

        time.sleep(1)
        pyautogui.click(x=554, y=452)

        time.sleep(11)
        pyautogui.click(x=640, y=453)

        time.sleep(1)
        pyautogui.click(x=541, y=444)

        time.sleep(3)
        pyautogui.hotkey('alt', 'f4')

    def abrir_e_maximizar_janela_de_emissao_nfe():
        # C:/SICNET/NFe5/nfe.exe
        count = 0
        retorno = False
        while count <= 4:
            try:
                window_get = pygetwindow.getWindowsWithTitle('Emissor de Nota Fiscal Eletrônica (NF-e)')[0]
                window_get.activate()
                window_get.maximize()
                retorno = True
                count = 10
            except:
                pyautogui.alert(text='O programa de Emissão de NFe não está aberto!\nAperte em OK para abrir e prosseguir com o programa!', button='Ok')
                abrir_programas_de_emissao("C:/SICNET/NFe5/nfe.exe", 2)
                window_get = pygetwindow.getWindowsWithTitle('Emissor de Nota Fiscal Eletrônica (NF-e)')[0]
                window_get.activate()
                window_get.maximize()
                retorno = True
                count = 10
        if retorno == True:
            return True
        elif retorno == False:
            return False

    def gerar_arquivos_nfe(mes):
        time.sleep(1)
        pyautogui.click(x=749, y=418)
        
        time.sleep(1)
        pyautogui.write(mes)

        time.sleep(1)
        pyautogui.click(x=670, y=391)

        time.sleep(1)
        pyautogui.click(x=570, y=386)
        
        time.sleep(1)
        pyautogui.click(x=557, y=458)

        time.sleep(4)
        pyautogui.click(x=595, y=436)

        time.sleep(1)
        pyautogui.click(x=571, y=435)

        time.sleep(3)
        pyautogui.hotkey('alt', 'f4')

    def recortando_arquivos_para_pasta_do_speed_fiscal(local):
        pasta_dos_arquivos_gerados = "C:/Users/joaod/Documents/Arquivos XML de notas emitidas"
        diretorios = []
        for diretorio, subpastas, arquivos in os.walk(pasta_dos_arquivos_gerados):
            for arquivo in arquivos:
                diretorios.append(os.path.join(os.path.realpath(diretorio), arquivo))
        for arquivo in diretorios:
            shutil.move(arquivo, local)

    def criando_diretorio_do_mes(m):
        mes = m.replace("/","-")
        local = f'C:/Users/joaod/Documents/SPEED/{mes}'
        try:
            os.mkdir(local)
        except:
            print("Diretorio Já existente!: "+str(local))
        return local

"""
-----------------------Metodos HotKey-----------------------
"""
def salvar_numeros(caminho, lista):
    arquivo = open(caminho, 'w')
    for item in lista:
        arquivo.writelines(str(item)+"\n")

def extraindo_do_clipboard():
    #win32clipboard.OpenClipboard()
    #data = win32clipboard.GetClipboardData()
    #win32clipboard.CloseClipboard()
    return ""#data

class KeyHot:

    def executando_hotkey():
        comparacao = extraindo_do_clipboard()
        numeros = []

        print("----------HEYHOT COPY BY: ADRIEL ;P----------\nCopie algum numero de pedido para dar inicio a gravação de dados.")
        while True:
            try:
                data = extraindo_do_clipboard()
                if data != comparacao:
                    print("Codigo de pedido copiado: "+str(data))
                    if str(data) == "exit":
                        break
                    else:
                        pass
                    numeros.append(str(data))
                    #print(numeros)
                    comparacao = data
                    #notificacao(data)
                elif data == comparacao:
                    pass
                time.sleep(0.5)
            except:
                pyautogui.alert("Nenhum dado encontrado no clipboard!\nCopie alguma informação de texto para area de transferência e execute novamente o programa para que ele funcione corretamente!")
        #caminho = "C:\\Users\\joaod\\Desktop\\projeto_alpha\\notas_a_dar_baixa.txt"
        caminho = str(os.getcwd()) + "\\notas_a_dar_baixa.txt"
        print(caminho)
        print("---Criando lista de notas---")
        print(numeros)
        salvar_numeros(caminho, numeros)
        print("---Lista criada com sucesso---")
        #os.system("C:\\Users\\joaod\\Desktop\\projeto_alpha\\notas_a_dar_baixa.txt")
        os.system(caminho)
        time.sleep(5)

        """
        108245
        108246
        108247
        exit
        """