from llm.extractor import Extractor

extractor=Extractor()
result=extractor.extract(input())
print()
print("topics: ",result["topics"])
print("entities: ",result["entities"])
print("summary: ",result["summary"])
print("takeaway: ",result["takeaway"])
print("response: ",result["response"])
print()