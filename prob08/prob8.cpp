#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <iostream>
#include <string>

using namespace std;

int pow10[] = {1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000};

int swap(int node, int i1, int j1, int i2, int j2) {
  int val1 = (node / pow10[3*i1+j1]) % 10;
  int val2 = (node / pow10[3*i2+j2]) % 10;
  return node + (val1-val2) * pow10[3*i2+j2] + (val2-val1) * pow10[3*i1+j1];
}

int get_value_at(int node, int i, int j) {
  return (node / pow10[3*i+j]) % 10;
}

vector<int> get_neighbors(int node, unordered_set<int> &visited) {
  vector<int> res;
  //vertical swaps
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      int ngb = swap(node, i, j, i+1, j);
      if (visited.count(ngb) == 0)
        res.push_back(ngb);
    }
  }
  //horizontal swaps
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 2; j++) {
      int ngb = swap(node, i, j, i, j+1);
      if (visited.count(ngb) == 0)
        res.push_back(ngb);
    }
  }
  return res;
}

int manhattan_distance(int i1, int j1, int i2, int j2) {
  int idiff = i1 > i2 ? i1-i2 : i2-i1;
  int jdiff = j1 > j2 ? j1-j2 : j2-j1;
  return idiff + jdiff;
}

unordered_map<int, pair<int, int> > get_node_description(int node) {
  unordered_map<int, pair<int, int> > desc;
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      desc[get_value_at(node, i, j)] = make_pair(i, j);
    }
  }
  return desc;
}

//Heuristic consists of sum of manhtann distances of people from the goal positions
//The maximum distance is taken into account fully, the second largest is decremented
//by 1 (we may place the person closer while moving the person at max distance)
//the third largest is decremented by 2 (we may place this person closer twice)
//After decrementing only positive values are added to the heuristic
//In practice it only makes sense to consider the 4 largest distances because the
//max manhattan distance in the board is 4 and the 5th largest distance would be penalized
//by decrementing 4
int compute_heuristic(int node, unordered_map<int, pair<int, int> > &gdesc) {
  vector<int> dists;
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      int val = get_value_at(node, i, j);
      dists.push_back(manhattan_distance(i, j, gdesc[val].first, gdesc[val].second));
    }
  }
  sort(dists.begin(), dists.end());
  int res = 0;
  //at most 4 largest distances will be used in the heuristic
  for (int i = 0; i < 4; i++) {
    int factor = dists[8-i] - i;
    if (factor <= 0)
      break;
    res += factor;
  }
  return res;
}

//vanilla A-star
//In this case the nodes that have their g_score updated while in the heap
//are not being removed - could implement the sift functions for the heap
//but as-is seems enough
int A_star(int start, int goal) {
  //int added = 0;
  if (start == goal)
    return 0;
  unordered_map<int, pair<int, int> > gdesc = get_node_description(goal);
  unordered_set<int> visited;
  unordered_map<int, int> g_score;
  g_score[start] = 0;
  vector<pair<int, int> > heap;
  heap.push_back(make_pair(-compute_heuristic(start, gdesc), start));
  while (heap.size() > 0) {
    pop_heap(heap.begin(), heap.end());
    pair<int, int> top = heap.back();
    heap.pop_back();
    int node = top.second;
    if (visited.count(node) == 1)
      continue;
    visited.insert(node);
    int g_score_n = g_score[node] + 1;
    vector<int> neighbors = get_neighbors(node, visited);
    for (int i = 0; i < neighbors.size(); i++) {
      int n = neighbors[i];
      if (n == goal)
        return g_score_n;
      if (g_score.count(n) == 0 || g_score_n < g_score[n]) {
        g_score[n] = g_score_n;
        heap.push_back(make_pair(-g_score_n - compute_heuristic(n, gdesc), n));
        push_heap(heap.begin(), heap.end());
        //added++;
      }
    }
  }
  return 0;
}


int main() {

  int T;
  cin >> T;
  unordered_map<string, int> names;
  string name = "";
  for (int test = 0; test < T; test++) {
    for (int i = 0; i < 3; i++) {
      cin >> name;
      names[name.substr(0, name.size()-1)] = 3*i;
      cin >> name;
      names[name.substr(0, name.size()-1)] = 3*i+1;
      cin >> name;
      names[name.substr(0, name.size())] = 3*i+2;
    }
    int start = 876543210;
    int goal = 0;
    int mult = 1;
    for (int i = 0; i < 3; i++) {
      cin >> name;
      goal += names[name.substr(0, name.size()-1)] * mult;
      mult *= 10;
      cin >> name;
      goal += names[name.substr(0, name.size()-1)] * mult;
      mult *= 10;
      cin >> name;
      goal += names[name.substr(0, name.size())] * mult;
      mult *= 10;
    }
    cout << A_star(start,goal) << endl;
  }
  return 0;
}


