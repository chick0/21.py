def get_winner(you: int, me: int, name: dict) -> (bool, str):
    if me == 21:
        # 플레이어의 21 확인
        win = True
        reason = "축하드립니다! 21을 만들었습니다!"

    elif you == 21:
        # 컴퓨터의 21 확인
        win = False
        reason = f"<b>{name['you']}</b>(이)가 21을 만들었습니다!"

    elif me == you:
        # 플레이어와 컴퓨터의 숫자 합이 같은지 확인
        win = None
        reason = f"모든 플레이어의 숫자 합이 {me}로 동일합니다."

    elif me > 21 or you > 21:
        # 플레이어 또는 컴퓨터의 숫자 합이 21을 넘었는지 확인

        if me > 21:
            # 플레이어의 숫자 합이 21을 넘었는지 확인

            if you > 21:
                # 플레이어의 숫자 합은 21을 넘었고,
                #   컴퓨터의 숫자 합은 21을 넘은 경우

                # 플레이어의 숫자 합이 더 작은 경우
                if me < you:
                    win = True
                    reason = f"당신의 숫자 합이 21보다 크지만, " \
                             f"<b>{name['you']}</b>보다 숫자 합이 21에 가깝습니다."

                # 플레이어의 숫자 합이 더 큰 경우
                else:
                    win = False
                    reason = f"모든 플레이어의 숫자 합이 21보다 크지만, " \
                             f"<b>{name['you']}</b>(이)의 숫자 합이 21에 가깝습니다."
            else:
                # 플레이어의 숫자 합은 21을 넘었고,
                #   컴퓨터의 숫자 합은 21을 넘지 않았음
                win = False
                reason = "당신의 숫자 합이 21보다 큽니다."

        else:
            # 플레이어의 숫자 합은 21을 넘지 않았고,
            #   컴퓨터의 숫자 합은 21을 넘은 경우
            win = True
            reason = f"축하드립니다! <b>{name['you']}</b>(이)의 숫자 합이 21보다 큽니다."

    elif me < you:
        # 플레이어의 숫자 합이 컴퓨터 보다 작은 경우
        win = False
        reason = f"당신의 숫자 합이 <b>{name['you']}</b>(이)의 숫자 합 보다 작습니다."

    elif me > you:
        # 플레이어의 숫자 합이 컴퓨터 보다 큰 경우
        win = True
        reason = f"축하드립니다! <b>{name['you']}</b>(이) 보다 큰 숫자를 만들었습니다!"

    else:
        # 그 어떠한 승리 조건도 만족하지 못한 경우
        win = None
        reason = "* 승리/패배 조건이 올바르지 않습니다. *"

    return win, reason
