from apscheduler.scheduler import Scheduler
import pika
import util
import json
import logging


class send_message():

    def __init__(self):
        credentials = pika.PlainCredentials('inspur', 'inspur')
        flag, rabbitmq_ip = util.getRabbitmqIp()
        parameters = pika.ConnectionParameters(rabbitmq_ip, 5672, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def send(self, name, body, arguments):
        """
        :param name:
        :param body:
        :param arguments:
        :return:
        """
        try:
            self.channel.queue_declare(queue=name, durable=True, auto_delete=True, arguments=arguments)
            body = json.dumps(body)
            self.channel.basic_publish(exchange="", routing_key=name, body=body)
            self.connection.close()
        except Exception as e:
            logging.error(str(e.message))
            self.connection.close()
            pass

    def exchange_send(self, name, body, arguments):
        """

        :param name:
        :param body:
        :param arguments:
        :return:
        """
        try:
            self.channel.exchange_declare(exchange="exchangeTest", type="direct", durable=True, auto_delete=False)
            self.channel.queue_declare(queue=name, durable=True, auto_delete=True, arguments=arguments)
            body = json.dumps(body)
            self.channel.basic_publish(exchange="exchangeTest", routing_key=name, body=body)
            self.connection.close()
        except Exception as e:
            logging.error(str(e.message))
            self.connection.close()
            pass

    def close_connect(self):
        self.connection.close()






