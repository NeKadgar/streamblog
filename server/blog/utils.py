from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.utils import timezone



def unique_slugify(title):
    slug = slugify(unidecode(title))
    return "{}-{}".format(slug, timezone.now().strftime("%j%H%M%S%f"))


def convert_editorjs_to_html(json):
    html = ""
    for block in json["blocks"]:
        if block["type"] == "paragraph":
            html += "<p class='ce-paragraph cdx-block'>{}</p>".format(block["data"]["text"])
        elif block["type"] == "header":
            html += "<h{0} class='ce-header'>{1}</h{0}>".format(block["data"]["level"], block["data"]["text"])
        elif block["type"] == "list":
            html += "<ul class='cdx-block cdx-list cdx-list--{}'>".format(block["data"]["style"])
            for item in block["data"]["items"]:
                html += "<li class='cdx-list__item'>{}</li>".format(item)
            html += "</ul>"
        elif block["type"] == "delimiter":
            html += "<div class='ce-delimiter cdx-block'></div>"
        elif block["type"] == "warning":
            html += "<div class='cdx-block cdx-warning'>" \
                    "<div class='cdx-input cdx-warning__title'>{}</div>" \
                    "<div class='cdx-input cdx-warning__message'>{}</div>" \
                    "</div>".format(block["data"]["title"], block["data"]["message"])
        elif block["type"] == "quote":
            html += "<blockquote class='cdx-block cdx-quote' style='text-align: {}'>" \
                    "<div class='cdx-input cdx-quote__text'>{}</div>" \
                    "<div class='cdx-input cdx-quote__caption'>{}</div>" \
                    "</blockquote>".format(block["data"]["alignment"], block["data"]["text"], block["data"]["caption"])
        elif block["type"] == "codeBox":
            html += "<div class='codeBoxTextArea hljs'>{}</div>".format(block["data"]["code"])
        elif block["type"] == "image":
            try:
                image_url = block["data"]["file"]["url"]
            except:
                image_url = "https://www.ledr.com/colours/grey.jpg"
            html += "<div class='cdx-block image-tool image-tool--filled {} {} {}'>" \
                    "<div class='image-tool__image'>" \
                    "<img class='image-tool__image-picture' src='{}'>" \
                    "</div>" \
                    "<div class='cdx-input image-tool__caption'>{}</div>" \
                    "</div>"\
                    .format(
                        "image-tool--withBackground" if block["data"]["withBackground"] else "",
                        "image-tool--stretched" if block["data"]["stretched"] else "",
                        "image-tool--withBorder" if block["data"]["withBorder"] else "",
                        image_url,
                        block["data"]["caption"]
                    )

    return html


def get_presave_info(content):
    print(content)
    return 1,2


def get_tags():
    pass