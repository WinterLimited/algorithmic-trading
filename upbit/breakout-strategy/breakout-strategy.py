import pyupbit
import pandas as pd
import time

def fetch_data(ticker="KRW-BTC", interval="day", count=100, rounds=1):
    final_df = pd.DataFrame()
    last_date = None
    for _ in range(rounds):
        df = pyupbit.get_ohlcv(ticker, interval=interval, count=count, to=last_date)
        if df is not None and not df.empty:
            final_df = pd.concat([df, final_df])
            last_date = df.index[0]
            time.sleep(0.1)  # API 요청 간격 준수
        else:
            break
    final_df = final_df.sort_index()
    return final_df

def calculate_target_price(df):
    df['Range'] = df['high'] - df['low']
    df['TargetPrice'] = df['open'] + df['Range'].shift(1) * 0.032  # 변동성 돌파 전략 대상 가격
    return df

def main():
    initial_capital = 200000  # 초기 자본
    fee = 0.0005  # 수수료
    win = 0
    lose = 0
    capital = initial_capital
    df = fetch_data(interval="day")  # 5분봉 데이터 가져오기
    df = calculate_target_price(df)

    for idx, row in df.iterrows():
        if row['high'] > row['TargetPrice']:  # 현재 가격이 매수 목표가를 돌파한 경우 매수
            actual_buy_price = min(row['TargetPrice'], row['high'])  # 실제 매수 가격은 목표가와 고가 중 낮은 가격

            # 자본 대비 매수량
            buy_amount = capital * (1 - fee) / actual_buy_price
            capital = 0
            print(f"매수 시간: {idx}, 매수 가격: {actual_buy_price:.2f}")

            # 매도 가격: 해당 5분봉의 종가
            actual_sell_price = row['close']

            # 매도량
            capital += buy_amount * actual_sell_price * (1 - fee)
            profit = actual_sell_price / actual_buy_price - 1
            if profit > 0:
                win += 1
            else:
                lose += 1

            print(f"매도 시간: {idx}, 매도 가격: {actual_sell_price:.2f}, 현재 자본: {capital:.2f}원, 수익률: {(actual_sell_price / actual_buy_price - 1):.2%}")

    print(f"최종 자본: {capital:.2f}원, 승: {win}, 패: {lose}, 승률: {win / (win + lose):.2%} 최종 수익률: {(capital / initial_capital - 1):.2%}")

if __name__ == "__main__":
    main()

