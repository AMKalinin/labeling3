from enum import Enum
import os

class methods(Enum):
    @classmethod
    def unique_id(cls):
        return list(map(lambda c: c.value[0], cls))
    @classmethod
    def base(cls):
        return list(map(lambda c: c.value[1], cls))
    @classmethod
    def code(cls):
        return list(map(lambda c: c.value[2], cls))
    @classmethod
    def color(cls):
        return list(map(lambda c: c.value[3], cls))
    @classmethod
    def name(cls):
        return list(map(lambda c: c.value[4], cls))


class bases(methods):
    water           = 0, '', '', '', 'Вода'
    green           = 1, '', '', '', 'Растительность'
    surface         = 2, '', '', '', 'Площадные объекты'
    infrastructure  = 3, '', '', '', 'Объекты и сооружения'


class classes(methods):
    #name = unique id, base, class number, globalcolor id [6-18], text description
    c100 = 0,   0, 100, 6,  "Базовый Вода" #"Объект отсутствует"
    c110 = 1,   0, 110, 7,  "Река, канал"
    c120 = 2,   0, 120, 8,  "Озеро, пруд, водохранилище"
    c130 = 3,   0, 130, 9,  "Болото, рисовое поле"
    c140 = 4,   0, 140, 10, "Океан, море"  

    c200 = 5,   1, 200, 11,  "Базовый Растительность" #"Объект отсутствует"
    c210 = 6,   1, 210, 12,  "Заросли кустарников и прочей низкой растительности (в т.ч. луга и степи)"
    c220 = 7,   1, 220, 13,  "Редкий лесной массив (редко стоящие деревья)"
    c230 = 8,   1, 230, 14, "Лесной массив (в т. ч. густые массивы)"

    c300 = 9,   2, 300, 15, "Базовый Площадные объекты" #"Объект отсутствует"
    c310 = 10,  2, 310, 16, "Город или другой населенный пункт"
    c320 = 11,  2, 320, 17, "Промышленное предприятие неопределённого типа"
    c321 = 12,  2, 321, 18, "Порт"
    c322 = 13,  2, 322, 6, "Эл. Станция"
    c323 = 14,  2, 323, 7, "НПЗ"
    c350 = 15,  2, 350, 8, "Пески"   

    c400 = 16,  3, 400, 9, "Базовый Объекты и сооружения"#"Объект отсутствует"
    с401 = 17,  3, 401, 10,  "Объект неопределенного типа"
    c410 = 18,  3, 410, 11,  "Плотина, дамба"
    с411 = 19,  3, 411, 12,  "Мост"
    c420 = 20,  3, 420, 13,  "Автомобильная дорога"
    с421 = 21,  3, 421, 14,  "Железная дорога"
    c430 = 22,  3, 430, 15,  "Линия эл. передач"
    c440 = 23,  3, 440, 16,  "Скалы"
    с441 = 24,  3, 441, 17,  "Террикон, отвал, насыпь, курган"
    c450 = 25,  3, 450, 18, "Здание неопределенного типа"
    с451 = 26,  3, 451, 6, "Жилое строение"
    с452 = 27,  3, 452, 7, "Промышленное строение или сооружение"
    с453 = 28,  3, 453, 8, "Причал"
    с454 = 29,  3, 454, 9, "Культурные и религиозные здания и сооружения"
    с455 = 30,  3, 455, 10, "Склад"
    с456 = 31,  3, 456, 11, "Склад горючего"
    с460 = 32,  3, 460, 12, "Аэродром"
    с461 = 33,  3, 461, 13, "Портовые сооружения и краны"
    с490 = 34,  3, 490, 14,  "Особые здания"

class hdfs(Enum):
    POSTFIX     = '.hdf5'
    NAME        = '__name__'
    CLASSES     = '__classes__'
    TIME_C      = '__time_created__'
    TIME_U      = '__time_updated__'
    DESCRIPTION = '__description__'
    TASK_COUNT  = '__task_count__'

class tasks(Enum):
    COUNT       = '__polygon_count__'
    STATUS      = '__task_status__'
    LEFT        = '__tasks_left__'
    RIGHT       = '__tasks_right__'
    TO_DO       = '__0__' #при создании файла проекта, при добавлении задачи
    IN_PROGRESS = '__1__' #у задачи есть хотя бы один атрибут маски
    TO_CHECK    = '__2__' #нажата кнопка отправить на проверку
    DONE        = '__3__' #модератор нажал кнопку 

class items(Enum):
    path        = os.getcwd()

    PROJECTS    = path + '/' + '__projects__'   + '/'
    IMAGES      = path + '/' + '__images__'     + '/'
    ICONS       = path + '/' + '__icons__'      + '/'
    FONTS       = path + '/' + '__fonts__'      + '/'

    #TASK_WIDGET
    #tocheck     = ICONS + '/' + 'cancel_tbtn.png'
    #redo        = ICONS + '/' + 'cancel_tbtn.png'
    #checked     = ICONS + '/' + 'cancel_tbtn.png'
    #status_todo = ICONS + '/' + 'previous_tbtn.png'
    #status_inpr = ICONS + '/' + 'next_tbtn.png'
    #status_toch = ICONS + '/' + 'tofirst_tbtn.png'

    tocheck     = ICONS  + 'next_tbtn.png'
    redo        = ICONS  + 'previous_tbtn.png'
    checked     = ICONS  + 'Проверена ОК.png'
    status_todo = ICONS  + 'Не начата.png'
    status_inpr = ICONS  + 'В работе.png'
    status_toch = ICONS  + 'Проверка.png'

    first       = ICONS  + 'Перейти к первой задаче.png'
    previous    = ICONS  + 'Перейти к предыдущей задаче.png'
    next        = ICONS  + 'Перейти к следующей задаче.png'
    last        = ICONS  + 'Перейти к последней задаче.png'

    add         = ICONS  + 'Добавить новую задачу.png'
    delete      = ICONS  + 'Удалить задачу.png'
    showall     = ICONS  + 'Показать все полигоны.png'
    hideall     = ICONS  + 'Спрятать все полигоны.png'

    new         = ICONS  + 'Новый полигон_1.png'
    save        = ICONS  + 'Сохранить.png'
    discard     = ICONS  + 'Спрятать все полигоны.png'
    reseg       = ICONS  + 'Сбросить нарисованное.png'
    delshape    = ICONS  + 'Удалить.png'



    #

class shapes(Enum):
    NONE        = 0
    POLYGON     = 1
    RECTANGLE   = 2
    ELLIPSE     = 3

class aerial(Enum):
    SOURCE      = '__aerial_device(txt)__'
    ALTITUDE    = '__altitude(km)__'
    LATITUDE    = '__latitude_top_left_point(xx:yy:zz)__'
    LONGITUDE   = '__longitude_top_left_point(xx:yy:zz)__'
    SUN         = '__sun_azimuth(xx:yy:zz)__'

    SPATIAL     = '__resolution(metres:pixel)__'
    SIZE        = '__pixels(width:height)__'

    DATE        = '__date_stamp(dd:mm:yy)__'
    TIME        = '__time_stamp(hh:mm)__'