# Full Command List: phrase -> behavior

Source: jarvis_commands.json + system slash commands from main.py

## 1) Voice command map (all phrases)

### Folder: Jarvis

1. `давай` -> launch_openfile(value="C:\Users\PC\OneDrive\Desktop\Наброски")
   cmd_name="давай", confirm=true

2. `печать` -> keyboard_text(value=Всем хааааааааааай, все работает)
   cmd_name="печать", confirm=false
   optional_phrase: ну ка, давай, а ну

### Folder: Jarvis/PowerPoint

3. `новый проект | новую презентацию` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Вы создали новый элемент.wav); keyboard_hotkey(value={CONTROL}({N}))
   cmd_name="Презентация в новом окне", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить, мне нужен, мне нужна

4. `слайд | новый слайд | еще один слайд` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LCONTROL}({M}))
   cmd_name="Новый слайд", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить, мне нужен, мне нужна

5. `удали слайд | удали лист | удалить слайд | удалить лист` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={LALT}({Z})); vc_pause(value=1000); keyboard_hotkey(value={LSHIFT}({E}))
   cmd_name="Удалить слайд", confirm=false

6. `продублируй объект | повтори объект | продублируй` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({D}))
   cmd_name="Дублировать объект", confirm=false

7. `группировать | сгруппируй объекты | соедини` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LCONTROL}({G}))
   cmd_name="Группировать выделенные объекты", confirm=false

8. `Разгруппируй | разгруппировать | раздели` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav); keyboard_hotkey(value={LSHIFT+LCONTROL}({G}))
   cmd_name="Разгрупировать выделенные объекты", confirm=false

9. `копируй формат | скопируй формат` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LCONTROL+LSHIFT}({C}))
   cmd_name="Копировать форматирование", confirm=false

10. `примени формат | вставь формат` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={LCONTROL+LSHIFT}({V}))
   cmd_name="Применить форматирование", confirm=false

11. `ссылка | ссылку` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LCONTROL}({K}))
   cmd_name="Гиперссылка", confirm=false
   optional_phrase: нужна, мне нужна, выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить

12. `повтори действие | повтори последнее действие` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LCONTROL}({Y}))
   cmd_name="Повтор последнего действия", confirm=false

13. `презентацию | проект | слайдов` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LALT}({P})); vc_pause(value=1000); keyboard_hotkey(value={LSHIFT}({X}))
   cmd_name="Слайд шоу", confirm=false
   optional_phrase: запусти, покажи, выведи на экран, воспроизведи

14. `настройки слайд шоу | настройки показа слайдов | настройки презентации` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LALT}({P})); vc_pause(value=300); keyboard_hotkey(value={F})
   cmd_name="Настройка слайд шоу", confirm=false

15. `смени слайд | смени лист | смени страница | смени страницу | дальше | далее | вперёд | сменить слайд | сменить лист | сменить страницу` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LSHIFT}({N}))
   cmd_name="Следующий слайд(в режиме слайд шоу)", confirm=false

16. `верни слайд | вернись обратно | назад | обратно | верни назад | вернись назад | отмотай назад` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LSHIFT}({P}))
   cmd_name="Предыдущий слайд(в режиме слайд шоу)", confirm=false

17. `черный экран | черная заставка | черная пауза` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav); keyboard_hotkey(value={LSHIFT}({B}))
   cmd_name="Черный экран(скрыть на время) (в режиме слайд шоу)", confirm=false

18. `белый экран | белая заставка | белая пауза` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={LSHIFT}({W}))
   cmd_name="Белый экран(скрыть на время) (в режиме слайд шоу)", confirm=false

19. `карандаш` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav); keyboard_hotkey(value={LCONTROL}({P}))
   cmd_name="Карандаш(в режиме слайд шоу)", confirm=false
   optional_phrase: активируй, включи, дай мне, мне нужен, активировать, включить, отключить, выключи, отключи, выключить, убрать, убери

20. `ластик` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({E}))
   cmd_name="Ластик(в режиме слайд шоу)", confirm=false
   optional_phrase: активируй, включи, дай мне, мне нужен, активировать, включить, отключить, выключи, отключи, выключить, убрать, убери

21. `Сохрани презентацию как` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LALT}({A})); vc_pause(value=1000); keyboard_hotkey(value={LSHIFT}({R}))
   cmd_name="Сохранить презентацию как", confirm=false

22. `жирным | жирный | на жирный` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Как пожелаете.wav); keyboard_hotkey(value={LCONTROL}({B}))
   cmd_name="Полужирный", confirm=false
   optional_phrase: выбери, сделай, выбрать, поставить, измени, изменить, сделать

23. `курсив | курсивом | на курсив` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({I}))
   cmd_name="Курсив", confirm=false
   optional_phrase: выбери, сделай, выбрать, поставить, измени, изменить, сделать

