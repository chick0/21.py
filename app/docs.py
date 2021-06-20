class Docs:
    def __init__(self, title: str, content: list):
        self.title = title
        self.content = content

    def __repr__(self):
        return f"<Docs title={self.title!r}>"


document = [
    Docs(
        title="규칙 설명",
        content=[
            "<b>Hit</b> 버튼을 누르면 새로운 카드를 한 장 받습니다.",
            "<b>Stand</b> 버튼을 누르면 더 이상 카드를 받지 않으며 게임이 종료됩니다.",
            "",
            "플레이어의 카드의 숫자 합은 <b>21</b>이 넘으면 안되고,",
            "상대방 보다 카드의 숫자 합이 <b>21</b>에 가까워야 합니다.",
            "",
            "승/패 처리는 다음과 같은 순서대로 진행됩니다.",
            "\t1) 플레이어의 숫자 합이 21인지 확인",
            "\t2) 상대 플레이어의 숫자 합이 21인지 확인",
            "\t3) 플레이어의 숫자 합이 21보다 큰지 확인",
            "\t4) 상대 플레이어의 숫자 합이 21보다 큰지 확인",
            "\t5) 상대 플레이어의 숫자 합이 더 큰지 확인",
            "\t6) 플레이어의 숫자 합이 더 큰지 확인",
            "\t7) 1~6중에 포함되는 상황이 없으므로 무승부",
        ]
    )
]
