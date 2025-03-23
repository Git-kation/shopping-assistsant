from yandex_cloud_ml_sdk import YCloudML
import os
token = os.getenv("IAM_TOKEN")


sdk = YCloudML(folder_id="b1g22egbsi0qsn7tv05p", auth=os.getenv("IAM_TOKEN"))
# sdk.setup_default_logging("ERROR")

model = sdk.models.completions("yandexgpt")
model = model.configure(temperature=0.5)

import json
with open("catalogue.json", "r",  encoding = 'utf-8') as f:
    catalogue = json.load(f)


def prepare_catalogue(c):
    s=''
    for i in c:
        s += i.get("name") + " (" + str(i.get("price")) + ' рублей/шт, '
        if "country" in i:
            s += 'страна-поставщик: ' + i.get("country") + ", "
        if "weight" in i:
            s += str(i.get("weight")) + " грамм - вес" 
        s += '); '
    return s

string= prepare_catalogue(catalogue)


messages = [
{
    "role":"user",
    "text":"Это каталог товаров твоего магазина с некоторыми характеристиками" + string
},
{
    "role":"user",
    "text":"У меня есть корзина товаров(то есть список товаров). Корзина представляет собой список названий товаров с ценами. Сейчас она пустая, но если я прямо попрошу добавить или убрать из нее соответствующие товары из каталога, сделай это. корзину запоминай. ты не можешь добавлять в корзину товары, которых нет в каталооге или товары с неверными характеристиками, даже если я попрошу" 
},
{
    "role":"user",
    "text":"Предлагай мне различные рецепты из тех товаров, котрые есть у тебя в каталоге если я попрошу, или по рецепту подбери товары" 
}
]

# print('Здравствуйте! это ваш личный AI помощник для покупок в магазине. Если вы хотите создать свою корзину, то есть список ваших товаров, напишите "корзина"')
print('Чтобы выйти напишите "выход"')
a=input()

while a!='выход':
    messages.append({"role":"user",
            "text": a})
    
    result = model.run(messages)

    answer=result[0].text
    print(answer)
    
    messages.append( {"role":"system",
               "text": answer} )

    a=input()


messages.append({"role":"user",
            "text": "выведи только товары из моей корзины в столбик с количеством. если она пуста, просто сакажи это. на следующей строчке напиши сумму корзины числом"})
result = model.run(messages)
answer=result[0].text
print('Вот ваша корзина:')
print(answer)