24. `подчеркнутый | подчеркнутым | зачеркни` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LCONTROL}({U}))
   cmd_name="Подчеркнутый", confirm=false
   optional_phrase: выбери, сделай, выбрать, поставить, измени, изменить, сделать

25. `зачеркнутый | зачеркни | на зачеркнутый | зачеркнутым | стандартный | обычный` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LALT}({Z})); vc_pause(value=1000); keyboard_hotkey(value={LALT}({4}))
   cmd_name="Зачеркнутый", confirm=false
   optional_phrase: выбери, сделай, выбрать, поставить, измени, изменить, сделать, верни, верни на

26. `по центру | на центр | на центре` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({E}))
   cmd_name="Разместить параграф по центру", confirm=false
   optional_phrase: выровняй, размести, сделай, выровнять, разместить, сделать

27. `произвольно | сплошным | по ширине` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({J}))
   cmd_name="Разместить параграф произвольно", confirm=false
   optional_phrase: выровняй, размести, сделай, выровнять, разместить, сделать

28. `по правому краю | по правому | направао | справа` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({R}))
   cmd_name="Разместить параграф по правому краю", confirm=false
   optional_phrase: выровняй, размести, сделай, выровнять, разместить, сделать

29. `по левому краю | по левому | налево | слева` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({L}))
   cmd_name="Разместить параграф по левому краю", confirm=false
   optional_phrase: выровняй, размести, сделай, выровнять, разместить, сделать

30. `Таблица шрифта | таблица шрифтов | таблицу шрифтов` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={LALT}({Z})); vc_pause(value=500); keyboard_hotkey(value={A}); vc_pause(value=500); keyboard_hotkey(value={N})
   cmd_name="Настройки шрифта", confirm=false
   optional_phrase: выровняй, размести, сделай, выровнять, разместить, сделать

31. `Настройки абзаца | настрой абзац | параметры абзаца` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LSHIFT}({Z})); vc_pause(value=500); keyboard_hotkey(value={LSHIFT}({P})); vc_pause(value=500); keyboard_hotkey(value={LSHIFT}({G}))
   cmd_name="Настройки абзаца", confirm=false

32. `таблицу | таблица` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LALT}({C})); vc_pause(value=300); keyboard_hotkey(value={W}); vc_pause(value=300); keyboard_hotkey(value={M}); vc_pause(value=300)
   cmd_name="Добавить таблицу", confirm=false
   optional_phrase: создай, открой, сделай, добавь, внеси, внести, добавить

33. `изображение | фото | картинку | фотографию | пикчу` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LALT}({C})); vc_pause(value=500); keyboard_hotkey(value={E})
   cmd_name="Добавить изображение", confirm=false
   optional_phrase: Добавить, внести, добавь, внеси, открой, открыть

34. `Фотоальбом` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LALT}({C})); vc_pause(value=300); keyboard_hotkey(value={F}); vc_pause(value=300); keyboard_hotkey(value={A})
   cmd_name="Фотоальбом", confirm=false
   optional_phrase: создай, создать, открой, открыть, добавь, добавить

35. `надпись | напиши отдельно | добавь надпись | добавить надпись` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LALT}({C})); vc_pause(value=300); keyboard_hotkey(value={B})
   cmd_name="Надпись ( в отдельном объекте)", confirm=false

36. `красивую надпись | декорированную надпись | красивая надпись` -> sound_play_wav(value=C:\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LALT}({C})); vc_pause(value=300); keyboard_hotkey(value={J})
   cmd_name="Декорированная надпись", confirm=false
   optional_phrase: сделай, сделать, добавь, добавить

37. `дату | время | дату и время | событие датой | событие временем` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LALT}({C})); vc_pause(value=300); keyboard_hotkey(value={D})
   cmd_name="Дата и время", confirm=false
   optional_phrase: добавь, внеси, отметь, сделай, сделать, добавить, внести

38. `параметры страницы | параметры страниц` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={S})
   cmd_name="Параметры страниц", confirm=false
   optional_phrase: открой, включи, выведи, измени, добавь, сделай, открыть, включить, вывести, изменить, добавить, сделать

39. `Ориентацию слайдов | ориентацию слайда | ориентация слайдов` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={Z})
   cmd_name="Ориентация слайда", confirm=false
   optional_phrase: открой, включи, выведи, измени, добавь, сделай, открыть, включить, вывести, изменить, добавить, сделать

40. `тему | темы | список тем` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={H})
   cmd_name="Темы", confirm=false
   optional_phrase: смени, открой, добавь, измени, сделай, вынеси, сменить, открыть, добавить, изменить, сделать, вынести

