#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <fstream>
#include <iostream>
#include <sstream>
using namespace std;


vector<long long> st;
vector<long long> et;
vector<string> char_bank;
//           pos, hidden?
vector< pair<int, int> > offset;
vector<int> is_key;
vector<char> opcode;
vector<int> shift;

map<int, int> counts;


void incIfAtLeast(int val, int thrs){
	for (int t = 0; t < offset.size(); t++) {
		if (offset[t].first > thrs) {
			offset[t].first += val;
		} else if (offset[t].first == thrs) {
			if ((offset[t].second == 1) && (val == 1)) {
				offset[t].second = 0;
			} else {
				offset[t].first += val;
			}
		}
	}
	return;
}

void hiddenize (int thrs) {
	for (int t = 0; t < offset.size(); t++) {
		if (offset[t].first == thrs) {
			offset[t].second = 1;
		}
	}
	return;
}


int main(){
	int N, L, p, is_keystroke;
	long long ct, prevt;
	
	string s, path;
	char c;
	
	cin >> N;
	cin >> path;
		
	for(int i = 0; i<N; i++){
		cin >> prevt;
		cin >> ct;
		cin >> L;
		for(int j = 0; j<L; j++){
			cin >> c;
			if (c == '+') {
				cin >> s;
				if (s == "#"){
					s = " ";
				}
			}else{
				s = "";
			}
			cin >> p;
			cin >> is_keystroke;
			
			if (c == '+') {
				incIfAtLeast(1, p);
				offset.push_back(make_pair(p, 0));
			}

			if (c == '-') {
				incIfAtLeast(-1, p + 1);
				hiddenize(p);
				offset.push_back(make_pair(p, 1));
			}
                     
   			st.push_back(prevt + (ct - prevt) * j / L);
   			et.push_back(prevt + (ct - prevt) * (j + 1) / L);
   			char_bank.push_back(s);
   			opcode.push_back(c);
   			is_key.push_back(is_keystroke);
		}
	}
	for (int t = 0; t < offset.size(); t++) {
		if (is_key[t]) {
			if (opcode[t] == '+') {
				counts[offset[t].first]++;
			}
			if (opcode[t] == '-') {
				counts[offset[t].first]--;
			}			
		}
	}
	for(map<int,int>::iterator it = counts.begin(); it != counts.end(); it++){
		if (it->second > 2) {
			//cout << "Fixing " << it->first << " " << it->second << "\n";
			int val = it->first;
			int no_extra = it->second - 1;
			int minuses = 0;
			vector <int> stuck_idx;
			// Fixing this copy paste by 
			for (int j = offset.size() - 1; j > -1; j--) {
				if ((offset[j].first == val) && (is_key[j])) {
					//cout << "Found one at j: " << j << "\n";
					if (opcode[j] == '-') {
						minuses++;
						stuck_idx.push_back(j);
					} else {
						if (minuses > 0) {
							minuses--;
							stuck_idx.push_back(j);
						} else {
							offset[j].first += no_extra;
							while (!stuck_idx.empty()) {
								offset[stuck_idx.back()].first += no_extra;
								stuck_idx.pop_back();
							}
							no_extra--;
						}
					}
				}
			}
		}
	}
	
	//converting path
	string newpath = path;
	if (path.size() > 30) {
		newpath = path.substr(11, 10);
		for (int j = path.size() - 1; j > -1; j--) {
			if (path[j] == '/') {
				newpath.append(path.substr(j, path.size() - 1));
	
				break;
			}
		}
	}
	
	ifstream inFile;
    inFile.open(path.append(".txt")); //open the input file

    stringstream strStream;
    strStream << inFile.rdbuf(); //read the file
    string str = strStream.str(); //str holds the content of the file

    map <int, string> r_file;
	for (int t = 0; t < offset.size(); t++){
		if ((is_key[t]) && (opcode[t] == '+')) {
			r_file[offset[t].first] = char_bank[t];
		}
	}

	int myshifts[] = {-1, -2, -3, 1, -4, -5, 2, -6, -7, -8, 3, -9, -10, 4, -11, -12, 5, -13, -14, -15, 6, -16, -17, -18, 7, -19, -20, -21, 8 };
  	vector<int> shifts (myshifts, myshifts + sizeof(myshifts) / sizeof(int) );

  	vector<pair<int, pair<int, int> > > to_shift;

  	for (int j = 0; j < shifts.size(); j++) {
		int sh = shifts[j];
		int from_pos = 0; int last_pos;
		int in_a_row = 0; int didit = 0;
		for (map<int, string>::iterator it = r_file.begin(); it != r_file.end(); it++) {
			if ((0 <= sh + it->first) && (sh + it->first < str.size())) {
				if ((str.substr(sh + it->first, 1) == it->second) || (it->second == "\\n")) {
					if (in_a_row == 0) {
						from_pos = it->first;
					}
					in_a_row ++;
				} else {
					if (in_a_row > 20) {
						// SHIFT
						if (to_shift.size() >= 1){
							if ((to_shift.back().first == sh) && (to_shift.back().second.second + 2 == from_pos)){
								to_shift.back().second.second = it->first - 1;
								didit = 1;
							}
						}
						if (didit) { didit = 0; } else { to_shift.push_back(make_pair(sh, make_pair(from_pos, it->first - 1))); }
					}
					in_a_row = 0;
				}
			}
			last_pos = it->first;
		}
		if (in_a_row > 20) {
			if (to_shift.size() >= 1){
				if ((to_shift.back().first == sh) && (to_shift.back().second.second + 2 == from_pos)){
					to_shift.back().second.second = last_pos - 1;
					didit = 1;
				}
			}
			if (didit) { didit = 0; } else { to_shift.push_back(make_pair(sh, make_pair(from_pos, last_pos - 1))); }
		}
	}

	for (int j = 0; j < to_shift.size(); j++) {
		cerr << "			Shifting by " << to_shift[j].first << " between positions " << to_shift[j].second.first << " and " << to_shift[j].second.second << "\n";
		for (int t = 0; t < offset.size(); t++) {
			if ((is_key[t]) && (offset[t].first >= to_shift[j].second.first) && (offset[t].first <= to_shift[j].second.second)) {
				offset[t].first += to_shift[j].first;
			}
		}
	}

	for (int t = 0; t < offset.size(); t++) {
		if (is_key[t]) {
			cout << et[t] - st[t] << "," << et[t] << ",\"" << char_bank[t] << "\"," << offset[t].first << "," << opcode[t] << "," << newpath << "\n";
		}
	}
	
	return 0;
}
