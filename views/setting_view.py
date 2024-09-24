import flet as ft
from tools import database_updater as du, balance_aspect as ba
import sys, os


gem_dlg = ft.AlertDialog(
        title=ft.Text("New Gem Value"),
        actions=[
            ft.IconButton(icon=ft.icons.CHECK)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

logs_dlg = ft.AlertDialog(content=ft.ListView(controls=[ft.Text()]))

reset_alert_ok = ft.ElevatedButton(text="OK")
reset_alert_cancel = ft.ElevatedButton(text="Cancel")
reset_alert = ft.AlertDialog(title=ft.Text('All Data Will Be Erased and App Will Be Closed!'),
                             actions=[reset_alert_ok, reset_alert_cancel])

reset_all = ft.ElevatedButton(content=ft.Row(controls=[ft.Icon(name=ft.icons.DATA_ARRAY, color=ft.colors.WHITE), ft.Text('Reset All Data', size=15, color=ft.colors.WHITE)]), bgcolor=ft.colors.RED_900)

edit_calendar = ft.ElevatedButton(content=ft.Row(controls=[ft.Icon(name=ft.icons.CALENDAR_MONTH), ft.Text('Change Calendar Mode', size=15)]))

def SettingView(page, ft=ft):
    sys.stderr.flush()
    
    balance = ba.balance(page)

    database = du.json_loader()
    gem_dlg.content=ft.TextField(value=database['gem'])
    gem_dlg.actions[0].on_click=lambda e: json_editor('gem', gem_dlg.content.value)

    
    def json_editor(string, value):
        if string == 'gem':
            try:
                value = int(value)
                if value < 1000000000000:
                    database['gem'] = value
                    du.update_json(page,database)
            except:
                pass
            gem_dlg.open = False
        page.update()
        page.go('/home')
    
    def gem_editor(e):
        gem_dlg.open = True
        page.update()

    def theme_editor(e):
        database =du.json_loader()

        if database['theme'] == "dark":
            database['theme'] = "light"
        else:
            database['theme'] = "dark"
        du.update_json(page,database)
        page.go('/home')

    def gemicon_editor(e):
        database['gem_icon']

    def recyclebin_recover(e):
        database =du.json_loader()
        if e.control.data == 'task':
            database['deletedtasks'] = []
            page.go('/home')
        elif e.control.data == 'shop':
            database['deletedshop'] = []
            page.go('/home/shop')
        du.update_json(page,database)
        
    def all_reseter(e):
        
        def ok_reset(e):
            reset_alert.open = False
            page.update()
            if e.control.text == "Cancel":
                return
            du.reset_database(page)
            
            try:
                sys.exit()
            except:
                try:
                    page.window_close()
                except:
                    pass
        
        reset_alert_ok.on_click=reset_alert_cancel.on_click=ok_reset

        reset_alert.open = True
        page.update()
    
    def calendar_editor(e):
        database =du.json_loader()
        if database['date'] == "miladi":
            database['date'] = "shamsi"
        else:
            database['date'] = "miladi"
        du.update_json(page, database)
        page.go('/home')
        
    def task_reseter(e):
        pass
    
    def shop_reseter(e):
        pass
    
    def task_pic_editor(e):
        pass
    
    def log_show(e):
        logs_dlg.content.height = balance/2
        
        with open('database/logs.txt', 'r', encoding='utf-8') as file:
            logs_dlg.content.controls[0].value = file.read()
        logs_dlg.open = True
        page.update()
        
    content = ft.Row(controls=[ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda e:page.go("/home")),ft.Text("Setting", weight='bold', size=26)])
    edit_gem = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.EDIT), ft.Text('Edit Gem Value', size=15)]), on_click=gem_editor))
    edit_theme = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.SUNNY), ft.Text('Change Theme', size=15)]), on_click=theme_editor))
    edit_gemicon = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.LIGHT), ft.Text('Edit Gem Icon', size=15)]), on_click=gemicon_editor))
    edit_taskpicsize = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.LIGHT), ft.Text('Edit Task Pic Size', size=15)]), on_click=task_pic_editor))
    recover_recyclebin = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.RECYCLING), ft.Text('Recover Deleted Tasks', size=15)]), on_click=recyclebin_recover, data='task'))
    recover_recyclebin2 = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.RECYCLING), ft.Text('Recover Deleted Shop Items', size=15)]), on_click=recyclebin_recover, data='shop'))
    see_logs = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.LAPTOP), ft.Text('See Logs', size=15)]), on_click=log_show))


    
    reset_all.on_click=all_reseter
    edit_calendar.on_click = calendar_editor
    
    reset_shop = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.DATA_ARRAY), ft.Text('Reset Shop', size=15)]), on_click=shop_reseter))
    reset_tasks = ft.ElevatedButton(content=ft.Container(content=ft.Row(controls=[ft.Icon(name=ft.icons.DATA_ARRAY), ft.Text('Reset Tasks', size=15)]), on_click=task_reseter))

    content2 = ft.Column(controls=[ft.Row(height=balance/20), content, edit_gem, edit_theme,edit_calendar, recover_recyclebin,recover_recyclebin2,see_logs, reset_all, reset_alert, gem_dlg, logs_dlg])
    return content2