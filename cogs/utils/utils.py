import json
import random

import discord
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw


def prepare_mask(size, antialias=2):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(size, Image.ANTIALIAS)


def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0:
        im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0:
        im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)


def draw_progress(image: Image, percent: int) -> Image:
    if percent < 0:
        return Image
    if percent > 100:
        percent = 100

    x1 = 260 + int(613 * percent / 100)
    image = image.copy()

    drawer = ImageDraw.Draw(image)
    drawer.rectangle(xy=[(260, 178), (x1, 218)], fill=(255, 20, 147))

    return image


def find_rank(users, member):
    high_score_list = sorted(users, key=(lambda x: users[x]['level']), reverse=True)
    id = str(member.id)
    rank = high_score_list.index(id) + 1
    return rank


async def update_warn(users, user, warn):
    users[str(user.id)]['warn'] += warn


async def update_money(users, user, money: int):
    users[str(user.id)]['balance'] += money


def save_data(users):
    with open('files/file/users_info.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=1, ensure_ascii=False)


async def update_data(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {

        }

        users[str(user.id)]['name'] = str(user.display_name)
        users[str(user.id)]['level'] = 1
        users[str(user.id)]['xp'] = 0
        users[str(user.id)]['xpTime'] = ''
        users[str(user.id)]['balance'] = 1000
        users[str(user.id)]['warn'] = 0

        print(f'Create info about user: {user}')

    if not str(user.display_name) == users[str(user.id)]['name']:
        users[str(user.id)]['name'] = str(user.display_name)

    save_data(users)


async def update_pets(pet, user):
    if not str(user.id) in pet:
        pet[str(user.id)] = {
        }

        pet[str(user.id)]['name'] = str(user.display_name)
        pet[str(user.id)]['box'] = 0
        pet[str(user.id)]['pets'] = {
        }

        pet[str(user.id)]['pets']['activated'] = 0
        pet[str(user.id)]['pets']['PutinTime'] = ''

        print(f'Create pets user: {user}')

    if not str(user.display_name) == pet[str(user.id)]['name']:
        pet[str(user.id)]['name'] = str(user.display_name)

    save_pets(pet)


def save_pets(pet):
    with open('files/file/users_pets.json', 'w', encoding='utf-8') as f:
        json.dump(pet, f, indent=1, ensure_ascii=False)


def checkPets(pet1, user):
    with open('files/file/users_pets.json', 'r', encoding='utf-8') as f:
        pet = json.load(f)

    pets = ['pikachu', 'lexa', 'putin']
    Jpet = pet[str(user.id)]['pets']
    v_0 = pets.index(pet1)

    if pets[v_0] in Jpet:
        if pet[str(user.id)]['pets'][pets[v_0]] == 1:
            return True
        else:
            return False


def randomColor():
    return discord.Color(value=random.randint(0, 16777215))
