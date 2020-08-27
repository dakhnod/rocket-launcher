import websockets
import asyncio


def control_socket_start(launcher_control):
    async def echo(websocket, path):
        async for message in websocket:
            print('message: ' + message)
            launcher_control.parse_command(message)

    print('control socket started')
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(echo, '', 82))
    asyncio.get_event_loop().run_forever()
