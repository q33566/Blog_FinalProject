import markdown
import nh3
from markupsafe import Markup

ALLOWED_TAGS = {
    'h2', 'h3', 'h4', 'p', 'br', 'hr', 'strong', 'em', 'del', 'blockquote',
    'ul', 'ol', 'li', 'a', 'code', 'pre', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
}


def render_markdown(text):
    """把文章的 Markdown 轉成 HTML，並用白名單清掉 script、事件屬性等危險內容。"""
    html = markdown.markdown(text, extensions=['fenced_code', 'tables'])
    clean = nh3.clean(html, tags=ALLOWED_TAGS,
                      attributes={'a': {'href', 'title'}, 'code': {'class'}},
                      url_schemes={'http', 'https', 'mailto'})
    return Markup(clean)


def zh_date(value):
    return f'{value.year} 年 {value.month} 月 {value.day} 日'
