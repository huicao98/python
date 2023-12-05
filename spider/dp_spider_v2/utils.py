import re

def sanitize_cost(text:str):
        if text:
            text=sanitize_text(text)
            text = text.replace('¥','')
            text = text.replace('￥','')
            text = text.replace('消费：', '')
            text = text.replace('消费:','')
            text = text.replace('元', '')
            text = text.replace('人均','')
            text = text.replace('/人','')
            text = text.replace('-','')
            if text=='':
                text = '0'
            
        return text

def sanitize_text(text: str):
        if text:
            text = text.strip()
            # 处理字符串混入html标签
            regex = re.compile(
                r'<(div|span|td)\s*[\w"=\.-]*>[\w\s=+/]*</(div|span|td)\s*\w*>')
            return regex.sub('', text)
        return text
