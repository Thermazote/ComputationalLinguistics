1. exploring site: https://v102.ru/
2. design database
DB fields:
-name
-date
-link
-text
-video link (opt)
-views count (opt)
-replies count (opt)
3. design parser
4. upgrade with parse period control: if article exist in DB (check "name", "date", "link"), then only update "views count" and "replies count"
5. creating web-UI (django?)
