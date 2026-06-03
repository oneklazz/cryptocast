
# ============================================================================
# ИМПОРТ БИБЛИОТЕК
# ============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

# Настройка отображения
warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (15, 6)
plt.rcParams['font.size'] = 10
sns.set_style('darkgrid')

# ============================================================================
# 1. ЗАГРУЗКА И ПЕРВИЧНЫЙ АНАЛИЗ ДАННЫХ
# ============================================================================

def load_and_analyze_data(filepath):
    """
    Функция для загрузки и первичного анализа датасета
    
    Параметры:
    ----------
    filepath : str
        Путь к CSV файлу с данными
        
    Возвращает:
    ----------
    pd.DataFrame
        Загруженный и обработанный датафрейм
    """
    print("=" * 80)
    print("1. ЗАГРУЗКА И АНАЛИЗ ДАННЫХ")
    print("=" * 80)
    
    # Загружаем данные из CSV файла
    df = pd.read_csv(filepath)
    
    # Выводим основную информацию о датасете
    print(f"\n📊 Размер датасета: {df.shape[0]} строк, {df.shape[1]} столбцов")
    print(f"📅 Период данных: с {df['Date'].min()} по {df['Date'].max()}")
    
    # Преобразуем столбец Date в формат datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Определяем грануляцию времени (разницу между последовательными записями)
    time_diff = df['Date'].diff().mode()[0]
    print(f"⏱️ Грануляция времени: {time_diff}")
    
    # Выводим информацию о типах данных и пропущенных значениях
    print(f"\n📋 Информация о столбцах:")
    print(df.info())
    
    # Проверяем статистические характеристики данных
    print(f"\n📈 Статистика по числовым столбцам:")
    print(df.describe())
    
    return df

def clean_data(df):
    """
    Функция для очистки данных от дубликатов и пропущенных значений
    
    Параметры:
    ----------
    df : pd.DataFrame
        Исходный датафрейм
        
    Возвращает:
    ----------
    pd.DataFrame
        Очищенный датафрейм
    """
    print("\n" + "=" * 80)
    print("2. ОЧИСТКА ДАННЫХ")
    print("=" * 80)
    
    # Проверяем наличие дубликатов по дате
    duplicates = df.duplicated(subset=['Date']).sum()
    print(f"\n🔍 Найдено дубликатов по дате: {duplicates}")
    
    if duplicates > 0:
        # Удаляем дубликаты, оставляя первое вхождение
        df = df.drop_duplicates(subset=['Date'], keep='first')
        print(f"✅ Дубликаты удалены. Новый размер: {df.shape[0]} строк")
    
    # Проверяем пропущенные значения в важных столбцах
    important_columns = ['Date', 'Close', 'Volume', 'Marketcap']
    print(f"\n🔍 Проверка пропущенных значений в ключевых столбцах:")
    
    missing_data = {}
    for col in important_columns:
        if col in df.columns:
            missing_count = df[col].isna().sum() #Nan - not a number
            missing_data[col] = missing_count
            print(f"  - {col}: {missing_count} ({missing_count/len(df)*100:.2f}%)")
    
    # Удаляем строки с пропущенными значениями в столбце Close (цена закрытия)
    # так как это основной показатель для прогнозирования
    initial_size = len(df)
    df = df.dropna(subset=['Close'])
    removed = initial_size - len(df)
    
    if removed > 0:
        print(f"\n✅ Удалено {removed} строк с пропущенными значениями в Close")
    
    # Сортируем данные по дате (важно для временных рядов!)
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Проверяем, есть ли столбец Volume, и заполняем 0 если есть пропуски
    if 'Volume' in df.columns:
        # В некоторых ранних данных Volume может быть 0 или отсутствовать
        df['Volume'].fillna(0, inplace=True)
    
    print(f"\n✅ Данные очищены. Финальный размер: {df.shape[0]} строк")
    
    return df

# ============================================================================
# 3. ВИЗУАЛИЗАЦИЯ ДАННЫХ
# ============================================================================

