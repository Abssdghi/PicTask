from tools import pictask_date, balance_aspect as ba
from bing_image_urls import bing_image_urls
import flet as ft
from tools import database_updater as du
import requests, os, shutil, sys

def validator(string):
    result = ''
    for i in string:
        if (i == "\'") or (i == "/") or (i== ":"):
            continue
        result += i
    return result



# def clean_page(page, ft=ft):
#     pic.content.src ="assets/pick_pic.png"
#     name.value = ""  
#     gem.value = 0
#     desc.value = ""
#     repeat.value = 1
#     date_picker.value = pictask_date.datetime.now()
#     update_date('e')
#     page.update()


def BingView(page, ft=ft):
    balance = ba.balance(page)
    sys.stderr.flush()
    
    def set_pic(e):
        nexttaskid = database['next_task_id']
        img = f'assets/taskspics/{nexttaskid}.jpg'
        
        page.go('/home/addtask')
        pic.content.src = "assets/pick_pic_loading.png"
        page.update()                
        res = requests.get(e.control.content.src)
        with open(img,'wb') as f:
            f.write(res.content)
        
        du.image_save_data(page, str(nexttaskid))
        pic.content.src = e.control.content.src
        page.update()

    
    def search(e):
        data = search_field.value
        images_result.controls.append(ft.ProgressRing(width=balance/4, height=balance/4))
        try:
            result = bing_image_urls(query=data, limit=33, adult_filter_off=True)
        except Exception as e:
            images_result.controls = []
            images_result.controls.append(ft.Text(value='Bad Connection... \n'+str(e), weight=ft.FontWeight.W_400))
            page.update()
            return
        
        images_result.controls = []
        for i in range(len(result)):
            show_pic = ft.Container(
                    content=
                    ft.Image(src=result[i],width=int(balance/(3.6)), height=balance/(3.6), border_radius=12, fit=ft.ImageFit.COVER,),
                    border_radius=25,
                    width=int(balance/(3.6)),
                    height=int(balance/(3.6)),
                    on_click=set_pic,
                    data=i)
            images_result.controls.append(show_pic)
            page.update()
        page.update()
    
    database = du.json_loader()        
    
    search_field = ft.TextField(hint_text="find a pic...", width=balance/1.8, border_radius=15)
    buttons = ft.Row(controls=[
        ft.IconButton(icon=ft.icons.CANCEL ,on_click=lambda e : page.go('/home/addtask'), bgcolor='red', icon_color='white'),
        ft.IconButton(icon=ft.icons.CHECK_CIRCLE, on_click=search, bgcolor='green', icon_color='white')])
    
    images_result = ft.Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True)
    images_result_final = ft.ListView(controls=[images_result], width=page.width, height=page.height-((15/100)*page.height))

    content = ft.Row([search_field, buttons], alignment=ft.MainAxisAlignment.CENTER)
    
    content2 = ft.Column(controls=[ft.Row(height=balance/20), content, images_result_final], alignment=ft.MainAxisAlignment.CENTER)

    return content2


