#include<bits/stdc++.h>
using namespace std;

/** A function to find the distance between two points given their latitude and longitude. We use the Haverline Formula **/
long double find_distance(long double lat1,long double lon1, long double lat2,long double lon2)
{
    //all calculations are in SI units
    long double del_lat,del_lon,A,C,D;
    long double pi = acos(-1.0), rad_earth = 6378100.0;
    lat1*=(pi/180.0);
    lat2*=(pi/180.0);
    lon1*=(pi/180.0);
    lon2*=(pi/180.0);
    del_lat = lat2-lat1;
    del_lon = lon2-lon1;
    A = 0.5*(1-cos(del_lat)) + 0.5*cos(lat1)*cos(lat2)*(1-cos(del_lon));
    C = 2*atan2(sqrtl(A),sqrtl(1-A));
    D = rad_earth*C;
    return D;
}

long double pixel_threshold = 0.5, grid_threshold = 0.5, walking_distance_circle=564.0;

vector<vector<int>> find_urban_extent(vector<vector<int>> &bu_matrix)
{
	vector<vector<int>> label = bu_matrix;	//label to indicate the type of the current pixel
	int N = bu_matrix.size(), M = bu_matrix[0].size();
	// walking distance circle's radius is taken to be 564 metres
	// long double walking_distance_circle = 1000.0;
	int ri = floor((long double)((walking_distance_circle))), rj = ri;
	for(int i=0;i<N;i++)
	{
		for(int j=0;j<M;j++)
		{
			if(bu_matrix[i][j]==0){
				label[i][j] = 3;
				continue;
			}
			int built = 0, tot = 0;
			for(int u=i-ri ; u<=i+ri;u++)
			{
				for(int v = j-rj; v<=j+rj; v++)
				{
					if(u<0 or u>=N or v<0 or v>=M)
						continue;
					if((rj*rj*((double)(u-i)*(u-i)) + ri*ri*((double)(v-j)*(v-j)) - ri*ri*rj*rj)<=0)
					{
						built+=(bu_matrix[u][v]==1);
					}
					tot++;
				}
			}
			//cout<<built<<" "<<tot<<'\n';
			long double perc = ((long double)(built))/tot;
			if(perc>=pixel_threshold)
				label[i][j] = 0;	//urban
			else if(perc>=(pixel_threshold/2.0))
				label[i][j] = 1;	//suburban
			else
				label[i][j] = 2;	//rural
		}
	}
	//labelled all pixels
	return label;
}

void preprocess(vector<vector<int>> &matrix, int keyMode)
{
	//keyMode = 0, image is png
	//keyMode = 1, image is tif
	if(keyMode == 0){
		for(auto &u:matrix)
		{
			for(auto &v:u)
			{
				if((v==64) or (v==127) or (v == 255))
					v=2;
				else if(v==191)
					v=1;
				else
					v=0;
			}
		}
	}
	else if(keyMode == 1){
		for(auto &u:matrix)
		{
			for(auto &v:u)
			{
				if((v==1) or (v==2) or (v == 4))
					v=2;
				else if(v==3)
					v=1;
				else
					v=0;
			}
		}
	}
}

vector<vector<int>> rotate_matrix(vector<vector<int>> &matrix){
	int new_i=0,new_j=0;
	int n = matrix.size(),m=matrix[0].size();
	vector<vector<int>> new_mat(m,vector<int>(n));
	for(int j=0;j<m;j++){
		new_j=0;
		for(int i=n-1;i>=0;i--){
			new_mat[new_i][new_j++] = matrix[i][j];
			new_j%=n;
		}
		new_i++;
	}
	return new_mat;
}

string convertToString(char* a, int size) 
{ 
    string s = a; 
    return s; 
} 

int main(int argc, char** argv)
{	
	string folderName = convertToString(argv[2], sizeof(argv[2]) / sizeof(char));
	string InfileName = "tempIn.txt";
	string OutfileName = "tempOut.txt";
	string inFile = folderName+"/"+InfileName;
	string outFile = folderName+"/"+OutfileName;
	freopen(inFile.c_str(),"r",stdin);
    vector<vector<int>> inp_matrix;
    string cur_line;
	while(getline(cin,cur_line)){
		vector<int> temp;
		int i=0,j=0;
		while(i<cur_line.size()){
			int val = 0;
			j = i;
			while((j<cur_line.size()) and (cur_line[j]!=' ')){
				val*=10;
				val+=(cur_line[j]-'0');
				j++;
			}
			temp.push_back(val);
			i = j+1;
		}	
		inp_matrix.push_back(temp);
	}
	preprocess(inp_matrix, atoi(argv[1]));
    vector<vector<int>> out_mat = find_urban_extent(inp_matrix);
	freopen(outFile.c_str(),"w",stdout);
	for(auto u:out_mat)
	{
		for(int i=0;i<u.size();i++)
			{
				cout<<u[i];
				if(i<u.size()-1)cout<<" ";
			}
		cout<<'\n';
	}
}
