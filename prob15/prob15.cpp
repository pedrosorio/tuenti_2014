#include <iostream>

using namespace std;

#define ull unsigned long long

/*
Representing the game as two 64-bit integers white board and black board
*/

//preferred moves in the upper left quadrant - highest probability of converting a corner
//and not giving a corner to the opponent
const int pref_moves_r[] = {0, 0, 2, 2, 0, 3, 2, 3, 3, 1, 1, 2, 3, 0, 1, 1};
const int pref_moves_c[] = {0, 2, 0, 2, 3, 0, 3, 2, 3, 2, 3, 1, 1, 1, 0, 1};

//bitwise operations for checking pieces and removing them
inline bool has_piece(ull board, int r, int c) {
	return board & (1LL << (8*r+c));
}

inline ull put_piece(ull board, int r, int c) {
	return board | (1LL << (8*r+c));
}

//Return a bitwise representation of the positions in the board that are flipped by a move
//in (r,c) - 0 if the move is not valid
ull get_move(ull my_board, ull opp_board, int r, int c) {
	ull move = 0;
	for (int mr = -1; mr <= 1; mr++) {
		for (int mc = -1; mc <= 1; mc++) {
			if (mr == 0 && mc == 0)
				continue;
			int mv = 1;
			int nr = r + mr;
			int nc = c + mc;
			bool possible_move = false;
			while (true) {
				//out of bounds
				if (nr == 8 || nr == -1 || nc == 8 || nc == -1)
					break;
				if (!has_piece(opp_board, nr, nc)) {
					if (has_piece(my_board, nr, nc)) {
						possible_move = (mv > 1);
					}
					break;
				}
				mv += 1;
				nr += mr;
				nc += mc;
			}

			if (possible_move) {
				do {
					mv--;
					nr -= mr;
					nc -= mc;
					move = put_piece(move, nr, nc);
				} while (mv > 1);
			}
		}
	}
	return move;
}

//Recursively check if there is a move to corner
//When it is the player's turn, returns the first move (r,c) as an integer in (1,64) -> (8*r+c+1)
//that ensures a corner will be attained.
//when it is the opponent's turn, returns 0 when (if) it finds a move that ensures the player will not attain a corner in the specified number of moves
//otherwise, it returns some positive integer in (1,64)
int move_to_corner(ull my_board, ull opp_board, bool my_turn, int moves_left) {
	if (moves_left < 1) {
		return 0;
	}
	ull filled_board = my_board | opp_board;
	ull move;
	int to_corner = 0;
	int new_moves_left = my_turn ? moves_left : moves_left - 1;
	bool made_move = false;
	for (int move_id = 0; move_id < 16; move_id++) {
		for (int shift_r = 0; shift_r < 2; shift_r++) {
			int r = (shift_r) ? 7 - pref_moves_r[move_id] : pref_moves_r[move_id];
			for (int shift_c = 0; shift_c < 2; shift_c++) {
				int c = (shift_c) ? 7 - pref_moves_c[move_id] : pref_moves_c[move_id];
				if (!has_piece(filled_board, r, c)) {
					move = get_move(my_board, opp_board, r, c);
					if (move) {
						if (my_turn && ((r == 0 && c == 0) || (r == 0 && c == 7) || (r == 7 && c == 0) || (r == 7 && c == 7))) {
							return 8*r+c+1;
						}
						made_move = true;
						to_corner = move_to_corner(opp_board & ~move, put_piece(my_board, r, c) | move, !my_turn, new_moves_left);

						//if the player has a move that achieves a corner, return it immediately
						if (my_turn && to_corner) {
							return 8*r+c+1;
						}
						//if the opponent has a move that makes it impossible to make a corner, return immediately
						if (!my_turn && !to_corner) {
							return 0;
						}
					}
				}
			}
		}
	}
	//ensure that skipping is considered
	//this will produce weird results if the first move of the player that wins is to skip
	if (!made_move) {
		to_corner = move_to_corner(opp_board, my_board, !my_turn, new_moves_left);
	}
	return to_corner;
}

int main() {
	int N,moves,result;
	string player, in, row;
	cin >> N;
	for (int test = 1; test <= N; test++) {
		cin >> player >> in >> moves;
		ull white_board = 0, black_board = 0;
		for (int r = 0; r < 8; r++) {
			cin >> row;
			for (int c = 0; c < 8; c++) {
				if(row[c] == 'X') {
					black_board = put_piece(black_board, r, c);
				}
				if (row[c] == 'O') {
					white_board = put_piece(white_board, r, c);
				}
			}
		}
		if (player[0] == 'W') {
			result = move_to_corner(white_board, black_board, true, moves);
		} else {
			result = move_to_corner(black_board, white_board, true, moves);
		}
		if (result == 0) {
			cout << "Impossible" << endl;
		} else {
			result--;
			int row = 1 + result/8;
			char col = 'a' + result%8;
			cout << col << row << endl;
		}
	}
	return 0;
}