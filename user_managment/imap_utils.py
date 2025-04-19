import imaplib
import email
from email.mime.text import MIMEText
from django.conf import settings

def send_email_via_imap(subject, body, to_email):
    # Connexion au serveur IMAP
    imap_server = imaplib.IMAP4_SSL(settings.EMAIL_HOST)
    imap_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Création du message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.DEFAULT_FROM_EMAIL
    msg['To'] = to_email

    # Envoi du message
    imap_server.append('Drafts', '', imaplib.Time2Internaldate(time.time()), str(msg).encode('utf-8'))
    
    # Déplacement du message des brouillons vers la boîte d'envoi
    imap_server.select('Drafts')
    typ, data = imap_server.search(None, 'ALL')
    for num in data[0].split():
        imap_server.copy(num, 'Sent')
        imap_server.store(num, '+FLAGS', '\\Deleted')
    imap_server.expunge()

    # Déconnexion
    imap_server.close()
    imap_server.logout()