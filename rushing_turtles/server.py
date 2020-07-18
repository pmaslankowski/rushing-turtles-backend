import json
import asyncio
import websockets
import logging

from typing import List

from rushing_turtles.game_controller import GameController
from rushing_turtles.messages import MessageDeserializer

class GameServer(object):

  def __init__(self, controller : GameController, deserializer : MessageDeserializer):
    self.controller = controller
    self.deserializer = deserializer

  async def serve(self, websocket, path):
    async for message in websocket:
      deserialized_message = self.deserializer.deserialize(message)
      messages_to_send = self.controller.handle(deserialized_message, websocket)

      if messages_to_send:
        if isinstance(messages_to_send, list):
          for msg in messages_to_send:
            await msg.send()
        else:
          await messages_to_send.send()

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