def balance(page):
    if page.height > page.width:
        balance = page.width
    elif page.height < page.width:
        balance = page.height
    
    if balance == 0:
        return 360
    return balance