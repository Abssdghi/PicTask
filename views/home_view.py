from tools import pictask_date, database_updater as du, balance_aspect as ba
import sys, os
import flet as ft


# devicename = socket.gethostname()



add = ft.IconButton(icon=ft.icons.ADD,
                    bgcolor=ft.colors.BLUE_GREY_900)
date_numeric = pictask_date.datetime.now().strftime("%Y%m%d")
date_picker = ft.IconButton(icon=ft.icons.CALENDAR_MONTH)
date_picker_banner = ft.DatePicker(
                        first_date=pictask_date.datetime.strptime(pictask_date.before(pictask_date.datetime.now().strftime("%Y%m%d"), 365), '%Y%m%d'),
                        last_date=pictask_date.datetime.strptime(pictask_date.after(pictask_date.datetime.now().strftime("%Y%m%d"), 365), '%Y%m%d'))

setting = ft.IconButton(icon=ft.icons.SETTINGS)

gem_icon = ft.Image(height=23)
gem_value = ft.Text(size=18, weight='w500')

gem_row = ft.Container(content=ft.Row(controls=[gem_icon, gem_value]))
right_buttons = ft.Row()
proper = ft.Row(spacing=40)

date_control_back =ft.IconButton(icon=ft.icons.NAVIGATE_BEFORE)
date_control_date = ft.Container(ft.Text(size=25, weight='bold'),border_radius=12, scale=1)
date_control_next = ft.IconButton(icon=ft.icons.NAVIGATE_NEXT)
date_control = ft.Row(controls=[date_control_back, date_control_date, date_control_next],
                      alignment=ft.MainAxisAlignment.CENTER,
                      spacing=5)


all_tasks = ft.Row(controls=[], alignment=ft.MainAxisAlignment.CENTER, wrap=True)
list_tasks = ft.ListView(controls=[all_tasks])

dlg_del_button = ft.IconButton(icon=ft.icons.DELETE,
                               icon_color=ft.colors.RED)
dlg_done_button = ft.IconButton(icon=ft.icons.CHECK,
                                icon_color=ft.colors.WHITE,
                                bgcolor="green")
dlg_edit_button = ft.IconButton(icon=ft.icons.EDIT,
                                icon_color=ft.colors.BLUE)

dlg = ft.AlertDialog(title=ft.Text(), content=ft.Text(),
                     actions=[dlg_del_button, dlg_done_button, dlg_edit_button],
                     actions_alignment=ft.MainAxisAlignment.CENTER)

task_del_yes = ft.ElevatedButton(text="Yes")
task_del_no = ft.ElevatedButton(text="No")
task_del_alert = ft.AlertDialog(title=ft.Text("Really?"), actions=[task_del_no, task_del_yes])


