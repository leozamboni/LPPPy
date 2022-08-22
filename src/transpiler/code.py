from transpiler.token import TokenKeys, TokenTypes

# Alguns tokens não são armazenados no array final de tokens (self.tokens),
# no parser os tokens que são ignorados estão presentes no array 'ignore'.
# 
# Saber os tokens que são ignorados é necessários para iterar o array 'tokens'
# e dar saida (stdout) ao seu respectivo código em linguagem python.
class CodeGen:
  tokens  =   []
  index   =   0
  stdout  =   ''

  def run(self, tokens):
    self.tokens = tokens
    self.initialPipeline()

  def getDType(self, key, _keytype):
    match key:
      case 'caractere':             return "''" 
      case 'inteiro':               return "0" 
      case 'real':                  return "0.0" 
      case 'conjunto':    
        match _keytype:
          case TokenKeys.inteiro:   return "[0]" 
          case TokenKeys.caractere: return "['']" 
          case TokenKeys.real:      return "[0.0]" 
          case _:                   return "[]" 


  def initialPipeline(self):
    self.stdout   =   f'# programa {self.tokens[self.index].key}\n\n'
    self.stdout   +=  '# var\n'
    self.index    +=  1
    self.varBlock()

  def varBlock(self):
    while self.tokens[self.index].type != TokenTypes.inicio: 
      if (self.tokens[self.index + 1].key == TokenKeys.conjunto):
        self.stdout += f'{self.tokens[self.index].key} = {self.getDType(self.tokens[self.index + 1].key, self.tokens[self.index + 4].key)}\n'
        self.index  += 3

      elif (self.tokens[self.index + 1].key == TokenKeys.dot):
        contents = 1
        while True:
          self.stdout += self.tokens[self.index].key
          if (self.tokens[self.index + 1].type == TokenTypes.dType): 
            self.index  +=  1
            break
          else: 
            contents    +=  1
            self.stdout +=  ', '
            self.index  +=  2
        
        if (self.tokens[self.index].key == TokenKeys.conjunto):
          self.stdout += " = "
          for x in range (0, contents):
            self.stdout += f"{self.getDType(self.tokens[self.index].key, self.tokens[self.index + 3].key)}"
            if (x < contents - 1): self.stdout += ', '
          self.stdout += "\n"
          self.index  +=  2
          
        else:
          self.stdout += " = "
          for x in range (0, contents):
            self.stdout += f"{self.getDType(self.tokens[self.index].key, None)}"
            if (x < contents - 1): self.stdout += ', '
          self.stdout += "\n"
          self.index  -=  1

      else: 
        self.stdout += f'{self.tokens[self.index].key} = {self.getDType(self.tokens[self.index + 1].key, None)}\n'
      self.index  += 2
    
    self.inicioBlock()

  def inicioBlock(self):
    self.stdout   +=  '\n# início\n'
    self.index    += 1
    token         = self.tokens[self.index]
    match token.type:
      case TokenTypes.fim: self.stdout += '\n# fim\n'