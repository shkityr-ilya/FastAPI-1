import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI(
    title='Сервис объявлений купли/продажи',
    description='''У каждого объявления должны быть следующие поля: 
                 - Заголовок (`title`)
                 - Описание (`description`)
                 - Цена (`price`)
                 - Автор(`author`)
                  - Дата создания (`creation_date`) 

                   Реализовать методы:
                 - Создание
                 - Обновление 
                 - Удаление
                 - Получение по ID
                 - Поиск по полям 
                 ''',
    version='0.0.1'
)


# Модель объявления
class Advertisement(BaseModel):
    id: int = None
    title: str
    description: str
    price: float
    author: str
    creation_date: date


classifieds_service = [
    {
        'id': 1,
        'title': 'Объявление № 1',
        'description': 'Продам велосипед в хорошем состоянии',
        'price': 15000,
        'author': 'Иван',
        'creation_date': '2026-08-31'
    },
    {
        'id': 2,
        'title': 'Объявление № 2',
        'description': 'Детские санки с веревкой, металлические, крепкие.',
        'price': 1500,
        'author': 'Аня',
        'creation_date': '2026-08-15'
    },
    {
        'id': 3,
        'title': 'Объявление № 3',
        'description': 'Отдам котенка британской породы в добрые руки',
        'price': 0,
        'author': 'Елена Сергеевна',
        'creation_date': '2026-08-29'
    },
    {
        'id': 4,
        'title': 'Объявление № 4',
        'description': 'iPhone 14 Pro Max 256Gb, цвет Deep Purple, состояние нового, полный комплект.',
        'price': 95000,
        'author': 'Максим',
        'creation_date': '2026-08-30'
    },
    {
        'id': 5,
        'title': 'Объявление № 5',
        'description': 'Услуги репетитора по математике для 5-9 классов. Подготовка к ЕГЭ.',
        'price': 1000,
        'author': 'Дмитрий Петрович',
        'creation_date': '2026-08-28'
    }
]


# Функция для генерации нового id
def get_next_id():
    return max(ad['id'] for ad in classifieds_service) + 1 if classifieds_service else 1


# Получить все объявления или поиск по полям
@app.get('/advertisement',
         summary='Получить все объявления или поиск по полям',
         tags=['Сервис объявлений📜'])
def all_advertisement(
        title: str = None,
        description: str = None,
        price: float = None,
        author: str = None,
        creation_date: date = None
):
    result = []
    for ad in classifieds_service:
        if title and ad['title'].lower() != title.lower():
            continue
        if description and ad['description'].lower() != description.lower():
            continue
        if price is not None and ad['price'] != price:
            continue
        if author and ad['author'].lower() != author.lower():
            continue
        if creation_date and ad['creation_date'] != str(creation_date):
            continue
        result.append(ad)
    return result


# Получить объявление по ID
@app.get('/advertisement/{ad_id}',
         summary='Получить объявление по ID',
         tags=['Сервис объявлений📜'])
def get_advertisement(ad_id: int):
    for advertisement in classifieds_service:
        if advertisement['id'] == ad_id:
            return advertisement
    raise HTTPException(status_code=404, detail='Объявление не найдено')


# Создать новое объявление
@app.post('/advertisement',
          summary='Создать новое объявление',
          tags=['Сервис объявлений📜'])
def create_advertisement(advertisement: Advertisement):
    new_ad = advertisement.dict()
    new_ad['id'] = get_next_id()
    classifieds_service.append(new_ad)
    return advertisement


# Обновить все объявление

@app.put('/advertisement/{ad_id}',
         summary='Обновить все объявление',
         tags=['Сервис объявлений📜']
         )
def replace_advertisement(ad_id: int, ad: Advertisement):
    for i, existing_ad in enumerate(classifieds_service):
        if existing_ad['id'] == ad_id:
            ad_dict = ad.dict()
            ad_dict['id'] = ad_id
            classifieds_service[i] = ad_dict
            return ad_dict
    raise HTTPException(status_code=404, detail='Объявление не найдено')


# Частичное обновление объявления

@app.patch('/advertisement/{ad_id}',
           summary='Частичное обновление объявления',
           tags=['Сервис объявлений📜']
           )
def update_advertisement_partially(ad_id: int, ad: Advertisement):
    for i, existing_ad in enumerate(classifieds_service):
        if existing_ad['id'] == ad_id:
            if ad.title is not None:
                existing_ad['title'] = ad.title
            if ad.description is not None:
                existing_ad['description'] = ad.description
            if ad.price is not None:
                existing_ad['price'] = ad.price
            if ad.author is not None:
                existing_ad['author'] = ad.author
            if ad.creation_date is not None:
                existing_ad['creation_date'] = str(ad.creation_date)
            return existing_ad
    raise HTTPException(status_code=404, detail='Объявление не найдено')


# Удалить объявление
@app.delete('/advertisement/{ad_id}',
            summary='Удалить объявление',
            tags=['Сервис объявлений📜']
            )
def delete_advertisement(ad_id: int):
    for index, ad in enumerate(classifieds_service):
        if ad['id'] == ad_id:
            del classifieds_service[index]
            return {'detail': 'Объявление удалено'}
    raise HTTPException(status_code=404, detail='Объявление не найдено')


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
