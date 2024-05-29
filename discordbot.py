from cmath import log
from distutils.sysconfig import PREFIX
import bs4_meal
import station
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.environ["TOKEN"]
bot = commands.Bot()

@bot.event
async def on_ready():
    print("The bot is ready!")  # 봇이 로그인 및 설정을 마치면 호출되는 함수

@bot.slash_command()
async def 막차시간(inter, *, line):  # '막차시간'이라는 슬래시 커맨드를 정의하며 'line'이라는 파라미터를 받음
    await inter.response.defer()  # 열차시간 크롤링에 시간이 걸려 지연
    try:
        line_color = 0x000000
        line_name = ""

        if line == "1":
            line_color = 0x00A4E3
            line_name = "4호선"

        elif line == "2":
            line_color = 0xFABE00
            line_name = "수인분당선"

        embed = disnake.Embed(title=f"{line_name} 정왕역 막차", color=line_color)  # 제목이 "정왕역 막차"인 임베드 메시지 생성
        real_last_canival = station.station(line)  # 'line'을 인자로 하여 station__ 모듈의 station 함수를 호출
        for canival in real_last_canival:  # 결과를 반복
            embed.add_field(name="\u200b", value=str(canival), inline=False)  # 각 결과를 임베드 필드로 추가
            embed.set_footer(text="본 정보는 네이버 검색 결과를 바탕으로 제공됩니다")    # 출처를 임베드 필드 아래로 추가

        await inter.edit_original_response(embed=embed)  # 원본 응답을 임베드 메시지로 수정

    except Exception as e:  # 예외 발생 시
        await inter.edit_original_response(content=f"오류가 발생했습니다...!: {e}")  # 원본 응답을 오류 메시지로 수정

@bot.slash_command()
async def tip학식(inter):  # 'tip학식'이라는 슬래시 커맨드를 정의
    try:
        bs4_meal.get_meal()  # bs4_meal 모듈의 get_meal 함수를 호출하여 학식 정보 스크래핑
        file_path_tip = './0.jpg'  # 학식 이미지 경로 설정
        img_file_tip = disnake.File(file_path_tip)  # 이미지 경로를 사용하여 File 객체 생성

        await inter.response.send_message("## 금주 TIP 지하 학식입니다!", file=img_file_tip)  # 이미지 파일과 함께 메시지 전송
    except Exception as e:  # 예외 발생 시
        await inter.response.send_message(f"오류가 발생했습니다...!: \n {e}")  # 오류 메시지 전송

@bot.slash_command()
async def e동학식(inter):  # 'e동학식'이라는 슬래시 커맨드를 정의
    try:
        bs4_meal.get_meal()  # bs4_meal 모듈의 get_meal 함수를 호출하여 학식 정보 스크래핑
        file_path_E = "./1.jpg"  # 학식 이미지 경로 설정
        img_file_E = disnake.File(file_path_E)  # 이미지 경로를 사용하여 File 객체 생성

        await inter.response.send_message("## 금주 E동 학식입니다!", file=img_file_E)  # 이미지 파일과 함께 메시지 전송
    except Exception as e:  # 예외 발생 시
        await inter.edit_original_response(f"오류가 발생했습니다...!: \n {e}")  # 원본 응답을 오류 메시지로 수정

bot.run(BOT_TOKEN)  # 주어진 토큰을 사용하여 봇 실행
