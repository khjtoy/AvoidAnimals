def cal_rect(rect, t):
    # rect -> pygame.Rect
    # t -> tuple
    r = rect.copy()     # deepcopy
    r.x += t[0]
    r.y += t[1]
    return r