from copy import deepcopy
from sympy import *


KNOWLEDGEBASE = [
            #R1
            #If there is a wumpus at square(i,j) there is a stench at all adjacent squares
            "W12<=>S11^S22^S13",
            "W13<=>S12^S23^S14",
            "W14<=>S13^S24",
            "W21<=>S11^S22^S31",
            "W22<=>S12^S23^S32^S21",
            "W23<=>S22^S13^S24^S33",
            "W24<=>S14^S23^S34",
            "W31<=>S21^S32^S41",
            "W32<=>S31^S22^S33^S42",
            "W33<=>S32^S23^S34^S43",
            "W34<=>S33^S24^S44",
            "W41<=>S31^S42",
            "W42<=>S41^S32^S43",
            "W43<=>S42^S33^S44",
            "W44<=>S43^S34",

            #R2
            #If there is a pit at square (i,j) there is a breeze at all adjacent squares
            "P11<=>B12^B21",
            "P12<=>B11^B22^B13",
            "P13<=>B12^B23^B14",
            "P14<=>B13^B24",
            "P21<=>B11^B22^B31",
            "P22<=>B12^B23^B21^B32",
            "P23<=>B13^B22^B24^B33",
            "P24<=>B14^B23^B34",
            "P31<=>B21^B32^B41",
            "P32<=>B31^B22^B33^B42",
            "P33<=>B23^B32^B34^B43",
            "P34<=>B24^B33^B44",
            "P41<=>B31^B42",
            "P42<=>B41^B32^B43",
            "P43<=>B33^B42^B44",
            "P44<=>B34^B43",

            #R3
            #if there is a breeze at square(i,j) there is a pit at one or more of the adjacent squares
            "B11<=>P12vP21",
            "B12<=>P11vP22vP13",
            "B13<=>P12vP23vP14",
            "B14<=>P13vP24",
            "B21<=>P11vP22vP31",
            "B22<=>P12vP23vP21vP32",
            "B23<=>P13vP22vP24vP33",
            "B24<=>P14vP23vP34",
            "B31<=>P21vP32vP41",
            "B32<=>P31vP22vP33vP42",
            "B33<=>P23vP32vP34vP43",
            "B34<=>P24vP33vP44",
            "B41<=>P31vP42",
            "B42<=>P41vP32vP43",
            "B43<=>P33vP42vP44",
            "B44<=>P34vP43",

            #R4
            "S11<=>W12vW21",
            "S12<=>W11vW22vW13",
            "S13<=>W12vW23vW14",
            "S14<=>W13vW24",
            "S21<=>W11vW22vW31",
            "S22<=>W12vW23vW21vW32",
            "S23<=>W13vW22vW24vW33",
            "S24<=>W14vW23vW34",
            "S31<=>W21vW32vW41",
            "S32<=>W31vW22vW33vW42",
            "S33<=>W23vW32vW34vW43",
            "S34<=>W24vW33vW44",
            "S41<=>W31vW42",
            "S42<=>W41vW32vW43",
            "S43<=>W33vW42vW44",
            "S44<=>W34vW43",

            #There is only one wumpus
            "W11vW12vW13vW14vW21vW22vW23vW24vW31vW32vW33vW34vW41vW42vW43vW44",
            "-W11v-W12", 
            "-W11v-W13",
            "-W11v-W14",
            "-W12v-W13",
            "-W12v-W14",
            "-W13v-W14",
            "-W21v-W22",
            "-W21v-W23",
            "-W21v-W24",
            "-W22v-W23",
            "-W22v-W24",
            "-W23v-W24",
            "-W31v-W32",
            "-W31v-W33",
            "-W31v-W34",
            "-W32v-W33",
            "-W32v-W34",
            "-W33v-W34",
            "-W41v-W42",
            "-W41v-W43",
            "-W41v-W44",
            "-W42v-W43",
            "-W42v-W44",
            "-W43v-W44",
]


