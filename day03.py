

import random

secret_number=random.randint(1,100)
guess_count=0

print("欢迎来到猜数字游戏，我已经想到了一个1-100之间的数字。")

while True:
    guess=input("请输入你猜测的数字：")
    guess=int(guess)
    guess_count+=1

    if guess>secret_number:
        print("太大了，再试试！")
    elif guess<secret_number:
        print("太小了，再试试！")
    else:
        print(f"恭喜你，猜对了！你一共猜了{guess_count}次。")
        break

