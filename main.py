# == Задание 1.
#
# Дана строка string и шаблон pattern (также строка). Необходимо реализовать функцию match, которая
# проверяет string на совпадение с pattern, то есть возвращает true, если string соответствует pattern,
# и false в противном случае.
#
# Соответствие с шаблоном проверяется следующим образом. Во-первых, количество символов шаблона должно
# совпадать с количеством символов строки. Далее, если в шаблоне на i-ой позиции находится символ 'd',
# то в строке на той же позиции должна находиться цифра 0 - 9. Аналогично, символ 'a' в шаблоне
# обозначает строчную латинскую букву (т.е. a - z), символ '*' - цифру или латинскую строчную букву,
# пробел ' ' обозначает сам себя. Другие символы в шаблоне запрещены, при их обнаружении функция должна
# генерировать исключение.
#
# Примеры:
#
# - строка 'xyz 123' соответствует шаблону 'aa* dd*'
# - строка '1xy' не соответствует шаблону 'aaa' (не сопадает по первому символу)

import traceback


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def match(string, pattern):
    if len(string) != len(pattern):
        return False
    for ind, pattern_char in enumerate(pattern):
        if pattern_char not in ('*', 'd', 'a', ' '):
            raise ValueError('Incorrect pattern.')
        char = string[ind]
        is_digit = char.isdigit()
        is_alpha = char.islower() and char.isalpha()
        if pattern_char == '*' and not (is_digit or is_alpha):
            return False
        elif pattern_char == 'd' and not is_digit:
            return False
        elif pattern_char == 'a' and not is_alpha:
            return False
        elif pattern_char == ' ' and char != ' ':
            return False
    return True


# ------------------------------------------------------------------------------------------------
# Решение задачи 1
# ------------------------------------------------------------------------------------------------

def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ', 'a'))

    runner.expectTrue(lambda: match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda: match('x', 'w'))


# == Задание 2.
#
# Дано дерево задач с одним корнем. Узлами дерева являются группы задач, листьми - сами задачи. Внутри
# группы могут содержаться либо другие группы, либо задачи, но не то и другое одновременно. Каждый элемент
# дерева имеет уникальный идентификатор id (неотрицательное целое число) и название name (строка).
# Дополнительно задачи имеют приоритет priority (неотрицательное целое число), а группы задач приоритета
# не имеют. Необходимо реализовать функцию findTaskHavingMaxPriorityInGroup, в которую передается дерево
# задач и идентификатор группы. Она должна найти задачу с наибольшим приоритетом среди всех из этой
# группы (включая те из них, которые находятся во вложенных группах). Если не удалось найти группу с
# указанным идентификатором, функция должна генерировать исключение. Если в группе нет ни одной задачи,
# должно возвращаться неопределенное значение (undefined в JavaScript, None в Python, nullptr в C++ и null в
# Kotlin).
#
# Пример:
#
# Допустим, имеется дерево задач
#
# * id = 0, name = "Все задачи"
#    * id = 1, name = "Разработка"
#       * id = 2, name = "Планирование разработок", priority = 1
#       * id = 3, name = "Подготовка релиза", priority = 4
#    * id = 4, name = "Аналитика"
#
# Отступами обозначается вложенность групп задач. Это дерево содержит три группы ("Все задачи", "Разработка"
# и "Аналитика"), а также две задачи ("Планирование разработок" и "Подготовка релиза"). Для этого дерева
# вызов функции findTaskHavingMaxPriorityInGroup c номером группы
#
# * 0 - должен вернуть задачу "Подготовка релиза" (имеет максимальный приоритет 4)
# * 3 - сгенерировать исключение (не является группой)
# * 5 - сгенерировать исключение (группа не существует)
# - 4 - вернуть неопределенное значение (в группе нет ни одной задачи)

tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
    tasks_queue = [tasks]
    group = None
    while tasks_queue:
        t = tasks_queue.pop()
        if t['id'] == groupId:
            group = t
            break
        tasks_queue = tasks_queue + t.get('children', [])
    if group.get('priority', None):
        raise ValueError('Not a group.')
    if group:
        tasks_queue = [group]
        max_priority = -1
        elem = None
        while tasks_queue:
            t = tasks_queue.pop()
            priority = t.get('priority', -1)
            if priority > max_priority:
                max_priority = priority
                elem = t
            tasks_queue = tasks_queue + t.get('children', [])
        if elem:
            return elem
        else:
            return None
    else:
        raise ValueError('Group not found.')


# ------------------------------------------------------------------------------------------------
# Решение задачи 2
# ------------------------------------------------------------------------------------------------


def taskEquals(a, b):
    return (
            not 'children' in a and
            not 'children' in b and
            a['id'] == b['id'] and
            a['name'] == b['name'] and
            a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)


testMatch()
testFindTaskHavingMaxPriorityInGroup()