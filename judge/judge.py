import docker
from docker.models.containers import Container
import requests

from time import sleep


def get_player(name: str, image: str, port: int) -> Container:
    client = docker.from_env()
    container = client.containers.run(
            image=image,
            detach=True,
            remove=True,
            ports={ '5000': port },
            name=name,
            )
    if not isinstance(container, Container):
        raise ValueError('Not an instastance of Container')
    return container

def get_move(oponents_last_move: str, port: int) -> str:
    return requests.post(
            f'http://localhost:{port}/',
            headers={'Content-type': 'text/json'},
            json={'oponents_last_move': oponents_last_move}
            ).json()['my_move']


def play(image_a: str, image_b: str) -> None:
    player_a = get_player('player_a', image_a, 6969)
    player_b = get_player('player_b', image_b, 9696)

    # give time to startup the containers
    sleep(1)

    n = 10
    round = 0
    score_a = 0
    score_b = 0
    last_move_a = 'none'
    last_move_b = 'none'

    while round < n:
        move_a = get_move(last_move_b, 6969)
        move_b = get_move(last_move_a, 9696)

        print(f'{move_a=}')
        print(f'{move_b=}')
        
        if move_a == 'stay silent' and move_b == 'stay silent':
            score_a += 1
            score_b += 1
        if move_a == 'stay silent' and move_b == 'testify':
            score_a += 3
            score_b += 0
        if move_a == 'testify' and move_b == 'stay silent':
            score_a += 0
            score_b += 3
        if move_a == 'testify' and move_b == 'testify':
            score_a += 2
            score_b += 2

        round += 1 
        last_move_a = move_a
        last_move_b = move_b

    player_a.kill()
    player_b.kill()
    print(f'{score_a=}')
    print(f'{score_b=}')
    if score_a < score_b:
        print('Player A wins')
    if score_a > score_b:
        print('Player B wins')
    if score_a == score_b:
        print('Tie')
    
