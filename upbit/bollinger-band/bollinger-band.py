import pyupbit
import pandas as pd

def fetch_data(ticker="KRW-BTC", interval="minute5", count=200):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    return df

# Bollinger Bands 계산
def calculate_bollinger_bands(df, window=20):

    # 이동평균(Moving Average)
    df['MA'] = df['close'].rolling(window=window).mean()

    # 표준편차(Standard Deviation)
    df['STD'] = df['close'].rolling(window=window).std(ddof=0)

    # 20기간 표준편차(Standard Deviation)

    # Bollinger Bands's Upper: MA + (20기간 표준편차 * 2)
    df['Upper'] = df['MA'] + (df['STD'] * 2)

    # Bollinger Bands's Lower: MA - (20기간 표준편차 * 2)
    df['Lower'] = df['MA'] - (df['STD'] * 2)

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

def trading_signal(df):

    # 매수 신호: 하한가가 Bollinger Bands의 Lower 밴드 아래에 있을 때
    df['BuySignal'] = (df['low'] < df['Lower'])

    # 매도 신호: 상한가가 Bollinger Bands의 Upper 밴드 위에 있을 때
    df['SellSignal'] = (df['high'] > df['Upper'])


    return df

def main():
    initial_capital = 200000
    fee = 0.0005
    win = 0
    lose = 0
    df = fetch_data()
    df = calculate_bollinger_bands(df)
    df = calculate_rsi(df)
    df = trading_signal(df)

    capital = initial_capital
    position_open = False
    buy_price = 0

    for idx, row in df.iterrows():
        if not position_open and row['BuySignal']:
            buy_price = row['Lower']

            # 자본 대비 매수량
            buy_amount = capital * (1 - fee) / buy_price
            capital = 0
            position_open = True
            print(f"매수 시간: {idx}, 매수 가격: {buy_price:.2f}")
        elif position_open and (row['SellSignal']
                                # 손절 기준 추가
                                or row['low'] < buy_price * 0.99):
            if row['SellSignal']:
                sell_price = row['Upper']
                win += 1
            else:
                sell_price = row['low']
                lose += 1

            # 매수량 대비 매도량
            sell_amount = buy_amount * sell_price * (1 - fee)
            capital += sell_amount
            position_open = False
            print(f"매도 시간: {idx}, 매도 가격: {sell_price:.2f}, 현재 자본: {capital:.2f}원, 수익률: {(sell_price / buy_price - 1) * 100:.2f}%")

    print(f"최종 자본: {capital:.2f}, 승: {win}, 패: {lose} 승률: {win / (win + lose) * 100:.2f}%, 최종 수익률: {(capital / 200000 - 1) * 100:.2f}%")


if __name__ == "__main__":
    main()