class KnowledgebasedAgent:
    """Testmodel to check propositional logic"""
    test_model = {
        "P11":False , "P12":False, "P13": False, "P14":False,
        "P21":False , "P22":False, "P23": False, "P24":False,
        "P31":False , "P32":False, "P33": False, "P34":False,
        "P41":False , "P42":False, "P43": False, "P44":False,
        "S11":False , "S12":False, "S13": False, "S14":False,
        "S21":False , "S22":False, "S23": False, "S24":False,
        "S31":False , "S32":False, "S33": False, "S34":False,
        "S41":False , "S42":False, "S43": False, "S44":False,
        "B11":False , "B12":False, "B13": False, "B14":False,
        "B21":False , "B22":False, "B23": False, "B24":False,
        "B31":False , "B32":False, "B33": False, "B34":False,
        "B41":False , "B42":False, "B43": False, "B44":False,
        "G11":False , "G12":False, "G13": False, "G14":False,
        "G21":False , "G22":False, "G23": False, "G24":False,
        "G31":False , "G32":False, "G33": False, "G34":False,
        "G41":False , "G42":False, "G43": False, "G44":False,
        "false":False, "true":True, "T":True, "F": False
    }

    def __init__(self, Algo):

        self.Algo = Algo
    
        #Setting initial ruleset from chapter 7.4.3 with a few additions
        self.knowledgebase = KNOWLEDGEBASE
        #self.knowledgebase = []
        
    
    def NonAdj(self, i, j ,Adj):
        """Function to update adjacent fields"""
        #Decide opposite Piece
        opp = ""
        if Adj == "-S":
            opp = "-W"
        elif Adj == "-B": 
            opp = "-P"

        right = "false"
        left = "false"       
        top ="false"
        down= "false"

        fields = []

        if i+1 <4:
            i+=1
            right= f"{opp}{i}{j}"
            fields.append(right)
            i-=1
        if i-1 >0:
            i-=1
            left = f"{opp}{i}{j}"
            fields.append(left)
            i+=1
        if j+1 <4:
            j+=1
            top= f"{opp}{i}{j}"
            fields.append(top)
            j-=1
        if j-1 >0:
            j-=1
            down = f"{opp}{i}{j}"
            fields.append(down)
            j+=1
        #Example: A Field has a breeze if there is a pit on any of the adjacent fields
        conclusion = "^".join(fields)
        self.knowledgebase.append(f"{Adj}{i}{j}<=>{conclusion}")

    def Adj(self, i,j, Adj):
        """Function to update adjacent fields"""
        #Decide opposite Piece
        opp = ""
        if Adj == "S":
            opp = "W"
        elif Adj == "B": 
            opp = "P"

        right = "false"
        left = "false"       
        top ="false"
        down= "false"

        fields = []

        if i+1 <4:
            i+=1
            right= f"{opp}{i}{j}"
            fields.append(right)
            i-=1
        if i-1 >0:
            i-=1
            left = f"{opp}{i}{j}"
            fields.append(left)
            i+=1
        if j+1 <4:
            j+=1
            top= f"{opp}{i}{j}"
            fields.append(top)
            j-=1
        if j-1 >0:
            j-=1
            down = f"{opp}{i}{j}"
            fields.append(down)
            j+=1
        #Example: A Field has a breeze if there is a pit on any of the adjacent fields
        conclusion = "v".join(fields)
        self.knowledgebase.append(f"{Adj}{i}{j}<=>{conclusion}")

    def TELL(self, percept):
        """Tells the knowledgebase what the agent percepts"""

        #Example Perception: 
        #{'x': 1, 'y': 2, 'gold': False, 'direction': <Direction.EAST: 1>, 'arrow': False, 'stench': False, 'breeze': False, 'glitter': False, 'bump': False, 'scream': False}
        
        x = percept['x'] + 1  #Use + 1 because gymlibrary starts with 0
        y = percept['y'] + 1 

        #If the agent is still alive at this point there is no pit or wumpus here
        self.knowledgebase.append(f"-W{x}{y}")
        self.knowledgebase.append(f"-P{x}{y}")


        #Update stench
        if percept['stench']:
            self.knowledgebase.append(f"S{x}{y}")
            self.Adj(x,y, "S")
        else:
            self.knowledgebase.append(f"-S{x}{y}")
            self.NonAdj(x,y, "-S")

        if percept['breeze']:
            self.knowledgebase.append(f"B{x}{y}")
            self.Adj(x,y, "B")
        else:
            self.knowledgebase.append(f"-B{x}{y}")
            self.NonAdj(x,y, "-B")
        self.knowledgebase = list(set(self.knowledgebase))

    def ASK(self,query):
        if self.Algo == "TTL-ENTAILS?":
            print(f"({self.Algo}): Does KB |= {query}? ", self.TT_ENTAILS(self.knowledgebase, query))
        elif self.Algo == "FC":
            print(f"({self.Algo}): Does KB |= {query}? ", self.PL_FC_ENTAILS(self.knowledgebase ,query))
        elif self.Algo == "RESOLUTION":
            print(f"({self.Algo}): Does KB |= {query}? ", self.PL_RESOLUTION(self.knowledgebase, query))
        


    def logical_xor(self, expression, model):
        """logical xor: xor """
        terms = expression.split("xor")
        truth_list = []
        for term in terms:
            truth_list.append(self.atomic_evaluation(term, model))
        
        out = truth_list[0]
        for i in range(1, len(truth_list)):
            out = out ^ truth_list[i]
        
        return out


    def logical_and(self, expression, model):
        """logical and: ^ """
        terms = expression.split("^")
        truth_list = []
        for term in terms:
            truth_list.append(self.atomic_evaluation(term, model))
        
        if(len(set(truth_list))==1 and truth_list[0]==True):
            return True
        return False;
    
    def logical_or(self, expression, model):
        """logical or: v """
        terms = expression.split("v")
        for term in terms:
            if "^" in term:
                val = self.logical_and(term)
            elif "xor" in term:
                val = self.logical_xor(term)
            else:
                val = self.atomic_evaluation(term, model)
            if val:
                return True
        return False
    
    def logical_implication(self, expression, model):
        """logical implication: => """
        terms = expression.split("=>")
        # p=>q is the same as not(p) or q
        if len(terms)!=2:
            raise ValueError
        p = terms[0]
        q = terms[1]
        
        return (not self.PL_TRUE(p, model) or self.PL_TRUE(q, model))

    def logical_biconditional(self, expression, model):
        """logical biconditional: <=> """
        terms = expression.split("<=>")
        # p<=>q is the same as  p=>q and q=>p
        if len(terms)!=2:
            raise ValueError
        p = terms[0]
        q = terms[1]
        return self.PL_TRUE(p, model) == self.PL_TRUE(q,model) 

    def atomic_evaluation(self, expression, model):
        """Evaluate atomic proposition """
        if expression[0] == "-":
            return not self.atomic_evaluation(expression[1:], model)

        if expression in model:   
            return model[expression]
        return False

    def PL_TRUE(self, expression, model):
        """Propositional term evaluation"""
        if "<=>" in expression:
            return self.logical_biconditional(expression, model)
        elif "=>" in expression:
            return self.logical_implication(expression, model)
        elif "^" in expression:
            return self.logical_and(expression, model)    
        elif "v" in expression:
            return self.logical_or(expression, model)
        elif "xor" in expression:
            return self.logical_xor(expression, model)
        return self.atomic_evaluation(expression, model)
    
    def get_symbols_from_sentence(self, sentence):
        """Only get symbols from  sentence.
           A^B^C -> [A, B, C]
        """
        sentence = sentence.replace("-", "")
        sentence = sentence.replace("^", "#")
        sentence = sentence.replace("<=>", "#")
        sentence = sentence.replace("=>", "#")
        sentence = sentence.replace("v", "#")
        sentence = sentence.replace("xor", "#")

        return sentence.split("#")

    
    def removeall(self,item,seq):
        """Utility function to remove instance from a sequence"""
        if isinstance(seq, str):
            return seq.replace(item, '')
        else:
            return [x for x in seq if x != item]

    def get_symbols(self, knowledgebase):
        """Return All unique symbols of a knowledgebase"""
        symbols = []
        for sentence in knowledgebase:
            symbols.extend(self.get_symbols_from_sentence(sentence))
        return sorted(list(set(symbols)))

    def extend_model(self, model, var, val):
        """Adds a key value pair to the model"""
        extended_model = model.copy()
        extended_model[var] = val
        return extended_model 

    #Returns True if all the rules within a knowledgebase apply
    def PL_TRUE_KNOWLEDGEBASE(self, sentences, model):
        """Evaluates if all sentences in the model are true"""
        truth_list= []
        for sentence in sentences:
            truth_list.append(self.PL_TRUE(sentence, model))      
      
        if(len(set(truth_list))==1 and truth_list[0]==True):
            return True
        return False;

    def TT_ENTAILS(self, knowledgebase, alpha):
        """Algorithm to determine if the current knowledgebase entails alpha"""
        symbols = self.get_symbols(knowledgebase)
        return self.TT_CHECK_ALL(knowledgebase, alpha, symbols,{})

    def TT_CHECK_ALL(self, knowledgebase, alpha,symbols,model):
        """Recursive Function that is used in TT_ENTAIL to check inferences"""
        if len(symbols) == 0:
            if self.PL_TRUE_KNOWLEDGEBASE(knowledgebase,model):
                return self.PL_TRUE(alpha, model)
            else:
                return True #If KB is false always return True
        else:
            P = symbols[0]
            rest = symbols[1:]

            true_check = self.TT_CHECK_ALL(knowledgebase, alpha, rest, self.extend_model(model, P, True))
            false_check = self.TT_CHECK_ALL(knowledgebase, alpha, rest, self.extend_model(model, P, False))
            return true_check and false_check 


    def sentence_to_cnf(self, sentence):
        """Convert sentence to conjunctive normal form"""
        if "<=>" in sentence:
            terms = sentence.split("<=>")
            if len(terms)!=2:
                raise ValueError
            a= terms[0]
            b= terms[1]
            sentence = f"(({a})=>({b}))^(({b})=>({a}))"

        sentence = sentence.replace("^", "&")
        sentence = sentence.replace("v", "|")
        sentence = sentence.replace("-", "~")
        sentence = sentence.replace("=>", ">>")

        
        expr = sympify(sentence)
        expr = str(to_cnf(expr))
        
        
        expr = expr.replace("|", "v")
        expr = expr.replace("&", "^")
        expr = expr.replace("~", "-")
        expr = expr.replace(" ", "")
        expr = expr.replace("(", "")
        expr = expr.replace(")", "")

        #print(expr)
        return expr

    def kb_to_cnf(self, knowledgebase):
        """Converts all sentences of the knowledgebase to CNF"""
        cnf_knowledge_base = []
        for sentence in knowledgebase:
            cnf_knowledge_base.append(self.sentence_to_cnf(sentence))
        
        return cnf_knowledge_base

    def extract_clauses(self, knowledgebase):
        """Function to extract clauses from CNF-Knowledgebase"""
        cnf_knowledge_base = self.kb_to_cnf(knowledgebase)
        clauses = []
        for cnf in cnf_knowledge_base:
            if "^" in cnf:
                terms = cnf.split("^")
                clauses.extend(terms)
            else:
                clauses.append(cnf)
        return list(set(clauses))
    
    def get_disjuncts(self, sentence):
        """Function that returns all disjuncts of a disjunction as a list"""
        if "v" in sentence:
            return sentence.split("v")
        return [sentence]

    def negate(self, sentence):
        """Negates given sentence
           Since we use sympy every biconditional should be replace by implications to easiert transform the expression
        """
        if "<=>" in sentence:
            terms = sentence.split("<=>")
            if len(terms)!=2:
                raise ValueError
            a= terms[0]
            b= terms[1]
            sentence = f"(({a})=>({b}))^(({b})=>({a}))"

        sentence = sentence.replace("^", "&")
        sentence = sentence.replace("v", "|")
        sentence = sentence.replace("-", "~")
        sentence = sentence.replace("=>", ">>")

        #print(expr)
        expr = sympify(sentence)
        expr = Not(expr)
        expr = str(simplify_logic(expr))
        #print(expr)

        expr = expr.replace("|", "v")
        expr = expr.replace("&", "^")
        expr = expr.replace("~", "-")
        expr = expr.replace(" ", "")
        expr = expr.replace("(", "")
        expr = expr.replace(")", "")

        return expr


    def PL_RESOLUTION(self, knowledgebase, alpha):
        """Algorithm to check Entailment by using proof of contradiction"""
        clauses = self.extract_clauses(knowledgebase)
        clauses.append(self.sentence_to_cnf(self.negate(alpha)))
        new = set()
        while True:
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i+1, len(clauses))]
            for (ci , cj) in pairs:
                resolvents = self.PL_RESOLVE(ci, cj)
                if '' in resolvents:
                    return True
                new = new.union(set(resolvents))
            if new.issubset(set(clauses)):
                return False
            for c in new:
                if c not in clauses: clauses.append(c)
    
    
    def to_disjuncts(self,sentences):
        """Function that converts a list of disjuncts to a disjunction"""
        result =""
        for sentence in sentences:
            result+=sentence + "v"
        return result[:-1]

    def PL_RESOLVE(self, ci, cj):
        """Returns a set of possible Clauses that result by Resolution on Ci and Cj
           The empty clause is equivalent to false
        """
        clauses = []
        ci_disjuncts = self.get_disjuncts(ci)
        cj_disjuncts = self.get_disjuncts(cj)
        for di in ci_disjuncts:
            for dj in cj_disjuncts:
                if di == self.negate(dj) or self.negate(di) == dj:
                    dnew = list(set(self.removeall(di, self.get_disjuncts(ci))+ self.removeall(dj, self.get_disjuncts(cj))))
                    clauses.append(self.to_disjuncts(dnew))
        return clauses

    def is_definitive_clause(self, clause):
        """A clause is definitive if it only has one positive literal"""
        count = 0
        terms = clause.split("v")

        for term in terms:
            if term[0] != "-":
                count+=1
        
        return count == 1
    
    def get_definitive_clauses(self, knowledgebase):
        """Function to extract a set of  definitive clauses from a knowledgebase"""
        clauses = self.extract_clauses(knowledgebase)
        definitive_clauses = []
        for clause in clauses: 
            if self.is_definitive_clause(clause):
                definitive_clauses.append(clause)
        return definitive_clauses 
    
    def convert_horn_to_implication(self, hornclause):
        """Function to convert horn/definitive clause to an implication"""
        if "v" in hornclause:
            terms = hornclause.split("v")
            conclusion = ""
            for term in terms:
                if "-" not in term:
                    conclusion = term
                    terms.remove(conclusion)
                    break
            
            premise = "v".join(terms)
            return self.negate(premise) + "=>" + conclusion
        else:
            return hornclause
        
        

    def chained_clauses(self, knowledgebase):
        """"""
        clauses = self.get_definitive_clauses(knowledgebase)
        definitive_clauses = []
        for clause in clauses: 
            definitive_clauses.append(self.convert_horn_to_implication(clause))
        return definitive_clauses 

    def is_true_symbol(self, clause):
        """Check if clause is a symbol that is true"""
        if "=>" not in clause and clause[0] !="-":
            return True 

        return False

    def get_premise(self, clause):
        """Get a list of Premises"""
        if "=>" not in clause:
            return []
        terms = clause.split("=>")
        premises = terms[0].split("^")

        return premises

    def get_conclusion(self, clause):
        """Get the conclusion of the implication"""
        if "=>" not in clause:
            return []
        terms = clause.split("=>")
        return terms[1]

    def get_clauses_with_premise(self, knowledgebase, premise):
        """Returns only those clauses from the knowlegebase which include the premise"""
        clauses_with_premise = []
        for c in knowledgebase:
            if premise in self.get_premise(c):
                clauses_with_premise.append(c)
        return clauses_with_premise

    def PL_FC_ENTAILS(self, knowledgebase, q):
        """Checks if the knowlegebase entails query q
           Beware, q can only be positive
        """

        
        #print("Knowledgebase: ", knowledgebase)
        #print("Clauses: ", self.extract_clauses(knowledgebase))
        #print("Definitive Clauses", self.get_definitive_clauses(knowledgebase))
        #print("Chained Clauses: ", self.chained_clauses(knowledgebase))

        knowledgebase = self.chained_clauses(knowledgebase)
       
        agenda = [x for x in knowledgebase if self.is_true_symbol(x)]
        count ={}
        for x in knowledgebase:
            count[x] = len(self.get_premise(x))

        inferred = {s:False for s in self.get_symbols(knowledgebase)} 

        while len(agenda)!=0:
            p = agenda.pop()
            if  p==q:
                return True
            if  inferred[p] == False:
                inferred[p] = True
                for c in self.get_clauses_with_premise(knowledgebase, p):
                    count[c] -=1
                    if count[c] == 0:
                        agenda.append(self.get_conclusion(c))
        return False

    def find_pure_symbol(self, symbols, clauses):
        """Finds pure symbols in the knowledgebase
        (A v -B) ^ (-A v C)  => [-B, C]
        """
        for symbol in symbols:
            pos_found , neg_found = False, False
            for clause in clauses:
                if not pos_found and symbol in self.get_disjuncts(clause):
                    pos_found = True
                if not neg_found and self.negate(symbol) in self.get_disjuncts(clause):
                    neg_found = True
            if pos_found != neg_found:
                return symbol, pos_found
        return None, None

    def find_unit_clause(self, clauses, model):
        """Finds unit clauses in the knowledgebase"""
        for clause in clauses:
            P, value = None, None
            for literal in self.get_disjuncts(clause):
                sym, value = literal, True
                if literal[0] == "-":
                    value = False
                    sym = literal[1:]
                if sym in model:
                    if model[sym] == value:
                        return None, None
                elif P:
                    return None, None
                else:
                    P, value = sym, value
        if P: 
            return P, value
        return None, None

    def dpll(self, knowledgebase, symbols, model):
        clauses = self.extract_clauses(knowledgebase)
        all_true = True 
        for c in clauses:
            val = self.PL_TRUE(c, model)
            if val == False:
                all_true = False
        if all_true:
            return True

        P, value = self.find_pure_symbol(symbols, clauses)
        if P:
            return self.dpll(knowledgebase, self.removeall(P, symbols),self.extend_model(model, P, value))

        P, value = self.find_unit_clause(clauses, model)
        if P:
            return self.dpll(knowledgebase, self.removeall(P, symbols),self.extend_model(model, P, value))
        if symbols:
            P, rest = symbols[0], symbols[1:]
            return (self.dpll(knowledgebase, rest, self.extend_model(model, P, True)) or
                    self.dpll(knowledgebase, rest, self.extend_model(model, P, False)))  
        return False



