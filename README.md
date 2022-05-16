# anaNginxAccessLog
 分析nginx access log，并存储为excell格式  
 使用正则表达式解析nginx日志类型，并使用openpyxl库写入excell    
 解析后的表头为：["源IP", "客户端用户名1", "客户端用户名2", "访问时间", "请求类型", "请求地址(URI)", "协议版本", "响应码", "请求包大小", "数据", "refer信息", "user-agent"]    
 使用方法：修改anaNginxLog.py 中 logFiles数组，将需要分析的文件的路径写入，支持绝对路径和相对路径    
 windows系统可以使用run.bat，会自动使用venv中的包运行，无需额外安装包，linux需要根据venv中linux对应脚本进行修改    

