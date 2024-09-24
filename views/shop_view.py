import flet as ft
from tools import database_updater as du, balance_aspect as ba
import sys

add = ft.IconButton(icon=ft.icons.ADD,
                    bgcolor=ft.colors.BLUE_GREY_900)
tabs = ft.Tabs(tabs=[ft.Tab('Inventory', icon=ft.icons.BACKPACK), ft.Tab('Shop', icon=ft.icons.SHOPPING_BASKET)], tab_alignment=ft.TabAlignment.CENTER)
all_shop = ft.Row(controls=[], alignment=ft.MainAxisAlignment.CENTER, wrap=True)
list_shop = ft.ListView(controls=[all_shop])

gem_icon = ft.Image(height=23)
gem_value = ft.Text(size=18, weight='w500')

gem_row = ft.Container(content=ft.Row(controls=[gem_icon, gem_value]))


shop_dlg_del_button = ft.IconButton(icon=ft.icons.DELETE,
                               icon_color=ft.colors.RED)
shop_dlg_buy_button = ft.ElevatedButton(icon=ft.icons.SELL,
                                icon_color=ft.colors.WHITE,
                                text="Get",
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.PURPLE_900)
shop_edit_button = ft.IconButton(icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE)

shop_dlg = ft.AlertDialog(title=ft.Text(), content=ft.Text(),
                     actions=[shop_dlg_del_button, shop_dlg_buy_button,shop_edit_button],
                     actions_alignment=ft.MainAxisAlignment.CENTER)


inventory_dlg_del_button = ft.IconButton(icon=ft.icons.DELETE,
                               icon_color=ft.colors.RED)


inventory_dlg_row_price = ft.Text()
inventory_dlg_row_icon = ft.Image()
# inventory_image = ft.Container(content=ft.Image(border_radius=12), alignment=ft.alignment.center)
inventory_dlg_row = ft.Row(controls=[inventory_dlg_row_icon, inventory_dlg_row_price])
inventory_dlg_desc = ft.Text()

inventory_dlg_content = ft.Column(controls=[inventory_dlg_row, inventory_dlg_desc])

inventory_dlg = ft.AlertDialog(title=ft.Text(), content=inventory_dlg_content,
                     actions=[inventory_dlg_del_button],
                     actions_alignment=ft.MainAxisAlignment.CENTER)


cancel_buy = ft.ElevatedButton(text="Cancel")
ok_buy = ft.ElevatedButton(text="OK")

buy_dlg = ft.AlertDialog(title=ft.Text(), actions=[cancel_buy, ok_buy])

gem_error_button = ft.ElevatedButton('OK')
gem_error = ft.AlertDialog(title=ft.Text("Not Enough Gems!"), actions=[gem_error_button])

del_shop_yes = ft.ElevatedButton(text="Yes")
del_shop_no = ft.ElevatedButton(text="No")
del_shop_really = ft.AlertDialog(title=ft.Text("Really?"), actions=[del_shop_no, del_shop_yes])


del_inventory_yes = ft.ElevatedButton(text="Yes")
del_inventory_no = ft.ElevatedButton(text="No")
del_inventory_really = ft.AlertDialog(title=ft.Text("Really?"), actions=[del_inventory_no, del_inventory_yes])

