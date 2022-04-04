from linebot.models import (
    FlexSendMessage,
    CarouselContainer,
    BubbleContainer,
    BoxComponent,
    ImageComponent,
    TextComponent,
    ButtonComponent,
    URIAction,
)


def generate_carousels(column):
    """
    column_template = {"img_url": "", "title": "", "text": "", "url": "", date:"}
    """

    columns = []
    for i in range(len(column)):
        # 최대 생성 갯수 설정(최대 12개)
        if i > 12:
            break

        # LINE 템플릿 상의 글자수 제한 :  제목 40자, 내용 60자
        # title = str(column[i]["title"][:39])
        title = str(column[i]["title"])
        # text = str(column[i]["text"][:59])
        text = str(column[i]["text"])
        image_url = str(column[i]["img_url"])
        url = str(column[i]["url"])
        date = "date here"
        bubble = BubbleContainer(
            hero=ImageComponent(
                url=image_url,
                size="full",
                aspect_ratio="16:9",
                aspect_mode="cover",
                action=URIAction(uri=url, label="label"),
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    # title
                    TextComponent(text=title, weight="bold", size="lg", wrap=True),
                    # review
                    BoxComponent(
                        layout="baseline",
                        margin="lg",
                        spacing="sm",
                        contents=[
                            # text
                            TextComponent(text=text, wrap=True)
                        ],
                    ),
                    # date
                    BoxComponent(
                        layout="baseline",
                        margin="md",
                        contents=[
                            TextComponent(
                                text=date,
                                wrap=True,
                                color="#9a9a9a",
                                size="xs",
                                flex=5,
                            ),
                        ],
                    ),
                ],
            ),
            footer=BoxComponent(
                layout="vertical",
                spacing="sm",
                color="#ffffff",
                flex="0",
                background_color="#42659a",
                contents=[
                    # callAction
                    ButtonComponent(
                        style="link",
                        height="sm",
                        action=URIAction(label="본문 읽기", uri=url),
                    ),
                ],
            ),
        )

        columns.append(bubble)

    return FlexSendMessage(
        alt_text="test",
        contents=CarouselContainer(columns),
    )


# # test data
# test_column = [
#     {
#         "img_url": "https://static.ff14.co.kr/Contents/2022/02/591B8BD37B5A73AC598DCFC8BBF39EB773E6120AB3432BFD3D40F5B1103B054B.png",
#         "title": "title1",
#         "text": "text",
#         "url": "https://linecorp.com",
#         "date": "03/16 ~ 12/31",
#     },
#     {
#         "img_url": "https://static.ff14.co.kr/Contents/2022/02/591B8BD37B5A73AC598DCFC8BBF39EB773E6120AB3432BFD3D40F5B1103B054B.png",
#         "title": "title2",
#         "text": "text",
#         "url": "https://linecorp.com",
#         "date": "03/16 ~ 12/31",
#     },
# ]

# message = generate_carousels(test_column)
# print(message)