41. `тему с пэка | тему с диска | темы с пэка | темы с диска` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={H}); vc_pause(value=300); keyboard_hotkey(value={G})
   cmd_name="Темы (загрузить с пк)", confirm=false
   optional_phrase: загрузи, загрузить

42. `тему | текущую тему` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Вы создали новый элемент.wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={H}); vc_pause(value=300); keyboard_hotkey(value={C})
   cmd_name="Сохрвнить текущую тему", confirm=false
   optional_phrase: сохрани, сохранить

43. `цвет темы | цвета темы` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={T}); vc_pause(value=300); keyboard_hotkey(value={F})
   cmd_name="(отдельно) Цвет темы", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить

44. `шрифт темы | шрифты темы` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={T}); vc_pause(value=300); keyboard_hotkey(value={A})
   cmd_name="(отдельно) Шрифт темы", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить

45. `стиль фона | фон | стили фона | стили фонов | стиль для фона | стили для фонов` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LALT}({Q})); vc_pause(value=300); keyboard_hotkey(value={F})
   cmd_name="(отдельно) Стиль фона", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить

46. `переход слайдов | переход слайда | схема перехода | схема перехода слайдов` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LALT}({B})); vc_pause(value=300); keyboard_hotkey(value={T})
   cmd_name="Схема перехода слайда", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить

47. `звук слайдов | звук слайда | звук перехода | звук перехода слайда` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LALT}({B})); vc_pause(value=300); keyboard_hotkey(value={D})
   cmd_name="Звук перехода слайда", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить

48. `скорость перехода | скорость перехода слайда` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LALT}({B})); vc_pause(value=300); keyboard_hotkey(value={G})
   cmd_name="Скорость перехода слайда", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить

49. `просмотр | анимацию | анимаций` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LALT}({B})); vc_pause(value=300); keyboard_hotkey(value={H})
   cmd_name="Просмотреть анимацию слайдов", confirm=false
   optional_phrase: покажи, просмотр

50. `параметры переходов ко всем слайдам | параметры переходов на все слайды | ко всем слайдам | на все слайды` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={LALT}({B})); vc_pause(value=300); keyboard_hotkey(value={N})
   cmd_name="Применить параметры переходов ко всем слайдам", confirm=false
   optional_phrase: применить, перенести, сохранить

51. `линейку | линейка` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={LALT}({J})); vc_pause(value=300); keyboard_hotkey(value={>}({2})); vc_pause(value=300); keyboard_hotkey(value={R})
   cmd_name="убрать\скрыть линейку", confirm=false
   optional_phrase: сделай, сделать, добавь, добавить, скрыть, убрать, убери, скрой

### Folder: Jarvis/Общение

52. `джарвис | бот | сын | компьютер | брат` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav)
   cmd_name="вызов", confirm=false

53. `ты тут | на месте | джарвис не спишь | нужна помощь | поможешь` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav)
   cmd_name="вызов2", confirm=false

54. `что делаешь | чем занимаешься | докладывай` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Импортирую установки, начинаю калибровку виртуальной среды.wav)
   cmd_name="что делаешь", confirm=false

55. `доброе утро | я проснулся` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Доброе утро.wav)
   cmd_name="доброе утро", confirm=false

### Folder: Jarvis/Открытие сайтов

56. `яндекс | браузер | дзен` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvisJarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); launch_openurl(value=https://dzen.ru/)
   cmd_name="Яндекс", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

57. `ютуб | ютубчик | ютюб` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); launch_openurl(value=https://www.youtube.com/)
   cmd_name="Ютуб", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

58. `вэка | вконтакте` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); launch_openurl(value=https://vk.com/feed)
   cmd_name="Вк", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

59. `переводчик | переведи | мне нужен перевод | английский` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); launch_openurl(value=https://translate.yandex.ru/?from=tableau_yabro)
   cmd_name="Переводчик", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

60. `гугл | хром | гугл хром` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); launch_openurl(value=https://www.google.com/?hl=ru)
   cmd_name="Гугл", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

### Folder: Jarvis/Открытие сайтов (копия)

61. `яндекс | браузер | дзен` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvisJarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); launch_openurl(value=https://dzen.ru/)
   cmd_name="Яндекс", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

62. `ютуб | ютубчик | ютюб` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); launch_openurl(value=https://www.youtube.com/)
   cmd_name="Ютуб", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

63. `вэка | вконтакте` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); launch_openurl(value=https://vk.com/feed)
   cmd_name="Вк", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

64. `переводчик | переведи | мне нужен перевод | английский` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); launch_openurl(value=https://translate.yandex.ru/?from=tableau_yabro)
   cmd_name="Переводчик", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

65. `гугл | хром | гугл хром` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); launch_openurl(value=https://www.google.com/?hl=ru)
   cmd_name="Гугл", confirm=false
   optional_phrase: открой, запусти, зайди в, открыть, запустить, зайти в, вруби, врубить, мне нужен, будь добр открой, выведи

### Folder: Jarvis/Протокололы

66. `пэка контроль | пэка контрол | один` -> launch_openfile(value=сюда пишите путь к файлу); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Импортирую установки, начинаю калибровку виртуальной среды.wav)
   cmd_name="Пк контроль (Если куплен)", confirm=true
   optional_phrase: активировать, запусти, открой, активируй, протокол

