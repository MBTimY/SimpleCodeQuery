from enum import Enum, auto
class BaseTypes(Enum):
    def _generate_next_value_(name, start, count, last_values):
        mapping_enum = [
            ("CU","COMPILATION_UNIT"),
            ("CLASS","TYPE"),
            ("INTERFACE","TYPE"),
            ("ENUM","TYPE"),
            ("ANNOTATION","TYPE"),
            ("METHOD","METHOD"),
            ("FIELD","FIELD"),
            ("PARAMS","PARAMETER"),
            ("METHODCALLEXPR","EXPRS"),
            ("MEMBERVALUEPAIR","EXPRS"),
            ("MARKERANNOTATION","EXPRS"),
            ("NORMALANNOTATIONEXPR","EXPRS"),
            ("OBJECTCREATION","EXPRS"),
            ("INSTANCEOFEXPR","EXPRS"),
            ("INITIALIZERDECL","EXPRS"),
            ("FIELDACCESS","EXPRS"),
            ("ENUMCONSTANTDECL","ENUM_CONSTANT_DECL"),
            ("ENCLOSED","EXPRS"),
            ("SIGNLEMEMBERANNOTATION","EXPRS"),
            ("THIS","EXPRS"),
            ("ARRAYACCESS","EXPRS"),
            ("ARRAYCREATION","EXPRS"),
            ("VOIDTYPE","EXPRS"),
            ("WILDCARDTYPE","EXPRS"),
            ("REFERENCETYPE","EXPRS"),
            ("ARRAYTYPE","EXPRS"),
            ("UNIONTYPE","EXPRS"),
            ("ARRAYINITIALIZER","EXPRS"),
            ("OPERATOR","EXPRS"),
            ("CAST","EXPRS"),
            ("CLASSEXPR","EXPRS"),
            ("CONDITIONAL","EXPRS"),
            ("SIMPLENAME","EXPRS"),
            ("SUPER","EXPRS"),
            ("VARIABLEDECLARATION","EXPRS"),
            ("METHODREFERENCE","EXPRS"),
            ("LAMBDA","EXPRS"),
            ("VARIABLEDECLARATOR","EXPRS"),
            ("ARRAYCREATIONLEVEL","EXPRS"),
            ("ASSERT","STMTS"),
            ("BLOCK","STMTS"),
            ("BREAK","STMTS"),
            ("CATCHCLAUSE","STMTS"),
            ("CONTINUE","STMTS"),
            ("DO","STMTS"),
            ("EMPTY","STMTS"),
            ("EXPLICITYCONSTRUCTORINVOCATION","STMTS"),
            ("EXPRESSION","STMTS"),
            ("FOREACH","STMTS"),
            ("FOR","STMTS"),
            ("IF","STMTS"),
            ("LABEL","STMTS"),
            ("RETURN","STMTS"),
            ("SWITCHENTRY","STMTS"),
            ("SWITCH","STMTS"),
            ("SYNCHRONIZED","STMTS"),
            ("THROW","STMTS"),
            ("TRY","STMTS"),
            ("LOCALCLASSDECLRATION","STMTS"),
            ("WHILE","STMTS"),
            ("UPARSABLE","STMTS"),
            ("RECEIVERPARAMETER","STMTS"),
            ("NAME","EXPRS"),
            ("LITERAL","EXPRS")
        ]
        for enum_constant in mapping_enum:
            if (name in enum_constant[0]):
                return (enum_constant[1], count)

class TYPES(BaseTypes):
    CU = auto()
    CLASS = auto()
    INTERFACE = auto()
    ENUM = auto()
    ANNOTATION = auto()
    METHOD = auto()
    FIELD = auto()
    PARAMS = auto()
    METHODCALLEXPR = auto()
    MEMBERVALUEPAIR = auto()
    MARKERANNOTATION = auto()
    NORMALANNOTATIONEXPR = auto()
    OBJECTCREATION = auto()
    INSTANCEOFEXPR = auto()
    INITIALIZERDECL = auto()
    FIELDACCESS = auto()
    ENUMCONSTANTDECL = auto()
    ENCLOSED = auto()
    SIGNLEMEMBERANNOTATION = auto()
    THIS = auto()
    ARRAYACCESS = auto()
    ARRAYCREATION = auto()
    VOIDTYPE = auto()
    WILDCARDTYPE = auto()
    REFERENCETYPE = auto()
    ARRAYTYPE = auto()
    UNIONTYPE = auto()
    ARRAYINITIALIZER = auto()
    OPERATOR = auto()
    CAST = auto()
    CLASSEXPR = auto()
    CONDITIONAL = auto()
    SIMPLENAME = auto()
    SUPER = auto()
    VARIABLEDECLARATION = auto()
    METHODREFERENCE = auto()
    LAMBDA = auto()
    VARIABLEDECLARATOR = auto()
    ARRAYCREATIONLEVEL = auto()
    ASSERT = auto()
    BLOCK = auto()
    BREAK = auto()
    CATCHCLAUSE = auto()
    CONTINUE = auto()
    DO = auto()
    EMPTY = auto()
    EXPLICITYCONSTRUCTORINVOCATION = auto()
    EXPRESSION = auto()
    FOREACH = auto()
    FOR = auto()
    IF = auto()
    LABEL = auto()
    RETURN = auto()
    SWITCHENTRY = auto()
    SWITCH = auto()
    SYNCHRONIZED = auto()
    THROW = auto()
    TRY = auto()
    LOCALCLASSDECLRATION = auto()
    WHILE = auto()
    UPARSABLE = auto()
    RECEIVERPARAMETER = auto()
    NAME = auto()
    LITERAL = auto()

    @classmethod
    def ofValue(cls, index: int) -> "TYPES":
        for _, enum_constaint in cls.__members__.items():
            if index == enum_constaint.value[1]:
                return enum_constaint
        return None

    @classmethod
    def ofName(cls, name: str) -> "TYPES":
        if (name in ["ASSIGN", "BINARY", "UNARY"]):
            return TYPES.OPERATOR
        elif (name == "METHODCALL"):
            return TYPES.METHODCALLEXPR
        elif ("LITERAL" in name ):
            return TYPES.LITERAL

        return cls.__members__[name]
    
    @classmethod
    def getTypes(cls) -> list:
        return list(cls.__members__.keys())
