import tkinter as tk
from tkinter import messagebox


class WSVGame:

    # =====================================
    # 初始化
    # =====================================

    def __init__(self, root):
        self.root = root
        self.root.title("狼羊菜過河")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # 0 = 左岸
        # 1 = 右岸
        self.farmer = 0
        self.wolf = 0
        self.goat = 0
        self.cabbage = 0

        # 船的位置
        self.boat_side = 0

        # 船上的物品
        self.boat_item = None

        self.steps = 0

        self.create_ui()
        self.draw_game()

    # =====================================
    # 建立介面
    # =====================================

    def create_ui(self):

        title = tk.Label(
            self.root,
            text="狼羊菜過河 🌊",
            font=("Microsoft JhengHei", 26, "bold")
        )
        title.pack(pady=10)

        self.canvas = tk.Canvas(
            self.root,
            width=850,
            height=400,
            bg="lightblue"
        )
        self.canvas.pack()

        self.status_label = tk.Label(
            self.root,
            text="請將狼、羊、菜和農夫全部送到右岸！",
            font=("Microsoft JhengHei", 14)
        )
        self.status_label.pack(pady=5)

        self.step_label = tk.Label(
            self.root,
            text="步數：0",
            font=("Microsoft JhengHei", 12)
        )
        self.step_label.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.cross_button = tk.Button(
            button_frame,
            text="🚤 過河",
            font=("Microsoft JhengHei", 14, "bold"),
            width=10,
            command=self.cross_river
        )
        self.cross_button.grid(row=0, column=0, padx=10)

        self.reset_button = tk.Button(
            button_frame,
            text="🔄 重新開始",
            font=("Microsoft JhengHei", 14),
            width=10,
            command=self.reset_game
        )
        self.reset_button.grid(row=0, column=1, padx=10)

        instruction = tk.Label(
            self.root,
            text="操作：點擊狼、羊或菜上船，再點擊船上的物品即可放回岸上",
            font=("Microsoft JhengHei", 11)
        )
        instruction.pack()

    # =====================================
    # 畫遊戲
    # =====================================

    def draw_game(self):

        self.canvas.delete("all")

        # 左岸
        self.canvas.create_rectangle(
            0, 0, 350, 400,
            fill="#7EC850",
            outline=""
        )

        # 河流
        self.canvas.create_rectangle(
            350, 0, 500, 400,
            fill="#4FA3D1",
            outline=""
        )

        # 右岸
        self.canvas.create_rectangle(
            500, 0, 850, 400,
            fill="#7EC850",
            outline=""
        )

        # 岸邊文字
        self.canvas.create_text(
            175, 30,
            text="左岸",
            font=("Microsoft JhengHei", 20, "bold")
        )

        self.canvas.create_text(
            675, 30,
            text="右岸",
            font=("Microsoft JhengHei", 20, "bold")
        )

        # 畫船
        self.draw_boat()

        # 畫農夫
        self.draw_character(
            "👨",
            self.farmer,
            "farmer"
        )

        # 畫狼
        if self.boat_item != "wolf":
            self.draw_character(
                "🐺",
                self.wolf,
                "wolf"
            )

        # 畫羊
        if self.boat_item != "goat":
            self.draw_character(
                "🐑",
                self.goat,
                "goat"
            )

        # 畫菜
        if self.boat_item != "cabbage":
            self.draw_character(
                "🥬",
                self.cabbage,
                "cabbage"
            )

        # =================================
        # 畫船上的物品
        # =================================

        if self.boat_item == "wolf":

            item = self.canvas.create_text(
                self.get_boat_x(),
                275,
                text="🐺",
                font=("Arial", 40),
                tags="boat_item"
            )

            self.canvas.tag_bind(
                item,
                "<Button-1>",
                lambda event: self.remove_from_boat()
            )

        elif self.boat_item == "goat":

            item = self.canvas.create_text(
                self.get_boat_x(),
                275,
                text="🐑",
                font=("Arial", 40),
                tags="boat_item"
            )

            self.canvas.tag_bind(
                item,
                "<Button-1>",
                lambda event: self.remove_from_boat()
            )

        elif self.boat_item == "cabbage":

            item = self.canvas.create_text(
                self.get_boat_x(),
                275,
                text="🥬",
                font=("Arial", 40),
                tags="boat_item"
            )

            self.canvas.tag_bind(
                item,
                "<Button-1>",
                lambda event: self.remove_from_boat()
            )

    # =====================================
    # 畫人物 / 物品
    # =====================================

    def draw_character(self, emoji, side, item):

        if side == 0:

            positions = {
                "farmer": (100, 100),
                "wolf": (100, 200),
                "goat": (100, 290),
                "cabbage": (220, 200)
            }

        else:

            positions = {
                "farmer": (600, 100),
                "wolf": (600, 200),
                "goat": (600, 290),
                "cabbage": (720, 200)
            }

        x, y = positions[item]

        tag = item

        object_id = self.canvas.create_text(
            x,
            y,
            text=emoji,
            font=("Arial", 45),
            tags=tag
        )

        # 只有狼、羊、菜可以點
        if item != "farmer":

            self.canvas.tag_bind(
                object_id,
                "<Button-1>",
                lambda event, i=item: self.select_item(i)
            )

    # =====================================
    # 畫船
    # =====================================

    def draw_boat(self):

        x = self.get_boat_x()

        self.canvas.create_polygon(
            x - 70, 300,
            x + 70, 300,
            x + 50, 350,
            x - 50, 350,
            fill="#8B4513",
            outline="black",
            width=2
        )

    # =====================================
    # 船的位置
    # =====================================

    def get_boat_x(self):

        if self.boat_side == 0:
            return 275
        else:
            return 575

    # =====================================
    # 點擊岸上的物品
    # =====================================

    def select_item(self, item):

        item_side = getattr(self, item)

        # 必須跟農夫同一岸
        if item_side != self.farmer:

            self.status_label.config(
                text="❌ 農夫必須和物品在同一岸！"
            )

            return

        # 船上已經有東西
        if self.boat_item is not None:

            self.status_label.config(
                text="❌ 船上已經有一個物品了！"
            )

            return

        # 放上船
        self.boat_item = item

        self.status_label.config(
            text=f"🐾 {self.get_item_name(item)} 已經上船！"
        )

        self.draw_game()

    # =====================================
    # 把船上的物品放回岸上
    # =====================================

    def remove_from_boat(self):

        if self.boat_item is None:
            return

        item = self.boat_item

        # 放回船目前所在的岸
        setattr(
            self,
            item,
            self.boat_side
        )

        self.boat_item = None

        self.status_label.config(
            text=f"↩️ {self.get_item_name(item)} 已放回岸上！"
        )

        self.draw_game()

    # =====================================
    # 過河
    # =====================================

    def cross_river(self):

        # 農夫必須和船在同一岸
        if self.farmer != self.boat_side:

            self.status_label.config(
                text="❌ 農夫不在船所在的岸！"
            )

            return

        # 農夫過河
        self.farmer = 1 - self.farmer

        # 船過河
        self.boat_side = 1 - self.boat_side

        # 船上的物品一起過河
        if self.boat_item is not None:

            setattr(
                self,
                self.boat_item,
                self.farmer
            )

            self.boat_item = None

        self.steps += 1

        self.step_label.config(
            text=f"步數：{self.steps}"
        )

        self.draw_game()

        # 檢查失敗
        if self.check_game_over():
            return

        # 檢查成功
        if self.check_win():

            messagebox.showinfo(
                "🎉 恭喜過關！",
                f"你成功把狼、羊、菜全部送到右岸！\n\n"
                f"總共使用 {self.steps} 步。"
            )

            self.status_label.config(
                text="🎉 恭喜！你成功完成遊戲！"
            )

    # =====================================
    # 遊戲失敗判斷
    # =====================================

    def check_game_over(self):

        # 農夫不在羊旁邊
        if self.farmer != self.goat:

            # 狼和羊在一起
            if self.wolf == self.goat:

                messagebox.showerror(
                    "❌ 遊戲失敗",
                    "狼把羊吃掉了！"
                )

                self.status_label.config(
                    text="❌ 狼把羊吃掉了！請重新開始。"
                )

                return True

            # 羊和菜在一起
            if self.goat == self.cabbage:

                messagebox.showerror(
                    "❌ 遊戲失敗",
                    "羊把菜吃掉了！"
                )

                self.status_label.config(
                    text="❌ 羊把菜吃掉了！請重新開始。"
                )

                return True

        return False

    # =====================================
    # 勝利判斷
    # =====================================

    def check_win(self):

        return (
            self.farmer == 1
            and self.wolf == 1
            and self.goat == 1
            and self.cabbage == 1
        )

    # =====================================
    # 重新開始
    # =====================================

    def reset_game(self):

        self.farmer = 0
        self.wolf = 0
        self.goat = 0
        self.cabbage = 0

        self.boat_side = 0
        self.boat_item = None

        self.steps = 0

        self.status_label.config(
            text="請將狼、羊、菜和農夫全部送到右岸！"
        )

        self.step_label.config(
            text="步數：0"
        )

        self.draw_game()

    # =====================================
    # 中文名稱
    # =====================================

    def get_item_name(self, item):

        names = {
            "wolf": "狼",
            "goat": "羊",
            "cabbage": "菜"
        }

        return names[item]


# ==========================================
# 啟動程式
# ==========================================

root = tk.Tk()

game = WSVGame(root)

root.mainloop()