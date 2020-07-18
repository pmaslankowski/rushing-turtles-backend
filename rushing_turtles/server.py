import json
import asyncio
import websockets
import logging

from typing import List

from rushing_turtles.game_controller import GameController
from rushing_turtles.messages import MessageDeserializer, MsgToSend

class GameServer(object):

  def __init__(self, controller : GameController, deserializer : MessageDeserializer):
    self.controller = controller
    self.deserializer = deserializer

  async def serve(self, websocket, path):
    try:
      async for message in websocket:
        try:
          print(f'Message received: {message}')

          deserialized_message = self.deserializer.deserialize(message)
          messages_to_send = self.controller.handle(deserialized_message, websocket)
          self._send_messages(messages_to_send)
        except ValueError as e:
          logging.error(f'An error occured: {e}')
          error_msg = MsgToSend(websocket,
            message='error', details=str(e), offending_message=message)
          await error_msg.send()
    finally:
      messages_to_send = self.controller.disconnected(websocket)
      await self._send_messages(messages_to_send)
  
  async def _send_messages(self, messages):
    if messages:
      if isinstance(messages, list):
        for msg in messages:
          await msg.send()
        else:
          await messages.send()

if __name__ == '__main__':
  addr = '0.0.0.0'
  port = 8000
  print(f'Starting server... Address: {addr}, port: {port}')

  controller = GameController()
  deserializer = MessageDeserializer()
  server = GameServer(controller, deserializer)

  start_server = websockets.serve(server.serve, addr, port)

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()