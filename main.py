
"""
Основне завдання.

o1. Написати програму, яка генерує текстовий контент,
що складається з заданої кількості речень. Кожне речення
складається з випадкової кількості умовних* слів
(діапазон кількості слів задається).
Кожне слово складається з випадкової кількості символів (діапазон задається).
Згенерований текст записується у текстовий файл (ім'я файлу задається).

o2. Прочитайте весь файл і виведіть його вміст.

o3. Прочитайте файл по рядках і додайте його в словник, де номер рядка є ключем,
а рядок змінною. Запишіть словник в інший файл в форматі JSON.

*Умовне слово - це випадковий набір певної кількості символів,
тут використовується для спрощення задачі написання програми,
так як основна мета заняття - робота з файлами, а не генерація тексту.
"""

import random
import json

class TextGenerator:
    def __init__(self, text_filename, json_filename, data_filename):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

        self.text_filename = text_filename
        self.json_filename = json_filename
        self.data_filename = data_filename

        self.word_length = (3, 10)
        self.sentence_length = (2, 20)
        self.sentence_num_length = (1, 100)
    
    def run(self):
        # o1.
        text = self.generate_text()
        self.save_to_file(self.text_filename, text)
        print(f"Text saved to {self.text_filename}")

        # o2. 
        print("\nFile Content:")
        print(self.read_file(self.text_filename))

        # o3.
        text_dict = self.file_to_dict(self.text_filename)
        self.save_dict_to_json(text_dict, self.json_filename)
        print(f"\nDictionary saved to {self.json_filename}")

        #i3.
        self.count_bytes_and_save(self.text_filename)
        self.read_and_print_data(self.data_filename)


    def generate_word(self):
        word_length = random.randint(*self.word_length)
        return ''.join(random.choices(self.alphabet, k=word_length))

    def generate_sentence(self):
        sentence_length = random.randint(*self.sentence_length)
        sentence = [self.generate_word() for _ in range(sentence_length)]
        return ' '.join(sentence).capitalize() + '.'

    def generate_text(self):
        sentence_num_length = random.randint(*self.sentence_num_length)
        return '\n'.join(self.generate_sentence() for _ in range(sentence_num_length))

    def save_to_file(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def file_to_dict(self, filename):
        line_dict = {}
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line_dict[line_number] = line.strip()
        return line_dict

    def save_dict_to_json(self, dictionary, json_filename):
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(dictionary, json_file, ensure_ascii=False, indent=4)

    
    def count_bytes_and_save(self, filename):
        with open(filename, 'rb') as file:
            data = file.read()
        
        byte_counts = {}
        for byte in data:
            if byte in byte_counts:
                byte_counts[byte] += 1
            else:
                byte_counts[byte] = 1
        
        with open(self.data_filename, 'w') as output_file:
            for byte, count in byte_counts.items():
                output_file.write(f"{byte} {count}\n")
        
        print(f"Byte count saved to {self.data_filename}")

    def read_and_print_data(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
        print("Content of", filename, "\n", content)
    
"""

Індивідуальні завдання.

Номер варіанту = номер студента в групі % 5 + 1
"""

variant_num = 7 % 5 + 1
print("variant: i" + str(variant_num))

"""
i3. Написати функцію, яка приймає в якості аргумента ім'я файлу і
читає вказаний файл в бінарному форматі. Для згенерованого в п.1 файлу
підрахувати кількість однакових байт, що зустрічається в файлі і записати
ці дані парами в новий файл з таким самим іменем і розширенням data.
"""

if __name__ == "__main__":
    text_generator = TextGenerator("text.txt", "text.json", "text.data")
    text_generator.run()