67. `уютный вечер | два | что-то для отдыха` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); vc_pause(value=2000); launch_openurl(value=https://www.youtube.com/watch?v=vV5q0gYlS0o); vc_pause(value=1500); launch_openurl(value=https://www.youtube.com/watch?v=x7SQaDTSrVg); vc_pause(value=3000); keyboard_hotkey(value={F})
   cmd_name="протокол я дома", confirm=false
   optional_phrase: протокол, запусти, открой, активаруй, включи

68. `я один дома | пора бы отдохнуть | протокол три` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Джарвис - приветствие.wav); vc_pause(value=7500); launch_openurl(value=https://www.youtube.com/watch?v=jYmeyW7oS1M); vc_pause(value=3000); keyboard_hotkey(value={F})
   cmd_name="Я один дома", confirm=false

### Folder: Jarvis/Управление Microsoft Word

69. `настройку шрифта` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LCONTROL+LSHIFT}({F}))
   cmd_name="Настройка шрифта", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить, мне нужен, мне нужна

70. `окно печати` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={LCONTROL}({P}))
   cmd_name="Окно печати", confirm=false
   optional_phrase: выбери, найди, поставь, открой, сделай, выбрать, поставить, открыть, создай, создать, измени, изменить, мне нужен, мне нужна

71. `найди и замени | найди и замени текст` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LCONTROL}({H}))
   cmd_name="Найди и замени", confirm=false

72. `во вкладку вставка | вкладку вставка | в вставку` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LALT}({C}))
   cmd_name="Вкладка вставка", confirm=false
   optional_phrase: перейди, открой, открыть, зайди, зайти, перейти

73. `во вкладку дизайн | вкладку дизайн | в дизайн` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LALT}({L}))
   cmd_name="Вкладка дизайн", confirm=false
   optional_phrase: перейди, открой, открыть, зайди, зайти, перейти

74. `во вкладку разметка страницы | вкладку разметка страницы | в разметку страницы` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={LALT}({P}))
   cmd_name="Вкладка разметка страницы", confirm=false
   optional_phrase: перейди, открой, открыть, зайди, зайти, перейти

75. `поля` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LALT}({K}))
   cmd_name="Поля", confirm=false
   optional_phrase: нажми на, выбери, выбрать, нажать на

76. `Открой поиск в документе` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={LCONTROL}({F}))
   cmd_name="Открой поиск в документе", confirm=false

77. `перемести влево | переместить влево | переведи влево` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={LEFT})
   cmd_name="Перемещение курсора влево", confirm=false

78. `перемести вправо | переместить вправо | переведи вправо` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={RIGHT})
   cmd_name="Перемещение курсора вправо", confirm=false

79. `перемести вниз | переместить | вереведи вниз` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={DOWN})
   cmd_name="Перемещение курсора вниз", confirm=false

80. `перемести вверх | преместить вверх | перейди вверх` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={UP})
   cmd_name="Перемещение курсора вверх", confirm=false

81. `перемести в начало строки | переместить в начало строки | перейди в начало строки | вернись в начало строки | открой начало строки | в начало строки` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={HOME})
   cmd_name="В начало строки", confirm=false

82. `перемести в конец строки | переместить в конец строки | перейди в конец строки | в конец строки` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={END})
   cmd_name="В конец строки", confirm=false

83. `в начало документа | в начале документа` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={LCONTROL}({HOME}))
   cmd_name="В начало документа", confirm=false
   optional_phrase: переместить, перейди, перейти, вернись, вернуть, открыть, открой

84. `в конец документа | в конце документа` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={LCONTROL}({END}))
   cmd_name="В конец документа", confirm=false
   optional_phrase: переместить, перейди, перейти, вернись, вернуть, открыть, открой

85. `сохрани документ как` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Сохранить его в центральной базе данных Stark Industries.wav); keyboard_hotkey(value={F12})
   cmd_name="Сохранить как", confirm=false

### Folder: Jarvis/Управление системой

86. `закрой окно | закрой программу` -> window_close(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Как пожелаете .wav)
   cmd_name="Закрыть окно", confirm=false

87. `на весь экран | разверни на максимум` -> window_maximize()
   cmd_name="На весь экран", confirm=false

88. `нормализуй окно` -> window_normalize()
   cmd_name="Норм окно", confirm=false

