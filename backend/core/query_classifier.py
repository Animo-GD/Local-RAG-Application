import dspy

class QueryClassifier(dspy.Signature):
    """Classify user query into SQL, Document, or General Categories based on intent"""
    question = dspy.InputField(desc="User's question")
    available_tables=dspy.InputField(desc="List of avaliable database tables")
    available_documents=dspy.InputField(desc="List of available document titles")

    query_type = dspy.OutputField(
        desc = "Classification: 'sql' for database queires, 'document' fo document-based questions, 'genera' for other questions"
    )
    confidence = dspy.OutputField(desc="Confidence score between 0 and 1")
    reasoning = dspy.OutputField(desc="Breif explaination of classification")

class SmartQueryClassifier(dspy.Module):
    def __init__(self, callbacks=None):
        super().__init__(callbacks)
        self.classifier = dspy.ChainOfThought(QueryClassifier)

    def forward(self,question:str,tables:list[str],documents:list[str]):
        result = self.classifier(
            question=question,
            available_tables=", ".join(tables) if tables else "None",
            available_documents=", ".join(documents) if documents else "None"
        )
        query_type = result.query_type.lower().strip()
        if query_type not in ['sql','document','general']:
            query_type = 'general'
        return {
            "query_type":query_type,
            "confidence":float(result.confidence) if result.confidence else 0.8,
            "reasoning": result.reasoning,
        }