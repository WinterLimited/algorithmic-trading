import pyupbit
import pandas as pd

def fetch_data(ticker="KRW-BTC", interval="minute3", count=400):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    return df


# RSI 계산
def calculate_rsi(df, periods=14):

    # 1일 종가 차이 계산
    delta = df['close'].diff(1)

    # 1일 종가 차이 중 양수만 추출하여 평균 계산
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()

    # 1일 종가 차이 중 음수만 추출하여 평균 계산
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()

    # RS(Relative Strength) 계산
    RS = gain / loss

    # RSI(Relative Strength Index) 계산
    df['RSI'] = 100 - (100 / (1 + RS))

    return df

def main():
    df = fetch_data()
    df = calculate_rsi(df)
    initial_capital = 200000
    fee = 0.0005
    capital = initial_capital
    position_open = False
    win = 0
    lose = 0
    last_rsi_high = 0
    last_rsi_low = float('inf')
    prev_rsi = 0

    for idx, row in df.iterrows():
        current_rsi = row['RSI']

        # 매매 조건
        # 1. 마지막 고가를 RSI가 50 이하로 내려갈 때 직전 고가로 설정
        # 2. RSI가 50 이하일 때, 기록한 저가를 갱신
        # 3. 기록된 고가와 저가를 기반으로 목표가 및 손절가 설정

        if prev_rsi > 50 and current_rsi <= 50:
            # RSI가 50 이상에서 50 이하로 내려갔을 때의 처리
            last_rsi_high = df.iloc[idx - 1]['high']  # 이전 행의 고가를 사용
            last_rsi_low = float('inf')  # 다시 초기화

        elif current_rsi < 50:
            # RSI가 50 이하일 때의 처리
            last_rsi_low = min(last_rsi_low, row['low'])

        # 고가와 저가가 설정되어 있을 때 매매 조건 검사
        if last_rsi_high > 0 & last_rsi_high < last_rsi_low:
            # 목표가 계산
            target_price = last_rsi_high + (last_rsi_high - last_rsi_low)

            # 손절가 계산
            stop_loss_price = target_price * 0.98

            print(f"현재시간: {idx}, 현재가: {row['close']}"
                  f" 목표가: {target_price:.2f}, 손절가: {stop_loss_price:.2f}")

            # 매수 조건 검사: 현재 가격이 이전 신고가를 도달하면 매수
            if not position_open and row['high'] > last_rsi_high:
                buy_price = last_rsi_high

                # 자본 대비 매수량
                buy_amount = capital * (1 - fee) / buy_price
                capital = 0
                position_open = True
                print(f"매수 시간: {idx}, 매수 가격: {buy_price:.2f}")

            # 매도 조건 검사: 목표가 도달 또는 손절 조건
            if position_open:
                if row['low'] < stop_loss_price or row['high'] > target_price:
                    sell_price = target_price

                    # 매수량 대비 매도량
                    sell_amount = buy_amount * sell_price * (1 - fee)
                    capital += sell_amount
                    position_open = False

                    if row['high'] > target_price:
                        win += 1
                    else:
                        lose += 1

                    # 조건 변수 초기화
                    last_rsi_high = 0
                    last_rsi_low = 0
                    target_price = 0
                    stop_loss_price = 0

                    print(f"매도 시간: {df.index[idx]}, 매도 가격: {sell_price:.2f}, 현재 자본: {capital:.2f}원")

    # print(f"최종 자본: {capital:.2f}, 승: {win}, 패: {lose} 승률: {win / (win + lose) * 100:.2f}%, 최종 수익률: {(capital / 200000 - 1) * 100:.2f}%")

if __name__ == "__main__":
    main()
