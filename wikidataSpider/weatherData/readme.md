## 互动百科页面爬取

* Citydata.py: 得到城市(市级)列表、城市气候等信息
* City.json:城市(市级)json
* City_weather.csv: 城市对应的气候
* Static_weather_list.csv: 筛选过的气候名称
* Weather2weather.txt: 气候名称到“有百科页面的气候名称”的映射
* weatherCrawler.py :获取weather.txt中指定气候的页面
* Weather_plant.csv: 气候和植物的对应关系



#### 将气候名称和适合种植的植物导入到neo4j

* 导入气候名称:

  将static_weather_list.csv放在指定的位置(import文件夹下)

  ```
  //导入节点
  LOAD CSV WITH HEADERS FROM "file:///static_weather_list.csv" AS line
  MERGE (:Weather { title: line.title })
  
  //添加索引
  CREATE CONSTRAINT ON (c:Weather)
  ASSERT c.title IS UNIQUE
  ```


* 导入气候与植物的关系

  将weather_plant.csv放在指定的位置(import文件夹下)

  ```
  //导入hudongItem和新加入节点之间的关系
  LOAD CSV  WITH HEADERS FROM "file:///weather_plant.csv" AS line
  MATCH (entity1:Weather{title:line.Weather}) , (entity2:HudongItem{title:line.Plant})
  CREATE (entity1)-[:Weather2Plant { type: line.relation }]->(entity2)
  ```

* 导入城市的气候

  将city_weather.csv放在指定的位置(import 文件夹下)

  ```
  //导入城市对应的气候
  LOAD CSV WITH HEADERS FROM "file:///city_weather.csv" AS line
  MATCH (city{title:line.city}) , (weather{title:line.weather})
  CREATE (city)-[:CityWeather { type: line.relation }]->(weather)
  ```


