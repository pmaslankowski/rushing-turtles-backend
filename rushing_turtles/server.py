import asyncio
import websockets
import logging

from rushing_turtles.game_controller import GameController
from rushing_turtles.messages import MessageDeserializer, MsgToSend

CLEAR_DISCONNECTED_PERIOD = 30


class GameServer(object):

    def __init__(self, controller: GameController,
                 deserializer: MessageDeserializer):
        self.controller = controller
        self.deserializer = deserializer

    async def serve(self, websocket, path):
        try:
            async for message in websocket:
                try:
                    logging.info(f'Message received: {message}')

                    deserialized_message = self.deserializer.deserialize(
                        message)
                    messages_to_send = self.controller.handle(
                        deserialized_message, websocket)
                    await self._send_messages(messages_to_send)
                except ValueError as e:
                    logging.error(f'An error occured: {e}')
                    error_msg = MsgToSend(
                        websocket,
                        message='error',
                        details=str(e),
                        offending_message=message
                    )
                    await error_msg.send()
        except Exception as e:
            logging.error(f'An exception occured: {e}')
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

    async def clear_disconnected(self):
        while True:
            await asyncio.sleep(CLEAR_DISCONNECTED_PERIOD)
            logging.info('Clearing disconnected players')
            await self._send_messages(self.controller.clear_disconnected())


if __name__ == '__main__':
    addr = '0.0.0.0'
    port = 8000
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info(f'Starting server... Address: {addr}, port: {port}')

    controller = GameController()
    deserializer = MessageDeserializer()
    server = GameServer(controller, deserializer)

    start_server = websockets.serve(server.serve, addr, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_until_complete(server.clear_disconnected())
    asyncio.get_event_loop().run_forever()
