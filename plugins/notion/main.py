from typing import Any
from libs.env import notion_env
from notion_database.page import Page
from notion_database.properties import Properties
from notion_database.const.query import Direction, Timestamp
from notion_database.search import Search

async def notion_post(table:str, params:dict[str,list[str,Any]]): # Функция загрузки новых данных в Notion
    D = Search(integrations_token=notion_env.token)
    D.search_database(query=table, sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})
    print(D.result)
    for i in D.result:
        PROPERTY = Properties()
        for key,value in params.items():
            if key == 'title':
                PROPERTY.set_title("title", value[1])
            else:
                if value[0] == 'text':
                    PROPERTY.set_rich_text(key, value[1])
                if value[0] == 'number':
                    PROPERTY.set_number(key,value[1])
                if value[0] == 'checkbox':
                    PROPERTY.set_checkbox(key,value[1])
        
        P = Page(integrations_token=notion_env.token)
        P.create_page(database_id=i["id"], properties=PROPERTY)


async def notion_update(table:str,id:str,params:dict[str,list[str,Any]]): # Функция обновления данных в Notion
    D = Search(integrations_token=notion_env.token)
    D.search_database(query=table, sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})
    PROPERTY = Properties()
    for key,value in params.items():
        if key == 'title':
            PROPERTY.set_title("title", value[1])
        else:
            if value[0] == 'text':
                PROPERTY.set_rich_text(key, value[1])
            if value[0] == 'number':
                PROPERTY.set_number(key,value[1])
            if value[0] == 'checkbox':
                PROPERTY.set_checkbox(key,value[1])
    
    P = Page(integrations_token=notion_env.token)
    D.search_pages(query=id, sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})
    print(D.result)
    P.update_page(D.result['results'][0]['url'].split('-')[1],properties=PROPERTY)
        

async def notion_get(table:str,id:str,params:list): # Функция для получения данных в Notion
    D = Search(integrations_token=notion_env.token)
    D.search_database(query=table, sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})
    result = {}
    D.search_pages(query=id, sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})
    P = Page(integrations_token=notion_env.token)
    print(D.result)
    P.retrieve_page(D.result['results'][0]['url'].split('-')[1])
    for value in params:
        get_type = P.result['properties'][value]['type']
        get_value = P.result['properties'][value][get_type]
        result.update({value:[get_type, get_value]})
    
    return result