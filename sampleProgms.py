math = '(- 30 (* (/ 10 2) 2) '

# 'cond'. note that it always returns something, because in racket each condition has a condition and a block to return if true.
cond1 = '(define (f x y) (cond ((< x y) x) ((eq? x y) 0 )((< y x) y)))'

nestednonsense = "(if (eq? 2 2) (define (f x y) (cond ((< x y) (define (x) hi)) ((eq? x y) 0 )((< y x) y))) (define (f) 500))"

nest = "(define (f x y) (if (null? x) (if (null? y) (define (y) 1) (+ y 1)) (define (x) 1)))"

car_cdr = "(if (< (car '(1 2)) (cdr '(1 2))) (car '(1 2)) (cdr '(1 2)))"

def_in_ifthen = "(if (eq? (car '(1 2 3)) 1) (define (x) 1) (define (x) 2))"

user_def = "(define (v) 3) (define (f x y) (cond ((< x y) x) ((eq? x y) 0 )((< y x) y))) (f e h)"

lamb = "(define (f x y) (lambda (x y) (* x y)))"

sample = "(define (f x y) (if (eq? x 0) x ((+ (- x 1) y))))"

sample2 = "(define (f x y) (cond ((< x y) (define (q) 3)) ((eq? x y) 0 )((< y x) y)))"

sample3 = "(define (f x y) (cond ((< x y) (car (list 1 2))) ((eq? x y) 0 )((< y x) y)))"

multiplelines = "(if (< y x)((+ x 1)(- y 1))((- x 1)(+ y 1)))"


