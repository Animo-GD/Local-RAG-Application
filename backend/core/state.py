from typing import Literal,Dict,TypedDict,List

class GraphState(TypedDict):
    question:str
    query_type: Literal["document","sql","general"]
    context:str
    sql_query:str
    sql_result:List[Dict]
    answer:str
    error:str
    metadata:Dict