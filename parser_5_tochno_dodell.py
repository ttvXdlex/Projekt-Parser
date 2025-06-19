import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk


class Link_obj:
    def __init__(self,link:str,title:str,desc:str,tags:list):
        self.__link=link
        self.__title=title
        self.__desc=desc
        self.__tags=tags

    def __repr__(self):
        return f"{self.__title}\n{self.__desc}\n{self.__tags}"

def all_link_collector():   #эта функция собирает все ссылки на статьи на основной страничке постимеес, превращает их в объекты и добавляет их в 1 список
    main_page = requests.get("https://rus.postimees.ee")
    main_page_soup = BeautifulSoup(main_page.text, 'html.parser')
    all_links = main_page_soup.find_all('a')
    obj_list = []
    for i in all_links:
        href = i.get('href')
        if ".postimees.ee/82" in href:
            link=href
            article = requests.get(href)
            soup = BeautifulSoup(article.text, 'html.parser')
            title = soup.find('meta', property="og:title")
            descr = soup.find('meta', property="og:description")
            tags_list = []
            tagss = soup.find_all('meta', property="article:tag")
            for i in tagss:
                tags_list.append(i['content'])
            abobjekt = Link_obj(link,title['content'],descr['content'],tags_list)
            if abobjekt in obj_list:
                continue
            else:
                obj_list.append(abobjekt)
        else:
            continue
    return obj_list

def all_tags_finder(links):   #эта находит все тэги на всех ссылках и собирает их в 1 список
    all_tags_list = []
    for l in links:
        for i in l._Link_obj__tags:
            if i not in all_tags_list:
                all_tags_list.append(i)
    all_tags_list.sort()
    return all_tags_list

def on_combo_select(event):  #эта функция подзываеться при выборе тэга
    selected_tag = combo.get()
    obj_pool = []
    for l in obj_list:
        if selected_tag in l._Link_obj__tags:
            obj_pool.append(l)

    output_box.config(state=NORMAL)
    output_box.delete(1.0, END)

    for i, link in enumerate(obj_pool, 1):
        tag_name = f"link_{i}"
        start_index = output_box.index(END)
        output_box.insert(END, f"{i}. {link._Link_obj__title}\n{'='*50}\n")

        output_box.tag_add(tag_name, start_index, f"{start_index} lineend")
        output_box.tag_config(tag_name, foreground="blue", underline=1, font=('Arial', 10, 'bold'))

        def handler(event, lnk=link):
            show_article_details(lnk)
        output_box.tag_bind(tag_name, "<Button-1>", handler)

    output_box.config(state=DISABLED)

def show_article_details(link_obj):  #эта функция показывает подробности самой новости при выборе новости и сохроняет ее в history.txt
    output_box2.config(state=NORMAL)
    output_box2.delete(1.0, END)
    output_box2.insert(END, f"Заголовок: {link_obj._Link_obj__title}\n\n")
    output_box2.insert(END, f"Описание: {link_obj._Link_obj__desc}\n\n")
    output_box2.insert(END, f"Ссылка: {link_obj._Link_obj__link}\n\n")
    output_box2.insert(END, f"Теги: {', '.join(link_obj._Link_obj__tags)}\n")
    with open("history.txt", "a+", encoding="utf-8") as myfile:
        myfile.write(f"{link_obj}")
        myfile.write("\n")
        myfile.write(f"{link_obj._Link_obj__link}")
        myfile.write("\n")
        myfile.write("\n")
    output_box2.config(state=DISABLED)

###INTERFACE###

root = Tk()
root.title("Postimees Parser")
root.geometry("900x600+500+200")
root.resizable(False, False)

lbl = Label(root, text="Выберите тэг:",)
lbl.place(x=10, y=15)

combo = ttk.Combobox(root, state="readonly", width=100) #тэги сверху
combo.set("Выберите")
combo.place(x=150, y=16)
combo.bind("<<ComboboxSelected>>", on_combo_select)

output_box = Text(root, height=19, width=109)  #выбор новости по середине
output_box.place(x=10, y=95)
output_box.config(state=DISABLED)

output_box2 = Text(root, height=10, width=109)  #сама новость в самооооом низу
output_box2.place(x=10, y=420)
output_box2.config(state=DISABLED)

# Инициализация данных
obj_list = all_link_collector()
tags = all_tags_finder(obj_list)
combo['values'] = tags

root.mainloop()