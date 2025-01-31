import json




class TDquestions():
    def __init__(self, generalPath='generalQ.json', enthalpyPath='enthalpyQ.json', CpPath='CpQ.json', entropyPath='entropyQ.json', freeEnergyPath='freeEnergyQ.json'):
        self.generalQuestionPath = generalPath
        self.enthalpyQuestionPath = enthalpyPath
        self.CpQuestionPath = CpPath
        self.entropyQuestionPath = entropyPath
        self.freeEnergyPath = freeEnergyPath
    
    # def generalQuestion(self):
    #     with open(self.generalQuestionPath, 'r', encoding='utf-8') as f:
    #         generalQList = json.load(f)
        
    #     return generalQList
    
    # def enthalpyQuestion(self):
    #     with open(self.enthalpyQuestionPath, 'r', encoding='utf-8') as f:
    #         enthalpyQList = json.load(f)
        
    #     return enthalpyQList
    
    # def CpQuestion(self):
    #     with open(self.CpQuestionPath, 'r', encoding='utf-8') as f:
    #         CpQList = json.load(f)
        
    #     return CpQList
    
    def entropyQuestion(self):
        with open(self.entropyQuestionPath, 'r', encoding='utf-8') as f:
            entropyQList = json.load(f)
        
        return entropyQList
    
    # def freeEnergyQuestion(self):
    #     with open(self.freeEnergyPath, 'r', encoding='utf-8') as f:
    #         freeEnergyQList = json.load(f)
        
    #     return freeEnergyQList


if __name__ == "__main__":
    questions = TDquestions()
    print(questions.CpQuestion())


