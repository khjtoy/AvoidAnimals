def cal_rect(rect, t):
    r = rect.copy()
    r.x += t[0]
    r.y += t[1]
    return r