89. `окно | окна` -> window_minimize(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav)
   cmd_name="Сверни окно", confirm=false
   optional_phrase: сверни, разверни, убери, убрать, вруби, врубить, вынеси, выведи, свернуть, развернуть

90. `вставить | вставь` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={CONTROL}({V}))
   cmd_name="Вставить", confirm=false

91. `скопировать | скопируй | скопируй текст` -> keyboard_hotkey(value={LCONTROL}({C})); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav)
   cmd_name="Скопировать", confirm=false

92. `отмена действия | отмени действия | отмени` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={CONTROL}({Z}))
   cmd_name="Отмена действия", confirm=false

93. `другое окно | смени окно | смена окна | сменить окно` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={ALT}({TAB}))
   cmd_name="Другое окно", confirm=false

94. `смени имя выбранного элемента` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={F2})
   cmd_name="Смена имени", confirm=false

95. `найди элемент` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={F3})
   cmd_name="Найди элемент", confirm=false

96. `обнови страницу | обновить` -> keyboard_hotkey(value={F5})
   cmd_name="Обнови страницу", confirm=false

97. `назад | вернись назад` -> keyboard_hotkey(value={ALT}({LEFT}))
   cmd_name="Назад", confirm=false

98. `вперёд | вернись вперёд` -> keyboard_hotkey(value={ALT}({RIGHT}))
   cmd_name="Вперёд", confirm=false

99. `открой адрес страницы | удали переписку | удали чат` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={ALT}({D}))
   cmd_name="Арес страницы", confirm=false

100. `повтори окно | дублируй окно | повторить окно | дублировать окно` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={CONTROL}({N}))
   cmd_name="Повтори окно", confirm=false

101. `поиск в системе` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={LWIN}({S}))
   cmd_name="Поиск по системе", confirm=false

102. `открой параметры | открыть параметры` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Как пожелаете .wav); keyboard_hotkey(value={LWIN}({I}))
   cmd_name="Открой параметры", confirm=false

103. `удали | удали текст | сотри` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={DELETE})
   cmd_name="Удали", confirm=false

104. `энтэр | отправить | поиск | отправь | найди` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={ENTER})
   cmd_name="Энтэр", confirm=false

105. `смени язык | смени раскладку | английский | русский | смена языка | сменить язык | сменить раскладку` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={SHIFT}({ALT}))
   cmd_name="Смени язык", confirm=false

106. `кликни | нажми | кликнуть | нажать` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); mouse_leftclick()
   cmd_name="Клик", confirm=false

107. `громкость на | звук на | прикрути на | убавь на | добавь на | прикрутить на | убавить на | добавить на` -> sound_setvol(value={1}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav)
   cmd_name="Управление звуком", confirm=false

108. `заблокируй монитор | блокировка монитора | заблокировать монитор` -> system_monitor_off(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav)
   cmd_name="Выключи монитор", confirm=true

109. `спящий режим | режим сна` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Отключаю питание, начинаю диагностику системы.wav); vc_pause(value=3000); system_sleep()
   cmd_name="Спящий режим", confirm=false
   optional_phrase: поставь в, перейди в

### Folder: Jarvis/Управление системой (копия)

110. `закрой окно | закрой программу` -> window_close(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Как пожелаете .wav)
   cmd_name="Закрыть окно", confirm=false

111. `на весь экран | разверни на максимум` -> window_maximize()
   cmd_name="На весь экран", confirm=false

112. `нормализуй окно` -> window_normalize()
   cmd_name="Норм окно", confirm=false

113. `окно | окна` -> window_minimize(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav)
   cmd_name="Сверни окно", confirm=false
   optional_phrase: сверни, разверни, убери, убрать, вруби, врубить, вынеси, выведи, свернуть, развернуть

114. `вставить | вставь` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={CONTROL}({V}))
   cmd_name="Вставить", confirm=false

115. `скопировать | скопируй | скопируй текст` -> keyboard_hotkey(value={LCONTROL}({C})); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav)
   cmd_name="Скопировать", confirm=false

116. `отмена действия | отмени действия | отмени` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={CONTROL}({Z}))
   cmd_name="Отмена действия", confirm=false

117. `другое окно | смени окно | смена окна | сменить окно` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={ALT}({TAB}))
   cmd_name="Другое окно", confirm=false

118. `смени имя выбранного элемента` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={F2})
   cmd_name="Смена имени", confirm=false

119. `найди элемент` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={F3})
   cmd_name="Найди элемент", confirm=false

120. `обнови страницу | обновить` -> keyboard_hotkey(value={F5})
   cmd_name="Обнови страницу", confirm=false

121. `назад | вернись назад` -> keyboard_hotkey(value={ALT}({LEFT}))
   cmd_name="Назад", confirm=false

