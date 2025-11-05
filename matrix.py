def generate(size = 10):

    matrix = []
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(0)
        
        matrix.append(row)
    
    return matrix
