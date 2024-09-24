import flet as ft
import sys

from views.home_view import HomeView
from views.addtask_view import AddTaskView, BingView
from views.setting_view import SettingView
from views.shop_view import ShopView
from views.addshop_view import AddShopView, ShopBingView

def main(page: ft.Page):
    sys.stderr.flush()
    output_file = open('database/logs.txt', 'a')
    
    sys.stdout = output_file
    sys.stderr = output_file

    # page.window_width=360
    # page.window_height=780
    page.title = "PicTask"
    # page.window_full_screen = True

    def route_change(route):
        
        if page.route == "/home":
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",
                    [],
                )
            )
            page.views.append(
                ft.View(
                    "/home",
                    [HomeView(page)],
                )
            )
        elif page.route == "/home/addtask":
            for i in page.views:
                if i.route == "/home/addtask/bing":
                    page.views.remove(i)
            for i in page.views:
                if i.route == "/home/addtask":
                    page.views.remove(i)
            page.views.append(
                ft.View(
                    "/home/addtask",
                    [AddTaskView(page)],
                )
            )
        elif page.route == "/home/addtask/bing":
            page.views.append(
                ft.View(
                    "/home/addtask/bing",
                    [BingView(page)],
                )
            )
        elif page.route == "/home/setting":
            page.views.append(
                ft.View(
                    "/home/setting",
                    [SettingView(page)],
                )
            )
        elif page.route == "/home/shop":

            for i in page.views:
                if i.route == "/home/shop/addshop/shopbing":
                    page.views.remove(i)
            for i in page.views:
                if i.route == "/home/shop/addshop":
                    page.views.remove(i)
            for i in page.views:
                if i.route == "/home/shop":
                    page.views.remove(i)
            page.views.append(
                ft.View(
                    "/home/shop",
                    [ShopView(page)],
                )
            )
            

        elif page.route == "/home/shop/addshop":
            for i in page.views:
                if i.route == "/home/shop/addshop/shopbing":
                    page.views.remove(i)
            for i in page.views:
                if i.route == "/home/shop/addshop":
                    page.views.remove(i)
            page.views.append(
                ft.View(
                    "/home/shop/addshop",
                    [AddShopView(page)],
                )
            )
        elif page.route == "/home/shop/addshop/shopbing":
            for i in page.views:
                if i.route == "/home/shop/addshop/shopbing":
                    page.views.remove(i)
            page.views.append(
                ft.View(
                    "/home/shop/addshop/shopbing",
                    [ShopBingView(page)],
                )
            )
        page.update()

    def view_pop(view):
        if page.route == ('/home'):
            try:
                sys.exit()
            except:
                page.window_close()
        else:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    # page.go(page.route)
    page.go('/home')

ft.app(target=main)