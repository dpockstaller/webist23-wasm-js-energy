/* based on: https://rosettacode.org/wiki/N-queens_problem#JavaScript (2021-12-24) */

/**
 * @param {number} rows
 * @param {number} columns
 * @returns {number[][]}
 */
function nqueens(rows, columns) {
  if (rows <= 0) {
    return [[]];
  } else {
    return addQueen(rows - 1, columns);
  }
}

/**
 * @param {number} newRow
 * @param {number} columns
 * @returns {number[][]}
 */
function addQueen(newRow, columns) {
  let newSolutions = [];
  const prev = nqueens(newRow, columns);
  for (let i = 0; i < prev.length; i++) {
    const solution = prev[i];
    for (let newColumn = 0; newColumn < columns; newColumn++) {
      if (!hasConflict(newRow, newColumn, solution))
        newSolutions.push(solution.concat([newColumn]))
    }
  }
  return newSolutions;
}

/**
 * @param {number} newRow
 * @param {number} newColumn
 * @param {number[]} solution
 * @returns {boolean}
 */
function hasConflict(newRow, newColumn, solution) {
  for (let i = 0; i < newRow; i++) {
    if (solution[i]     === newColumn          ||
      solution[i] + i === newColumn + newRow ||
      solution[i] - i === newColumn - newRow) {
      return true;
    }
  }
  return false;
}
