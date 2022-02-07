## Modelos

### Hay que hacer un lenguaje lo suficientemente expresivo como para implementar el simplex

# Definiciones globales

- N,R,Z ===> SET
- x acompanyado de `x in SET`
- n in N
- Sequence de los naturEvenales {init...end}
  - sequence {f(x, step(n))} | n in sequence[N]
  - x[i] in Seq | i/2 in N, x < 10 `// primer elemento`
    - Seq = {30,1,3,4,13} newSeq = {3}

Even = i in N| i/2 in N

x[i,j] in Mmxn| i in Even, j in Odd

Let N be the set of naturals;
Let X be set of variables
Let Nplus be the set of naturals | x in Nplus, x > 0
Let R be set of reals;
Let Mmxn be the set (R^n)^m | n and m in N;
Let Mmxn be the set of matrix;


Def LinealEq be c*x | n in N, c in R^n and x in X^n

Let n,m,i and j in N, A in R^n^m, i <= n and j <= m 
  Def transposed like transposed(A) = Atransposed |
    Atransposed[i,j] = A[j,i];

Let n in N, c in R^n and x in X^n 
  Def LinealEq like tarnsposed(c)*x


