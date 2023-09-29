from src.model.model import Modelos
from src.view.view import View
from random import shuffle, choice

class Jogo():

    def apresenta():
        View.saudacao()
        # mostrar as regras depois
    
    def define_jogadores(): # coletar jogadores
        nomes_jogadores: list[str] # Lista para armazenar o nome dos jogadores
        nomes_jogadores = Modelos.coletar_jogadores() # Coletando os jogadores
        jogadores = Jogo.sortear_ordem_jogadores(nomes_jogadores)
        return jogadores

    def sortear_ordem_jogadores(lista):
        View.embaralhando_jogadores()
        shuffle(lista)
        return lista

    def define_tubo_dados(): # criar o tubo com os dados
        try:
            dados_cores = list[str]
            dados_cores = Modelos.definir_dados()
            dados_faces = list[str]
            dados_faces = Modelos.definir_faces()
            tubo = [dados_cores, dados_faces]
            return tubo
        except Exception as error:
            print("\nAn exception occurred:", error)

    def jogar_dados(tubo):
        if len(tubo[0]) < 4:
            print('Enchendo os dados de volta... ')
            tubo[0] = Modelos.definir_dados()
        dado_sorteado = choice(tubo[0])
        if dado_sorteado in tubo[1]:
            face_sorteada = choice(tubo[1][dado_sorteado])
        return [dado_sorteado,face_sorteada]
    
    def salvar_cerebros(resultado, pontos): # salvando os pontos da rodada
        if resultado[1] == '🧠':
            pontos.append(resultado[1])
        return pontos
    
    def contar_tiros_rodada(resultado, tiros_rodada): # salvando os pontos da rodada
        if resultado[1] == '🔫':
            tiros_rodada.append(resultado[1])
        return tiros_rodada
    
    def retirar_dados_jogada(resultado, dados):
        if resultado[1] != '👣':
            dados.remove(resultado[0])
        return dados

    def retornar_dados_jogada(resultado, dados):
        if resultado[1] != '🧠':
            dados.append(resultado[0])
        return dados


    def start():
        Jogo.apresenta()
        jogadores = Jogo.define_jogadores()
        View.mostrar_ordem_jogadores(jogadores)
        vencedor = False

        while True: # jogar enquanto não houver vencedor

            for jogador in jogadores: # definir a rodada conforme o jogadore da vez
                View.mostrar_jogador_da_vez(jogador)
                tubo_dados = Jogo.define_tubo_dados()
                tiros_rodada = []

                while True: # jogar enquanto não perder rodada

                    rodada = []

                    print('')
                    # print('tubo = ',tubo_dados[0])
                    print('roda = ',rodada)

                    for i in range(3):
                        
                        resultado = Jogo.jogar_dados(tubo_dados) # jogar os dados
                        rodada.append(resultado)
                        tubo_dados[0] = Jogo.retirar_dados_jogada(resultado, tubo_dados[0]) # retirar do tubo os dados que sairam


                    for i in range(3):
                        Jogo.salvar_cerebros(rodada[i], jogador['pontos']) # guardar os pontos de cada jogador
                        Jogo.contar_tiros_rodada(rodada[i], tiros_rodada)
                    

                    print('')
                    print('Resultado rodada: ', rodada) 
                    # print('dados que sobraram: ', tubo_dados[0])
                    print('tiros... ', tiros_rodada) 
                    print('cerebros acumulado: ', jogador['pontos']) 

                    encerra_rodada = tiros_rodada.count('🔫') > 2
                    if encerra_rodada:
                        View.mostrar_msg_perda(jogador)
                        break

                    encerra_rodada = jogador['pontos'].count('🧠') > 12
                    if encerra_rodada:
                        vencedor = True
                        View.mostrar_msg_vencedor(jogador) # mostrar vencedor
                        break

                    continua_rodada = input('\nVai continuar jogando os dados? (S/N):\n ') # verificar se jogador da vez vai continuar 
                    if continua_rodada == 'n':
                        break
                        

                    tubo_dados[0] = Jogo.retornar_dados_jogada(resultado, tubo_dados[0]) # redefinir os dados no tubo


            if vencedor:
                break


        View.encerramento_jogo()