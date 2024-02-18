import os
import json


class FileHelper:

    def make_file(self, content, filename, dirname, should_use_json=False):
        current_dir = os.getcwd()
        folder_dir = os.path.join(current_dir, dirname)

        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with open(os.path.join(folder_dir, filename), 'w', encoding='utf-8') as file:
            if should_use_json:
                json.dump(content, file, ensure_ascii=False, indent=10) # Сохраняем unicode символы и ставим отступ для читаемости
            else:
                file.write(content)

            file.close()