122. `вперёд | вернись вперёд` -> keyboard_hotkey(value={ALT}({RIGHT}))
   cmd_name="Вперёд", confirm=false

123. `открой адрес страницы | удали переписку | удали чат` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={ALT}({D}))
   cmd_name="Адрес страницы", confirm=false

124. `повтори окно | дублируй окно | повторить окно | дублировать окно` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={CONTROL}({N}))
   cmd_name="Повтори окно", confirm=false

125. `поиск в системе` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={LWIN}({S}))
   cmd_name="Поиск по системе", confirm=false

126. `открой параметры | открыть параметры` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Как пожелаете .wav); keyboard_hotkey(value={LWIN}({I}))
   cmd_name="Открой параметры", confirm=false

127. `удали | удали текст | сотри` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={DELETE})
   cmd_name="Удали", confirm=false

128. `энтэр | отправить | поиск | отправь | найди` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={ENTER})
   cmd_name="Энтэр", confirm=false

129. `смени язык | смени раскладку | английский | русский | смена языка | сменить язык | сменить раскладку` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={SHIFT}({ALT}))
   cmd_name="Смени язык", confirm=false

130. `кликни | нажми | кликнуть | нажать` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); mouse_leftclick()
   cmd_name="Клик", confirm=false

131. `громкость на | звук на | прикрути на | убавь на | добавь на | прикрутить на | убавить на | добавить на` -> sound_setvol(value={1}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav)
   cmd_name="Управление звуком", confirm=false

132. `заблокируй монитор | блокировка монитора | заблокировать монитор` -> system_monitor_off(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav)
   cmd_name="Выключи монитор", confirm=true

133. `спящий режим | режим сна` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Отключаю питание, начинаю диагностику системы.wav); vc_pause(value=3000); system_sleep()
   cmd_name="Спящий режим", confirm=false
   optional_phrase: поставь в, перейди в

### Folder: Jarvis/Управление системой (копия) 2

134. `закрой окно | закрой программу` -> window_close(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Как пожелаете .wav)
   cmd_name="Закрыть окно", confirm=false

135. `на весь экран | разверни на максимум` -> window_maximize()
   cmd_name="На весь экран", confirm=false

136. `нормализуй окно` -> window_normalize()
   cmd_name="Норм окно", confirm=false

137. `окно | окна` -> window_minimize(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav)
   cmd_name="Сверни окно", confirm=false
   optional_phrase: сверни, разверни, убери, убрать, вруби, врубить, вынеси, выведи, свернуть, развернуть

138. `вставить | вставь` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={CONTROL}({V}))
   cmd_name="Вставить", confirm=false

139. `скопировать | скопируй | скопируй текст` -> keyboard_hotkey(value={LCONTROL}({C})); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav)
   cmd_name="Скопировать", confirm=false

140. `отмена действия | отмени действия | отмени` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={CONTROL}({Z}))
   cmd_name="Отмена действия", confirm=false

141. `другое окно | смени окно | смена окна | сменить окно` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={ALT}({TAB}))
   cmd_name="Другое окно", confirm=false

142. `смени имя выбранного элемента` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={F2})
   cmd_name="Смена имени", confirm=false

143. `найди элемент` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={F3})
   cmd_name="Найди элемент", confirm=false

144. `обнови страницу | обновить` -> keyboard_hotkey(value={F5})
   cmd_name="Обнови страницу", confirm=false

145. `назад | вернись назад` -> keyboard_hotkey(value={ALT}({LEFT}))
   cmd_name="Назад", confirm=false

146. `вперёд | вернись вперёд` -> keyboard_hotkey(value={ALT}({RIGHT}))
   cmd_name="Вперёд", confirm=false

147. `открой адрес страницы | удали переписку | удали чат` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={ALT}({D}))
   cmd_name="Арес страницы", confirm=false

148. `повтори окно | дублируй окно | повторить окно | дублировать окно` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={CONTROL}({N}))
   cmd_name="Повтори окно", confirm=false

149. `поиск в системе` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav); keyboard_hotkey(value={LWIN}({S}))
   cmd_name="Поиск по системе", confirm=false

150. `открой параметры | открыть параметры` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Как пожелаете .wav); keyboard_hotkey(value={LWIN}({I}))
   cmd_name="Открой параметры", confirm=false

151. `удали | удали текст | сотри` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); keyboard_hotkey(value={DELETE})
   cmd_name="Удали", confirm=false

152. `энтэр | отправить | поиск | отправь | найди` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={ENTER})
   cmd_name="Энтэр", confirm=false

153. `смени язык | смени раскладку | английский | русский | смена языка | сменить язык | сменить раскладку` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav); keyboard_hotkey(value={SHIFT}({ALT}))
   cmd_name="Смени язык", confirm=false

