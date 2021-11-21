from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    TemplateSendMessage,
)


def generate_carousels(column):
    """
    column_template = {"img_url": "", "title": "", "text": "", "url": ""}
    """

    columns = []
    for i in range(len(column)):
        # 최대 생성 갯수 설정(현재 5개)
        if i > 4:
            break

        # LINE 템플릿 상의 글자수 제한 :  제목 40자, 내용 60자
        title = column[i]["title"][:39]
        text = column[i]["text"][:59]
        columns.append(
            CarouselColumn(
                thumbnail_image_url=str(column[i]["img_url"]),
                title=str(title),
                text=str(text),
                actions=[
                    {
                        "type": "uri",
                        "label": "전체 읽기",
                        "uri": column[i]["url"],
                    },
                ],
            )
        )

    return TemplateSendMessage(
        alt_text="PC 미지원 양식입니다.",
        template=CarouselTemplate(columns=columns, image_size="contain"),
    )
