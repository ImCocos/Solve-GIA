import os

import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolveGia.settings')
django.setup()

from SolveGiaApp.models import Task


def parsing():
    our_media = 'media/tasks/images/'
    our_files = 'media/tasks/files/'
    their_media = 'https://kpolyakov.spb.ru/cms/images/'
    their_files = 'https://kpolyakov.spb.ru/cms/files/'

    urls = ["https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=2&cat8=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=3&cat169=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=4&cat21=on&cat22=on&cat23=on&cat25=on&cat166=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=5&cat27=on&cat28=on&cat144=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=6&cat175=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=7&cat38=on&cat39=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=8&cat42=on&cat43=on&cat145=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=9&cat146=on&cat147=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=10&cat148=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=11&cat52=on&cat53=on&cat54=on&cat149=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=12&cat55=on&cat56=on&cat57=on&cat58=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=13&cat59=on&cat173=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=14&cat60=on&cat61=on&cat62=on&cat174=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=15&cat67=on&cat68=on&cat69=on&cat70=on&cat123=on&cat167=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=16&cat44=on&cat45=on&cat46=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=17&cat168=on&cat170=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=18&cat152=on&cat153=on&cat165=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=19&cat154=on&cat163=on&cat171=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=22&cat176=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=23&cat78=on&cat79=on&cat80=on&cat162=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=24&cat155=on&cat156=on&cat164=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=25&cat157=on&cat158=on&cat159=on&cat172=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=26&cat160=on",
            "https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=27&cat161=on"
            ]
    task_number = 0
    for url in enumerate(urls):
        local_task_number = 0
        task_number += 1
        print(f'##### TYPE:{task_number} #####')
        while True:
            try:
                data = requests.get(url[1])
                break
            except:
                continue

        soup = BeautifulSoup(data.content, 'lxml')
        soup = soup.find('table', class_='vartopic')
        is_task = True

        img_name = None
        img_url = None
        files_names = None
        files_urls = None
        files_names_for_save = None

        for task_or_answer in soup.find_all('tr'):
            if is_task:
                local_task_number += 1
                text = str(task_or_answer).split("document.write( changeImageFilePath('")[1].split("'")[0]
                img_name = None if '<img' not in text else text.split('<img src="')[1].split('.gif')[0] + '.gif'
                img_url = None if img_name is None else their_media + img_name
                files_names = None
                files_urls = None
                files_names_for_save = None

                if '<a href="' in text:
                    if url[0] == 23:
                        files_names = [text.split('<a href="')[1].split('"')[0],
                                       text.split('<a href="')[-1].split('"')[0]]
                        files_urls = [their_files + file_name for file_name in files_names]
                        files_names_for_save = [file_name_for_save.split('/')[-1] for file_name_for_save in files_names]
                    else:
                        files_names = [text.split('<a href="')[1].split('"')[0]]
                        files_urls = [their_files + file_name for file_name in files_names]
                        files_names_for_save = [file_name_for_save.split('/')[-1] for file_name_for_save in files_names]

                print(f'{url[0] + 1}.{local_task_number}')
                # print(f'TASK({task_number}):\n{text}')
                # print(f'IMAGE: {img_url}')
                # print(
                #     f'FILES: {[f"{files_names_for_save[i]}: {files_urls[i]}" for i in range(len(files_names))] if files_names is not None else None}')

                is_task = False
            else:
                answer = str(task_or_answer).split("document.write( changeImageFilePath('")[1].split("'")[0]
                # print(f'ANSWER:\n{answer}')
                is_task = True
                # print()

                current_task = Task(type_number=task_number, text=text, answer=answer, category='Informatika')

                if img_url is not None:
                    file = open(our_media + img_name, 'wb')
                    while True:
                        try:
                            image = requests.get(img_url).content
                            break
                        except:
                            continue
                    file.write(image)
                    file.close()
                    current_task.photos = our_media + img_name

                if files_names is not None:
                    for i in range(len(files_names)):
                        file = open(our_files + files_names_for_save[i], 'wb')
                        while True:
                            try:
                                file_d = requests.get(files_urls[i]).content
                                break
                            except:
                                continue
                        file.write(file_d)
                        file.close()

                    files_for_save_str_format = '+'.join(files_names_for_save)
                    current_task.files = files_for_save_str_format

                current_task.save()


# parsing()

our_media = 'media/tasks/images/'
our_files = 'media/tasks/files/'
their_media = 'https://kpolyakov.spb.ru/cms/images/'
their_files = 'https://kpolyakov.spb.ru/cms/files/'

ALL_TASKS = list(Task.objects.all())
for task in ALL_TASKS:
    print(task)
    if '<img' in task.text:
        their_img_path = task.text.split('<img src="')[1].split('"')[0]
        task.text = task.text.replace(their_img_path, '{{task.get_photo_url()}}')

    if '<a href' in task.text:
        their_file_path = task.text.split('<a href="')[1].split('"')[0]
        second_file_exists = task.text.split('<a href="')[-1].split('"')[0] != their_file_path
        task.text = task.text.replace(their_file_path, '{{task.get_file_url()[0]}}')

        if second_file_exists:
            their_file_path = task.text.split('<a href="')[-1].split('"')[0]
            task.files += '+' + their_file_path.split('/')[-1]
            task.text = task.text.replace(their_file_path, '{{task.get_file_url()[1]}}')
