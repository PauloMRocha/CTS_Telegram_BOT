from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, Contact
import logging


#relacionado a erros e excessões -
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#Extrai o horario da resposta
def extract_time(answer):
    h = ""
    m = ""

    #porcura por :
    idx = answer.find(':')

    #caso não exista : procura por h
    if(idx < 0):
        idx = answer.find('h')

    #caso i ou h sejam  encontrados muito no começo da resposta
    if(idx < 1):
        return -100, -2

    #extracao das horas
    if(idx>1 and answer[idx-2]>='0' and answer[idx-2]<='9'):
        h += answer[idx-2]
    if(idx>0 and answer[idx-1]>='0' and answer[idx-1]<='9'):
        h += answer[idx-1]

    #extracao dos minutos
    if(idx<(len(answer)-2)):
        if( answer[idx+2]>='0' and answer[idx+2]<='9'):
            m += answer[idx+1]
        if(answer[idx+1]>='0' and answer[idx+1]<='9'):
            m += answer[idx+2]

    #returns
    print(h+":"+m)
    if(h!="" and m==""):
        return int(h), 0

    if(h=="" or m==""):
        return -100, -1
    return int(h), int(m)

# define o comportamento dependendo da resposta
def resp(answer):
    try:
        h,m = extract_time(answer)
    except:
        return -1
    else:
        if(h==-100):
            return m
        if(h<0 or h>23 or m<0 or m>59):
            return 3
        if(h == 13):
            if(m>=50 and m<=55):
                return 1
        if(h == 4 or h==16):
            if(m==20):
                return 4
        if(h == 13):
            if(m==37):
                return 5
    return 2

def start(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ah! Olá jovem, tudo bem com você?\nVocê pode me dizer que horas são?')

def wtii(update,context):
    if context.args:
        answer = str(context.args[0])
        res = resp(answer)

        #mensagnes enviadas para cada resposta
        if(res == 1): #mensagem da resposta correta
            context.bot.send_message(chat_id=update.effective_chat.id, text='Ah óptimo!! Esse era o horário que eu precisava!!')
            context.bot.send_message(chat_id=update.effective_chat.id, text='Aqui, pegue isso como um agradecimento.')
            context.bot.sendDocument(chat_id=update.effective_chat.id, document=open("01", "rb"))
        elif(res == 2): #mensagem para respostas aleatórias
            context.bot.send_message(chat_id=update.effective_chat.id, text='Bom, parece que nossos relógios não batem, alguem terá que ajustar as horas.')
        elif(res == 3): #mensagem para horarios impossíveis
            context.bot.send_message(chat_id=update.effective_chat.id, text='Você está tentando me fazer de bobo?\n Preciso de um horário real!!!')
        elif(res == 4): #mensagem para 4:20
            context.bot.send_message(chat_id=update.effective_chat.id, text='Essa não era a resposta que eu precisava. De qualquer forma parece que está no horário da minha pausa.')
        elif(res == 5): #mensagem para 13:37
            context.bot.send_message(chat_id=update.effective_chat.id, text='3553 3 um 071m0 h0r4r10, m45 41nd4 n40 3 0 qu3 3u pr3c150. V0l73 qu4nd0 3571v3r c0m 53u r3l0610 4ju574d0.')
        else: #mensagem para não horários
            context.bot.send_message(chat_id=update.effective_chat.id, text='Que maneira estranha de escrever um horário. O que geralmente vejo segue o padrão HH:MM! Lembre-se que aqui no Brasil usamos o formato com 24 horas.\nBom, de qualquer forma eu agradeço a resposta...\nEu acho 🤔')
    else: #mensagem para o comando sem argumento
        context.bot.send_message(chat_id=update.effective_chat.id, text='Por favor envie uma resposta junto com o comando.\nExemplo: /resp 10:30')


def main():
    #seta o token
    file_token = open("token.txt", "r")
    token = file_token.read().splitlines()
    file_token.close()

    updater = Updater(token=token[0] , use_context=True)
    dispatcher = updater.dispatcher

    #comandos
    dispatcher.add_handler(CommandHandler("resp", wtii))
    dispatcher.add_handler(CommandHandler("oi", start))
    dispatcher.add_handler(CommandHandler("start", start))

    #starta o bot
    updater.start_polling()
    logging.info("=== A relojoaria está aberta! ===")

    #para o bot
    updater.idle()
    logging.info("===  A relojoaria está fechada! === ")


if __name__ == '__main__':
    main()
