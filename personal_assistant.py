import json
import csv
from datetime import datetime
import os

NOTES_FILE = 'notes.json'
TASKS_FILE = 'tasks.json'
CONTACTS_FILE = 'contacts.json'
FINANCE_FILE = 'finance.json'


def create_files_if_not_exist():
    files = {
        NOTES_FILE: [],
        TASKS_FILE: [],
        CONTACTS_FILE: [],
        FINANCE_FILE: []
    }

    for file_name, default_content in files.items():
        if not os.path.isfile(file_name):
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(default_content, file, ensure_ascii=False, indent=4)
            print(f"Создан файл: {file_name}")


def get_objects_by_json_file(filename, instance):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            results = json.load(file)
            return [instance(**result) for result in results]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат файла заметок.")
        return []


class Note:
    def __init__(self, id: int, title: str, content: str, timestamp=None):
        self.id = id
        self.title = title
        self.content = content
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }


class NoteManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load_notes(self):
        return get_objects_by_json_file(self.filename, Note)

    def save_notes(self, notes):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([note.to_dict() for note in notes], file, ensure_ascii=False, indent=4)

    def add_note(self, title: str, content: str):
        notes = self.load_notes()
        new_id = max(note.id for note in notes) + 1 if notes else 1
        new_note = Note(new_id, title, content)
        notes.append(new_note)
        self.save_notes(notes)
        print("Заметка успешно добавлена!")

    def view_notes(self):
        notes = self.load_notes()
        if not notes:
            print("Нет доступных заметок.")
            return
        for note in notes:
            print(f"{note.id}: {note.title} (Создано: {note.timestamp})")

    def view_note_details(self, note_id: int):
        notes = self.load_notes()
        note = next((n for n in notes if n.id == note_id), None)
        if note:
            print(f"Заголовок: {note.title}\nСодержимое:\n{note.content}\nДата и время: {note.timestamp}")
        else:
            print("Заметка не найдена.")

    def edit_note(self, note_id: int, title: str, content: str):
        notes = self.load_notes()
        note = next((n for n in notes if n.id == note_id), None)
        if note:
            note.title = title
            note.content = content
            note.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.save_notes(notes)
            print("Заметка успешно отредактирована!")
        else:
            print("Заметка не найдена.")

    def delete_note(self, note_id: int):
        notes = self.load_notes()
        notes = [n for n in notes if n.id != note_id]
        self.save_notes(notes)
        print("Заметка успешно удалена!")

    def export_notes_to_csv(self):
        notes = self.load_notes()
        with open('notes_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'content', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for note in notes:
                writer.writerow(note.to_dict())

        print("Заметки успешно экспортированы в notes_export.csv!")

    def import_notes_from_csv(self):
        with open(input("Введите имя CSV-файла для импорта: "), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            notes = self.load_notes()

            for row in reader:
                new_note = Note(int(row['id']), row['title'], row['content'])
                new_note.timestamp = row['timestamp']
                notes.append(new_note)

            self.save_notes(notes)

        print("Заметки успешно импортированы из CSV-файла.")


class Task:
    def __init__(self, id: int, title: str, description: str, priority: str, due_date: str, done: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.done = done

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }


class TaskManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load_tasks(self):
        return get_objects_by_json_file(self.filename, Task)

    def save_tasks(self, tasks):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title: str, description: str, priority: str, due_date: str):
        tasks = self.load_tasks()
        new_id = max(task.id for task in tasks) + 1 if tasks else 1
        new_task = Task(new_id, title, description, priority, due_date)
        tasks.append(new_task)
        self.save_tasks(tasks)
        print("Задача успешно добавлена!")

    def view_tasks(self):
        tasks = self.load_tasks()
        if not tasks:
            print("Нет доступных задач.")
            return
        for task in tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(f"{task.id}: {task.title} | Статус: {status} | Приоритет: {task.priority} | Срок: {task.due_date}")

    def mark_task_as_done(self, task_id: int):
        tasks = self.load_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        if task:
            task.done = True
            self.save_tasks(tasks)
            print("Задача отмечена как выполненная!")
        else:
            print("Задача не найдена.")

    def edit_task(self, task_id: int, title: str, description: str, priority: str, due_date: str):
        tasks = self.load_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        if task:
            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            self.save_tasks(tasks)
            print("Задача успешно отредактирована!")
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id: int):
        tasks = self.load_tasks()
        tasks = [t for t in tasks if t.id != task_id]
        self.save_tasks(tasks)
        print("Задача успешно удалена!")

    def export_tasks_to_csv(self):
        tasks = self.load_tasks()
        with open('tasks_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'description', 'done', 'priority', 'due_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for task in tasks:
                writer.writerow(task.to_dict())

        print("Задачи успешно экспортированы в tasks_export.csv!")

    def import_tasks_from_csv(self):
        with open(input("Введите имя CSV-файла для импорта: "), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            tasks = self.load_tasks()

            for row in reader:
                new_task = Task(int(row['id']), row['title'], row['description'], row['priority'], row['due_date'])
                new_task.done = row['done'] == 'True'
                tasks.append(new_task)

            self.save_tasks(tasks)

        print("Задачи успешно импортированы из CSV-файла.")


class Contact:
    def __init__(self, id: int, name: str, phone: str, email: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }


class ContactManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load_contacts(self):
        return get_objects_by_json_file(self.filename, Contact)

    def save_contacts(self, contacts):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([contact.to_dict() for contact in contacts], file, ensure_ascii=False, indent=4)

    def add_contact(self, name: str, phone: str, email: str):
        contacts = self.load_contacts()
        new_id = max(contact.id for contact in contacts) + 1 if contacts else 1
        new_contact = Contact(new_id, name, phone, email)
        contacts.append(new_contact)
        self.save_contacts(contacts)
        print("Контакт успешно добавлен!")

    def search_contact(self, query: str):
        contacts = self.load_contacts()
        found_contacts = [c for c in contacts if query.lower() in c.name.lower() or query in c.phone]

        if not found_contacts:
            print("Контакты не найдены.")
            return

        for contact in found_contacts:
            print(f"{contact.id}: {contact.name} | Телефон: {contact.phone} | Email: {contact.email}")

    def edit_contact(self, contact_id: int, name: str, phone: str, email: str):
        contacts = self.load_contacts()
        contact = next((c for c in contacts if c.id == contact_id), None)

        if contact:
            contact.name = name
            contact.phone = phone
            contact.email = email
            self.save_contacts(contacts)
            print("Контакт успешно отредактирован!")
        else:
            print("Контакт не найден.")

    def delete_contact(self, contact_id: int):
        contacts = self.load_contacts()
        contacts = [c for c in contacts if c.id != contact_id]
        self.save_contacts(contacts)
        print("Контакт успешно удалён!")

    def export_contacts_to_csv(self):
        contacts = self.load_contacts()

        with open('contacts_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'phone', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact.to_dict())

        print("Контакты успешно экспортированы в contacts_export.csv!")

    def import_contacts_from_csv(self):
        with open(input("Введите имя CSV-файла для импорта: "), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            contacts = self.load_contacts()

            for row in reader:
                new_contact = Contact(int(row['id']), row['name'], row['phone'], row['email'])
                contacts.append(new_contact)

            self.save_contacts(contacts)

        print("Контакты успешно импортированы из CSV-файла.")


class FinanceRecord:
    def __init__(self, id: int, amount: float, category: str, date: str, description: str):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }


class FinanceManager:
    def __init__(self, filename: str):
        self.filename = filename

    def load_records(self):
        return get_objects_by_json_file(self.filename, FinanceRecord)

    def save_records(self, records):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([record.to_dict() for record in records], file, ensure_ascii=False, indent=4)

    def add_record(self, amount: float, category: str, date: str, description: str):
        records = self.load_records()
        new_id = max(record.id for record in records) + 1 if records else 1
        new_record = FinanceRecord(new_id, amount, category, date, description)
        records.append(new_record)
        self.save_records(records)
        print("Финансовая запись успешно добавлена!")

    def view_records(self):
        records = self.load_records()
        if not records:
            print("Нет доступных финансовых записей.")
            return

        for record in records:
            print(
                f"{record.id}: {record.amount} | Категория: {record.category}\
| Дата: {record.date} | Описание: {record.description}")

    def filter_records(self, category=None, start_date=None, end_date=None):
        records = self.load_records()

        if category:
            records = [r for r in records if r.category.lower() == category.lower()]

        if start_date:
            records = [r for r in records if
                       datetime.strptime(r.date, '%d-%m-%Y') >= datetime.strptime(start_date, '%d-%m-%Y')]

        if end_date:
            records = [r for r in records if
                       datetime.strptime(r.date, '%d-%m-%Y') <= datetime.strptime(end_date, '%d-%m-%Y')]

        return records

    def generate_report(self, start_date: str, end_date: str):
        filtered_records = self.filter_records(start_date=start_date, end_date=end_date)

        total_income = sum(record.amount for record in filtered_records if record.amount > 0)
        total_expenses = sum(record.amount for record in filtered_records if record.amount < 0)

        print(f"Финансовый отчёт за период с {start_date} по {end_date}:")
        print(f"Общий доход: {total_income:.2f}")
        print(f"Общие расходы: {total_expenses:.2f}")
        print(f"Баланс: {total_income + total_expenses:.2f}")

    def export_records_to_csv(self):
        records = self.load_records()

        with open('finance_export.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'amount', 'category', 'date', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for record in records:
                writer.writerow(record.to_dict())

        print("Финансовые записи успешно экспортированы в finance_export.csv!")

    def import_records_from_csv(self):
        with open(input("Введите имя CSV-файла для импорта: "), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            records = self.load_records()

            for row in reader:
                new_record = FinanceRecord(int(row['id']), float(row['amount']), row['category'], row['date'],
                                           row['description'])
                records.append(new_record)

            self.save_records(records)

        print("Финансовые записи успешно импортированы из CSV-файла.")


class PersonalAssistantApp:
    def __init__(self):
        self.note_manager = NoteManager(NOTES_FILE)
        self.task_manager = TaskManager(TASKS_FILE)
        self.contact_manager = ContactManager(CONTACTS_FILE)
        self.finance_manager = FinanceManager(FINANCE_FILE)

    def main_menu(self):
        while True:
            print("\nДобро пожаловать в Персональный помощник!")
            print("Выберите действие:")
            print("1. Управление заметками")
            print("2. Управление задачами")
            print("3. Управление контактами")
            print("4. Управление финансовыми записями")
            print("5. Калькулятор")
            print("6. Выход")

            choice = input("Ваш выбор: ")

            if choice == '1':
                self.manage_notes_menu()
            elif choice == '2':
                self.manage_tasks_menu()
            elif choice == '3':
                self.manage_contacts_menu()
            elif choice == '4':
                self.manage_finance_menu()
            elif choice == '5':
                self.calculator_menu()
            elif choice == '6':
                print("Выход из приложения.")
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    def manage_notes_menu(self):
        while True:
            print("\nУправление заметками:")
            print("1. Добавить новую заметку")
            print("2. Просмотреть список заметок")
            print("3. Просмотреть подробности заметки")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Экспорт заметок в CSV")
            print("7. Импорт заметок из CSV")
            print("8. Назад")

            choice = input("Ваш выбор: ")

            if choice == '1':
                title = input("Введите заголовок заметки: ")
                content = input("Введите содержимое заметки: ")
                self.note_manager.add_note(title, content)

            elif choice == '2':
                self.note_manager.view_notes()

            elif choice == '3':
                note_id = int(input("Введите ID заметки для просмотра: "))
                self.note_manager.view_note_details(note_id)

            elif choice == '4':
                note_id = int(input("Введите ID заметки для редактирования: "))
                title = input("Введите новый заголовок заметки: ")
                content = input("Введите новое содержимое заметки: ")
                self.note_manager.edit_note(note_id, title, content)

            elif choice == '5':
                note_id = int(input("Введите ID заметки для удаления: "))
                self.note_manager.delete_note(note_id)

            elif choice == '6':
                self.note_manager.export_notes_to_csv()

            elif choice == '7':
                self.note_manager.import_notes_from_csv()

            elif choice == '8':
                break

            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    def manage_tasks_menu(self):
        while True:
            print("\nУправление задачами:")
            print("1. Добавить новую задачу")
            print("2. Просмотреть список задач")
            print("3. Отметить задачу как выполненную")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Экспорт задач в CSV")
            print("7. Импорт задач из CSV")
            print("8. Назад")

            choice = input("Ваш выбор: ")

            if choice == '1':
                title = input("Введите краткое описание задачи: ")
                description = input("Введите подробное описание задачи: ")
                priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")
                due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
                self.task_manager.add_task(title, description, priority, due_date)
            elif choice == '2':
                self.task_manager.view_tasks()
            elif choice == '3':
                task_id = int(input("Введите ID задачи для отметки как выполненной: "))
                self.task_manager.mark_task_as_done(task_id)
            elif choice == '4':
                task_id = int(input("Введите ID задачи для редактирования: "))
                title = input("Введите новое краткое описание задачи: ")
                description = input("Введите новое подробное описание задачи: ")
                priority = input("Выберите новый приоритет (Высокий/Средний/Низкий): ")
                due_date = input("Введите новый срок выполнения (ДД-ММ-ГГГГ): ")
                self.task_manager.edit_task(task_id, title, description, priority, due_date)
            elif choice == '5':
                task_id = int(input("Введите ID задачи для удаления: "))
                self.task_manager.delete_task(task_id)
            elif choice == '6':
                self.task_manager.export_tasks_to_csv()
            elif choice == '7':
                self.task_manager.import_tasks_from_csv()
            elif choice == '8':
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    def manage_contacts_menu(self):
        while True:
            print("\nУправление контактами:")
            print("1. Добавить новый контакт")
            print("2. Поиск контакта")
            print("3. Редактировать контакт")
            print("4. Удалить контакт")
            print("5. Экспорт контактов в CSV")
            print("6. Импорт контактов из CSV")
            print("7. Назад")

            choice = input("Ваш выбор: ")

            if choice == '1':
                name = input("Введите имя контакта: ")
                phone = input("Введите номер телефона: ")
                email = input("Введите адрес электронной почты: ")
                self.contact_manager.add_contact(name, phone, email)

            elif choice == '2':
                query = input("Введите имя или номер телефона для поиска: ")
                self.contact_manager.search_contact(query)

            elif choice == '3':
                contact_id = int(input("Введите ID контакта для редактирования: "))
                name = input("Введите новое имя контакта: ")
                phone = input("Введите новый номер телефона: ")
                email = input("Введите новый адрес электронной почты: ")
                self.contact_manager.edit_contact(contact_id, name, phone, email)

            elif choice == '4':
                contact_id = int(input("Введите ID контакта для удаления: "))
                self.contact_manager.delete_contact(contact_id)

            elif choice == '5':
                self.contact_manager.export_contacts_to_csv()

            elif choice == '6':
                self.contact_manager.import_contacts_from_csv()

            elif choice == '7':
                break

            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    def manage_finance_menu(self):
        while True:
            print("\nУправление финансовыми записями:")
            print("1. Добавить новую финансовую запись")
            print("2. Просмотреть все записи")
            print("3. Сгенерировать отчёт о финансах за период")
            print("4. Экспорт записей в CSV")
            print("5. Импорт записей из CSV")
            print("6. Назад")

            choice = input("Ваш выбор: ")

            if choice == '1':
                amount = float(
                    input("Введите сумму операции (положительное число для доходов, отрицательное для расходов): "))
                category = input("Введите категорию операции: ")
                date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
                description = input("Введите описание операции: ")
                self.finance_manager.add_record(amount, category, date, description)

            elif choice == '2':
                self.finance_manager.view_records()

            elif choice == '3':
                start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
                end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
                self.finance_manager.generate_report(start_date, end_date)

            elif choice == '4':
                self.finance_manager.export_records_to_csv()

            elif choice == '5':
                self.finance_manager.import_records_from_csv()

            elif choice == '6':
                break

            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    def calculator_menu(self):
        while True:
            print("\nКалькулятор:")
            print("1. Посчитать значение арифметического выражения")
            print("2. Назад")

            choice = input("Ваш выбор: ")

            if choice == '1':
                user_input = input("Ввод арифметического выражения: ")
                try:
                    if len(set(user_input) - set("0123456789+-*/ ")) > 0:
                        print("Вы ввели запрещенный символ (разрешены только 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, +, -, *, /")
                    else:
                        print(eval(user_input))
                except ZeroDivisionError:
                    print("Ошибка деления на ноль!")
                except Exception as e:
                    print("Ошибка при вычислении:", e)

            elif choice == '2':
                break

            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")


if __name__ == "__main__":
    create_files_if_not_exist()
    app = PersonalAssistantApp()
    app.main_menu()