154. `кликни | нажми | кликнуть | нажать` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav); mouse_leftclick()
   cmd_name="Клик", confirm=false

155. `громкость на | звук на | прикрути на | убавь на | добавь на | прикрутить на | убавить на | добавить на` -> sound_setvol(value={1}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Есть.wav)
   cmd_name="Управление звуком", confirm=false

156. `заблокируй монитор | блокировка монитора | заблокировать монитор` -> system_monitor_off(); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Всегда к вашим услугам сэр.wav)
   cmd_name="Выключи монитор", confirm=true

157. `спящий режим | режим сна` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Отключаю питание, начинаю диагностику системы.wav); vc_pause(value=3000); system_sleep()
   cmd_name="Спящий режим", confirm=false
   optional_phrase: поставь в, перейди в

### Folder: Jarvis/Управление Ютубом

158. `пауза | стоп | продолжи | плэй | поставь на паузу | продолжить | продолжай | можешь продолжать | я скоро вернусь | я сейчас | подожди секундку` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav); keyboard_hotkey(value={K})
   cmd_name="Остановка/ воспроизведение видео", confirm=false

159. `перемотка | перемотай | перемотать | дальше | вперёд | вправо` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav); keyboard_hotkey(value={L})
   cmd_name="Перемотать вперед ( на 10 сек)", confirm=false

160. `отмотка | отмотай | отмотать | обратно | влево` -> keyboard_hotkey(value={J}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav)
   cmd_name="Перемотать видео (на 10 сек назад)", confirm=false

161. `следующее видео | некст видос | следующий видос | некст видео` -> keyboard_hotkey(value={shift+N}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav)
   cmd_name="Следующее видео", confirm=false
   optional_phrase: включи, включить, перелестни, перелестнуть, перейди на, вруби, активируй, выведи

162. `Предыдущее видео | предыдущий видос` -> keyboard_hotkey(value={shift+P}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav)
   cmd_name="Предыдущее видео", confirm=false
   optional_phrase: включи, включить, перелестни, перелестнуть, перейди на, вруби, активируй, выведи

163. `в начало | начало видео | начало | сначала` -> keyboard_hotkey(value={0}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav)
   cmd_name="Перемотать на начало видео", confirm=false
   optional_phrase: включи, включить, перелестни, перелестнуть, перейди на, вруби, выведи, запусти

164. `десять процентов` -> keyboard_hotkey(value={1}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav)
   cmd_name="Перемотать на 10% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

165. `двадцать процентов` -> keyboard_hotkey(value={2}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav)
   cmd_name="Перемотать на 20% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

166. `тридцать процентов` -> keyboard_hotkey(value={3}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav)
   cmd_name="Перемотать на 30% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

167. `сорок процентов` -> keyboard_hotkey(value={4}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav)
   cmd_name="Перемотать на 40% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

168. `половина | пятьдесят процентов` -> keyboard_hotkey(value={5}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav)
   cmd_name="Перемотать на 50% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

169. `шестьдесят процентов` -> keyboard_hotkey(value={6}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav)
   cmd_name="Перемотать на 60% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

170. `семьдесят процентов` -> keyboard_hotkey(value={7}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav)
   cmd_name="Перемотать на 70% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

171. `восемьдесят процентов` -> keyboard_hotkey(value={8}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\К вашим услугам сэр.wav)
   cmd_name="Перемотать на 80% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

172. `концовка | конец видео | девяносто процентов` -> keyboard_hotkey(value={9}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav)
   cmd_name="Перемотать на 90% видео", confirm=false
   optional_phrase: включи, включить, перелестни на, перелестнуть на, перейти на, перейди на, запусти на, вруби на, врубить на

173. `во весь экран | на весь экран | полный экран | экран | полноэкранный режим | на полный экран | большой режим видео` -> keyboard_hotkey(value={F}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav)
   cmd_name="Полноэкранный режим", confirm=false
   optional_phrase: включи, включить, вывести, выведи, открой, открыть, сделать, сделай, вруби, врубить, выруби, вырубить, выключи, выключить, убрать, убери, отменить, отмени

174. `субтитры` -> keyboard_hotkey(value={C}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Запрос выполнен сэр.wav)
   cmd_name="Субтитры", confirm=false
   optional_phrase: включи, включить, вывести, выведи, открой, открыть, сделать, сделай, вруби, врубить, выруби, вырубить, выключи, выключить, убрать, убери, отменить, отмени

175. `другой режим | другой режим просмотра | режим просмотра | режим видео | другой режим видео | средний режим видео` -> keyboard_hotkey(value={T}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр.wav)
   cmd_name="2 режима просмотра видео", confirm=false
   optional_phrase: включи, включить, вывести, выведи, открой, открыть, сделать, сделай, вруби, врубить, смени, сменить

