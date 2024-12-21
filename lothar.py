
import numpy as np
import sympy as sp


def column_deter(k: int) -> sp.Rational:
    """ φ(k)=log2((k-1 XOR k) + 1) """
    assert  isinstance(k, int), f"Parameter `c` must be an integer (got {k})"
    assert             k > -1,  f"Invalid column index `c` (expected non-negative integer, got {k})"
    return sp.Rational(np.log2( (0b11 ^ 0b00 if k == 0 else (k-1) ^ k) + 1 ), 1)

def column_coeff(k: int) -> sp.Rational:
    """ m(k)=6^(2-φ(k))"""
    return sp.Rational(36, 6**column_deter(k))

def cc_fact(k: int) -> sp.Rational:
    """ m!(k)=m(k)*m(k-1)*...*m(2)*m(1) """
    return sp.prod([ column_coeff(d) for d in range(1, k+1) ])

def beta_coeff(w: int, k: int) -> sp.Rational:
    """ β(w,k)=m!(k)/(2^w) """
    return sp.Rational( cc_fact(k), 2**w )

def omega_coeff(k: int) -> sp.Rational:
    """ ω(c)=Σ_{n=0}^{k}[m!(k)/m!(n)*(1/2-3^(φ(n+1)-2))] """
    omeg = sp.Rational(0,1)
    half = sp.Rational(1,2)
    fact = cc_fact(k)
    for i in range(k):
        omeg += sp.Rational( fact, cc_fact(i) ) * (half - sp.Rational( 3**column_deter(i+1), 9 ))
    return omeg

def default_proc(x: int, w: int, k: int, beta: sp.Rational, omega: sp.Rational) -> sp.Rational:
    """ K(x,w,k)=β(w,k)x+ω(c) """
    return beta*x+omega

def table(x: int,
          row_range: tuple = (None, None),
          col_range: tuple = (None, None),
          show: bool = False,
          spacing: int = 0,
          proc = lambda x,w,k,beta,omega: default_proc(x,w,k,beta,omega)) -> list:
    """ Constructs table translation of extended collatz tree. Tree vertices are aligned to the right,
        tree depth grows from top to bottom and column index grows from right to left. """
    assert row_range[1] is not None, "Row range end is not defined"
    assert col_range[1] is not None, "Column range end is not defined"
    assert row_range[1]>=row_range[0] and row_range[0] is not None and row_range[1] is not None, "Invalid row range"
    assert col_range[1]>=col_range[0] and col_range[0] is not None and col_range[1] is not None, "Invalid column range"
    tab = []
    rows = row_range[1]-row_range[0]+1
    cols = col_range[1]-col_range[0]+1
    for w in range(rows):
        tab.append([0]*cols)
        row=row_range[0]+w
        for k in range(cols):
            col=col_range[0]+k
            tab[w][cols-1-k]=proc(x,row,col,beta_coeff(row,col),omega_coeff(col))
    if show:
        max_len =  0
        for sub in tab:
            new_len = len(str( max(sub, key=lambda elem: len(str(elem))) ))
            max_len = new_len if new_len > max_len else max_len
        if spacing > 0:
            max_len = spacing
        row_index  = 0
        for sub in tab:
            ri = row_range[0]+row_index
            sub.append(f"{ri}{'_'*(max_len-len(str(ri)))}")
            row_index += 1
        hor_bar = '-' * ( (cols + 1) * (max_len + 3) + 1 )
        tab.insert(0, [f"{i}{'_'*(max_len-len(str(i)))}" for i in range(col_range[0], col_range[1]+1)][::-1])
        tab[0].append('X'*max_len)
        print(hor_bar)
        for sub in tab:
            fmt = "|"
            for ele in sub:
                fmt += f" {ele}{' ' * (max_len - len(str(ele)))} |"
            del sub[-1]
            print(fmt)
            print(hor_bar)
        del tab[0]
    return tab

