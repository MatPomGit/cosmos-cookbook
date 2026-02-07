# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
🎓 SKRYPT PRZETWARZANIA DANYCH WTS (WovenTraffic Safety)

CO ROBI TEN SKRYPT:
Ten skrypt przekształca surowe adnotacje (annotacje) z zestawu danych WTS
do formatu używanego przez modele AI do uczenia się rozumienia scen drogowych.

WTS (WovenTraffic Safety) to zbiór danych z wideo ruchu drogowego zawierający:
- Nagrania z góry (overhead view) pokazujące skrzyżowania
- Pytania wielokrotnego wyboru (MCQ) o bezpieczeństwo i sytuacje na drodze
- Adnotacje środowiska (environment) - warunki pogodowe, pora dnia, etc.

DLACZEGO PRZETWARZAMY DANE:
Surowe dane są w jednym formacie, ale model AI wymaga innego formatu (LLaVA).
To jak tłumaczenie między językami - te same informacje, inna struktura.

FORMAT LLaVA:
LLaVA to format konwersacji, gdzie:
- "human" zadaje pytanie (z referencją do wideo)
- "gpt" odpowiada (prawidłowa odpowiedź)

PRZYKŁAD TRANSFORMACJI:
PRZED (surowe dane):
{
    "question": "Jaka jest pogoda?",
    "a": "słonecznie",
    "b": "deszczowo",
    "correct": "a"
}

