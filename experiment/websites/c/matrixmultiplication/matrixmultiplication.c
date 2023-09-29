/* based on: https://rosettacode.org/wiki/Matrix_multiplication#C (2022-01-03) */

#include <stdio.h>
#include <stdlib.h>
#include <emscripten/emscripten.h>

/* Make the data structure self-contained.  Element at row i and col j
   is x[i * w + j].  More often than not, though,  you might want
   to represent a matrix some other way */
typedef struct { int h, w; double *x;} matrix_t, *matrix;

double dot(double *a, double *b, int len, int step) {
	double r = 0;
	while (len--) {
		r += *a++ * *b;
		b += step;
	}
	return r;
}

matrix mat_new(int h, int w) {
	matrix r = malloc(sizeof(matrix_t) + sizeof(double) * w * h);
	r->h = h, r->w = w;
	r->x = (double*)(r + 1);
	return r;
}

matrix mat_mul(matrix a, matrix b) {
	matrix r;
	double *p, *pa;
	int i, j;
	if (a->w != b->h) return 0;

	r = mat_new(a->h, b->w);
	p = r->x;
	for (pa = a->x, i = 0; i < a->h; i++, pa += a->w)
		for (j = 0; j < b->w; j++)
			*p++ = dot(pa, b->x + j, a->w, b->w);
	return r;
}

void mat_show(matrix a) {
	int i, j;
	double *p = a->x;
	for (i = 0; i < a->h; i++, putchar('\n'))
		for (j = 0; j < a->w; j++)
			printf("\t%7.3f", *p++);
	putchar('\n');
}

EMSCRIPTEN_KEEPALIVE
int run_matrixmultiplication(double *da, int ah, int aw, double *db, int bh, int bw) {

	matrix_t a = { ah, aw, da }, b = { bh, bw, db };
	matrix c = mat_mul(&a, &b);

	//mat_show(&a), mat_show(&b);
	//mat_show(c);
	/* free(c) */
	return 0;
}