176. `минипроигрыватель | мини проигрыватель | маленький режим видео` -> keyboard_hotkey(value={I}); sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Да сэр(второй).wav)
   cmd_name="Мини-проигрыватель", confirm=false
   optional_phrase: включи, включить, вывести, выведи, открой, открыть, сделать, сделай, вруби, врубить, выруби, вырубить, выключи, выключить, убрать, убери, отменить, отмени, вернуть, верни

177. `звук` -> sound_play_wav(value=C:\Program Files (x86)\jarvis\Vox jarvis\Jarvis Sound Pack от Jarvis Desktop\Загружаю сэр.wav); keyboard_hotkey(value={M})
   cmd_name="Звук", confirm=false
   optional_phrase: включи, включить, сделать, сделай, вруби, врубить, выруби, вырубить, выключи, выключить, убрать, убери

## 2) Commands with empty phrase

1. cmd_name="успех" (folder=Jarvis) -> voice_say(value=Поздравляю Сэр), confirm=true
2. cmd_name="беда" (folder=Jarvis) -> voice_say(value=Сэр, что будем делать?), confirm=false

## 3) Функции и системные команды (`/`)

1. `/main` -> выход из режима редактирования, возврат в основное окно
2. `/основное` -> русская форма `/main`
3. `/edit` -> включить режим редактирования
4. `/редактировать [section]` -> русская форма `/edit` (можно сразу указать раздел)
5. `/section <home|commands|plugins|settings|profile>` -> переключить раздел редактирования
6. `/секция <...>` -> русская форма `/section`
7. `/window <WxH>` -> изменить размер окна приложения (только в режиме редактирования)
8. `/окно <ШxВ>` -> русская форма `/window`
9. `/rounding <0..64>` -> изменить скругление углов окна
10. `/скругление <0..64>` -> русская форма `/rounding`
11. `/sidebar <left|right>` -> перенести сайдбар влево/вправо
12. `/сайдбар <слева|справа>` -> русская форма `/sidebar`
13. `/texts` -> вывести список текстовых id
14. `/тексты` -> русская форма `/texts`
15. `/text <id> <new text>` -> изменить текст UI-элемента по id
16. `/текст <id> <новый текст>` -> русская форма `/text`
17. `/layout` -> вывести текущие параметры/геометрию
18. `/параметры` -> русская форма `/layout`
19. `/elements` -> вывести список редактируемых элементов
20. `/элементы` -> русская форма `/elements`
21. `/size <history|controls|mic|mode|waves> <WxH>` -> изменить размер элемента
22. `/размер <...> <ШxВ>` -> русская форма `/size`
23. `/position <history|controls|mic|title|mode|waves> <X Y>` -> изменить позицию элемента
24. `/позиция <...> <X Y>` -> русская форма `/position`
25. `/rotate waves <deg>` -> повернуть блок волн на главной
26. `/поворот волны <градусы>` -> русская форма `/rotate waves`
27. `/scale [section] <0.55..1.8>` -> изменить масштаб раздела
28. `/масштаб [раздел] <0.55..1.8>` -> русская форма `/scale`
29. `/param <section> <key> <value>` -> установить конкретный параметр секции
30. `/параметр <раздел> <параметр> <значение>` -> русская форма `/param`
31. `/background <waves1|circles|reactor|gradient|neon|life>` -> сменить фон главной
32. `/фон <волны1|круги|reactor|градиент|неон|life>` -> русская форма `/background`
33. `/mode <base|neuro>` -> сменить режим главной страницы
34. `/режим <база|нейро>` -> русская форма `/mode`
35. `/save` -> сохранить изменения
36. `/сохранить` -> русская форма `/save`
37. `/resetedit` -> сбросить правки текущего раздела
38. `/сброситьредактирование` -> русская форма `/resetedit`

## 4) Встроенные функции без явной пользовательской команды

1. Команды громкости (например: `громкость 40`, `сделай громче`, `mute`) -> меняют/читают системную громкость.
2. Команды яркости (например: `яркость 60`, `сделай ярче`) -> меняют/читают системную яркость.
3. Вопросы вида `кто ...` / `что ...` (`who/what ...`) -> запускают web lookup.
4. `закрой все окна` / `close all windows` -> закрывает все окна через обязательное подтверждение.
5. Загрузка Arduino-режима голосом (если включено `arduino_allow_freeform_voice_upload=true`).

## 5) Обязательное подтверждение для критических системных действий

Даже если у команды выключен тумблер `Подтверждать`, подтверждение будет обязательным для действий:
1. `system_shutdown`
2. `system_restart`
3. `system_sleep`
4. `system_lock_screen`
5. `monitor_off`
6. `monitor_on`
7. `monitor_standby`
8. `system_monitor_off`
9. `system_monitor_on`
10. `system_monitor_standby`

