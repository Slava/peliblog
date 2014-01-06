Title: TCO 2013 Qual 1A
Slug: tco-2013-qual-1a
Date: 2013-02-23

Every year TCO qualification rounds attract attention of thousands of coders. Not just active TopCoder participants but old veterans and newcommers as well. For me it was just another round with lowered difficulty. Let's look into it.

### 250

Problem was extremely simple and was intended to test implemenation skills. Ususal difficulty level for second division easy problems. A lot of correct submits in first minutes, very low fail rate.

### 500

Problem involved some math or geometry on plane (depends on solution). I am usually very bad at such problems and this was not exception. Wasting more than 20 minutes on it I came up with approximating solution which was wrong and it failed on system test as expected. Some solutions (correct ones) failed due to time limit, probably because of massive calculations in real numbers (`double` in C++/Java). Those are very slow compared to integer calculations. I could successfully challenge one solution (the only successful challenge in room) and fail three times. Lost 25 points on challenge phase.

### 1000

The first time I am sure in my solution for 1000. Ususally I try to submit some facile code but today it made my day.

From the first sight I recognized my favorite mincost-maxflow problem. Looks like this problem was intended to be implementation based difficult. As I had pre-written MCMF algo I just constructed correct net and submitted for 565 pts (spent a lot of time actually debugging old pre-written code).

Solution: we need to construct directed graph which has only simple cycles. It means every vertix in graph has one incomming and one outcomming edge. We can construct bipartite graph. For outcomming edges count on the left and incomming ones on the right. As total number of vertixes in table with $R$ rows and $C$ columns will not be very big, we can use $O(N^3)$ algorithm (actually it is $O(MN)$ algo but it is bipartite graph). $$R \times C \times 2 \le 512$$

### Code

250 - HouseBuilding

```cpp
vector<string> a;

int go(int x) {
	int res = 0;
	for (int i = 0; i < (int)a.size(); i++)
		for (int j = 0; j < (int)a[0].size(); j++) {
			res += min(abs(x-a[i][j]+'0'), abs(x-a[i][j]+'0'+1));
		}
	return res;
}

int res;
class HouseBuilding {
public:
	int getMinimum(vector <string> area) {
		res = 1<<30;
		a=  area;
		for (int i = 0; i < 9; i++) {
			res = min(res, go(i));
			cout << i << " " << go(i) << endl;
		}

		return res;
	}
};
```

1000 - DirectionBoard

```cpp
int N, M;

int to(int x, int y, char d) {
	switch(d) {
		case 'U': x--; if (x == -1) x = N-1; break;
		case 'D': x++; if (x == N) x = 0; break;
		case 'L': y--; if (y == -1) y = M-1; break;
		case 'R': y++; if (y == M) y = 0; break;
	}
	return x * M + y;
}

int res;
class DirectionBoard {
public:
	int getMinimum(vector <string> board) {
		N = (int)board.size();
		M = (int)board[0].size();

MCMF::init();
		MCMF::n = N*M*2+2;
		int S = N*M*2;
		int T = S+1;

		for (int i = 0; i < N*M; i++) {
			MCMF::add_edge(S,i,0,1);
			MCMF::add_edge(i+N*M,T,0,1);
		}

		string allD = "UDLR";
		for (int i = 0; i < N; i++)
			for (int j = 0; j < M; j++)
				for (int k = 0; k < 4; k++)
					MCMF::add_edge(i*M+j,N*M+to(i,j,allD[k]),board[i][j] != allD[k],1);

		return MCMF::mincost_maxflow(S,T);
	}
};
```

MCMF namespace has functions for mincost-maxflow algorithm implemented with dijkstra for finding shortest paths.
