import numpy as np

class Board(object):
    def __init__(self):
        #ボードの初期化を行います．
        print('initializing board')
        self.B_SIZE = 8
        self.board = np.zeros((self.B_SIZE, self.B_SIZE))
        cnt = self.B_SIZE // 2
        self.board[cnt, cnt] = 1
        self.board[cnt-1, cnt-1] = 1
        self.board[cnt, cnt-1] = 2
        self.board[cnt-1, cnt] = 2
        self.show_board()
        print('')
    def show_board(self):
        #描画
        display=self.board
        display=np.where(display==1, '◯', display)
        display=np.where(display=='2.0', '●', display)
        display=np.where(display=='3.0', '×', display)
        display=np.where(display=='0.0', '⬜︎', display)
        num = np.array([['0','1','2','3','4','5','6','7']])
        display = np.vstack([num, display])
        num = np.array([[' ', '0','1','2','3','4','5','6','7']]).T
        display = np.hstack([num, display])
        self.count_stone()
        print(display)
    def where_stone(self, own):
        #今どの位置に石が置いてあるかを確認します．
        arr_y, arr_x = np.where(self.board==own)
        arr_yx = np.array([arr_y,arr_x]).T
        return arr_yx

    def suggest_stone(self, enem, own):
        #石を置ける候補地を提案します．
        self.board = np.where(self.board==3,0,self.board)
        arr_yx = self.where_stone(own)
        num = arr_yx.shape[0]
        xy_num = []
        direc=[-1, 0, 1]
        #置いてある石の周りを見ていきます．
        for i in range(num):
            #2重for文で左上から下に右に．
            for j in direc:
                for k in direc:
                    if j == 0 and k == 0:
                        continue
                    depth = 0
                    tmp = []
                    while True:
                        depth+=1
                        ry = arr_yx[i][0]+k*depth
                        rx = arr_yx[i][1]+j*depth
                        #壁にめり込まないように
                        if 0 <= rx < self.B_SIZE and 0 <= ry < self.B_SIZE:
                            #進行方向に同じ石がある場合はさらに奥を見る
                            if self.board[ry, rx] == 0:
                                #真横に石がない場合はbreak
                                #連続した後にあった場合は登録してbreak
                                if tmp!=[]:
                                    tmp.append((ry, rx))
                                    xy_num.append([[ry,rx],tmp])
                                    self.board[ry, rx] = 3
                                break
                            if self.board[ry, rx] == own:
                                #真横が自分自身だった場合はbreak
                                break
                            elif self.board[ry, rx] == enem:
                                #真横が相手だった場合はtmpに登録して次のループに
                                tmp.append((ry, rx))
                            elif self.board[ry, rx] == 3:
                                tmp.append((ry, rx))
                                xy_num.append([[ry,rx],tmp])
                                self.board[ry, rx] = 3
                                break
                        else:
                            break
        return xy_num

    def reverse(self, pcolor):
        #石をひっくり返す処理
        #敵味方判別
        if pcolor==1:
            own=1
            enem=2
            color='◯'
        else:
            own=2
            enem=1
            color='●'
        xy_num = self.suggest_stone(enem, own)
        candidate = self.where_stone(3)
        if candidate.shape[0]<1:
            print('候補地が見つかりませんでした．相手ターンになります．')
        else:
            self.show_board()
            print('候補地です．左側の番号を選んでください(user{}){}'.format(own, color))
            print('  [y x]')
            for i, cand in enumerate(candidate):
                print(i, cand)
            print('v')
            stn_idx=100
            try:
                stn_idx=int(input())
            except:
                pass
            if stn_idx==-1:
                print('終了します')
                exit()
            elif candidate.shape[0]<stn_idx:
                print('候補から選んでください')
                self.reverse(pcolor)
            else:
                candidate = candidate.tolist()
                stn = candidate[stn_idx]
                out = []
                #候補地は先に石を置く
                #self.board[stn[0], stn[1]] = own
                #同じ座標が複数枚の石をひっくり返すかもしれない
                for i in range(len(xy_num)):
                    if xy_num[i][0] == stn:
                        out.append(xy_num[i][1])
                #上で同じ座標を一つのリストにしたので実際にひっくり返す
                for i in range(len(out)):
                    for j in range(len(out[i])):
                        self.board[out[i][j][0], out[i][j][1]] = own
                print('')
    def count_stone(self):
        black = self.where_stone(1)
        white = self.where_stone(2)
        print('black:', len(black), 'white:', len(white))
        return len(black), len(white)
class Game(Board):
    def __init__(self, turn=0, start_player=1):
        super().__init__()
        self.player = start_player
        self.turn = turn
    def judge(self):
        black, white = self.count_stone()
        if self.turn>60:
            self.show_board()
            if black>white:
                print('黒の勝ち〜')
            elif black<white:
                print('白の勝ち〜')
            elif black==white:
                print('引き分け')
            exit()
        elif black==0:
            self.show_board()
            print('白の勝ち〜')
            exit()
        elif white==0:
            self.show_board()
            print('黒の勝ち〜')
            exit()
        else:
            pass


    def next_player(self, player):
        if player == 1:
            self.player=2
        else:
            self.player=1
    def player_action(self):
        self.judge()
        self.turn+=1
        print('turn:{}'.format(self.turn))
        self.reverse(self.player)
        self.next_player(self.player)
        self.player_action()

def main():
    print('オセロゲーム')
    game = Game()
    game.player_action()
if __name__=='__main__':
    main()
