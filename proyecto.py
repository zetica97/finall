#Se define las variables para el acceso al API de twitter
import tweepy
from time import sleep
from datetime import datetime
from textblob import TextBlob 
import matplotlib.pyplot as plt 
#%matplotlib inline
consumer_key = 'BpbiwlobtyjDgDf1Be5SemEyB'
consumer_secret = '7bCb5Bo0GJv6FKMCj25c9lweSC7q5J1txdoj9TzQUiCbmVGxB7'
access_token = '1130938369284956165-JwMWsQkcKfpIIVde1ONCuXwBvMm5Pg'
access_token_secret = '33FHGD1jlhvcSRSLLZ5EzWIkH08UkHLMHP42uIiHsiWkU'

 #Se autentica en twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
wait_on_rate_limit_notify=True)

print(api.me().name)

palabra = 'sad'
numero_de_Tweets = 10
lenguaje = 'en'

def ObtenerTweets(palabra="happy",times=100,leguanje="en"):
    #Se define las listas que capturan la popularidad
    popularidad_list = []
    numeros_list = []
    numero = 1
    for tweet in tweepy.Cursor(api.search, palabra, lang=lenguaje).items(numero_de_Tweets):
        try:
            #Se toma el texto, se hace el analisis de sentimiento
            #y se agrega el resultado a las listas
            analisis = TextBlob(tweet.text)
            analisis = analisis.sentiment
            popularidad = analisis.polarity
            popularidad_list.append(popularidad)
            numeros_list.append(numero)
            numero = numero + 1

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break
    return (numeros_list,popularidad_list,numero)





def GraficarDatos(numeros_list,popularidad_list,numero):

    axes = plt.gca()
    axes.set_ylim([-1, 2])
    
    plt.scatter(numeros_list, popularidad_list)
    popularidadPromedio = (sum(popularidad_list))/(len(popularidad_list))
    popularidadPromedio = "{0:.0f}%".format(popularidadPromedio * 100)
    time  = datetime.now().strftime("A : %H:%M\n El: %m-%d-%y")
    plt.text(0, 1.25, 
             "Sentimiento promedio:  " + str(popularidadPromedio) + "\n" + time, 
             fontsize=12, 
             bbox = dict(facecolor='none', 
                         edgecolor='black', 
                         boxstyle='square, pad = 1'))
    
    plt.title("Sentimientos sobre " + palabra + " en twitter")
    plt.xlabel("Numero de tweets")
    plt.ylabel("Sentimiento")
    plt.show()



numeros_list,popularidad_list,numero = ObtenerTweets(palabra,numero_de_Tweets,lenguaje)

GraficarDatos(numeros_list,popularidad_list,numero)


