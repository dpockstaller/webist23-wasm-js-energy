/* based on: http://rosettacode.org/wiki/K-means%2B%2B_clustering#JavaScript (2021-12-21) */

/**
 * kmeans++ initialization module
 */
import * as kmeans from "./kmeans.js";

export function kmeanspp(observations, k) {

  /**
   * given a set of n  weights,
   * choose a value in the range 0..n-1
   * at random using weights as a distribution.
   *
   * @param {*} weights
   * @param {number} normalizationWeight
   * @return {Object}
   */
  function weightedRandomIndex(weights, normalizationWeight) {
    const n = weights.length;
    if(typeof normalizationWeight !== 'number') {
      normalizationWeight = 0.0;
      for(let i = 0; i < n; i += 1) {
        normalizationWeight += weights[i];
      }
    }

    const r = Math.random();  // uniformly random number 0..1 (a probability)
    let index = 0;
    let cumulativeWeight = 0.0;
    for(let i = 0; i < n; i += 1) {
      //
      // use the uniform probability to search
      // within the normalized weighting (we divide by totalWeight to normalize).
      // once we hit the probability, we have found our index.
      //
      cumulativeWeight += weights[i] / normalizationWeight;
      if(cumulativeWeight > r) {
        return i;
      }
    }

    throw Error("algorithmic failure choosing weighted random index");
  }

  const n = observations.length;
  const distanceToCloseCentroid = []; // distance D(x) to closest centroid for each observation
  const centroids = [];   // indices of observations that are chosen as centroids

  //
  // keep list of all observations' indices so
  // we can remove centroids as they are created
  // so they can't be chosen twice
  //
  const index = [];
  for(let i = 0; i < n; i += 1) {
    index[i] = i;
  }

  //
  //  1. Choose one center uniformly at random from among the data points.
  //
  let centroidIndex = Math.floor(Math.random() * n);
  centroids.push(centroidIndex);

  for(let c = 1; c < k; c += 1) {
    index.slice(centroids[c - 1], 1);    // remove previous centroid from further consideration
    distanceToCloseCentroid[centroids[c - 1]] = 0;  // this effectively removes it from the probability distribution

    //
    // 2. For each data point x, compute D(x), the distance between x and
    //    the nearest center that has already been chosen.
    //
    // NOTE: we used the distance squared (L2 norm)
    //
    let totalWeight = 0.0;
    for(let i = 0; i < index.length; i += 1) {
      //
      // if this is the first time through, the distance is undefined, so just set it.
      // Otherwise, choose the minimum of the prior closest and this new centroid
      //
      const distanceToCentroid = kmeans.distanceSquared(observations[index[i]], observations[centroids[c - 1]]);
      distanceToCloseCentroid[index[i]] =
        (typeof distanceToCloseCentroid[index[i]] === 'number')
          ? Math.min(distanceToCloseCentroid[index[i]], distanceToCentroid)
          : distanceToCentroid;
      totalWeight += distanceToCloseCentroid[index[i]];
    }

    //
    //  3. Choose one new data point at random as a new center,
    //     using a weighted probability distribution where a point x is chosen with probability proportional to D(x)^2.
    //
    centroidIndex = index[weightedRandomIndex(distanceToCloseCentroid, totalWeight)];
    centroids.push(centroidIndex);

    //  4. Repeat Steps 2 and 3 until k centers have been chosen.
  }

  //
  //  5. Now that the initial centers have been chosen, proceed using
  //     standard k-means clustering. Return the model so that
  //     kmeans can continue.
  //
  return {
    'observations': observations,
    'centroids': centroids.map(x => observations[x]), // map centroid index to centroid value
    'assignments': observations.map((x, i) => i % centroids.length) // distribute among centroids
  }
}
