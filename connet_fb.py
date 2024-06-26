# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:01:59 2023

@author: Casta
"""

from fbchat import log, Client
import common_functions

# Subclase fbchat.Client y anula los métodos requeridos
class EchoBot(Client):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # If you're not the author, echo
        if author_id != self.uid:
            self.send(message_object, thread_id=thread_id, thread_type=thread_type)        