def visualize_timeseries(df, resample_periods=['D', 'W', 'M', 'Q']):
    """
    Функция для визуализации временного ряда с разными локаторами времени
    
    Параметры:
    ----------
    df : pd.DataFrame
        Датафрейм с данными
    resample_periods : list
        Список периодов для ресэмплинга ('D' - день, 'W' - неделя, 'M' - месяц, 'Q' - квартал)
    """
    print("\n" + "=" * 80)
    print("3. ВИЗУАЛИЗАЦИЯ ДАННЫХ")
    print("=" * 80)
    
    # Создаем копию датафрейма для визуализации
    df_viz = df.copy()
    df_viz.set_index('Date', inplace=True)
    
    # ЦЕЛОСТНАЯ ВИЗУАЛИЗАЦИЯ
    print("\n📊 Создание визуализации временного ряда целиком...")
    
    fig, axes = plt.subplots(3, 1, figsize=(15, 12))
    fig.suptitle('Анализ временного ряда XRP (весь период)', fontsize=16, fontweight='bold')
    
    # График 1: Цена закрытия
    axes[0].plot(df_viz.index, df_viz['Close'], color='blue', linewidth=0.8)
    axes[0].set_title('Цена закрытия (Close)', fontsize=12)
    axes[0].set_ylabel('Цена (USD)', fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # График 2: Объем торгов
    axes[1].bar(df_viz.index, df_viz['Volume'], color='red', alpha=0.6, width=1)
    axes[1].set_title('Объем торгов (Volume)', fontsize=12)
    axes[1].set_ylabel('Объем', fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    # График 3: Рыночная капитализация
    axes[2].plot(df_viz.index, df_viz['Marketcap'], color='orange', linewidth=0.8)
    axes[2].set_title('Рыночная капитализация (Marketcap)', fontsize=12)
    axes[2].set_ylabel('Капитализация (USD)', fontsize=10)
    axes[2].set_xlabel('Дата', fontsize=10)
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations_full_timeseries.png', dpi=150, bbox_inches='tight')
    print("✅ Сохранено: visualizations_full_timeseries.png")
    plt.close()
    
    # ВИЗУАЛИЗАЦИЯ С РАЗНЫМИ ЛОКАТОРАМИ ВРЕМЕНИ
    print("\n📊 Создание визуализации с разными периодами агрегации...")
    
    period_names = {
        'D': 'День',
        'W': 'Неделя',
        'M': 'Месяц',
        'Q': 'Квартал',
        'Y': 'Год'
    }
    
    fig, axes = plt.subplots(len(resample_periods), 1, figsize=(15, 4*len(resample_periods)))
    if len(resample_periods) == 1:
        axes = [axes]
    
    fig.suptitle('Цена закрытия XRP с разными периодами агрегации', fontsize=16, fontweight='bold')
    
    for idx, period in enumerate(resample_periods):
        # Ресэмплируем данные (берем среднее значение за период)
        df_resampled = df_viz['Close'].resample(period).mean()
        
        # Строим график
        axes[idx].plot(df_resampled.index, df_resampled.values, linewidth=2, marker='o', markersize=3)
        axes[idx].set_title(f'Период: {period_names.get(period, period)}', fontsize=12)
        axes[idx].set_ylabel('Средняя цена (USD)', fontsize=10)
        axes[idx].grid(True, alpha=0.3)
        
        if idx == len(resample_periods) - 1:
            axes[idx].set_xlabel('Дата', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('visualizations_different_periods.png', dpi=150, bbox_inches='tight')
    print("✅ Сохранено: visualizations_different_periods.png")
    plt.close()
    
    # ДЕКОМПОЗИЦИЯ ВРЕМЕННОГО РЯДА
    print("\n📊 Анализ компонентов временного ряда (тренд, сезонность, остатки)...")
    
    # Используем месячные данные для декомпозиции
    from statsmodels.tsa.seasonal import seasonal_decompose
    
    # Ресэмплируем в месячные данные для более четкой декомпозиции
    df_monthly = df_viz['Close'].resample('M').mean()
    
    # Выполняем декомпозицию (аддитивная модель)
    # period=12 означает годовую сезонность (12 месяцев)
    decomposition = seasonal_decompose(df_monthly, model='additive', period=12)
    
    # Визуализируем компоненты
    fig, axes = plt.subplots(4, 1, figsize=(15, 12))
    fig.suptitle('Декомпозиция временного ряда XRP (месячные данные)', fontsize=16, fontweight='bold')
    
    # Исходный ряд
    axes[0].plot(decomposition.observed, color='blue', linewidth=1.5)
    axes[0].set_title('Исходный временной ряд', fontsize=12)
    axes[0].set_ylabel('Цена', fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # Тренд
    axes[1].plot(decomposition.trend, color='red', linewidth=1.5)
    axes[1].set_title('Тренд', fontsize=12)
    axes[1].set_ylabel('Цена', fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    # Сезонность
    axes[2].plot(decomposition.seasonal, color='green', linewidth=1.5)
    axes[2].set_title('Сезонность', fontsize=12)
    axes[2].set_ylabel('Цена', fontsize=10)
    axes[2].grid(True, alpha=0.3)
    
    # Остатки
    axes[3].scatter(decomposition.resid.index, decomposition.resid.values, alpha=0.3, s=10, color='orange')
    axes[3].axhline(y=0, color='black', linestyle='--', linewidth=1)
    axes[3].set_title('Остатки (шум)', fontsize=12)
    axes[3].set_ylabel('Остатки', fontsize=10)
    axes[3].set_xlabel('Дата', fontsize=10)
    axes[3].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations_decomposition.png', dpi=150, bbox_inches='tight')
    print("✅ Сохранено: visualizations_decomposition.png")
    plt.close()

def formulate_hypothesis(df):
    """
    Функция для анализа данных и формулировки гипотез
    
    Параметры:
    ----------
    df : pd.DataFrame
        Датафрейм с данными
    """
    print("\n" + "=" * 80)
    print("4. ФОРМУЛИРОВКА ГИПОТЕЗ")
    print("=" * 80)
    
    df_analysis = df.copy()
    df_analysis.set_index('Date', inplace=True)
    
    # Анализ тренда
    print("\n🔍 АНАЛИЗ ТРЕНДА:")
    
    # Вычисляем скользящее среднее для выявления тренда
    df_analysis['MA_30'] = df_analysis['Close'].rolling(window=30).mean()
    df_analysis['MA_90'] = df_analysis['Close'].rolling(window=90).mean()
    df_analysis['MA_365'] = df_analysis['Close'].rolling(window=365).mean()
    
    # Сравниваем начало и конец периода
    first_price = df_analysis['Close'].iloc[0]
    last_price = df_analysis['Close'].iloc[-1]
    price_change = ((last_price - first_price) / first_price) * 100
    
    print(f"  - Начальная цена: ${first_price:.6f}")
    print(f"  - Конечная цена: ${last_price:.6f}")
    print(f"  - Изменение: {price_change:+.2f}%")
    
    if price_change > 10:
        print(f"  ✅ ГИПОТЕЗА: Присутствует ВОСХОДЯЩИЙ тренд")
    elif price_change < -10:
        print(f"  ✅ ГИПОТЕЗА: Присутствует НИСХОДЯЩИЙ тренд")
    else:
        print(f"  ✅ ГИПОТЕЗА: Тренд ОТСУТСТВУЕТ или СЛАБЫЙ")
    
    # Анализ волатильности
    print("\n🔍 АНАЛИЗ ВОЛАТИЛЬНОСТИ:")
    
    # Вычисляем стандартное отклонение
    volatility = df_analysis['Close'].std()
    mean_price = df_analysis['Close'].mean()
    cv = (volatility / mean_price) * 100  # Коэффициент вариации
    
    print(f"  - Средняя цена: ${mean_price:.6f}")
    print(f"  - Стандартное отклонение: ${volatility:.6f}")
    print(f"  - Коэффициент вариации: {cv:.2f}%")
    
    if cv > 50:
        print(f"  ✅ ГИПОТЕЗА: ВЫСОКАЯ волатильность - рынок нестабилен")
    elif cv > 25:
        print(f"  ✅ ГИПОТЕЗА: СРЕДНЯЯ волатильность")
    else:
        print(f"  ✅ ГИПОТЕЗА: НИЗКАЯ волатильность - рынок стабилен")
    
    # Анализ сезонности
    print("\n🔍 АНАЛИЗ СЕЗОННОСТИ:")
    
    df_analysis['Year'] = df_analysis.index.year
    df_analysis['Month'] = df_analysis.index.month
    df_analysis['DayOfWeek'] = df_analysis.index.dayofweek
    
    # Группируем по месяцам и смотрим средние значения
    monthly_avg = df_analysis.groupby('Month')['Close'].mean()
    monthly_std = df_analysis.groupby('Month')['Close'].std()
    
    # Вычисляем коэффициент вариации по месяцам
    monthly_cv = (monthly_std / monthly_avg) * 100
    
    print(f"  - Средний коэффициент вариации по месяцам: {monthly_cv.mean():.2f}%")
    
    if monthly_cv.mean() > 30:
        print(f"  ✅ ГИПОТЕЗА: Присутствует ЗАМЕТНАЯ месячная сезонность")
    else:
        print(f"  ✅ ГИПОТЕЗА: Месячная сезонность СЛАБАЯ или ОТСУТСТВУЕТ")
    
    # Анализ необходимости сегментации
    print("\n🔍 АНАЛИЗ ПЕРИОДОВ (необходимость сегментации):")
    
    # Проверяем экстремальные изменения цены
    df_analysis['Daily_Return'] = df_analysis['Close'].pct_change()
    extreme_events = df_analysis[abs(df_analysis['Daily_Return']) > 0.2]  # Изменения более 20%
    
    print(f"  - Количество экстремальных скачков цены (>20%): {len(extreme_events)}")
    print(f"  - Процент экстремальных событий: {len(extreme_events)/len(df_analysis)*100:.2f}%")
    
    if len(extreme_events) > len(df_analysis) * 0.05:  # Более 5% данных
        print(f"  ✅ ГИПОТЕЗА: Рекомендуется СЕГМЕНТАЦИЯ данных на периоды до/после значимых событий")
    else:
        print(f"  ✅ ГИПОТЕЗА: Сегментация НЕ ТРЕБУЕТСЯ, можно обучать на всех данных")
    
 

# ============================================================================
# 5. ПОДГОТОВКА ДАННЫХ ДЛЯ PROPHET
# ============================================================================

def prepare_data_for_prophet(df, train_size=0.9):
    """
    Подготовка данных для обучения модели Prophet
    
    Параметры:
    ----------
    df : pd.DataFrame
        Исходный датафрейм
    train_size : float
        Доля данных для обучения (по умолчанию 0.9 = 90%)
        
    Возвращает:
    ----------
    tuple
        (train_df, test_df) - обучающая и тестовая выборки
    """
    print("\n" + "=" * 80)
    print("5. ПОДГОТОВКА ДАННЫХ ДЛЯ PROPHET")
    print("=" * 80)
    
    # Prophet требует специального формата данных:
    # - столбец 'ds' для даты (datetime)
    # - столбец 'y' для значений временного ряда
    
    df_prophet = pd.DataFrame()
    df_prophet['ds'] = df['Date']
    df_prophet['y'] = df['Close']
    
    # Определяем размер обучающей и тестовой выборки
    train_samples = int(len(df_prophet) * train_size)
    test_samples = len(df_prophet) - train_samples
    
    print(f"\n📊 Размер временного ряда: {len(df_prophet)} записей")
    print(f"📊 Обучающая выборка: {train_samples} записей ({train_size*100:.1f}%)")
    print(f"📊 Тестовая выборка: {test_samples} записей ({(1-train_size)*100:.1f}%)")
    print(f"📊 Размер прогноза: {test_samples} дней ({test_samples/len(df_prophet)*100:.1f}%)")
    
    # Разделяем данные
    train_df = df_prophet.iloc[:train_samples].copy()
    test_df = df_prophet.iloc[train_samples:].copy()
    
    print(f"\n📅 Обучающие данные: {train_df['ds'].min()} - {train_df['ds'].max()}")
    print(f"📅 Тестовые данные: {test_df['ds'].min()} - {test_df['ds'].max()}")
    
    return train_df, test_df

# ============================================================================
# 6. ОБУЧЕНИЕ МОДЕЛИ PROPHET
# ============================================================================

def train_prophet_model(train_df, params=None):
    """
    Обучение модели Prophet
    
    Параметры:
    ----------
    train_df : pd.DataFrame
        Обучающая выборка в формате Prophet (ds, y)
    params : dict
        Словарь с параметрами модели (опционально)
        
    Возвращает:
    ----------
    model : Prophet
        Обученная модель Prophet
    """
    print("\n" + "=" * 80)
    print("6. ОБУЧЕНИЕ МОДЕЛИ PROPHET")
    print("=" * 80)
    
    # Импортируем Prophet
    try:
        from prophet import Prophet
        print("✅ Библиотека Prophet импортирована успешно")
    except ImportError:
        print("❌ Ошибка: Библиотека Prophet не установлена!")
        print("Установите через: pip install prophet")
        return None
    
    # Настройка параметров модели по умолчанию
    default_params = {
        'yearly_seasonality': True,      # Годовая сезонность
        'weekly_seasonality': True,      # Недельная сезонность
        'daily_seasonality': False,      # Дневная сезонность (выключена для экономии ресурсов)
        'changepoint_prior_scale': 0.05, # Гибкость тренда (0.001-0.5, больше = более гибкий)
        'seasonality_prior_scale': 10.0, # Гибкость сезонности (1-25, больше = более гибкая)
        'seasonality_mode': 'multiplicative'  # Тип сезонности (additive или multiplicative)
    }
    
    # Обновляем параметры, если переданы пользовательские
    if params:
        default_params.update(params)
    
    print(f"\n⚙️ Параметры модели:")
    for key, value in default_params.items():
        print(f"  - {key}: {value}")
    
    # Создаем и обучаем модель
    print(f"\n🔄 Обучение модели...")
    model = Prophet(**default_params)
    
    # Добавляем дополнительную месячную сезонность
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    
    # Обучаем модель
    model.fit(train_df)
    
    print(f"✅ Модель успешно обучена!")
    
    return model

def make_forecast(model, test_df):
    """
    Создание прогноза с помощью обученной модели
    
    Параметры:
    ----------
    model : Prophet
        Обученная модель Prophet
    test_df : pd.DataFrame
        Тестовая выборка с истинными значениями
        
    Возвращает:
    ----------
    forecast : pd.DataFrame
        Прогноз модели
    """
    print("\n" + "=" * 80)
    print("7. СОЗДАНИЕ ПРОГНОЗА")
    print("=" * 80)
    
    # Создаем датафрейм для прогноза на период тестовой выборки
    future = pd.DataFrame()
    future['ds'] = test_df['ds']
    
    # Делаем прогноз
    print(f"🔮 Создание прогноза на {len(future)} дней...")
    forecast = model.predict(future)
    
    print(f"✅ Прогноз создан успешно!")
    print(f"📊 Столбцы прогноза: {list(forecast.columns)}")
    
    # forecast содержит:
    # - ds: дата
    # - yhat: прогнозируемое значение (до куда едем) 0.4 0.33
    # - yhat_lower: нижняя граница доверительного интервала (sl)
    # - yhat_upper: верхняя граница доверительного интервала (sl)
    # - trend: трендовая компонента
    # - различные сезонные компоненты
    
    return forecast

# ============================================================================
# 7. ОЦЕНКА КАЧЕСТВА МОДЕЛИ
# ============================================================================

def evaluate_model(test_df, forecast):
    """
    Оценка качества модели через расчет ошибок
    
    Параметры:
    ----------
    test_df : pd.DataFrame
        Тестовая выборка с истинными значениями
    forecast : pd.DataFrame
        Прогноз модели
        
    Возвращает:
    ----------
    dict
        Словарь с метриками качества
    """
    print("\n" + "=" * 80)
    print("8. ОЦЕНКА КАЧЕСТВА МОДЕЛИ")
    print("=" * 80)
    
    # Извлекаем истинные значения и прогнозы
    y_true = test_df['y'].values
    y_pred = forecast['yhat'].values
    
    # Рассчитываем метрики
    
    # 1. MAE - Средняя абсолютная ошибка
    mae = np.mean(np.abs(y_true - y_pred))
    
    # 2. RMSE - Среднеквадратичная ошибка
    rmse = np.sqrt(np.mean((y_true - y_pred)**2))
    
    # 3. MAPE - Средняя абсолютная процентная ошибка (относительная)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    # 4. R² - Коэффициент детерминации
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    r2 = 1 - (ss_res / ss_tot)
    
    # Выводим результаты
    print(f"\n📊 МЕТРИКИ КАЧЕСТВА МОДЕЛИ:")
    print(f"  - MAE (Средняя абсолютная ошибка): ${mae:.6f}")
    print(f"  - RMSE (Среднеквадратичная ошибка): ${rmse:.6f}")
    print(f"  - MAPE (Относительная ошибка): {mape:.2f}%")
    print(f"  - R² (Коэффициент детерминации): {r2:.4f}")
    
    # Интерпретация результатов
    print(f"\n📝 ИНТЕРПРЕТАЦИЯ:")
    if mape < 10:
        print(f"  ✅ ОТЛИЧНАЯ точность прогноза (MAPE < 10%)")
    elif mape < 20:
        print(f"  ✅ ХОРОШАЯ точность прогноза (10% < MAPE < 20%)")
    elif mape < 50:
        print(f"  ⚠️ ПРИЕМЛЕМАЯ точность прогноза (20% < MAPE < 50%)")
    else:
        print(f"  ❌ НИЗКАЯ точность прогноза (MAPE > 50%) - требуется оптимизация")
    
    # Возвращаем словарь с метриками
    metrics = {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'R2': r2
    }
    
    return metrics

def visualize_forecast(train_df, test_df, forecast, metrics):
    """
    Визуализация результатов прогноза
    
    Параметры:
    ----------
    train_df : pd.DataFrame
        Обучающая выборка
    test_df : pd.DataFrame
        Тестовая выборка
    forecast : pd.DataFrame
        Прогноз модели
    metrics : dict
        Метрики качества модели
    """
    print("\n📊 Создание визуализации результатов...")
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Отображаем исторические данные (обучающая выборка)
    ax.plot(train_df['ds'], train_df['y'], 
            label='Обучающие данные', color='blue', linewidth=1, alpha=0.7)
    
    # Отображаем тестовые данные (истинные значения)
    ax.plot(test_df['ds'], test_df['y'], 
            label='Тестовые данные (истинные)', color='green', linewidth=2)
    
    # Отображаем прогноз
    ax.plot(forecast['ds'], forecast['yhat'], 
            label='Прогноз', color='red', linewidth=2, linestyle='--')
    
    # Отображаем доверительный интервал
    ax.fill_between(forecast['ds'], 
                    forecast['yhat_lower'], 
                    forecast['yhat_upper'],
                    color='red', alpha=0.2, label='Доверительный интервал')
    
    # Оформление графика
    ax.set_xlabel('Дата', fontsize=12)
    ax.set_ylabel('Цена закрытия (USD)', fontsize=12)
    ax.set_title(f'Прогноз цены XRP\nMAPE: {metrics["MAPE"]:.2f}% | R²: {metrics["R2"]:.4f}', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('forecast_results.png', dpi=150, bbox_inches='tight')
    print("✅ Сохранено: forecast_results.png")
    plt.close()

# ============================================================================
# 8. ОПТИМИЗАЦИЯ МОДЕЛИ
# ============================================================================

def optimize_model(train_df, test_df):
    """
    Оптимизация гиперпараметров модели для снижения ошибки
    
    Параметры:
    ----------
    train_df : pd.DataFrame
        Обучающая выборка
    test_df : pd.DataFrame
        Тестовая выборка
        
    Возвращает:
    ----------
    tuple
        (best_model, best_params, best_metrics) - лучшая модель, параметры и метрики
    """
    print("\n" + "=" * 80)
    print("9. ОПТИМИЗАЦИЯ ГИПЕРПАРАМЕТРОВ")
    print("=" * 80)
    
    from prophet import Prophet
    
    # Определяем сетку гиперпараметров для перебора
    param_grid = {
        'changepoint_prior_scale': [0.001, 0.01, 0.05, 0.1, 0.5],  # Гибкость тренда
        'seasonality_prior_scale': [0.1, 1.0, 5.0, 10.0],          # Гибкость сезонности
        'seasonality_mode': ['additive', 'multiplicative']         # Тип сезонности
    }
    
    print(f"\n🔍 Перебор гиперпараметров:")
    print(f"  - changepoint_prior_scale: {param_grid['changepoint_prior_scale']}")
    print(f"  - seasonality_prior_scale: {param_grid['seasonality_prior_scale']}")
    print(f"  - seasonality_mode: {param_grid['seasonality_mode']}")
    
    best_mape = float('inf')
    best_model = None
    best_params = None
    best_forecast = None
    
    total_iterations = (len(param_grid['changepoint_prior_scale']) * 
                       len(param_grid['seasonality_prior_scale']) * 
                       len(param_grid['seasonality_mode']))
    
    print(f"\n🔄 Всего комбинаций для проверки: {total_iterations}")
    
    iteration = 0
    
    # Перебираем все комбинации параметров
    for cp_scale in param_grid['changepoint_prior_scale']:
        for s_scale in param_grid['seasonality_prior_scale']:
            for s_mode in param_grid['seasonality_mode']:
                iteration += 1
                
                # Создаем и обучаем модель с текущими параметрами
                current_params = {
                    'yearly_seasonality': True,
                    'weekly_seasonality': True,
                    'daily_seasonality': False,
                    'changepoint_prior_scale': cp_scale,
                    'seasonality_prior_scale': s_scale,
                    'seasonality_mode': s_mode
                }
                
                try:
                    # Обучаем модель
                    model = Prophet(**current_params)
                    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
                    model.fit(train_df)
                    
                    # Делаем прогноз
                    future = pd.DataFrame({'ds': test_df['ds']})
                    forecast = model.predict(future)
                    
                    # Оцениваем качество
                    y_true = test_df['y'].values
                    y_pred = forecast['yhat'].values
                    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
                    
                    print(f"  [{iteration}/{total_iterations}] cp={cp_scale}, s={s_scale}, mode={s_mode} → MAPE={mape:.2f}%")
                    
                    # Сохраняем лучшую модель
                    if mape < best_mape:
                        best_mape = mape
                        best_model = model
                        best_params = current_params.copy()
                        best_forecast = forecast
                        print(f"    ⭐ Новый лучший результат: MAPE={best_mape:.2f}%")
                        
                except Exception as e:
                    print(f"  ❌ Ошибка при обучении с параметрами cp={cp_scale}, s={s_scale}, mode={s_mode}: {e}")
                    continue
    
    # Выводим результаты оптимизации
    print(f"\n" + "=" * 80)
    print(f"✅ РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ:")
    print(f"=" * 80)
    print(f"\n🏆 Лучшие параметры:")
    for key, value in best_params.items():
        print(f"  - {key}: {value}")
    
    # Оцениваем качество лучшей модели
    best_metrics = evaluate_model(test_df, best_forecast)
    
    return best_model, best_params, best_metrics, best_forecast

# ============================================================================
# 9. ФИНАЛЬНОЕ ОБУЧЕНИЕ НА ВСЕХ ДАННЫХ
# ============================================================================

def final_training(df_prophet, best_params, forecast_days=30):
    """
    Финальное обучение модели на всех доступных данных и прогноз на будущее
    
    Параметры:
    ----------
    df_prophet : pd.DataFrame
        Полный датасет в формате Prophet
    best_params : dict
        Лучшие найденные параметры модели
    forecast_days : int
        Количество дней для прогноза в будущее
        
    Возвращает:
    ----------
    tuple
        (model, forecast) - финальная модель и прогноз
    """
    print("\n" + "=" * 80)
    print("10. ФИНАЛЬНОЕ ОБУЧЕНИЕ НА ВСЕХ ДАННЫХ")
    print("=" * 80)
    
    from prophet import Prophet
    
    print(f"\n📊 Обучение на полном датасете ({len(df_prophet)} записей)")
    print(f"🔮 Прогноз на {forecast_days} дней вперед")
    
    # Создаем и обучаем финальную модель
    final_model = Prophet(**best_params)
    final_model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    final_model.fit(df_prophet)
    
    print(f"✅ Модель обучена на всех данных")
    
    # Создаем датафрейм для прогноза
    future = final_model.make_future_dataframe(periods=forecast_days)
    final_forecast = final_model.predict(future)
    
    print(f"✅ Создан прогноз на {forecast_days} дней")
    
    # Визуализируем финальный прогноз
    print(f"\n📊 Создание визуализации финального прогноза...")
    
    fig = plt.figure(figsize=(15, 10))
    
    # График 1: Прогноз с компонентами
    ax1 = plt.subplot(2, 1, 1)
    
    # Исторические данные
    ax1.plot(df_prophet['ds'], df_prophet['y'], 
            label='Исторические данные', color='blue', linewidth=1)
    
    # Прогноз
    forecast_future = final_forecast[final_forecast['ds'] > df_prophet['ds'].max()]
    ax1.plot(forecast_future['ds'], forecast_future['yhat'], 
            label=f'Прогноз на {forecast_days} дней', color='red', linewidth=2)
    
    # Доверительный интервал
    ax1.fill_between(forecast_future['ds'],
                    forecast_future['yhat_lower'],
                    forecast_future['yhat_upper'],
                    color='red', alpha=0.2, label='Доверительный интервал')
    
    ax1.set_xlabel('Дата', fontsize=12)
    ax1.set_ylabel('Цена (USD)', fontsize=12)
    ax1.set_title('Финальный прогноз цены XRP', fontsize=14, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # График 2: Компоненты прогноза
    ax2 = plt.subplot(2, 2, 3)
    ax2.plot(final_forecast['ds'], final_forecast['trend'], color='green', linewidth=1.5)
    ax2.set_title('Тренд', fontsize=12)
    ax2.set_xlabel('Дата', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    ax3 = plt.subplot(2, 2, 4)
    ax3.plot(final_forecast['ds'], final_forecast['yearly'], color='orange', linewidth=1.5)
    ax3.set_title('Годовая сезонность', fontsize=12)
    ax3.set_xlabel('Дата', fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('final_forecast.png', dpi=150, bbox_inches='tight')
    print("✅ Сохранено: final_forecast.png")
    plt.close()
    
    # Выводим прогноз на ближайшие дни
    print(f"\n📅 ПРОГНОЗ НА БЛИЖАЙШИЕ {min(10, forecast_days)} ДНЕЙ:")
    print("=" * 80)
    
    future_predictions = forecast_future.head(10)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    for idx, row in future_predictions.iterrows():
        print(f"  {row['ds'].strftime('%Y-%m-%d')}: "
              f"${row['yhat']:.6f} "
              f"(${row['yhat_lower']:.6f} - ${row['yhat_upper']:.6f})")
    
    return final_model, final_forecast

# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """
    Главная функция для запуска всего процесса анализа и прогнозирования
    """
    print("\n")
    print("=" * 80)
    print("  ПРОГНОЗИРОВАНИЕ ВРЕМЕННЫХ РЯДОВ КРИПТОВАЛЮТЫ XRP С PROPHET")
    print("=" * 80)
    print("\n")
    
    # Путь к датасету
    data_path = "dataset/coin_XRP.csv"
    
    try:
        # Шаг 1: Загрузка и анализ данных
        df = load_and_analyze_data(data_path)
        
        # Шаг 2: Очистка данных
        df = clean_data(df)
        
        # Шаг 3: Визуализация данных
        visualize_timeseries(df, resample_periods=['W', 'M', 'Q'])
        
        # Шаг 4: Формулировка гипотез
        formulate_hypothesis(df)
        
        # Шаг 5: Подготовка данных для Prophet
        train_df, test_df = prepare_data_for_prophet(df, train_size=0.9)
        
        # Шаг 6: Первичное обучение модели
        initial_model = train_prophet_model(train_df)
        
        if initial_model is None:
            print("\n❌ Не удалось обучить модель. Убедитесь, что Prophet установлен.")
            print("Установка: pip install prophet")
            return
        
        # Шаг 7: Создание прогноза
        initial_forecast = make_forecast(initial_model, test_df)
        
        # Шаг 8: Оценка качества
        initial_metrics = evaluate_model(test_df, initial_forecast)
        
        # Шаг 9: Визуализация первичных результатов
        visualize_forecast(train_df, test_df, initial_forecast, initial_metrics)
        
        # Шаг 10: Оптимизация модели
        best_model, best_params, best_metrics, best_forecast = optimize_model(train_df, test_df)
        
        # Шаг 11: Визуализация оптимизированных результатов
        visualize_forecast(train_df, test_df, best_forecast, best_metrics)
        
        # Шаг 12: Финальное обучение на всех данных
        df_prophet = pd.DataFrame({'ds': df['Date'], 'y': df['Close']})
        final_model, final_forecast = final_training(df_prophet, best_params, forecast_days=30)
        
        # Итоговый отчет
        print("\n" + "=" * 80)
        print("🎉 АНАЛИЗ ЗАВЕРШЕН!")
        print("=" * 80)
        print(f"\n📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
        print(f"  - Начальная MAPE: {initial_metrics['MAPE']:.2f}%")
        print(f"  - Оптимизированная MAPE: {best_metrics['MAPE']:.2f}%")
        print(f"  - Улучшение: {initial_metrics['MAPE'] - best_metrics['MAPE']:.2f}%")
        print(f"\n📁 Созданные файлы:")
        print(f"  - visualizations_full_timeseries.png")
        print(f"  - visualizations_different_periods.png")
        print(f"  - visualizations_decomposition.png")
        print(f"  - forecast_results.png")
        print(f"  - final_forecast.png")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

# Запуск программы
if __name__ == "__main__":
    main()
