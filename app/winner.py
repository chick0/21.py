def get_winner(you: int, me: int, name: dict) -> (bool, str):
    if me == 21:
        win = True
        reason = "축하드립니다! 21을 만들었습니다!"
    elif you == 21:
        win = False
        reason = f"<b>{name['you']}</b>(이)가 21을 만들었습니다!"
    elif me == you:
        win = None
        reason = f"모든 플레이어의 숫자 합이 {me}로 동일합니다"
    elif me > 21 or you > 21:
        if me > 21 and you > 21:
            if me < you:
                win = True
                reason = f"당신의 숫자 합이 21보다 크지만, <b>{name['you']}</b>보다 숫자 합이 21에 가깝습니다"
            else:
                win = False
                reason = f"모든 플레이어의 숫자 합이 21보다 크지만, <b>{name['you']}</b>(이)의 숫자 합이 21에 가깝습니다"
        elif me > 21 and you < 21:
            win = False
            reason = "당신의 숫자 합이 21보다 큽니다"
        else:
            win = True
            reason = f"축하드립니다! <b>{name['you']}</b>(이)의 숫자 합이 21보다 큽니다"
    elif me < you:
        win = False
        reason = f"당신의 숫자합이 <b>{name['you']}</b>(이)의 숫자 합 보다 작습니다"
    elif me > you:
        win = True
        reason = f"축하드립니다! <b>{name['you']}</b>(이) 보다 큰 숫자를 만들었습니다!"
    else:
        win = None
        reason = ""

    return win, reason
