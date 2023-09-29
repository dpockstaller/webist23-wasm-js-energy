/* based on: https://rosettacode.org/wiki/K-means%2B%2B_clustering#C (2021-12-13) */

//#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <emscripten/emscripten.h>

typedef struct {
	double	x;
	double	y;
	int		group;
} POINT;

/**
 * Set points by provided flat array dataset
 * x: even dataset entry ids
 * y: odd dataset entry ids
 */
POINT * set_points(double *dataset, int num_pts)
{
  int		i;
  POINT * pts;

  pts = (POINT*) malloc(sizeof(POINT) * num_pts);

  int pt_i;
  int entries = num_pts*2;
  for ( i = 0; i < entries; i++ ) {
    pts[pt_i].x = dataset[i];
    i++;
    pts[pt_i].y = dataset[i];
    pt_i++;
  }
  return pts;
}

/*-------------------------------------------------------
	dist2

	This function returns the squared euclidean distance
	between two data points.
-------------------------------------------------------*/
double dist2(POINT * a, POINT * b)
{
	double x = a->x - b->x;
	double y = a->y - b->y;
	return x*x + y*y;
}

/*------------------------------------------------------
	nearest

  This function returns the index of the cluster centroid
  nearest to the data point passed to this function.
------------------------------------------------------*/
int nearest(POINT * pt, POINT * cent, int n_cluster)
{
	int i, clusterIndex;
	double d, min_d;

	min_d = HUGE_VAL;
	clusterIndex = pt->group;
	for (i = 0; i < n_cluster; i++) {
		d = dist2(&cent[i], pt);
		if ( d < min_d ) {
			min_d = d;
			clusterIndex = i;
		}
	}
	return clusterIndex;
}

/*------------------------------------------------------
	nearestDistance

  This function returns the distance of the cluster centroid
  nearest to the data point passed to this function.
------------------------------------------------------*/
double nearestDistance(POINT * pt, POINT * cent, int n_cluster)
{
	int i;
	double d, min_d;

	min_d = HUGE_VAL;
	for (i = 0; i < n_cluster; i++) {
		d = dist2(&cent[i], pt);
		if ( d < min_d ) {
			min_d = d;
		}
	}

	return min_d;
}

/*-------------------------------------------------------
	kpp

	This function uses the K-Means++ method to select
	the cluster centroids.
-------------------------------------------------------*/
void kpp(POINT * pts, int num_pts, POINT * centroids,
		 int num_clusters)
{
	int j;
	int cluster;
	double sum;
	double * distances;


	distances = (double*) malloc(sizeof(double) * num_pts);

	/* Pick the first cluster centroids at random. */
	centroids[0] = pts[ rand() % num_pts ];


	/* Select the centroids for the remaining clusters. */
	for (cluster = 1; cluster < num_clusters; cluster++) {

		/* For each data point find the nearest centroid, save its
		   distance in the distance array, then add it to the sum of
		   total distance. */
		sum = 0.0;
		for ( j = 0; j < num_pts; j++ ) {
			distances[j] =
				nearestDistance(&pts[j], centroids, cluster);
			sum += distances[j];
		}

		/* Find a random distance within the span of the total distance. */
		sum = sum * rand() / (RAND_MAX - 1);

		/* Assign the centroids. the point with the largest distance
			will have a greater probability of being selected. */
		for (j = 0; j < num_pts; j++ ) {
			sum -= distances[j];
			if ( sum <= 0)
			{
				centroids[cluster] = pts[j];
				break;
			}
		}
	}

	/* Assign each observation the index of it's nearest cluster centroid. */
	for (j = 0; j < num_pts; j++)
		pts[j].group = nearest(&pts[j], centroids, num_clusters);

	free(distances);

	return;
}	/* end, kpp */


/*-------------------------------------------------------
	lloyd

	This function clusters the data using Lloyd's K-Means algorithm
	after selecting the intial centroids using the K-Means++
	method.
	It returns a pointer to the memory it allocates containing
	the array of cluster centroids.
-------------------------------------------------------*/
POINT * lloyd(POINT * pts, int num_pts, int num_clusters, int maxTimes)
{
	int i, clusterIndex;
	int changes;
	int acceptable = num_pts / 1000;	/* The maximum point changes acceptable. */


	if (num_clusters == 1 || num_pts <= 0 || num_clusters > num_pts )
		return 0;


	POINT * centroids = (POINT *)malloc(sizeof(POINT) * num_clusters);

	if ( maxTimes < 1 )
		maxTimes = 1;

/*	Assign initial clustering randomly using the Random Partition method
	for (i = 0; i < num_pts; i++ ) {
		pts[i].group = i % num_clusters;
	}
*/

	/* or use the k-Means++ method */

	kpp(pts, num_pts, centroids, num_clusters);

	do {
		/* Calculate the centroid of each cluster.
		  ----------------------------------------*/

		/* Initialize the x, y and cluster totals. */
		for ( i = 0; i < num_clusters; i++ ) {
			centroids[i].group = 0;		/* used to count the cluster members. */
			centroids[i].x = 0;			/* used for x value totals. */
			centroids[i].y = 0;			/* used for y value totals. */
		}

		/* Add each observation's x and y to its cluster total. */
		for (i = 0; i < num_pts; i++) {
			clusterIndex = pts[i].group;
			centroids[clusterIndex].group++;
			centroids[clusterIndex].x += pts[i].x;
			centroids[clusterIndex].y += pts[i].y;
		}

		/* Divide each cluster's x and y totals by its number of data points. */
		for ( i = 0; i < num_clusters; i++ ) {
			centroids[i].x /= centroids[i].group;
			centroids[i].y /= centroids[i].group;
		}

		/* Find each data point's nearest centroid */
		changes = 0;
		for ( i = 0; i < num_pts; i++ ) {
			clusterIndex = nearest(&pts[i], centroids, num_clusters);
			if (clusterIndex != pts[i].group) {
				pts[i].group = clusterIndex;
				changes++;
			}
		}

		maxTimes--;
	} while ((changes > acceptable) && (maxTimes > 0));

	/* Set each centroid's group index */
	for ( i = 0; i < num_clusters; i++ )
		centroids[i].group = i;

	return centroids;
}	/* end, lloyd */

/*-------------------------------------------------------
	main
-------------------------------------------------------*/
EMSCRIPTEN_KEEPALIVE
void run_kmeanspp(double *dataset, int num_clusters, int maxTimes, int num_pts)
{
	POINT * pts;
	POINT * centroids;

  /* Set points by dataset */
  pts = set_points(dataset, num_pts);

	/* Cluster using the Lloyd algorithm and K-Means++ initial centroids. */
	centroids = lloyd(pts, num_pts, num_clusters, maxTimes);

  /* Log centroids result */
  /*int i;
  for ( i = 0; i < num_clusters; i++ )
    printf("centroid %d\nx= %f, y= %f\n", centroids[i].group, centroids[i].x, centroids[i].y);*/

	free(pts);
	free(centroids);
}
