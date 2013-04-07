import __main__
from naoqi import ALModule as _ALModule

class ALModule(_ALModule):
    '''
    Wrap the original ALModule.
    Store the module in the globals directly.
    So you don't have to care about the rule 
    "The name given in the constructor must be the same as the variable name, which must be global".
    
    Just instanciate your module the way you want!
    '''
    def __init__(self, moduleName):
        moduleName = str(moduleName)
        _ALModule.__init__(self, moduleName)
        setattr(__main__, moduleName, self)
