from SymbolTable import SymbolTable

class Context:
    def __init__(self, identifier: str, parent=None):
        self.identifier = identifier
        self.symbol_table = SymbolTable()
        self.context_counter = 0
        self.current_context_counter = 0
        self.subcontexts = [] 
        self.parent = parent 
        self.nature = None

    def add_subcontext(self, subcontext_name: str):
        new_subcontext = Context(subcontext_name, parent=self)
        self.context_counter += 1
        self.subcontexts.append(new_subcontext)
        return new_subcontext

    def get_subcontext(self, identifier: str):
        for sub in self.subcontexts:
            if identifier in sub.identifier:
                return sub
        return None

    def add_symbol(self, id_name: str, linha: int, coluna: int):
        idIdx = self.symbol_table.findIdIdx(id_name)
        
        if(idIdx == None):
            return self.symbol_table.add(id_name, linha, coluna)
        else:
            return idIdx
    
    def lookup(self, id_name: str):
        idx = self.symbol_table.lookup(id_name)
        if idx is not None:
            return self, idx  # Retorna o contexto e o índice do símbolo
        if self.parent:
            return self.parent.lookup(id_name)  # Busca no contexto pai
        return None, None  # Não encontrado na hierarquia

    def list_symbols(self):
        print(f"Contexto: {self.identifier}")
        self.symbol_table.list()
        
        for subcontext in self.subcontexts:
            subcontext.list_symbols()
            
    def generate_unique_name(self, base_name):
      unique_name = f"{self.context_counter}_{base_name}"
      return unique_name
  
    def context_hierarchy(self, context, depth=0):
        indent = "    " * depth
        print(f"{indent} -> {context.identifier}")
        for subcontext in context.subcontexts:
            self.context_hierarchy(subcontext, depth + 1)