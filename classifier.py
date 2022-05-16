"""
code_base = ([  "Вода",
                "Растительность",
                "Площадные объекты",
                "Объекты и сооружения"                              ])

code_100 = ([       "100_Объект отсутствует",
                    "110_Река, канал",
                    "120_Озеро, пруд, водохранилище",
                    "130_Болото, рисовое поле",
                    "140_Океан, море"                                 ])

code_200 = ([       "200_Объект отсутствует",
                    "210_Заросли кустарников и прочей низкой растительности (в т.ч. луга и степи)",
                    "220_Редкий лесной массив (редко стоящие деревья)",
                    "230_Лесной массив (в т. ч. густые массивы)"        ])

code_300 =([        "300_Объект отсутствует",
                    "310_Город или другой населенный пункт",
                    "320_Промышленное предприятие неопределённого типа",
                    "350_Пески"                                        ])

code_320 =([            "321_Порт",
                        "322_Эл. Станция",
                        "323_НПЗ"                                       ])

code_400 =([        "400_Объект отсутствует",
                    "410_Плотина, дамба",
                    "420_Автомобильная дорога",
                    "430_Линия эл. передач",
                    "440_Скалы",
                    "450_Здание неопределенного типа",
                    "460_Аэродром",
                    "490_Особые здания"                                 ])


code_490 =([            "401_Объект неопределенного типа"               ])

code_410 =([            "411_Мост"                                      ])

code_420 =([            "421_Железная дорога"                           ])

code_440 =([            "441_Террикон, отвал, насыпь, курган"           ])

code_450 =([            "451_Жилое строение",
                        "452_Промышленное строение или сооружение",
                        "453_Причал",
                        "454_Культурные и религиозные здания и сооружения",
                        "455_Склад",
                        "456_Склад горючего"                            ])

code_460 =([            "461_Портовые сооружения и краны"               ])
"""
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
    #name = unique id, base, class number, globalcolor id [2-18], text description
    c100 = 0,   0, 100, 2,  "Базовый Вода" #"Объект отсутствует"
    c110 = 1,   0, 110, 3,  "Река, канал"
    c120 = 2,   0, 120, 4,  "Озеро, пруд, водохранилище"
    c130 = 3,   0, 130, 5,  "Болото, рисовое поле"
    c140 = 4,   0, 140, 6,  "Океан, море"  

    c200 = 5,   1, 200, 7,  "Базовый Растительность" #"Объект отсутствует"
    c210 = 6,   1, 210, 8,  "Заросли кустарников и прочей низкой растительности (в т.ч. луга и степи)"
    c220 = 7,   1, 220, 9,  "Редкий лесной массив (редко стоящие деревья)"
    c230 = 8,   1, 230, 10, "Лесной массив (в т. ч. густые массивы)"

    c300 = 9,   2, 300, 11, "Базовый Площадные объекты" #"Объект отсутствует"
    c310 = 10,  2, 310, 12, "Город или другой населенный пункт"
    c320 = 11,  2, 320, 13, "Промышленное предприятие неопределённого типа"
    c321 = 12,  2, 321, 14, "Порт"
    c322 = 13,  2, 322, 15, "Эл. Станция"
    c323 = 14,  2, 323, 16, "НПЗ"
    c350 = 15,  2, 350, 17, "Пески"   

    c400 = 16,  3, 400, 18, "Базовый Объекты и сооружения"#"Объект отсутствует"
    с401 = 17,  3, 401, 2,  "Объект неопределенного типа"
    c410 = 18,  3, 410, 3,  "Плотина, дамба"
    с411 = 19,  3, 411, 4,  "Мост"
    c420 = 20,  3, 420, 5,  "Автомобильная дорога"
    с421 = 21,  3, 421, 6,  "Железная дорога"
    c430 = 22,  3, 430, 7,  "Линия эл. передач"
    c440 = 23,  3, 440, 8,  "Скалы"
    с441 = 24,  3, 441, 9,  "Террикон, отвал, насыпь, курган"
    c450 = 25,  3, 450, 10, "Здание неопределенного типа"
    с451 = 26,  3, 451, 11, "Жилое строение"
    с452 = 27,  3, 452, 12, "Промышленное строение или сооружение"
    с453 = 28,  3, 453, 13, "Причал"
    с454 = 29,  3, 454, 14, "Культурные и религиозные здания и сооружения"
    с455 = 30,  3, 455, 15, "Склад"
    с456 = 31,  3, 456, 16, "Склад горючего"
    с460 = 32,  3, 460, 17, "Аэродром"
    с461 = 33,  3, 461, 18, "Портовые сооружения и краны"
    с490 = 34,  3, 490, 2,  "Особые здания"

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
    TO_DO       = '__0__' #при создании файла проекта, при добавлении задачи
    IN_PROGRESS = '__1__' #у задачи есть хотя бы один атрибут маски
    REVIEW      = '__2__' #нажата кнопка отправить на проверку
    DONE        = '__3__' #модератор нажал кнопку 

