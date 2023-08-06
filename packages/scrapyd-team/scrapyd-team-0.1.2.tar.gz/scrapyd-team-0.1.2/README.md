# Scrapyd

## 版本变动 v 0.1.1 2022/7/11

* 将缓存区解包egg文件加入到环境变量XDG_CONFIG_HOME,scrapy项目能正常引用scrapy.cfg中配置
* 对于scrapy项目中非py文件,如xlsx文件在程序中引用,请取os.environ["XDG_CONFIG_HOME"]位置作为项目根目录
   * 例:
   ```
   # win
   with open(os.environ["XDG_CONFIG_HOME"]+'\\readme.txt',encoding = "utf-8") as f:
      read_content = f.read()
   ```