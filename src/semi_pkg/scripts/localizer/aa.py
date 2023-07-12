import numpy as np

def moving_average(data, window_size):
    # 이동 평균 계산을 위해 필요한 윈도우 크기보다 작은 경우 예외 처리
    if len(data) < window_size:
        raise ValueError("데이터 크기가 윈도우 크기보다 작습니다.")
    
    # 이동 평균 계산
    weights = np.repeat(1.0, window_size) / window_size
    ma = np.convolve(data, weights, 'valid')
    
    return ma

# 테스트용 데이터 생성
data = np.array([1, 2, 3, 4, 6, 6, 6, 8, 9, 10])

# 이동 평균 계산 (윈도우 크기: 3)
ma = moving_average(data, 3)

# 결과 출력
print("원본 데이터:", data)
print("이동 평균 결과:", ma)