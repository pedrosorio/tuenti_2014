#include <sstream>
#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAX_RADIUS = 500;

struct Point {
  int coords[2];
  int radius;
  int id;
};

struct Node {
  Point *location;
  Node *left_child;
  Node *right_child;
};

struct Comparator {
  int axis;
  Comparator(int axis) {this->axis = axis;}
  bool operator() (Point* p1, Point* p2) {
    return p1->coords[axis] < p2->coords[axis];
  }
};

//inspired by kd_tree python code in wikipedia =D
Node* kd_tree(vector<Point*>::iterator start, vector<Point*>::iterator end, int depth = 0, int k = 2) {
  int n = end-start;
  if (n == 0)
    return NULL;

  int axis = depth % k;
  sort(start, end, Comparator(axis));

  int median = n/2;

  Node *node = new Node();
  node->location = *(start+median);
  node->left_child = kd_tree(start, start+median, depth+1);
  node->right_child = kd_tree(start+median+1, end, depth+1);
  return node;
}

//return points in a k-dimensional rectangle
//returns only points whose id is larger than min_id -> more efficient to avoid counting collisions with self and double counting
void get_in_kcube(Node *tree, vector<int> &mins, vector<int> &maxs, vector<Point*> &neighbors, int min_id, int depth = 0, int k = 2) {
  if (tree == NULL)
    return;
  int axis = depth % k;
  Point *point = tree->location;
  bool point_in_kcube = (point->id > min_id);
  for (int i = 0; i < k && point_in_kcube; i++) {
    if (point->coords[i] < mins[i] || point->coords[i] > maxs[i])
      point_in_kcube = false;
  }
  if (point_in_kcube)
    neighbors.push_back(point);
  if (point->coords[axis] >= mins[axis])
    get_in_kcube(tree->left_child, mins, maxs, neighbors, min_id, depth + 1, k);
  if (point->coords[axis] <= maxs[axis])
    get_in_kcube(tree->right_child, mins, maxs, neighbors, min_id, depth + 1, k);
}

int main() {
  int start, num_points;
  char c;
  cin >> start >> c >> num_points;

  Point *point_data = new Point[num_points];
  vector<Point*> points;

  ifstream infile("points");
  string line;

  int count = 0, index = -start;
  while (getline(infile, line)) {
    count++;
    index++;
    if (count < start) continue;
    if (count == start + num_points) break;
    istringstream iss(line);
    iss >> point_data[index].coords[0] >> point_data[index].coords[1] >> point_data[index].radius;
    point_data[index].id = index;
    points.push_back(point_data+index);
  }
  infile.close();

  Node *tree = kd_tree(points.begin(), points.end());
  int collisions = 0;
  vector<int> mins(2);
  vector<int> maxs(2);
  for(int p = 0; p < num_points; p++) {
    Point point = point_data[p];
    for (int i = 0; i < 2; i++) {
      mins[i] = point.coords[i]-point.radius-MAX_RADIUS;
      maxs[i] = point.coords[i]+point.radius+MAX_RADIUS;
    }
    vector<Point*> neighbors;
    //get all the points that are within the square of side 2*(point.radius + MAX_RADIUS)
    //centered at the current point, and have id larger than our point
    get_in_kcube(tree, mins, maxs, neighbors, point.id);
    for (int p2 = 0; p2 < neighbors.size(); p2++) {
      Point point2 = *(neighbors[p2]);
      int dist2 = 0;
      for (int i = 0; i < 2; i++) {
        int df = point.coords[i] - point2.coords[i];
        dist2 += df*df;
      }
      if (dist2 < (point.radius + point2.radius) * (point.radius + point2.radius))
        collisions++;
    }
  }
  cout << collisions << endl;
  return 0;
}
