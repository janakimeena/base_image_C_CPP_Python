/*
	author: krshubham
	11.03.2018, 13:36 IST
*/
#include<iostream>
using namespace std;
#include<vector>
#include <set> 
#include <iterator> 
#include<algorithm>


const long long int MAXN = 1e5+5;

multiset<long long int,greater<long long int>> t[4*MAXN];
long long int a[MAXN];

// Need to write custom merge function to keep only the top most 50 elements at each node at max;
// multiset<long long int,greater<long long int>> combine(multiset<long long int,greater<long long int>> a, multiset<long long int,greater<long long int>> b){
// 	vector<long long int> v1(a.begin(),a.end());
// 	vector<long long int> v2(a.begin(),a.end());
// 	multiset<long long int, greater<long long int>> temp;
// 	long long int x=0,y=0,c = 0;
// 	while(1){
// 		if(a.size() == 0) break;
// 		else if(b.size() == 0) break;
// 		if(v1[x] >= v2[y]){
// 			temp.insert(v1[x]);
// 			x++;
// 		}
// 		else{
// 			temp.insert(v2[y]);
// 			y++;
// 		}
// 		c++;
// 		if(c == 50 || v1.size() == x || v2.size() == y) break;
// 	}
// 	if(c < 50){
// 		if(v1.size() == x && v2.size() != y){
// 			while(1){
// 				temp.insert(v2[y]);
// 				y++;
// 				c++;
// 				if(c == 50 || y == v2.size()) break;
// 			}
// 		}
// 		else if(x != v1.size() && y == v2.size()){
// 			while(1){
// 				temp.insert(v1[x]);
// 				x++;
// 				c++;
// 				if(c == 50 || x == v1.size()) break;
// 			}
// 		}
// 	}
// 	return temp;
// }

// Reference from: https://e-maxx-eng.appspot.com/data_structures/segment_tree.html
void build(long long int v, long long int l , long long int r){
	if(l == r){
		t[v].insert(a[l]);
	}
	else{
		long long int mid = (l+r)/2;
		build(v*2, l, mid);
		build(v*2+1, mid+1,r);
		multiset<long long int, greater<long long int>> temp;
		auto it = temp.begin();
		merge(t[v*2].begin(), t[v*2].end(), t[v*2+1].begin(), t[v*2+1].end(),inserter(temp,it));
		t[v].clear();
		int c = 0;
		for(auto it = temp.begin(); it != temp.end(); it++){
			t[v].insert(*it);
			if(c > 50) break;
		}
		// t[v] = combine(t[2*v],t[2*v+1]);
	}
}

void update(long long int v, long long int l, long long int r, long long int pos, long long int val){
	t[v].erase(t[v].find(a[pos]));
	t[v].insert(val);
	// cout<<"YES"<<endl;
	if(l != r){
		long long int mid = (l+r)/2;
		if(pos <= mid){
			update(2*v, l,mid,pos,val);
		}
		else{
			update(2*v+1,mid+1,r,pos,val);
		}
		t[v].clear();
		auto it = t[v].begin();
		merge(t[v*2].begin(), t[v*2].end(), t[v*2+1].begin(), t[v*2+1].end(),inserter(t[v],it));
	}
	else{
		a[pos] = val;
	}
}


// multiset<long long int> query(long long int v, long long int l, long long int r, long long int ql, long long int qr){
// 	if(l == ql && r == qr){
// 		return t[v];
// 	}

// 	long long int mid = (l+r)/2;
// }

multiset<long long int,greater<long long int>> query(long long int node, long long int start, long long int end, long long int l, long long int r) {
	if(r < start || end < l){
		multiset<long long int,greater<long long int>> temp;
		return temp;
	}
	if(l <= start and end <= r){
		return t[node];
	}
	long long int tm = (start + end) / 2;
	multiset<long long int,greater<long long int>> m1 = query(node*2, start, tm, l, r);
	multiset<long long int,greater<long long int>> m2 = query(node*2+1, tm+1, end,l, r);
	// return combine(m1,m2);
	// return m1;
	m1.insert(m2.begin(),m2.end());
	return m1;
}

int main(){
	long long int n,q;
	cin>>n>>q;
	long long int x,y,z;
	for (long long int i = 1; i <= n; ++i){
		cin>>a[i];
	}
	build(1,1,n);
	while(q--){
		cin>>x>>y>>z;
		if(x==1){
			update(1,1,n,y,z);
		}
		else{
			auto ans = query(1,1,n,y,z);
			vector<long long int> v(ans.begin(),ans.end());
			if(ans.size() < 3){
				cout<<0<<endl;
				continue;
			}
			// cout<<"this is the final value"<<endl;
			// for(auto it = ans.begin(); it!=ans.end(); it++){
			// 	cout<<*it<<" ";
			// }
			// cout<<endl;
			bool fl = false;
			int c = 0;
			for (long long int i = 0; i < v.size()-2; ++i){
				if(v[i+1]+v[i+2] <= v[i]) continue;
				else{
					fl = true;
					cout<<(v[i]+v[i+1]+v[i+2])<<endl;
					break;
				}
				if(c > 50){
					break;
				}
				c++;
			}
			if(!fl){
				cout<<0<<endl;
			}
		}
	}
	return 0;
} 