def HomeView(page, ft=ft):
        sys.stderr.flush()
        try:
            if not os.path.exists("assets/taskspics"):
                os.makedirs("assets/taskspics")
        except:
            pass
        
        try:
            if not os.path.exists("assets/shoppics"):
                os.makedirs("assets/shoppics")
        except:
            pass

        database = du.json_loader()

        if database['reset'] == 1:
            du.get_data(page)
            database = du.json_loader()

        balance = ba.balance(page)
        page.theme_mode = database['theme']
        database['device_name'] = 'devicename'
        du.update_json(page, database)
        add.on_click=lambda e: page.go('/home/addtask')
        
        def check_date(date):
            now = pictask_date.datetime.now().strftime("%Y%m%d")
            if date == now:
                date_control_date.content.bgcolor=ft.colors.PINK_800
            else:
                date_control_date.content.bgcolor=None
            page.update()

        def task_menu(e):
            task = e.control.data['task']
            date = e.control.data['date']
            dlg.title.value = ""
            dlg.content.value = ""
            
            def done_task(e):
                date = task['date']
                database = du.json_loader()
                do = database['tasks'][task['date']][str(task['id'])]['do']
                if do == 0:
                    database['tasks'][task['date']][str(task['id'])]['do'] = 1
                    database['gem'] += database['tasks'][task['date']][str(task['id'])]['gem']
                else:
                    database['tasks'][task['date']][str(task['id'])]['do'] = 0
                    database['gem'] -= database['tasks'][task['date']][str(task['id'])]['gem']
                du.update_json(page,database)
                dlg.open = False
                load_tasks(page, date)
                page.go('/home')
                page.update()
            
            def del_task(e):
                
                def close_del(e):
                    task_del_alert.open = False
                    page.update()
                
                def ok_del_task(e):
                    database = du.json_loader()
                    database['deletedtasks'].append(task['id'])
                    du.update_json(page,database)
                    dlg.open = False
                    load_tasks(page, date)
                    task_del_alert.open = False
                    page.update()
            
                task_del_yes.on_click = ok_del_task
                task_del_no.on_click = close_del
                task_del_alert.open = True

                dlg.open = False
                page.update()
            
            xofx = f"({task['count']} of {task['repeat']})"
            if xofx == "(1 of 1)":
                xofx = " "
            
            if (task['name'] == "") and (xofx == " "):
                pass
            else:
                dlg.title.value = str(task['name'])+" "+ xofx
                
            if task['desc'] != "":
                dlg.content.value=(task['desc'])

            dlg_del_button.on_click= del_task
            dlg_done_button.on_click = done_task


            
            dlg.open = True
            page.update()

        def load_tasks(page, date):
            all_tasks.controls = []

            page.update()
            database = du.json_loader()
            
            if database['gem'] > 99999999:
                gem_row.content.controls[1].size = 14
            if database['gem'] > 9999999999:
                gem_row.content.controls[1].size = 12
            
            list_tasks.width=page.width
            list_tasks.height = page.height-((8/100)*page.height)
            
            try:
                day_tasks = database["tasks"][date]
            except KeyError as e:
                database["tasks"][date] = {}
                du.update_json(page,database)
                day_tasks = database["tasks"][date]
                        
            for task in day_tasks.values():
                dead = 0
                for i in database['deletedtasks']:
                    if task['id']==i:
                        dead = 1
                if dead == 1:
                    continue
                
                show_task = ft.Container(
                content=ft.Stack(
                    controls=[
                        ft.Image(src=task['image'], width=int(balance/(3.6)),height=int(balance/(3.6)), border_radius=12, fit=ft.ImageFit.COVER),
                        # ft.Container(
                        #     content=ft.Icon(name=ft.icons.CIRCLE, size=18, color="black"),alignment=ft.alignment.bottom_right, scale=1),
                        ft.Container(
                            content=ft.Container(ft.Text(task['gem'], size=11, color=ft.colors.BLACK, weight='bold', bgcolor='white'), border_radius=6),alignment=ft.alignment.bottom_right, scale=0.94),
                    ]
                ),
                border_radius=12,
                width=int(balance/(3.6)),
                height=int(balance/(3.6)),
                on_click=task_menu,
                data = {'task':task,'date':date})
                
                if task['do'] == 1:
                    done_img = ft.Image(src='assets/donetask.png', width=int(balance/(3.6)),height=int(balance/(3.6)), border_radius=12, fit=ft.ImageFit.COVER, color=ft.colors.GREEN_900, opacity=0.7)
                    show_task.content.controls.append(done_img)
                
                all_tasks.controls.append(show_task)
                page.update()
                
            value = gem_value.value
            database_value = database['gem']
            
            
            if database_value > value:
                for i in range(database_value - value):
                    gem_row.content.controls[1].value += 1
                    # time.sleep(0.0004)
                    page.update()
            else:
                for i in range(value - database_value):
                    gem_row.content.controls[1].value -= 1
                    # time.sleep(0.0004)
                    page.update()
            
            page.update()
            
        def handle_change(e):
            date_picker_banner.open = False
            date_changed = e.control.value.strftime('%Y%m%d')
            change_date(page, date_changed)
    
        def change_date(page, date):
            # if date > pictask_date.datetime.now().strftime("%Y%m%d"):
            #     return
            date_numeric = date
            today_date = pictask_date.format_date(date)[database["date"]]

            check_date(date)
            date_control_date.content.value=today_date
            date_control_back.on_click=lambda e : change_date(page, pictask_date.before(date_numeric,1))
            date_control_next.on_click=lambda e : change_date(page, pictask_date.after(date_numeric,1))
            load_tasks(page, date)
            # add.on_click=lambda e: page.go('/addtask')

            page.update()
                
        today_date = pictask_date.format_date(date_numeric)[database["date"]]
        
        date_picker_banner.on_change = handle_change
        
        def pageopendate_picker_banner(e):
            date_picker_banner.open = True
            page.update()

        
        date_picker.on_click=lambda e: pageopendate_picker_banner(e)
        
        setting.on_click=lambda e: page.go('/home/setting')

        gem_icon.src=database['gem_icon']
        gem_row.on_click=lambda e: page.go("/home/shop")
        gem_value.value=database['gem']
        
        right_buttons.controls=[setting, date_picker, add]
        proper.controls=[gem_row, ft.Container(expand=True),right_buttons]
        
        check_date(date_numeric)
        date_control_date.content.value=today_date
        # if today_date == pictask_date.format_date(date_numeric)[database["date"]]:
        #     date_control_date
        date_control_back.on_click=lambda e : change_date(page, pictask_date.before(date_numeric,1))
        date_control_next.on_click=lambda e : change_date(page, pictask_date.after(date_numeric,1))

        load_tasks(page, date_numeric)
                
        all_page = ft.Column(controls=[ft.Row(height=balance/20), proper, date_control, list_tasks, dlg, date_picker_banner, task_del_alert], alignment=ft.MainAxisAlignment.CENTER)
        
        return all_page