PO (format LLaVA):
{
    "video": "path/to/video.mp4",
    "conversations": [
        {"from": "human", "value": "<video> Jaka jest pogoda? A: słonecznie B: deszczowo"},
        {"from": "gpt", "value": "A"}
    ]
}
"""

# 🎓 IMPORTY - biblioteki potrzebne do pracy ze skryptem
import argparse  # Do parsowania argumentów z linii poleceń
import json      # Do czytania i zapisywania plików JSON (format przechowywania danych)
import os        # Do operacji na plikach i katalogach
from pathlib import Path  # Do wygodnej pracy ze ścieżkami
from typing import Any, Dict, List, Optional, Tuple  # Typy dla lepszej czytelności kodu

from tqdm import tqdm  # Pasek postępu - pokazuje ile pracy jeszcze zostało


def parse_arguments() -> str:
    """Parsuj argumenty z linii poleceń.

    🎓 WYJAŚNIENIE - CO TO SĄ ARGUMENTY LINII POLECEŃ:
    Gdy uruchamiasz program z terminala, możesz przekazać mu informacje:
    python script.py --data_path /ścieżka/do/danych
    
    --data_path to "argument" - informacja którą przekazujesz programowi.
    
    DLACZEGO TO JEST UŻYTECZNE:
    - Nie musisz zmieniać kodu by użyć innej ścieżki
    - Ten sam skrypt działa z różnymi danymi
    - Łatwiejsza automatyzacja
    
    Returns:
        str: Ścieżka do katalogu zawierającego pliki JSON z adnotacjami
        
    PRZYKŁAD UŻYCIA:
    python data_preprocess.py --data_path /home/user/wts_data
    """
    parser = argparse.ArgumentParser(
        description="Formatuj adnotacje WTS do generowania danych treningowych (best view)"
    )
    parser.add_argument(
        "--data_path", 
        type=Path, 
        required=True, 
        help="Katalog z plikami JSON adnotacji"
    )
    args = parser.parse_args()
    return str(args.data_path)


def process_question(row: Dict[str, Any]) -> str:
    """Przetwórz pytanie do formatu promptu z opcjami wielokrotnego wyboru.

    🎓 WYJAŚNIENIE - CO TO JEST MCQ (Multiple Choice Question):
    MCQ to pytanie z kilkoma opcjami odpowiedzi, gdzie tylko jedna jest prawidłowa.
    Przykład:
    "Jaki kolor ma niebo?
     A: Zielony
     B: Niebieski
     C: Czerwony"
    
    DLACZEGO TAK FORMATUJEMY:
    Model AI musi "widzieć" pytanie w określonym formacie:
    1. <video> - znacznik mówiący "tu jest wideo"
    2. Pytanie
    3. Opcje A, B, C, D
    
    To jak wypełnianie formularza egzaminacyjnego - musi być w standardowej formie.

    Args:
        row: Słownik z danymi pytania zawierający:
            - 'question': Tekst pytania
            - 'a', 'b', 'c', 'd': Opcje odpowiedzi (opcjonalne)

    Returns:
        Sformatowany prompt w formacie: "<video> \n [pytanie] \n A: ... B: ..."
        
    PRZYKŁAD:
    Input: {"question": "Jaka pogoda?", "a": "słonecznie", "b": "deszczowo"}
    Output: "<video> \n Jaka pogoda? \n A: słonecznie \n B: deszczowo \n "
    """
    # 🎓 Rozpocznij od znacznika <video> i pytania
    prompt = f"<video> \n {row['question']} \n "

    # 🎓 Dodaj wszystkie dostępne opcje odpowiedzi (A, B, C, D)
    # Iterujemy przez wszystkie możliwe opcje
    for option in ["a", "b", "c", "d"]:
        # Sprawdź czy ta opcja istnieje w danych
        if option in row:
            # Dodaj opcję w formacie "A: odpowiedź"
            # option.upper() zmienia 'a' na 'A'
            prompt += f"{option.upper()}: {row[option]} \n "

    return prompt


def format_training_data_mcq_llava(
    id: str,
    video_file: str,
    question: str,
    answer: str,
    qtype: str,
    phase: str,
    wts_id: str,
) -> Dict[str, Any]:
    """Formatuj dane treningowe dla zadań MCQ w formacie konwersacji LLaVA.

    🎓 WYJAŚNIENIE - FORMAT LLaVA:
    LLaVA to format używany przez modele vision-language (widzenie + język).
    Przedstawia dane jako "konwersację" między człowiekiem a AI.
    
    STRUKTURA KONWERSACJI:
    1. "human" (człowiek) - zadaje pytanie, pokazuje wideo
    2. "gpt" (model AI) - odpowiada
    
    DLACZEGO TAK:
    - Modele AI uczą się przez "rozmowę"
    - To naturalna forma interakcji
    - Łatwa do walidacji (jedna odpowiedź = jeden przykład)

    Args:
        id: Unikalny identyfikator próbki treningowej (np. "video1_q3")
        video_file: Ścieżka do pliku wideo (np. "scene123/overhead_view/cam1.mp4")
        question: Tekst pytania z opcjami MCQ (już sformatowany przez process_question)
        answer: Prawidłowa odpowiedź (litera A, B, C lub D)
        qtype: Typ pytania (np. "environment", "behavior", "safety")
        phase: Faza sceny drogowej (np. "full_video", "before_incident")
        wts_id: Identyfikator sceny WTS (np. "WTS_001234")

    Returns:
        Słownik z danymi treningowymi w formacie LLaVA:
        {
            "id": ...,           # Identyfikator
            "video": ...,        # Ścieżka do wideo
            "type": ...,         # Typ pytania
            "conversations": [   # Konwersacja human-gpt
                {"from": "human", "value": "pytanie..."},
                {"from": "gpt", "value": "A"}
            ]
        }
        
    🎓 PRZYKŁAD TRANSFORMACJI:
    Input:
        id="scene1_0"
        video_file="scene1/overhead_view/video.mp4"
        question="<video> Jaka pogoda? A: słonecznie B: deszczowo"
        answer="a"
        
    Output:
        {
            "id": "scene1_0",
            "video": "scene1/overhead_view/video.mp4",
            "conversations": [
                {
                    "from": "human",
                    "value": "<video> Jaka pogoda? A: słonecznie B: deszczowo\nAnswer with..."
                },
                {"from": "gpt", "value": "A"}
            ]
        }
    """
    # 🎓 Utwórz słownik z wszystkimi metadanymi
    item = {
        "id": id,              # Unikalny identyfikator próbki
        "wts_id": wts_id,      # ID sceny w zbiorze WTS
        "video": video_file,   # Ścieżka do wideo
        "type": qtype,         # Typ pytania (do późniejszej analizy)
        "phase": phase,        # Faza sceny (do późniejszej analizy)
        
        # 🎓 Kluczowa część - konwersacja w formacie LLaVA
        "conversations": [
            {
                "from": "human",  # Pytanie od człowieka
                "value": question
                + "\nAnswer with the option's letter from the given choices directly.",
                # 🎓 Instrukcja: "Odpowiedz literą opcji bezpośrednio"
                # To mówi modelowi jak ma sformatować odpowiedź
            },
            {
                "from": "gpt",           # Odpowiedź od modelu
                "value": answer.upper()  # Litera w wersji wielkiej (A, B, C, D)
            },
        ],
    }
    return item


def process_wts_environment_mcq(root_dir: str, split: str) -> List[Dict]:
    """Przetwórz dane MCQ dotyczące środowiska z widoków WTS.

    🎓 WYJAŚNIENIE - CO TO SĄ PYTANIA O ŚRODOWISKO:
    "Environment" (środowisko) to pytania o warunki w których odbywa się scena:
    - Pogoda (słonecznie, deszczowo, mgliście)
    - Pora dnia (dzień, noc, zmierzch)
    - Stan drogi (sucha, mokra, oblodzona)
    - Widoczność (dobra, ograniczona)
    
    DLACZEGO TO JEST WAŻNE:
    Warunki środowiskowe wpływają na bezpieczeństwo ruchu drogowego.
    Model musi nauczyć się rozpoznawać te warunki z wideo.

    STRUKTURA DANYCH WTS:
    WTS/
    ├── scene_001/
    │   ├── overhead_view/        # Wideo z góry
    │   │   ├── video1.mp4
    │   │   └── video2.mp4
    │   └── environment/          # Adnotacje środowiska
    │       └── scene_001.json
    ├── scene_002/
    └── ...

    Args:
        root_dir: Bazowa ścieżka do plików wejściowych (katalog ze scenami)
        split: Nazwa podziału danych ("train", "val", "test")

    Returns:
        Lista słowników z sformatowanymi danymi MCQ dla wszystkich scen
        
    🎓 PROCES KROK PO KROKU:
    1. Przejdź przez wszystkie katalogi scen
    2. Dla każdej sceny, załaduj plik environment JSON
    3. Dla każdego wideo w scenie:
       - Dla każdego pytania o środowisko:
         - Przetwórz pytanie (dodaj opcje A, B, C, D)
         - Sformatuj do LLaVA
         - Dodaj do listy wynikowej
    4. Zwróć wszystkie przetworzone próbki
    """
    # 🎓 Lista do przechowywania wszystkich przetworzonych próbek
    mcq_env_dataset = []
    root_dir = os.path.join(root_dir)

    # 🎓 Przejdź przez wszystkie katalogi w root_dir
    # tqdm() pokazuje pasek postępu - widzisz ile pracy zostało
    for name in tqdm(os.listdir(root_dir)):
        # 🎓 Pomiń pliki "normal_trimmed" - są przetwarzane osobno
        if "normal_trimmed" in name:
            continue

        # 🎓 Skonstruuj ścieżkę do pliku JSON z adnotacjami środowiska
        # Struktura: root_dir/nazwa_sceny/environment/nazwa_sceny.json
        env_file = os.path.join(root_dir, name, "environment", name + ".json")
        
        # 🎓 Sprawdź czy plik istnieje (może być niepełny zbiór danych)
        if not os.path.exists(env_file):
            print(f"Environment file not found for {name}")
            continue

        # 🎓 Załaduj plik JSON z adnotacjami
        with open(env_file, "r") as e:
            data = json.load(e)

        # 🎓 Pobierz ID sceny WTS (używane do śledzenia)
        wts_id = data[0]["id"]

        # 🎓 Przetwórz pytania o środowisko dla każdego wideo w scenie
        for vid in data[0]["overhead_videos"]:
            # 🎓 Usuń rozszerzenie pliku (.mp4) do tworzenia ID
            fir = vid[:-4]
            cnt = 0  # Licznik pytań dla tego wideo
            
            # 🎓 Skonstruuj pełną ścieżkę do pliku wideo
            vid2 = os.path.join(name, "overhead_view", vid)
            
            # 🎓 Specjalna obsługa dla "normal_trimmed" - dodaj prefix
            if "normal_trimmed" in root_dir:
                vid2 = "normal_trimmed/" + vid2

            # 🎓 Przetwórz każde pytanie o środowisko
            for row in data[0]["environment"]:
                # 🎓 Utwórz unikalny identyfikator: nazwa_pliku_numer_pytania
                lab = fir + "_" + str(cnt)
                
                # 🎓 KROK 1: Przetwórz pytanie (dodaj opcje A, B, C, D)
                question = process_question(row)
                
                # 🎓 KROK 2: Sformatuj do formatu LLaVA
                item = format_training_data_mcq_llava(
                    lab,                 # ID próbki
                    vid2,                # Ścieżka do wideo
                    question,            # Sformatowane pytanie
                    row["correct"],      # Prawidłowa odpowiedź (a, b, c, d)
                    "environment",       # Typ pytania
                    "full_video",        # Faza (pełne wideo)
                    wts_id,             # ID sceny WTS
                )
                
                # 🎓 KROK 3: Dodaj do zbioru danych
                mcq_env_dataset.append(item)
                cnt += 1  # Zwiększ licznik pytań

    return mcq_env_dataset


def main():
    """Główna funkcja wykonawcza orkiestrująca kompletny pipeline przetwarzania danych.

    🎓 WYJAŚNIENIE - CO TO JEST PIPELINE:
    Pipeline to "rurociąg" - sekwencja kroków przetwarzania danych.
    Każdy krok przetwarza dane i przekazuje je dalej.
    
    PIPELINE W TYM SKRYPCIE:
    1. Parsowanie argumentów (gdzie są dane?)
    2. Ładowanie surowych danych WTS
    3. Przetwarzanie do formatu LLaVA
    4. Zapisywanie wyników do plików JSON
    
    DLACZEGO ROZDZIELAMY TRAIN I VAL:
    - train (treningowy) - dane do uczenia modelu
    - val (walidacyjny) - dane do sprawdzenia czy model dobrze się uczy
    
    To jak podział na:
    - Zadania domowe (uczymy się)
    - Sprawdziany (sprawdzamy wiedzę)
    
    Model NIE widzi danych val podczas treningu - inaczej byłoby to ściąganie!

    🎓 PROCES KROK PO KROKU:
    """
    # 🎓 KROK 1: Parsuj argumenty i przygotuj katalogi
    user_path = parse_arguments()
    os.makedirs(user_path, exist_ok=True)  # Utwórz katalog jeśli nie istnieje

    print("Starting WTS annotations processing...")

    # 🎓 KROK 2: Przetwórz zbiory treningowe MCQ
    print("\n📚 Przetwarzanie zbioru treningowego...")
    
    # 🎓 Przetwórz główny zbiór treningowy
    train_mcq_env_dataset = process_wts_environment_mcq(
        os.path.join(user_path, "annotations", "vqa", "train"), 
        "train"
    )
    
    # 🎓 Dodaj również dane "normal_trimmed" (przycięte wideo)
    # += oznacza "dodaj do istniejącej listy"
    train_mcq_env_dataset += process_wts_environment_mcq(
        os.path.join(user_path, "annotations", "vqa", "train", "normal_trimmed"),
        "train",
    )

    # 🎓 KROK 3: Zapisz zbiór treningowy do JSON
    output_dir = user_path
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "environment_mcq_llava_train.json")
    with open(output_file, "w") as f:
        # indent=4 sprawia że JSON jest czytelny (sformatowany)
        json.dump(train_mcq_env_dataset, f, indent=4)
    
    print(f"✅ Zapisano zbiór treningowy: {output_file}")

    # 🎓 KROK 4: Przetwórz zbiory walidacyjne MCQ
    print("\n🔍 Przetwarzanie zbioru walidacyjnego...")
    
    val_mcq_env_dataset = process_wts_environment_mcq(
        os.path.join(user_path, "annotations", "vqa", "val"), 
        "val"
    )
    val_mcq_env_dataset += process_wts_environment_mcq(
        os.path.join(user_path, "annotations", "vqa", "val", "normal_trimmed"), 
        "val"
    )

    # 🎓 KROK 5: Zapisz zbiór walidacyjny
    output_file = os.path.join(output_dir, "environment_mcq_llava_val.json")
    with open(output_file, "w") as f:
        json.dump(val_mcq_env_dataset, f, indent=4)
    
    print(f"✅ Zapisano zbiór walidacyjny: {output_file}")

    # 🎓 KROK 6: Podsumowanie
    print("\n" + "="*60)
    print("✨ Przetwarzanie adnotacji WTS zakończone!")
    print("="*60)
    print(f"📊 Statystyki:")
    print(f"   • Zbiór treningowy:    {len(train_mcq_env_dataset):,} próbek")
    print(f"   • Zbiór walidacyjny:   {len(val_mcq_env_dataset):,} próbek")
    print(f"   • Suma:                {len(train_mcq_env_dataset) + len(val_mcq_env_dataset):,} próbek")
    print("\n🎯 Dane gotowe do treningu modelu!")
    print("="*60)


if __name__ == "__main__":
    main()