def AddTaskView(page, ft=ft):
    balance = ba.balance(page)

    sys.stderr.flush()
    
    def clean_page(page, ft=ft):
        pic.content.src ="assets/pick_pic.png"
        name.value = ""  
        gem.value = 0
        desc.value = ""
        repeat.value = 1
        date_picker.value = pictask_date.datetime.now()
        update_date('e')
        page.update()

    def file_picked(e):
        database = du.json_loader()
        nexttaskid = database['next_task_id']
        img = f'assets/taskspics/{nexttaskid}.jpg'
        if (e.files):
            shutil.copy(e.files[0].path, img)
            pic.content.src = e.files[0].path
        du.image_save_data(page, str(nexttaskid))
        page.update()

    def sumbit_add(e):
        
        def close_error(e):
            error.open = False
            page.update()

        if pic.content.src == "assets/pick_pic.png":
            error = ft.AlertDialog(modal=True, title=ft.Text('Set a Pic !'), actions=[ft.ElevatedButton('OK', on_click= close_error)])
            page.dialog = error
            error.open = True
            page.update()
            return
        
        nexttaskid = database['next_task_id']
            
        for i in range(int(repeat.value)):
            mydate = pictask_date.after(date_picker.value.strftime("%Y%m%d"), i)
            try:
                database['tasks'][mydate]
            except:
                database['tasks'][mydate] = {}
            task_json = {}
            task_json['id'] = nexttaskid
            task_json['name'] = name.value
            task_json['desc'] = desc.value
            task_json['do'] = 0
            task_json['gem'] = int(gem.value)
            task_json['repeat'] = repeat.value
            task_json['start'] = date_picker.value.strftime("%Y%m%d")
            task_json['date'] = mydate
            task_json['count'] = i+1
            task_json['end'] = pictask_date.after(date_picker.value.strftime("%Y%m%d"), int(repeat.value)-1)
            task_json['image'] = f'assets/taskspics/{nexttaskid}.jpg'
            database['tasks'][mydate][task_json['id']] = task_json
        
        database['next_task_id'] += 1    
        du.update_json(page, database)
        clean_page(page)
        page.go('/home')
        # page.update()
        
    def cancel_add(e):
        database = du.json_loader()
        page.go('/home')
        clean_page(page)
        nexttaskid = database['next_task_id']
        img = f'assets/taskspics/{nexttaskid}.jpg'
        
        try:
            os.remove(img)
        except Exception as e:
            pass

    def update_date(e):
        formatted_date = date_picker.value.strftime("%Y/%m/%d")
        formatted_date_2 = date_picker.value.strftime("%Y%m%d")
        converted = pictask_date.convert_to_shamsi(formatted_date_2)
        if database['date'] == "shamsi":
            date_pick_button.controls[0].text = converted[:4]+'/'+converted[4:6]+'/'+converted[6:]
        elif database['date'] == "miladi":
            date_pick_button.controls[0].text = formatted_date
        page.update()       


    database = du.json_loader()

    
    # date_pick_button.text=pictask_date.datetime.now().strftime("%Y/%m/%d")
    update_date('e')
    
    first_row.controls=[pic]
    buttons.controls=[cancel_addtask,done_addtask]
    
    # page.overlay.append(file_picker)
    file_picker.on_result = file_picked
    
    from_gallery.on_click = lambda e:file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)
    from_net.on_click = lambda e: page.go("/home/addtask/bing")
    
    gem.width = repeat.width = balance/2
    date_pick_button.controls[0].width = balance/2
    
    def pageopendate_picker(e):
        date_picker.open = True
        page.update()

    date_picker.on_change = update_date
    date_pick_button.controls[0].on_click=lambda e: pageopendate_picker(e)
    
    cancel_addtask.width = done_addtask.width = balance/2.2
    cancel_addtask.content.on_click = cancel_add
    done_addtask.content.on_click = sumbit_add
    
    all_addtask = ft.Column(controls=[ft.Row(height=balance/40), first_row, name, gem, date_pick_button,repeat, desc, buttons, date_picker, file_picker], alignment=ft.MainAxisAlignment.CENTER)
    
    return all_addtask

from_gallery = ft.PopupMenuItem('Gallery')
from_net = ft.PopupMenuItem('Internet')

pic = ft.PopupMenuButton(content=ft.Image(src = "assets/pick_pic.png", width="175",
                                          height="175",
                                          fit=ft.ImageFit.COVER, border_radius=50),
                         items=[from_gallery, from_net],
                         menu_position=ft.PopupMenuPosition.UNDER)

name = ft.TextField(value="", label="Name", border_radius=15)   
gem = ft.Dropdown(value=0, label="Gem", options=[ft.dropdown.Option(day) for day in [int(i) for i in range(0, 201)]], border_radius=15)
desc = ft.TextField(value="", label="Description", border_radius=15)
repeat = ft.Dropdown(value=1, label="Repeat", options=[ft.dropdown.Option(day) for day in [int(i) for i in range(1, 366)]], border_radius=15)

date_pick_button = ft.Row(controls=[ft.ElevatedButton()],alignment=ft.MainAxisAlignment.CENTER)
date_picker = ft.DatePicker(value=pictask_date.datetime.now(),
                            first_date=pictask_date.datetime.strptime(pictask_date.before(pictask_date.datetime.now().strftime("%Y%m%d"), 365), '%Y%m%d'),
                            last_date=pictask_date.datetime.strptime(pictask_date.after(pictask_date.datetime.now().strftime("%Y%m%d"), 365), '%Y%m%d'))

first_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

cancel_addtask = ft.Container(ft.IconButton(icon=ft.icons.CANCEL, icon_color='white'), bgcolor='red', border_radius=15)
done_addtask = ft.Container(ft.IconButton(icon=ft.icons.CHECK_CIRCLE, icon_color='white'), bgcolor='green',  border_radius=15)

buttons = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

file_picker = ft.FilePicker()