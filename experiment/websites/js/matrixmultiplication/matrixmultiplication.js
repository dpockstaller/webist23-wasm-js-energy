/* based on: https://rosettacode.org/wiki/Matrix_multiplication#ES6 (2022-01-03) */

// matrixMultiply :: Num a => [[a]] -> [[a]] -> [[a]]
const matrixMultiply = a =>
  b => {
    const cols = transpose(b);
    return map(
      compose(
        flip(map)(cols),
        dotProduct
      )
    )(a);
  };

// dotProduct :: Num a => [[a]] -> [[a]] -> [[a]]
const dotProduct = xs =>
  compose(sum, zipWith(mul)(xs));

// ---------------------- GENERIC ----------------------

// compose (<<<) :: (b -> c) -> (a -> b) -> a -> c
const compose = (...fs) =>
  fs.reduce(
  (f, g) => x => f(g(x)),
  x => x
);

// flip :: (a -> b -> c) -> b -> a -> c
const flip = f =>
  x => y => f(y)(x);

// length :: [a] -> Int
const length = xs =>
  // Returns Infinity over objects without finite
  // length. This enables zip and zipWith to choose
  // the shorter argument when one is non-finite,
  // like cycle, repeat etc
  (Array.isArray(xs) || 'string' === typeof xs) ? (
    xs.length
  ) : Infinity;

// map :: (a -> b) -> [a] -> [b]
const map = f =>
  // The list obtained by applying f
  // to each element of xs.
  // (The image of xs under f).
  xs => xs.map(f);

// mul :: Num a => a -> a -> a
const mul = a =>
  b => a * b;

// sum :: (Num a) => [a] -> a
const sum = xs =>
  xs.reduce((a, x) => a + x, 0);

// take :: Int -> [a] -> [a]
// take :: Int -> String -> String
const take = n =>
  // The first n elements of a list,
  // string of characters, or stream.
  xs => xs.slice(0, n);

// transpose :: [[a]] -> [[a]]
const transpose = rows =>
  // The columns of the input transposed
  // into new rows.
  // Assumes input rows of even length.
  0 < rows.length ? rows[0].map(
    (x, i) => rows.flatMap(
      x => x[i]
    )
  ) : [];

// zipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
const zipWith = f =>
  // A list constructed by zipping with a
  // custom function, rather than with the
  // default tuple constructor.
  xs => ys => {
    const
      lng = Math.min(length(xs), length(ys)),
      vs = take(lng)(ys);
    return take(lng)(xs)
      .map((x, i) => f(x)(vs[i]));
  };
