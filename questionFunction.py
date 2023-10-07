import json




class TDquestions():
    def __init__(self, generalPath='generalQ.json', enthalpyPath='enthalpyQ.json', CpPath='CpQ.json', entropyPath=None, freeEnergyPath=None):
        self.generalQuestionPath = generalPath
        self.enthalpyQuestionPath = enthalpyPath
        self.CpQuestionPath = CpPath
        self.entropyQuestionPath = entropyPath
        self.freeEnergyPath = freeEnergyPath
    
    def generalQuestion(self):
        with open(self.generalQuestionPath, 'r', encoding='utf-8') as f:
            generalQList = json.load(f)
        
        return generalQList
    
    def enthalpyQuestion(self):
        with open(self.enthalpyQuestionPath, 'r', encoding='utf-8') as f:
            enthalpyQList = json.load(f)
        
        return enthalpyQList
    
    def CpQuestion(self):
        with open(self.CpQuestionPath, 'r', encoding='utf-8') as f:
            CpQList = json.load(f)
        
        return CpQList
    
    # def entrolpyQuestion(self):
    #     with open(self.enthalpyQuestionPath, 'r', encoding='utf-8') as f:
    #         entrolpyQList = json.load(f)
        
    #     return entrolpyQList
    
    # def freeEnergyQuestion(self):
    #     with open(self.freeEnergyQuestion, 'r', encoding='utf-8') as f:
    #         freeEnergyQList = json.load(f)
        
    #     return freeEnergyQList


if __name__ == "__main__":
    questions = TDquestions()
    print(questions.CpQuestion())


