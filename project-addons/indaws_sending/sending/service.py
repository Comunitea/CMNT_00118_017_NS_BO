import md5
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport

import logging

_logger = logging.getLogger(__name__)


class SendingService:

    delivery_url = 'https://wssending.alertran.net/sending/ws_clientes?wsdl'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def grabar_envio(self, fichero, center):

        session = Session()
        # session.auth = HTTPBasicAuth(self.username, self.password)
        # connect_client = Client(self.delivery_url,
        #                         transport=Transport(session=session))
        connect_client = Client(self.delivery_url)

        passwd = md5.new()
        passwd.update(self.password)
        result = connect_client.service.\
            entrada_expediciones(str(center), fichero, 'xml',
                                 str(passwd.hexdigest()))

        _logger.warning("fichero: ")
        _logger.warning(fichero)
        _logger.warning("Resultado: " + result)

        return result

    def conseguir_pdf(self, expedicion, center):

        session = Session()
        # session.auth = HTTPBasicAuth(self.username, self.password)
        # connect_client = Client(self.delivery_url,
        #                         transport=Transport(session=session))
        connect_client = Client(self.delivery_url)
        passwd = md5.new()
        passwd.update(self.password)
        result = connect_client.service.\
            etiquetarExpedicionPDF(str(center), expedicion, self.username,
                                   str(passwd.hexdigest()))

        _logger.warning("Resultado: " + result)

        return result
