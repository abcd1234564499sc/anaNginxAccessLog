# anaNginxAccessLog
 分析nginx access log，并存储为excell格式  
 使用正则表达式解析nginx日志类型，并使用openpyxl库写入excell    
 解析后的表头为：["源IP", "客户端用户名1", "客户端用户名2", "访问时间", "请求类型", "请求地址(URI)", "协议版本", "响应码", "请求包大小", "数据", "refer信息", "user-agent"]    
 使用方法：   
 1、修改anaNginxLog.py 中 logFiles数组，将需要分析的文件的路径写入，支持绝对路径和相对路径   
 2、使用requirements.txt安装需要库    
 3、使用python anaNginxLog.py 运行
     
 PS：可以使用项目中venv的site-packages运行项目，方法是修改venv/pyvenv.cfg 中配置，将本机python安装路径写入，然后windows可以使用项目中run.bat运行，linux可以参照run.bat进行修改    