class items(Enum):
    path        = os.getcwd()

    PROJECTS    = path + '/' + '__projects__'   + '/'
    IMAGES      = path + '/' + '__images__'     + '/'

    previous    = IMAGES + '/' + 'previous_tbtn.png'

class shapes(Enum):
    NONE        = 0
    POLYGON     = 1
    RECTANGLE   = 2
    ELLIPSE     = 3


project_classes = []

HDF_GROUP_SRCS_NAME = '__srcs_images'
HDF_GROUP_FEATURES_NAME = '__features'
HDF_GROUP_OBJECT_LAYERS_NAME = '__object_layers'
HDF_POSTFIX = '.hdf5'

HDF_FILE_NAME = 'name'
HDF_FILE_CLASSES = 'classes'
HDF_FILE_TIME_C = 'time_created'
HDF_FILE_TIME_U = 'time_updated'
HDF_FILE_DESCRIPTION = 'description'
HDF_FILE_TASK_COUNT = 'task_count'

HDF_TASK_POLYGON_COUNT = '__polygon_count'
HDF_TASK_STATUS = '__task_status'
HDF_TASK_STATUS_0 = 'to do' #при создании файла проекта, при добавлении задачи
HDF_TASK_STATUS_1 = 'in progress' #у задачи есть хотя бы один атрибут маски
HDF_TASK_STATUS_2 = 'review' #нажата кнопка отправить на проверку
HDF_TASK_STATUS_3 = 'done' #модератор нажал кнопку 


TASK_WIDGET_MODE_0 = 'to do'
TASK_WIDGET_MODE_1 = 'to check'



ICON_FOLDER_NAME = '__icons'
ICON_FOLDER_NAME_FULL = os.getcwd() + '/' + ICON_FOLDER_NAME

IMAGES_FOLDER_NAME = '__images'
IMAGES_FOLDER_NAME_FULL = os.getcwd() + '/' + IMAGES_FOLDER_NAME

ICON_SEG_TBTN_PREVIOUS = 'previous_tbtn.png'
ICON_SEG_TBTN_PREVIOUS_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_PREVIOUS

ICON_SEG_TBTN_NEXT = 'next_tbtn.png'
ICON_SEG_TBTN_NEXT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_NEXT

ICON_SEG_TBTN_TOFIRST = 'tofirst_tbtn.png'
ICON_SEG_TBTN_TOFIRST_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_TOFIRST

ICON_SEG_TBTN_TOLAST = 'tolast_tbtn.png'
ICON_SEG_TBTN_TOLAST_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_TOLAST

ICON_SEG_TBTN_DOTS_INSTRUMENT = 'dots_instrument_tbtn.png'
ICON_SEG_TBTN_DOTS_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SEG_TBTN_DOTS_INSTRUMENT

ICON_PENCIL_TBTN_DRAW_INSTRUMENT = 'pencil_tbtn.png'
ICON_PENCIL_TBTN_DRAW_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_PENCIL_TBTN_DRAW_INSTRUMENT

ICON_POLYGON_TBTN_DRAW_INSTRUMENT = 'polygon_tbtn'
ICON_POLYGON_TBTN_DRAW_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_POLYGON_TBTN_DRAW_INSTRUMENT

ICON_CANCEL_TBTN_DRAW_INSTRUMENT = 'cancel_tbtn.png'
ICON_CANCEL_TBTN_DRAW_INSTRUMENT_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_CANCEL_TBTN_DRAW_INSTRUMENT

ICON_SAVE_TO_ATTRS_TBTN = 'save_to_attrs_tbtn.png'
ICON_SAVE_TO_ATTRS_TBTN_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_SAVE_TO_ATTRS_TBTN

ICON_DELETE_TASK = 'delete_tbtn.png'
ICON_DELETE_TASK_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_DELETE_TASK

ICON_FORWARD_PASS_TASK = 'forward_pass_tbtn.png'
ICON_FORWARD_PASS_TASK_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_FORWARD_PASS_TASK

ICON_FORWARD_CHECK_TASK = 'forward_check_tbtn.png'
ICON_FORWARD_CHECK_TASK_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_FORWARD_CHECK_TASK

ICON_BACKWARD_DELETE_TASK = 'backward_delete_tbtn.png'
ICON_BACKWARD_DELETE_TASK_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_BACKWARD_DELETE_TASK

ICON_BACKWARD_PASS_TASK = 'backward_pass_tbtn.png'
ICON_BACKWARD_PASS_TASK_FULL = ICON_FOLDER_NAME_FULL + '/' + ICON_BACKWARD_PASS_TASK


PROJECTS_FOLDER_NAME = '__projects'
PROJECTS_FOLDER_FULL_NAME = os.getcwd() + '/' + PROJECTS_FOLDER_NAME
#PROJECTS_LIST = os.listdir(PROJECTS_FOLDER_FULL_NAME)




import time

class project_ini():
    name = ""
    id = 0
    author = ""
    time_start = time.localtime()
    time_last_change = time.localtime()
    classes = []
    description = ""
    base_project = None
    selected_files = []

current_project = project_ini()