def ShopView(page, ft=ft):
    balance = ba.balance(page)
    sys.stderr.flush()
    database = du.json_loader()
    
    def shop_menu(e):
        shop = e.control.data
        
        def close_error(e):
            gem_error.open = False
            page.update()
        def close_dlg(e):
            buy_dlg.open = False
            page.update()
        def close_del(e):
            del_shop_really.open = False
            page.update()
        
        def del_shop(e):
            def ok_del(e):
                database = du.json_loader()
                database['deletedshop'].append(shop['id'])
                du.update_json(page,database)
                load_shop(page)
                del_shop_really.open = False
                page.update()

                
            del_shop_yes.on_click = ok_del
            del_shop_no.on_click = close_del
            del_shop_really.open = True

            shop_dlg.open = False
            page.update()
        
        gem_error_button.on_click=close_error
        
        def buy_shop(e):
            buy_dlg.title.value = f"Pay {shop['price']} Gems?"
            
            def okbuy(e):
                database['shop'][str(shop['id'])]['bought'] = 1
                database['gem']-=database['shop'][str(shop['id'])]['price']
                du.update_json(page,database)
                buy_dlg.open = False
                load_shop(page)
                page.update()
                
            ok_buy.on_click = okbuy
            cancel_buy.on_click = close_dlg
            
            database = du.json_loader()
            if database['gem'] >= shop['price']:
                buy_dlg.open = True
                page.update()
            else:
                gem_error.open = True
                page.update()
                return
            page.update()

            
        

        shop_dlg.title.value = shop['name']
        shop_dlg.content.value = shop['desc']
                
        
        shop_dlg_buy_button.on_click = buy_shop
        shop_dlg_del_button.on_click = del_shop
        
        shop_dlg.open = True
        page.update()

    
    def inventory_menu(e):
        inventory = e.control.data
        
        def close_del(e):
            del_inventory_really.open = False
            page.update()      
        
        def del_inventory(e):
            def ok_inventory_del(e):
                database = du.json_loader()
                database['deletedshop'].append(inventory['id'])
                du.update_json(page,database)
                inventory_dlg.open = False
                del_inventory_really.open = False
                load_inventory(page)
                page.update()
            
            del_inventory_yes.on_click = ok_inventory_del
            del_inventory_no.on_click = close_del
            del_inventory_really.open = True

            inventory_dlg.open = False
            page.update()
        
        
        inventory_dlg.title.value = inventory['name']
        # inventory_image.content.src = inventory['image']
        # inventory_image.content.height=page.height/2

        inventory_dlg.content = inventory_dlg_content
        inventory_dlg_row_price.value = str(inventory['price'])
        inventory_dlg_row_icon.src = database['gem_icon']
        inventory_dlg_row_icon.height = balance/23
        inventory_dlg_content.height = balance/4
        
        inventory_dlg_desc.value = inventory['desc']
        
        
        inventory_dlg_del_button.on_click = del_inventory
        
        inventory_dlg.open = True
        page.update()
    
    def tabs_change(e):
        if ((e.control.selected_index) == 0):
            load_inventory(page)
        elif ((e.control.selected_index) == 1):
            load_shop(page)
    
    def load_shop(page):
        all_shop.controls = []
        database = du.json_loader()
        gem_value.value=database['gem']

        page.update()
        
        shops = database['shop']
        
        for shop in shops.values():            
            dead = 0
            for i in database['deletedshop']:
                if shop['id']==i:
                    dead = 1
                
            if dead == 1:
                continue
            
            if shop['bought'] == 1:
                continue
            show_shop = ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Row(controls=[ft.Image(height=14, src=database['gem_icon']),ft.Text(value=(shop['price']), size=13, color=ft.colors.BLACK, weight='bold')],
                                       alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),alignment=ft.alignment.bottom_center,bgcolor='white', width=int(balance/(3.6)),height=int(balance/(2.1))),                    
                    ft.Image(src=shop['image'], width=int(balance/(3.6)),height=int(balance/(2.4)), border_radius=12, fit=ft.ImageFit.COVER),]),
            border_radius=12,
            width=int(balance/(3.6)),
            height=int(balance/(2.1)),
            alignment=ft.alignment.center,
            on_click=shop_menu,
            data = shop)
            
            all_shop.controls.append(show_shop)
            page.update()
    
    def load_inventory(page):
        all_shop.controls = []
        database = du.json_loader()
        gem_value.value=database['gem']


        page.update()
        
        
        inventory = database['shop']
        
        for i in inventory.values():
            
            dead = 0
            for j in database['deletedshop']:
                if i['id']==j:
                    dead = 1
                
            if dead == 1:
                continue
            
            if i['bought'] == 0:
                continue
            
            show_i = ft.Container(
            content=ft.Stack(
                controls=[                    
                    ft.Image(src=i['image'], width=int(balance/(3.6)),height=int(balance/(2.4)), border_radius=12, fit=ft.ImageFit.COVER),]),
            border_radius=12,
            width=int(balance/(3.6)),
            height=int(balance/(2.4)),
            on_click=inventory_menu,
            data = i)
            
            all_shop.controls.append(show_i)
            page.update()
        
    tabs.on_change=tabs_change
    tabs.selected_index=1
    load_shop(page)
    add.on_click=lambda e: page.go('/home/shop/addshop')
    
    gem_icon.src=database['gem_icon']
    gem_value.value=database['gem']
    
    list_shop.width=balance
    list_shop.height = balance-((8/100)*balance)
    
    content = ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e:page.go("/home")),ft.Container(expand=True),gem_row, ft.Container(expand=True),add])
    content2 = ft.Column(controls=[ft.Row(height=balance/20),content,tabs, all_shop, shop_dlg, buy_dlg, inventory_dlg, gem_error, del_shop_really, del_inventory_really])
    return content2