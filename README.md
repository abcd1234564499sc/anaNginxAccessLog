# anaNginxAccessLog
 分析nginx access log，并存储为excell格式  
 使用正则表达式解析nginx日志类型，并使用openpyxl库写入excell    
 解析后的表头为：["源IP", "客户端用户名1", "客户端用户名2", "访问时间", "请求类型", "请求地址(URI)", "响应码", "请求包大小", "数据", "refer信息", "user-agent"]    
 使用的正则表达式为：r'(?P<ip>.*?) (?P<username1>.*?) (?P<username2>.*?) \[(?P<time>.*?)\] "(?P<reqtype>.*?)[ ]*(?P<request>.*?)" (?P<status>.*?) (?P<bytes>.*?) (?P<data>.*?) "(?P<referer>.*?)" "(?P<ua>.*?)"')
