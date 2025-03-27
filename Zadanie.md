# Zadanie rekrutacyjne – analiza objętości hałd na podstawie chmury punktów

## Dane wejściowe:

- Chmura punktów LiDAR (format LAS/LAZ):
    - Układ współrzędnych: ETRF2000-PL/CS92 (EPSG:2180).
    - Dane sklasyfikowane (klasyfikacja standardowa LAS).
    - Dodatkowe pola klasyfikacji (Scalar Field): 
        -pred_class (0 – brak hałdy, 1 – hałda).
        -pred_ID (identyfikatory poszczególnych hałd).
- Poligony (format GeoJSON/Shapefile):
    -Obrysy hałd.
    -Układ współrzędnych: WGS84 (EPSG:4326).

## Zadanie podstawowe:

Przygotuj skrypt/aplikację w języku Python, która wykona następujące czynności:
1. Przetransformuje dane poligonowe (EPSG:4326) do układu chmury punktów (EPSG:2180).
2. Wyznaczy powierzchnię bazową (powierzchnię terenu) o dokładności przestrzennej XY 10 cm.
3. Dla każdego poligonu obliczy zestaw statystyk: 
    - Objętość hałdy (względem powierzchni bazowej).
    - Powierzchnia 3D hałdy.
    - Powierzchnia pokrycia poligonu punktami.
4. Wyniki zapisze w formacie CSV lub GeoJSON.

## Rozszerzenie zadania:

Dla punktów, które mają przypisane pola pred_class i pred_ID:
- Zaproponuj i zaimplementuj metodę automatycznego wyodrębniania obrysów hałd (np. za pomocą AlphaShape).
- Porównaj wyznaczone automatycznie obrysy z dostarczonymi poligonami wejściowymi (opcjonalnie).

Kryteria oceny rozwiązania:
- Dobór narzędzi i bibliotek.
- Podejście do rozwiązania problemu (algorytmy, struktura rozwiązania).
- Optymalizacja pamięciowa i czasowa (wydajność rozwiązania).
- Jakość i czytelność kodu.
- Obecność i jakość testów jednostkowych.

## Forma przekazania rozwiązania:

- Kod źródłowy (repozytorium git).
- Krótka dokumentacja opisująca uruchomienie rozwiązania.
- Wyniki przykładowego przetworzenia danych (w formacie CSV lub GeoJSON).
- Testy jednostkowe pokrywające kluczowe funkcjonalności.