#Knowledgebase from chapter 7.4.3
knowledgebase_chapter_seven= [
    "-P11",
    "B11<=>P12vP21",
    "B21<=>P11vP22vP31",
    "-B11",
    "B21",
]

KBA = KnowledgebasedAgent("FC")
#print(KBA.get_symbols(knowledgebase_chapter_seven))
#print(KBA.TT_ENTAILS(knowledgebase_chapter_seven, "-P12"))
#Example p. 309 R13 in R15 and  R1 in R16
#print(KBA.PL_RESOLVE("-P22", "P11vP22vP31"))
#print(KBA.PL_RESOLVE("-P11", "P31vP11"))
#print(KBA.PL_RESOLVE("AvB", "Av-B"))
#print(KBA.sentence_to_cnf("B11<=>P12vP21"))
#print(KBA.sentence_to_cnf("A<=>BvC"))
#print(KBA.chained_clauses(knowledgebase_chapter_seven))

#print("Does KB|=-P12 using TT Checks: ", KBA.TT_ENTAILS(knowledgebase_chapter_seven, "-P12"))
#print("Does KB|=-P12 using Resolution: ",KBA.PL_RESOLUTION(knowledgebase_chapter_seven, "-P12"))
#print("Does KB|=-P12 using Forward chaining: ", KBA.PL_FC_ENTAILS(knowledgebase_chapter_seven, "P22"))
#print("Is my Knowledgebase satifiable using DPLL: ", KBA.dpll(knowledgebase_chapter_seven, KBA.get_symbols(knowledgebase_chapter_seven), {}))
