from django.shortcuts import render, get_object_or_404, redirect

from SolveGiaApp.models import *


def index(request):
    return render(request=request, template_name='index.html')


def show_task(request, category, id):
    print(category, id)
    return render(request=request, template_name='task.html', context={
        'task': get_object_or_404(Task, id=id, category=category)
    })


def parse(request):
    def parsing():
        from bs4 import BeautifulSoup
        import requests
        import lxml
        from SolveGiaApp.models import Task

        inf = 'Informatika'

        urls = ["https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on"]
        answer = None
        type_number = 0
        for url in urls:
            type_number += 1
            data = requests.get(url)
            soup = BeautifulSoup(data.content, 'lxml')

            for script in soup.find_all('script'):
                script_text = script.text.strip()

                if 'document.write' in script_text and 'changeImageFilePath' in script_text and '№&nbsp' in script_text:
                    is_task = True
                    text = script_text
                    text = text.split("document.write( changeImageFilePath('")[1].split("')")[0]

                    if '<img src=' in text:
                        img_name = text.split('src="')[1].split('"')[0]
                        text = text.replace(img_name, '{{task.get_photo_url()}}')
                        img_url = 'https://kpolyakov.spb.ru/cms/images/' + img_name
                        image = requests.get(img_url).content
                        with open(f'SolveGiaApp/media/tasks/images/{img_name}', 'wb') as file:
                            file.write(image)
                        file.close()
                    else:
                        image = None
                    # print('TEXT:' + text + '\nIMAGE: ' + img_name)

                if 'document.write' in script_text and 'changeImageFilePath' in script_text and '№&nbsp' not in script_text:
                    is_task = True
                    answer = script_text
                    answer = answer.split("document.write( changeImageFilePath('")[1].split("')")[0]
                    # print('ANSWER:' + answer)

                if answer is not None:
                    task_for_save = Task(type_number=type_number, text=text, photos=img_name, answer=answer, category=inf)
                    task_for_save.save()
                    answer = None

    parsing()
    return redirect('')
