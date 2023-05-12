def parsing():
    from bs4 import BeautifulSoup
    import requests
    import lxml
    from SolveGiaApp.models import Category, Task

    inf = Category(name='Info')
    inf.save()

    urls = ["https://kpolyakov.spb.ru/school/ege/gen.php?action=viewAllEgeNo&egeId=1&cat12=on&cat13=on"]

    for url in urls:
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'lxml')

        for script in soup.find_all('script'):
            script_text = script.text.strip()
            img_name = None
            text = None
            answer = None
            is_task = False

            if 'document.write' in script_text and 'changeImageFilePath' in script_text and '№&nbsp' in script_text:
                is_task = True
                text = script_text
                text = text.split("document.write( changeImageFilePath('")[1].split("')")[0]

                if '<img src=' in text:
                    img_name = text.split('src="')[1].split('"')[0]
                    text = text.replace(img_name, '{{task.get_photo_url()}}')
                    img_url = 'https://kpolyakov.spb.ru/cms/images/' + img_name
                    image = requests.get(img_url).content
                    file = open(f'media/tasks/images/{img_name}', 'w')
                    file.close()
                else:
                    image = None
                print('TEXT:' + text)

            if 'document.write' in script_text and 'changeImageFilePath' in script_text and '№&nbsp' not in script_text:
                is_task = True
                answer = script_text
                answer = answer.split("document.write( changeImageFilePath('")[1].split("')")[0]
                print('ANSWER:' + answer)

            if is_task and img_name is not None and answer is not None:
                task_for_save = Task(text=text, image=img_name, answer=answer, category=inf)
                # task_for_save.save()
parsing()