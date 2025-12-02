from typing import Literal,Dict,TypedDict

class GraphState(TypedDict):
    question:str
    query_type: Literal["document","sql","general"]
    context:str
    sql_query:str
    sql_result:str
    answer:str
    error:str
    metadata:Dict