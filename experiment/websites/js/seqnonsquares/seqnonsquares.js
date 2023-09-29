/* based on: https://rosettacode.org/wiki/Sequence_of_non-squares#JavaScript (2022-01-04) */

const nonSquare = n =>
  n + Math.floor(1 / 2 + Math.sqrt(n));
