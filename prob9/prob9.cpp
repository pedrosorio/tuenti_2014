#include <iostream>
#include <limits.h>
#include <string.h>
#include <queue>
#include <vector>
#include <algorithm>

using namespace std;

bool bfs(vector<vector<pair<int, int> > > &r_graph, int s, int t, int parent[], int location[]) {

    int V = r_graph.size();
    bool visited[V];
    memset(visited, 0, sizeof(visited));

    queue <int> q;
    q.push(s);
    visited[s] = true;
    parent[s] = -1;
    location[s] = -1;
    int min_capacity = INT_MAX;

    while (!q.empty())
    {
        int u = q.front();
        q.pop();

        vector<pair<int, int> > adj_list = r_graph[u];
        for (int i = 0; i < adj_list.size(); i++) {
            pair<int, int> edge = adj_list[i];
            int v = edge.first;
            int capacity = edge.second;

            if (visited[v]==false && capacity > 0)
            {
                q.push(v);
                parent[v] = u;
                location[v] = i;
                visited[v] = true;
            }
        }
    }

    // If we reached sink in BFS starting from source, then return
    // true, else false
    return visited[t];
}

// Returns tne maximum flow from s to t in the given graph
int fordFulkerson(vector<vector<pair<int, int> > > &r_graph, int s, int t)
{
    int u, v;


    int parent[r_graph.size()];
    int location[r_graph.size()];
    int max_flow = 0;

    while (bfs(r_graph, s, t, parent, location))
    {

        int path_flow = INT_MAX;
        for (v=t; v!=s; v=parent[v]) {
            u = parent[v];
            path_flow = min(path_flow, r_graph[u][location[v]].second);
        }

        for (v=t; v != s; v=parent[v]) {
            u = parent[v];
            r_graph[u][location[v]].second -= path_flow;
            int i = 0;
            while (r_graph[v][i++].first != u);
            r_graph[v][i].second += path_flow;
        }

        max_flow += path_flow;
    }

    // Return the overall flow
    return max_flow;
}

int place_to_id(string place, int I, string &city_name) {
    if (place == city_name) {
        return 0;
    } else if (place == "AwesomeVille") {
        return I+1;
    }
    return atoi(place.c_str()) + 1;
}

int main() {
    int C;
    cin >> C;
    for (int city = 0; city < C; city++) {
        string city_name;
        cin >> city_name;
        int S,D;
        cin >> S >> D;
        int I,R;
        cin >> I >> R;
        vector<vector<pair<int, int> > > graph(I+2, vector<pair<int,int> >());
        for (int i = 0; i < R; i++) {
            string from, to, type;
            int lanes, from_id, to_id;
            cin >> from >> to >> type >> lanes;
            from_id = place_to_id(from, I, city_name);
            to_id = place_to_id(to, I, city_name);
            int capacity = type == "normal" ? lanes * S : lanes * D;
            graph[from_id].push_back(make_pair(to_id, capacity));
            //build residual graph right here
            graph[to_id].push_back(make_pair(from_id, 0));
        }
        //multiply max flow by 200 since we have 1000/(4+1) = 200 cars per km
        cout << city_name << " " << fordFulkerson(graph, 0, I+1) * 200 << endl;
    }

    return 0;
}
