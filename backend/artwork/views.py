from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

MINIO_HOST = '127.0.0.1'
MINIO_PORT = 9000
MINIO_DIR = 'web-img'

# Данные о картинах
paintings = [
    {
        'id': 0,
        'title': "Постоянство Памяти",
        'img_name': "memory.png",
        
       
        'short_description': "Известная картина, изображающая плавящиеся часы.",
        'description': "Картина 'Постоянство памяти' (1931) является одной из самых узнаваемых работ сюрреализма. Она изображает плавящиеся карманные часы в пейзаже, который символизирует относительность времени и нестабильность реальности."
    },
    {
        'id': 1,
        'title': "Крик",
        'img_name': "krik.png",
        
        'short_description': "Эмоциональная картина , представляющая внутренние страхи и тревоги.",
        'description': "Картина 'Крик' (1893)  изображает фигуру на мосту с ужасающим криком, выражая человеческое состояние отчаяния и страха."
    },
    {
        'id': 2,
        'title': "Звездная ночь",
        'img_name': "starry_night.png",
       
        'short_description': "Одна из самых известных картин , изображающая вихри ночного неба.",
        'description': "'Звездная ночь' (1889) — это шедевр, где изображается завораживающее ночное небо, полное вихрей и светящихся звезд, создавая уникальное представление о природе."
    },
    {
        'id': 3,
        'title': "Афинская школа",
        'img_name': "school.png",
        
        'short_description': "Фреска, изображающая знаменитых философов античности.",
        'description': "Фреска 'Афинская школа' (1511)  изображает Платона и Аристотеля в центре, окруженных философами и учеными, представляя триумф разума и научной мысли."
    },
    {
        'id': 4,
        'title': "Ночной дозор",
        'img_name': "night.png",
       
        'short_description': "Известная картина, изображающая вооруженную городскую милицию.",
        'description': "'Ночной дозор' (1642) — это шедевр, который изображает членов амстердамской стрелковой роты, подготовленных к выполнению своего долга. Картина выделяется своим драматизмом и светотеневым контрастом."
    },
    {
        'id': 5,
        'title': "Сотворение Адама",
        'img_name': "adam.png",
        
        'short_description': "Фреска, изображающая момент создания человека.",
        'description': "'Сотворение Адама' (1512) — одна из фресок Сикстинской капеллы, изображающая библейскую сцену, где Бог протягивает руку к Адаму, даруя ему жизнь. Это один из самых узнаваемых образов в истории искусства."
    }
]


order_list = [
    {
        'id': 0,
        'title': "Сальвадор Дали",
        'img_name': "memory.png"
    },
    {
        'id': 1,
        'title': "Эдвард Мунк",
        'img_name': "krik.png"
    },
    {
        'id': 2,
        'title': "Винсент Ван Гог",
        'img_name': "starry_night.png"
    }
]



# artwork/views.py


def paintings_list(request):
    # Получаем данные из строки поиска
     # Получаем данные из строки поиска
    search_query = request.GET.get('painting_title', '').lower()

    # Формируем список отфильтрованных картин по запросу
    filtered_paintings = [
        painting for painting in paintings
        if painting['title'].lower().startswith(search_query)
    ] if search_query else paintings  # Если строка поиска пуста, показываем все картины

    # Формируем путь к изображениям для каждого элемента списка
    for painting in filtered_paintings:
        painting['img_path'] = f'http://{MINIO_HOST}:{MINIO_PORT}/{MINIO_DIR}/{painting["img_name"]}'

    # Рендерим шаблон с данными о картинах
    return render(request, 'paintings_list.html', {
        'data': {
            'paintings': filtered_paintings,
            'search_query': search_query,
            'order_count': len(order_list)  
        }
    })

def painting_detail(request, id):
    # Детальная информация о картине
    for painting in paintings:
        if painting['id'] == id:
            painting['img_path'] = f'http://{MINIO_HOST}:{MINIO_PORT}/{MINIO_DIR}/{painting["img_name"]}'
            return render(request, 'painting_detail.html', {'painting': painting})

    return render(request, 'painting_detail.html')

def view_order(request, order_id):
    # Здесь мы передаём весь список картин в шаблон
    order_items = order_list  # Моделируем три заявки на экспертизу

    # Если заказ не найден, можем вернуть 404 или другое сообщение
    if not order_items:
        return render(request, 'order_not_found.html', {})

    # Отображаем три картины в заявке
    return render(request, 'order_summary.html', {'data': order_items})