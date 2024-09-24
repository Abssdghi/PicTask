from bing_image_urls import bing_image_urls
import flet as ft
from tools import database_updater as du
from tools import balance_aspect as ba
import requests, os, shutil, sys


def clean_page(page, ft=ft):
    pic.content.src ="assets/pick_shop.png"
    name.value = ""  
    price.value = 1
    desc.value = ""
    page.update()


def ShopBingView(page, ft=ft):
    balance = ba.balance(page)

    sys.stderr.flush()

    def set_pic(e):
        nextshopid = database['next_shop_id']
        img = f'assets/shoppics/{nextshopid}.jpg'
        
        page.go('/home/shop/addshop')
        pic.content.src = "assets/pick_shop_loading.png"
        page.update()                
        res = requests.get(e.control.content.src)
        with open(img,'wb') as f:
            f.write(res.content)
        
        du.image_save_data(page, str(nextshopid))
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
                    ft.Image(src=result[i],width=int(balance/(3.6)), height=balance/(2.4), border_radius=12, fit=ft.ImageFit.COVER,),
                    border_radius=25,
                    width=int(balance/(3.6)),
                    height=int(balance/(2.4)),
                    on_click=set_pic,
                    data=i)
            images_result.controls.append(show_pic)
            page.update()
        page.update()
    
    database = du.json_loader()        
    
    search_field = ft.TextField(hint_text="find a pic...", width=balance/1.8, border_radius=15)
    buttons = ft.Row(controls=[
        ft.IconButton(icon=ft.icons.CANCEL ,on_click=lambda e : page.go('/home/shop/addshop'), bgcolor='red', icon_color='white'),
        ft.IconButton(icon=ft.icons.CHECK_CIRCLE, on_click=search, bgcolor='green', icon_color='white')])
    
    images_result = ft.Row(alignment=ft.MainAxisAlignment.CENTER, wrap=True)
    images_result_final = ft.ListView(controls=[images_result], width=page.width, height=page.height-((15/100)*page.height))

    content = ft.Row([search_field, buttons], alignment=ft.MainAxisAlignment.CENTER)
    
    content2 = ft.Column(controls=[ft.Row(height=balance/40), content, images_result_final], alignment=ft.MainAxisAlignment.CENTER)

    return content2


def AddShopView(page, ft=ft):
    balance = ba.balance(page)
    sys.stderr.flush()
    
    def file_picked(e):
        database = du.json_loader()
        nextshopid = database['next_shop_id']
        img = f'assets/shoppics/{nextshopid}.jpg'
        if (e.files):
            shutil.copy(e.files[0].path, img)
            pic.content.src = e.files[0].path
        du.image_save_data(page, str(nextshopid))
        page.update()

    def sumbit_add(e):
        
        def close_error(e):
            error.open = False
            page.update()

        if pic.content.src == ("assets/pick_shop.png"):
            error = ft.AlertDialog(modal=True, title=ft.Text('Set a Pic !'), actions=[ft.ElevatedButton('OK', on_click= close_error)])
            page.dialog = error
            error.open = True
            page.update()
            return
        
        nextshopid = database['next_shop_id']

        task_json = {}
        task_json['id'] = nextshopid
        task_json['name'] = name.value
        task_json['desc'] = desc.value
        task_json['bought'] = 0
        task_json['price'] = int(price.value)
        task_json['image'] = f'assets/shoppics/{nextshopid}.jpg'
        database['shop'][task_json['id']] = task_json
        
        database['next_shop_id'] += 1    
        du.update_json(page,database)
        clean_page(page)
        page.go('/home/shop')
        # page.update()
        
    def cancel_add(e):
        database = du.json_loader()
        nextshopid = database['next_shop_id']
        img1 = f'assets/shoppics/{nextshopid}.jpg'
        
        try:
            os.remove(img1)
        except Exception as e:
            pass
        clean_page(page)
        page.go('/home/shop')
        

    database = du.json_loader()
    
    first_row.controls=[pic]
    buttons.controls=[cancel_addshop,done_addshop]
    
    file_picker.on_result = file_picked
    
    from_gallery.on_click = lambda e:file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)
    from_net.on_click = lambda e: page.go("/home/shop/addshop/shopbing")
    
    price.width = balance/2.5
    
    cancel_addshop.width = done_addshop.width = balance/2.2
    cancel_addshop.content.on_click = cancel_add
    done_addshop.content.on_click = sumbit_add
    
    all_addtask = ft.Column(controls=[ft.Row(height=balance/20), first_row, name, price, desc, buttons, file_picker], alignment=ft.MainAxisAlignment.CENTER)
    
    return all_addtask

from_gallery = ft.PopupMenuItem('Gallery')
from_net = ft.PopupMenuItem('Internet')

pic = ft.PopupMenuButton(content=ft.Image(src = "assets/pick_shop.png",
                                          width="160",
                                          height="240",
                                          fit=ft.ImageFit.COVER, border_radius=50),
                         items=[from_gallery, from_net],
                         menu_position=ft.PopupMenuPosition.UNDER)

name = ft.TextField(value="", label="Name", border_radius=15)   
price = ft.TextField(value=1, label="Gem Price", keyboard_type=ft.KeyboardType.NUMBER, border_radius=15)
desc = ft.TextField(value="", label="Description", border_radius=15)


first_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

cancel_addshop = ft.Container(ft.IconButton(icon=ft.icons.CANCEL, icon_color='white'), bgcolor='red', border_radius=15)
done_addshop = ft.Container(ft.IconButton(icon=ft.icons.CHECK_CIRCLE, icon_color='white'), bgcolor='green',  border_radius=15)

buttons = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

file_picker = ft.FilePicker()