class Imageclass():
    def __init__(self,name):
        self.id = id
        self.name = name
        self.prediction = ""
        self.approved = False
        self.newlabel = ""
        self.counter = 0

    def nameImage(self, filepath,counter):
        self.name = filepath
        self.id = counter
    
    def labelImage(self, prediction):
        self.prediction = prediction
    
    
    def approved(self, approved):
        self.approved = approved
        self.newlabel = self.prediction


    def newLabel(self, newlabel):
         self.newlabel = newlabel
         self.approved = False
         