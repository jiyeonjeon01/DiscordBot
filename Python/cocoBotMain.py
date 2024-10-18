import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# 필수 intents 설정 (메시지와 멤버 관련 이벤트 허용)
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용 접근 권한

# 봇 생성 시 intents 전달
bot = commands.Bot(command_prefix='!', intents=intents)

user_balances = {}  # 사용자별 잔액을 저장할 딕셔너리
user_last_claim = {}  # 사용자별 마지막 돈 수령 시간을 저장할 딕셔너리

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')

@bot.command()
async def 안녕(ctx):
    await ctx.send('>>> 안녕하세요! 코코봇이에요^^* ''!도움'' 이라는 명령어로 명령어 목록을 보여줄게요')

@bot.command()
async def 누구(ctx):
    await ctx.send('>>> 도박을 하고싶은데 돈이없어서 만든 봇이에요')    

@bot.command()
async def 돈줘(ctx):
    user_id = str(ctx.author.id)
    if user_id not in user_balances:
        user_balances[user_id] = 0  # 처음 돈을 받을 때 초기 잔액 설정
        user_last_claim[user_id] = None  # 마지막 돈 수령 시간 초기화

    if user_last_claim[user_id] is None or (discord.utils.utcnow() - user_last_claim[user_id]).days >= 1:
        user_balances[user_id] += 10000  # 10000원 지급
        user_last_claim[user_id] = discord.utils.utcnow()  # 현재 시간 저장
        await ctx.send(f'>>> {ctx.author.mention}, 10000원이 지급되었습니다. 돈은 하루에 한 번만 받을 수 있습니다.')
    else:
        await ctx.send(f'>>> {ctx.author.mention}, 돈은 하루에 한 번만 받을 수 있습니다.')

@bot.command()
async def 도박(ctx, amount: int):
    user_id = str(ctx.author.id)

    if user_id not in user_balances:
        await ctx.send(f'>>> {ctx.author.mention}, 도박을 하기 전에 먼저 돈을 받아야 합니다.')
        return

    if user_balances[user_id] < amount:
        await ctx.send(f'>>> {ctx.author.mention}, 잔액이 부족합니다. 현재 잔액: {user_balances[user_id]}원')
        return

    # 0부터 99까지의 숫자 중 하나를 랜덤으로 선택
    gamble_result = random.randint(0, 99)

    # 0 ~ 44는 승리 (45%), 45 ~ 99는 패배 (55%)
    if gamble_result < 45:
        user_balances[user_id] += amount  # 돈을 얻음
        await ctx.send(f'>>> {ctx.author.mention}, 축하합니다! {amount}원을 추가로 얻었습니다. 현재 잔액: {user_balances[user_id]}원')
    else:
        user_balances[user_id] -= amount  # 돈을 잃음
        await ctx.send(f'>>> {ctx.author.mention}, 아쉽게도 {amount}원을 잃었습니다. 현재 잔액: {user_balances[user_id]}원')

@bot.command()
async def 도움(ctx):
    help_message = (
        '>>> 다음은 명령어 목록이에요. 필요한 명령어를 입력해보세요.\n'
        '1. !안녕\n'
        '2. !누구\n'
        '3. !돈줘\n'
        '4. !도박'
    )
    await ctx.send(help_message)

# 환경 변수에서 토큰 가져오기
load_dotenv()  # .env 파일 로드
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # 환경 변수에서 토큰 값 가져오기

bot.run(DISCORD_TOKEN)
