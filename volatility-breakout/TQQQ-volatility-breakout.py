import pandas as pd

# CSV 데이터를 DataFrame으로 읽어들임
data = pd.read_csv('data/TQQQ.csv')
data = data[::-1].reset_index(drop=True)  # 데이터를 오름차순으로 정렬

# 변동성 돌파 전략에 사용될 비율 k 설정
k = 0

# 초기 자본과 매매 결과를 저장할 리스트 초기화
initial_capital = 10000  # 초기 자본금
capital = initial_capital
positions = []  # 매매 기록을 저장할 리스트
fee = 0.002 # 수수료 0.2%

# 변동성 돌파 전략 실행
for i in range(1, len(data)):

    # 전일 데이터
    previous_row = data.iloc[i - 1]
    # 목표 가격 계산
    target_price = previous_row['close'] + (previous_row['high'] - previous_row['low']) * k

    # 당일 데이터
    current_row = data.iloc[i]

    # 매수 조건: 당일 목표가 달성 시 매수
    if current_row['high'] > target_price:
        # 실제 매수 가능한 자본을 수수료를 고려하여 계산
        available_capital_for_buy = capital * (1 - fee)

        # 매수 가격 결정
        buy_price = max(target_price, current_row['low'])  # 목표 가격이나 저가 중 높은 가격으로 매수

        # 매수 수량 결정 (수수료를 제외한 자본으로 계산)
        buy_quantity = available_capital_for_buy / buy_price

        # 매수에 사용될 실제 금액 계산
        actual_buy_cost = buy_price * buy_quantity
        capital = 0

        # 매도 시 종가에 매도하고 수수료 적용
        sell_price = current_row['close']
        sell_revenue = sell_price * buy_quantity

        # 매도 수수료 적용
        actual_sell_revenue = sell_revenue * (1 - fee)

        # 자본에 매도 수익 추가
        capital += actual_sell_revenue

        # 수익률 계산
        profit = (sell_price - buy_price) / buy_price - 2 * fee  # 매수, 매도 시 수수료 고려
        print(f"날짜: {current_row['date']}, 매수가: {buy_price}, 매도가: {sell_price}, 수익률: {profit * 100:.2f}%, 자본: {capital}")

# 전체 수익률 계산
total_return = (capital - initial_capital) / initial_capital

print(f"최종 자본: {capital}, 총 수익률: {total_return * 100:.2f}%")

# 매매 없이 보유한 경우의 수익률 계산
buy_and_hold_return = (data.iloc[-1]['close'] - data.iloc[0]['close']) / data.iloc[0]['close']
print(f"매수가: {data.iloc[0]['close']}, 매도가: {data.iloc[-1]['close']}")
print(f"보유한 경우의 수익률: {buy_and_hold_return * 100:.2f}%")