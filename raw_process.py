"""
RAW画像処理ライブラリ。
"""

import numpy as np
import scipy
from numpy.lib.stride_tricks import as_strided
from scipy import signal


def white_balance(raw_array, wb_gain, raw_colors):
    """
    ホワイトバランス補正処理を行う。

    Parameters
    ----------
    raw_array: numpy array
        入力BayerRAW画像データ。
    wb_gain: float[4]
        ホワイトバランスゲイン。
    raw_colors: int[h, w]
        RAW画像のカラーチャンネルマトリクス。

    Returns
    -------
    wb_img: numpy array
        出力RAW画像。
    """
    norm = wb_gain[1]
    gain_matrix = np.zeros(raw_array.shape)
    for color in (0, 1, 2, 3):
        gain_matrix[raw_colors == color] = wb_gain[color] / norm
    wb_img = raw_array * gain_matrix
    return wb_img


def simple_demosaic(raw_array, bayer_pattern):
    """
    簡易デモザイク処理を行う。

    Parameters
    ----------
    raw_array: numpy array
        入力BayerRAW画像データ
    bayer_pattern: int[2, 2]
        ベイヤーパターン。0:赤、1:緑、2:青、3:緑。

    Returns
    -------
    dms_img: numpy array
        出力RGB画像。サイズは入力の縦横共に1/2。
    """
    height, width = raw_array.shape
    dms_img = np.zeros((height//2, width//2, 3))
    bayer_pattern[bayer_pattern == 3] = 1
    dms_img[:, :, bayer_pattern[0, 0]] = raw_array[0::2, 0::2]
    dms_img[:, :, bayer_pattern[0, 1]] += raw_array[0::2, 1::2]
    dms_img[:, :, bayer_pattern[1, 0]] += raw_array[1::2, 0::2]
    dms_img[:, :, bayer_pattern[1, 1]] += raw_array[1::2, 1::2]
    dms_img[:, :, 1] /= 2
    return dms_img


def black_level_correction(raw_array, blc, bayer_pattern):
    """
    ブラックレベル補正処理を行う。

    Parameters
    ----------
    raw_array: numpy array
        入力BayerRAW画像データ。
    blc: float[4]
        各カラーチャンネルごとのブラックレベル。
    bayer_pattern: int[2, 2]
        ベイヤーパターン。0:赤、1:緑、2:青、3:緑。

    Returns
    -------
    blc_raw: numpy array
        出力RAW画像。
    """
    # 符号付き整数として入力画像をコピー
    blc_raw = raw_array.astype('int')
    # 各カラーチャンネル毎にブラックレベルを引く。
    blc_raw[0::2, 0::2] -= blc[bayer_pattern[0, 0]]
    blc_raw[0::2, 1::2] -= blc[bayer_pattern[0, 1]]
    blc_raw[1::2, 0::2] -= blc[bayer_pattern[1, 0]]
    blc_raw[1::2, 1::2] -= blc[bayer_pattern[1, 1]]
    return blc_raw


def gamma_correction(input_img, gamma):
    """
    ガンマ補正処理を行う。

    Parameters
    ----------
    input_img: numpy array [h, w, 3]
        入力RGB画像データ。
        0-1の範囲で正規化されていること。
    gamma: float
        ガンマ補正値。通常は2.2。

    Returns
    -------
    gamma_img: numpy array [h, 2, 3]
        出力RGB画像。
    """
    # デモザイク後の画像をコピー。
    gamma_img = input_img.copy()
    gamma_img[gamma_img < 0] = 0
    gamma_img[gamma_img > 1] = 1.0
    # numpyのpower関数を使って、ガンマ関数を適用。
    gamma_img = np.power(gamma_img, 1/gamma)
    return gamma_img


def demosaic(raw_array, raw_colors):
    """
    線形補間でデモザイクを行う

    Parameters
    ----------
    raw_array: numpy array
        入力BayerRAW画像データ。
    raw_colors: numpy array
        RAW画像のカラーチャンネルマトリクス。
        通常Rawpyのraw_colorsを用いて与える。

    Returns
    -------
    dms_img: numpy array
        出力RAW画像。
    """
    h, w = raw_array.shape
    dms_img = np.zeros((h, w, 3))

    # 緑画素の処理
    # 元のRAW画像から緑画素だけ抜き出す
    green = raw_array.copy()
    green[(raw_colors == 0) | (raw_colors == 2)] = 0
    # 緑画素の線形補間フィルター
    # [[0, 1, 0]]
    #  [1, 4, 1]
    #  [0, 1, 0]] / 4.0
    g_flt = np.array([[0, 1, 0], [1, 4, 1], [0, 1, 0]]) / 4.0
    # フィルターの適用
    # boundary='symm': 画像のヘリで折り返す。
    # mode='same': 出力画像サイズは入力画像と同じ。
    dms_img[:, :, 1] = signal.convolve2d(green, g_flt, boundary='symm', mode='same')

    # 元のRAW画像から赤画素だけ抜き出す
    red = raw_array.copy()
    red[raw_colors != 0] = 0
    # 赤画素の線形補間フィルター
    # [[1, 2, 1]]
    #  [2, 4, 2]
    #  [1, 2, 1]] / 4.0
    rb_flt = np.array([[1 / 4, 1 / 2, 1 / 4], [1 / 2, 1, 1 / 2], [1 / 4, 1 / 2, 1 / 4]])
    # フィルターの適用
    dms_img[:, :, 0] = signal.convolve2d(red, rb_flt, boundary='symm', mode='same')

    # 元のRAW画像から青画素だけ抜き出す
    blue = raw_array.copy()
    blue[raw_colors != 2] = 0
    # 青画素の線形補間フィルターは赤と共通
    # フィルターの適用
    dms_img[:, :, 2] = signal.convolve2d(blue, rb_flt, boundary='symm', mode='same')
    return dms_img


def defect_correction(raw_array, threshold):
    """
    線形補間でデモザイクを行う

    Parameters
    ----------
    raw_array: numpy array
        入力BayerRAW画像データ。
    threshold: int
        欠陥画素判定の閾値。
        10bitRAW入力に対して典型的には16程度。

    Returns
    -------
    dpc_raw: numpy array
        出力RAW画像。
    """
    dpc_raw = raw_array.copy()
    # footprintとして5x5のマスクを作成
    # [[1 1 1 1 1]
    #  [1 1 1 1 1]
    #  [1 1 0 1 1]
    #  [1 1 1 1 1]
    #  [1 1 1 1 1]]
    footprint = np.ones((5, 5))
    footprint[2, 2] = 0
    # 各カラーごとの処理。左上(0, 0)、左下(1, 0), 右上(0, 1), 右下(1, 1)
    for (yo, xo) in ((0, 0), (1, 0), (0, 1), (1, 1)):
        single_channel = dpc_raw[yo::2, xo::2]
        # 上下左右の平均をとるフィルター
        flt = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / 4
        # 上下左右の平均値をとった画像の作成
        average = scipy.signal.convolve2d(single_channel, flt, mode='same')
        # 周辺画像の最大値を求める。footprintにより、対象となる画素は含めない。
        local_max = scipy.ndimage.filters.maximum_filter(single_channel, footprint=footprint, mode='mirror')
        # 周辺画像の最小値を求める。footprintにより、対象となる画素は含めない。
        local_min = scipy.ndimage.filters.minimum_filter(single_channel, footprint=footprint, mode='mirror')
        # 中心画素が最大値よりthreshold分以上大きい、または最小値よりthreshold分以上小さければ欠陥とみなす。
        # 欠陥の位置をTrueとして保存。
        mask = (single_channel < local_min - threshold) + (single_channel > local_max + threshold)
        # 欠陥画素を平均値で置換。
        single_channel[mask] = average[mask]
        # single_channelはdpc_rawへの参照なので書き戻す必用がない
    return dpc_raw

def color_correction_matrix(rgb_array, color_matrix):
    """
    カラーマトリクス補正を行う。

    Parameters
    ----------
    rgb_array: numpy array
        入力RGB画像
    color_matrix: 2D (3x3) array like
        3x3 Color Correction Matrix
        Need to be normalized to 1.0

    Returns
    -------
    ccm_img: numpy array
        出力RGB画像
    """

    # 出力先を作成
    ccm_img = np.zeros_like(rgb_array)
    # CCMが3x3フォーマットでない場合、3x3に変換
    ccm = np.array(color_matrix).reshape((3, 3))
    # 各色毎に処理。この方が各画素ごとに処理するよりも高速なようだ。
    for color in (0, 1, 2):
        # 行列と入力画像の各色を掛け合わせる。
        ccm_img[:, :, color] = ccm[color, 0] * rgb_array[:, :, 0] + \
                               ccm[color, 1] * rgb_array[:, :, 1] + \
                               ccm[color, 2] * rgb_array[:, :, 2]
    return ccm_img


def lens_shading_correction(raw_array, coef):
    """
    レンズシェーディング補正を行う。

    Parameters
    ----------
    raw_array: numpy array
        Bayerフォーマット入力RAW画像
    coef: array of size 4x2
        coef[c][1]: 定数項
        coef[c][0]: 傾き
        cはBayer配列内のカラーチャンネル
        c = 0: 左上
        c = 1: 右上
        c = 2: 左下
        c = 3: 右下
    
    Returns
    -------
    lsc_raw: numpy array
        出力RAW画像
    """
    
    # ゲインマップの保存場所。
    gain_map = np.zeros(raw_array.shape)
    # 起点となる画像の中心位置。
    h, w = raw_array.shape
    center_y, center_x = h // 2, w // 2
    # 中心からの距離を配列に保存。
    x = np.arange(0, w) - center_x
    y = np.arange(0, h) - center_y
    # numpyのmeshgridは,x, yを並べた配列を生成する。
    # この場合範囲内のi, jに対し、xs[i, j] = x[j]
    # 同様にi, jに対し、ys[i, j] = y[i]
    xs, ys = np.meshgrid(x, y, sparse=True)
    # 各点ごとの中心からの距離を計算
    r2 = ys * ys + xs * xs
    # 中心からの距離に係数をかけて各点のゲインを計算。
    gain_map[::2, ::2] = r2[::2, ::2] * coef[0][0] + coef[0][1]
    gain_map[1::2, ::2] = r2[1::2, ::2] * coef[1][0] + coef[1][1]
    gain_map[::2, 1::2] = r2[::2, 1::2] * coef[2][0] + coef[2][1]
    gain_map[1::2, 1::2] = r2[1::2, 1::2] * coef[3][0] + coef[3][1]
    # 入力画像にゲインをかけ合わせる。
    lsc_array = raw_array * gain_map
    return lsc_array


def noise_filter(rgb_img, noise_model, coef=0.1):
    """
    バイラテラルノイズフィルター処理を行う。

    Parameters
    ----------
    rgb_img: numpy array
        入力RGB画像
    noise_model: array of 2 
        ノイズモデル。
        noise[0]:傾き
        noise[1]:切片
    coef: float
        ノイズフィルター強度。
        チューニングパラメーター。

    Returns
    -------
    flt_img: numpy array
        ノイズ除去後のRGB画像
    """
    h, w, _ = rgb_img.shape
    # 平均画像からノイズ量を見積もる。
    luma_img = rgb_img.mean(2)
    average = scipy.ndimage.filters.uniform_filter(luma_img, 5, mode='mirror')
    sigma_map = average * noise_model[0] + noise_model[1]
    sigma_map[sigma_map < 0.1] = 0.1
    sy, sx = sigma_map.strides
    sigma_tile = as_strided(sigma_map, strides=(sy, sx, 0, 0), shape=(h, w, 5, 5))
    sigma_tile = sigma_tile[2:h-2, 2:w-2, : , :]
    # 各画素に与える重みを求める。
    sy, sx = luma_img.strides
    luma_tile = as_strided(luma_img, strides=(sy, sx, 0, 0), shape=(h, w, 5, 5))
    luma_tile = luma_tile[2:h-2, 2:w-2, : , :]
    luma_box = as_strided(luma_img, strides=(sy, sx, sy, sx), shape=(h-4, w-4, 5, 5))
    diff = luma_box - luma_tile
    weight = np.exp(-coef * diff * diff / sigma_tile)
    weight_sum = weight.sum(axis=(2, 3))
    
    # 各色毎にノイズフィルターをかける。
    flt_img = rgb_img.copy()
    for color in (0, 1, 2):
        single = rgb_img[:, :, color]
        sy, sx = single.strides
        single_boxes = as_strided(single, strides=(sy, sx, sy, sx), shape=(h-4, w-4, 5, 5))
        single_out = (weight * single_boxes).sum(axis=(2, 3)) / weight_sum
        flt_img[2:h-2, 2:w-2, color] = single_out
    return flt_img
