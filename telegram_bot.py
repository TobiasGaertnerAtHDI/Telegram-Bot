import requests

from config import TELEGRAM_SEND_MESSAGE_URL

class TelegramBot:

    def __init__(self):
        """"
        Initializes an instance of the TelegramBot class.

        Attributes:
            chat_id:str: Chat ID of Telegram chat, used to identify which conversation outgoing messages should be send to.
            text:str: Text of Telegram chat
            first_name:str: First name of the user who sent the message
            last_name:str: Last name of the user who sent the message
        """

        self.chat_id = None
        self.text = None
        self.first_name = None
        self.last_name = None


    def parse_webhook_data(self, data):
        """
        Parses Telegram JSON request from webhook and sets fields for conditional actions

        Args:
            data:str: JSON string of data
        """

        message = data['message']

        self.chat_id = message['chat']['id']
        self.incoming_message_text = message['text'].lower()
        self.first_name = message['from']['first_name']
        self.last_name = message['from']['last_name']


    def action(self):
        """
        Conditional actions based on set webhook data.

        Returns:
            bool: True if the action was completed successfully else false
        """

        success = None

        if self.incoming_message_text == '/start':
            self.outgoing_message_text = 'Herzlich Willkommen {} {} 👋 ! Freut mich, dich kennenzulernen. Hast du Interesse an einer günstigen /Haftpflichtversicherung?'.format(self.first_name, self.last_name)
            success = self.send_message()

        if self.incoming_message_text == '/haftpflichtversicherung':
            self.outgoing_message_text = 'Da hast du Glück, dafür bist du hier an der richtigen Stelle.\nBeantworte einfach ein paar kurze Fragen und schon suchen wir dir in ein paar Minuten den günstigsten Preis 👍 \n/weiter'
            success = self.send_message()

        if self.incoming_message_text == '/weiter':
            self.outgoing_message_text = 'Was würde deine derzeitige Lebenssituation am besten beschreiben? \n/Berufstaetig👷\n/Student👩‍🎓\n/Rentner👵👴 '
            success = self.send_message()

        if self.incoming_message_text == '/berufstaetig' or self.incoming_message_text == '/student' or self.incoming_message_text == '/rentner':
            self.outgoing_message_text = 'Danke!\nNun wüssten wir gerne noch wie du lebst, was würde denn am besten auf dich zutreffen?\n/Wohnung🏢 \n/Einfamilienhaus🏡 \n/Doppelhaushaelfte🏘'
            success = self.send_message()

        if self.incoming_message_text == '/wohnung' or self.incoming_message_text == '/einfamilienhaus' or self.incoming_message_text == '/doppelhaushaelfte':
            self.outgoing_message_text = 'Jetzt haben wir es gleich schon geschafft💪.\nKannst du uns noch schnell deine Adresse mitteilen (Straße+Hausnummer,PLZ+Ort)?'
            success = self.send_message()

        if self.incoming_message_text == 'paulstrasse 15,31067 hannover':
            self.outgoing_message_text =  'Zur Berechnung des günstigsten Preises benötigen wir nun noch eine Angabe wie oft du in den letzen 3 Jahren Schäden gemeldet hast.\n /0  \n/1  \n/2 oder mehr'
            success = self.send_message()

        if self.incoming_message_text == '/1' or self.incoming_message_text == '/2' or self.incoming_message_text == '/0':
            self.outgoing_message_text = 'Besitzt du einen einzelnen Gegenstand, der 5000 Euro oder mehr wert ist?\n /Ja       /Nein'
            success = self.send_message()

        if self.incoming_message_text == '/ja' or self.incoming_message_text == '/nein':
            self.outgoing_message_text = 'Sehr schön, dann hätten wir jetzt alles was wir brauchen.\nWenn du uns jetzt noch dein Geburtsdatum mitteilst, können wir dir deinen günstigsten Preis suchen!\n(Bitte im Format DD.MM.YYYY📅)'
            success = self.send_message()

        if self.incoming_message_text == '03.06.1996':
            geburtsdatum = self.incoming_message_text
            self.outgoing_message_text = 'Dann wären wir jetzt fertig.\nUnser Mega-Angebot für dich lautet :\nEine Privat-Haftpflichtversicherung für nur 50 Euro im Jahr‼️\nBitte bestätige mit deinem Vor und Nachnamen, dass du das Angebot anehmen möchtest.\nMöchtest du das Angebot nicht anehmen, drücke auf /Abbrechen.'
            success = self.send_message()

        if self.incoming_message_text == 'bastian goerlich':
            self.outgoing_message_text = 'Herzlichen Glückwunsch zu deiner neuen Haftpflichtversicherung! 🎉🎉 \nMit der Eingabe deiner Email-Adresse kriegst du nun alle nötigen Dokumente zugeschickt.\n Falls du dich für eine weitere Versicherung interessierst, besuche uns gerne auf unserer Internetadresse : www.hdi.de. '
            success = self.send_message()

        if self.incoming_message_text == '/abbrechen':
            self.outgoing_message_text = 'Oh, das ist ja schade. Falls du dich für eins unserer anderen Angebote interessierst, besuche uns auf unserer Internetseite: www.hdi.de\n Einen schönen Tag noch und auf Wiedersehen!👋'
            success = self.send_message()

        if self.incoming_message_text == 'bastian.goerlich@gmx.net':
            self.outgoing_message_text = 'Vielen herzlichen Dank für dein Vertrauen in die HDI. Die Dokumente sollten nun zu dir unterwegs sein📧.\nEinen schönen Tag noch und auf Wiedersehen!👋'
            success = self.send_message()
        
        if self.incoming_message_text == '/rad':
            self.outgoing_message_text = '🤙'
            success = self.send_message()
            
           
        return success


    def send_message(self):
        """
        Sends message to Telegram servers.
        """

        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(self.chat_id, self.outgoing_message_text))

        return True if res.status_code == 200 else False
    
 
    @staticmethod
    def init_webhook(url):
        """
        Initializes the webhook

        Args:
            url:str: Provides the telegram server with a endpoint for webhook data
        """

        requests.get(url)


