
# 📦 pandas.tseries.offsets (pd.offsets)

El submódulo `pd.offsets` de **pandas** proporciona clases para representar **desplazamientos de tiempo** (time offsets), que pueden aplicarse a objetos como `DatetimeIndex`, `Timestamp` o `Series` de tipo datetime.

---

## 📆 Desplazamientos de fecha y tiempo básicos

| Clase | Descripción |
|-------|--------------|
| `DateOffset` | Clase base para todos los desplazamientos de tiempo. |
| `Day` | Desplazamiento en días. |
| `Hour` | Desplazamiento en horas. |
| `Minute` | Desplazamiento en minutos. |
| `Second` | Desplazamiento en segundos. |
| `Milli` | Desplazamiento en milisegundos. |
| `Micro` | Desplazamiento en microsegundos. |
| `Nano` | Desplazamiento en nanosegundos. |

---

## 📅 Desplazamientos de calendario

| Clase | Descripción |
|-------|--------------|
| `MonthBegin` | Salta al comienzo del mes. |
| `MonthEnd` | Salta al final del mes. |
| `BMonthBegin` | Comienzo del mes hábil (business month). |
| `BMonthEnd` | Fin del mes hábil. |
| `QuarterBegin` | Comienzo del trimestre. |
| `QuarterEnd` | Fin del trimestre. |
| `BQuarterBegin` | Comienzo del trimestre hábil. |
| `BQuarterEnd` | Fin del trimestre hábil. |
| `YearBegin` | Comienzo del año. |
| `YearEnd` | Fin del año. |
| `BYearBegin` | Comienzo del año hábil. |
| `BYearEnd` | Fin del año hábil. |
| `FY5253` | Calendario fiscal de 52–53 semanas. |

---

## 💼 Desplazamientos de días hábiles

| Clase | Descripción |
|-------|--------------|
| `BusinessDay` o `BDay` | Día hábil (omite fines de semana). |
| `CBMonthBegin` | Comienzo de mes hábil personalizado. |
| `CBMonthEnd` | Fin de mes hábil personalizado. |
| `CustomBusinessDay` | Día hábil con calendario definido por el usuario. |
| `CustomBusinessMonthBegin` | Inicio de mes hábil personalizado. |
| `CustomBusinessMonthEnd` | Fin de mes hábil personalizado. |

---

## 📈 Desplazamientos semanales

| Clase | Descripción |
|-------|--------------|
| `Week` | Desplazamiento en semanas. |
| `WeekOfMonth` | Semana específica dentro de un mes (ej. segundo lunes). |

---

## 🕐 Otros desplazamientos especializados

| Clase | Descripción |
|-------|--------------|
| `SemiMonthBegin` | Mitad del mes (inicio del día 1 o 15). |
| `SemiMonthEnd` | Mitad del mes (fin del día 15 o último día). |
| `BusinessHour` | Desplazamiento en horas laborales. |
| `CustomBusinessHour` | Desplazamiento en horas laborales personalizadas. |
| `Tick` | Desplazamiento de frecuencia fija (unidad base mínima). |

---

## 🧠 Ejemplo de uso

```python
import pandas as pd

ts = pd.Timestamp("2025-10-22")

print(ts + pd.offsets.MonthEnd())   # Fin del mes
print(ts + pd.offsets.BDay(5))      # 5 días hábiles después
print(ts + pd.offsets.Week(2))      # 2 semanas después
```
