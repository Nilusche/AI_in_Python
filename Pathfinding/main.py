
from graph import *
if __name__ == '__main__':
    q = Queue("FIFO")
    romania = Graph( ['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
    'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
    'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
    [
    ('Or', 'Ze', 71), ('Or', 'Si', 151),
    ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
    ('Ia', 'Va', 92), ('Ar', 'Si', 140),
    ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
    ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
    ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
    ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
    ('Lu', 'Me', 70), ('Me', 'Dr', 75),
    ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
    ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
    ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
    ('Hi', 'Ef', 86)
    ] )

    romania.print()
    #romania.bfs("Bu", "Ti")
    #romania.dfs("Bu", "Ti")
    romania.ucs("Bu", "Ti")
    


    