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

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "cosmos-reason2-utils[inference]",
#   "datasets",
#   "vllm",
# ]
# [tool.uv.sources]
# cosmos-reason2-utils = { path = "../../cosmos_reason2_utils", editable = true }
# ///

"""Uruchamianie inferencji na zbiorze danych videophy2 w trybie offline.

🎓 WYJAŚNIENIE DLA STUDENTÓW:
Ten skrypt analizuje wideo i ocenia, czy zjawiska fizyczne w nim pokazane są wiarygodne.
Na przykład, jeśli widzimy jak piłka spada w górę zamiast w dół, model wykryje,
że to jest niewiarygodne fizycznie.

CO ROBI TEN SKRYPT:
1. Pobiera metadane wideo z HuggingFace (bez pobierania samych wideo)
2. Przetwarza każde wideo przez model AI Cosmos Reason2
3. Model ocenia wiarygodność fizyczną na skali 1-5
4. Zapisuje wyniki w plikach JSON

DLACZEGO TO JEST WAŻNE:
- Pomaga wykrywać błędy w wygenerowanych wideo (np. w grach, filmach CGI)
- Trenowanie modeli AI do rozumienia fizyki
- Kontrola jakości w produkcji treści wideo

Przykład użycia:
    uv run examples/video_critic/inference_videophy2.py --model nvidia/Cosmos-Reason2-2B
"""

from cosmos_reason2_utils.init import init_script

# 🎓 WYJAŚNIENIE: init_script() przygotowuje środowisko do pracy
# Jest to pierwszy krok przed importowaniem innych modułów
init_script()

# 🎓 IMPORTY - Biblioteki potrzebne do działania skryptu:
import argparse  # Do parsowania argumentów linii poleceń (--model, --output-dir, etc.)
import json      # Do zapisywania i odczytywania danych w formacie JSON
import os        # Do operacji na plikach i katalogach
import re        # Do pracy z wyrażeniami regularnymi (szukanie wzorców w tekście)
import traceback # Do wyświetlania szczegółowych komunikatów o błędach
from pathlib import Path  # Do wygodnej pracy ze ścieżkami plików

# 🎓 Biblioteki zewnętrzne do pracy z AI:
import datasets  # HuggingFace datasets - do pobierania zbiorów danych
import qwen_vl_utils  # Narzędzia do przetwarzania wizji (obrazy i wideo)
import transformers  # Biblioteka do pracy z modelami transformerów
import vllm  # vLLM - szybka biblioteka do inferencji LLM (Large Language Models)
import yaml  # Do czytania plików konfiguracyjnych YAML
from cosmos_reason2_utils.script.inference import Offline
from cosmos_reason2_utils.text import SYSTEM_PROMPT, create_conversation
from cosmos_reason2_utils.vision import VisionConfig

# 🎓 ROOT - ścieżka do głównego katalogu projektu
# Path(__file__) zwraca ścieżkę do tego pliku
# .resolve() konwertuje ją na absolutną ścieżkę
# .parent.parent.parent idzie 3 poziomy w górę w strukturze katalogów
ROOT = Path(__file__).resolve().parent.parent.parent


def get_video_data(dataset_name: str, split: str = "train"):
    """Załaduj zbiór danych i zwróć URL-e wideo z prawdziwymi ocenami.
    
    🎓 WYJAŚNIENIE:
    Ta funkcja pobiera TYLKO metadane (informacje o wideo) z HuggingFace,
    nie pobiera samych plików wideo. Dzięki temu oszczędzamy czas i miejsce.
    
    Args:
        dataset_name: Nazwa zbioru danych w HuggingFace (np. "videophysics/videophy2_test")
        split: Która część zbioru ("train", "test", "validation")
    
    Returns:
        Lista słowników z informacjami o wideo:
        [{
            "video_url": "https://...",  # Link do wideo
            "ground_truth": 3.5           # Prawdziwa ocena fizyczności (1-5)
        }]
    
    DLACZEGO TO TAK DZIAŁA:
    - HuggingFace przechowuje zbiory danych w chmurze
    - load_dataset() pobiera tylko strukturę i metadane (szybko!)
    - Samo wideo jest ładowane dopiero podczas inferencji (oszczędność pamięci)
    """
    print(f"Loading dataset: {dataset_name}, split: {split}")
    
    # 🎓 Pobierz zbiór danych z HuggingFace Hub
    dataset = datasets.load_dataset(dataset_name)
    
    # 🎓 Wybierz odpowiednią część zbioru (train/test/validation)
    dataset_split = dataset[split]

    print(
        f"Dataset loaded successfully. {split} split has {len(dataset_split)} examples."
    )

    # 🎓 Przygotuj listę z danymi wideo
    video_data = []
    for example in dataset_split:
        video_data.append(
            {
                "video_url": example["video_url"],      # URL do wideo
                "ground_truth": example["pc"],          # pc = physical correctness (poprawność fizyczna)
            }
        )

    # 🎓 Wyświetl przykładowe dane żeby zobaczyć strukturę
    if video_data:
        print(f"Sample data: {video_data[0]}")
    return video_data


def parse_answer_from_text(text: str) -> float | None:
    """Wyodrębnij numeryczną odpowiedź z tekstu wygenerowanego przez model.

    🎓 WYJAŚNIENIE - DLACZEGO TA FUNKCJA JEST POTRZEBNA:
    Model AI nie zwraca tylko liczby - zwraca pełny tekst z wyjaśnieniami.
    Na przykład może zwrócić:
    "Po przeanalizowaniu wideo widzę, że fizyka jest poprawna. Ocena: 4"
    
    Ta funkcja musi znaleźć tę liczbę "4" w całym tekście.
    
    MOŻLIWE FORMATY ODPOWIEDZI:
    - Liczba sama w linii: "3" lub "4"
    - Z tekstem szablonu: "[Score between 1 and 5.]\n\n3"
    - Z wyjaśnieniem: "3\n\nOkej, widzę że..."
    
    Args:
        text: Pełna odpowiedź modelu (może być długa)
    
    Returns:
        float: Ocena 1-5 jeśli znaleziona
        None: Jeśli nie udało się znaleźć oceny
    
    DLACZEGO UŻYWAMY WYRAŻEŃ REGULARNYCH (REGEX):
    Regex pozwala znaleźć wzorce w tekście. Wzorzec "^([1-5])\.?\s*$" oznacza:
    ^ = początek linii
    [1-5] = dokładnie jedna cyfra od 1 do 5
    \.? = opcjonalna kropka
    \s* = dowolna ilość białych znaków (spacje, tabulatory)
    $ = koniec linii
    """
    # 🎓 Podziel tekst na linie (każda linia osobno)
    lines = text.strip().split("\n")

    # 🎓 Przeszukaj każdą linię w poszukiwaniu oceny
    for line in lines:
        line = line.strip()  # Usuń białe znaki z początku i końca
        
        # 🎓 Sprawdź czy linia zawiera pojedynczą cyfrę 1-5
        match = re.match(r"^([1-5])\.?\s*$", line)
        if match:
            try:
                # 🎓 match.group(1) zwraca pierwszą grupę z regex (cyfrę w nawiasach)
                value = float(match.group(1))
                return value
            except ValueError:
                # 🎓 Jeśli konwersja się nie uda, spróbuj następnej linii
                continue

    # 🎓 Jeśli nie znaleziono oceny w żadnej linii, zwróć None
    return None


def load_prompt_config(prompt_path: str) -> tuple[str, str]:
    """Załaduj konfigurację promptu z pliku YAML.
    
    🎓 WYJAŚNIENIE - CO TO JEST PROMPT:
    Prompt to instrukcja którą dajemy modelowi AI. To jak zadanie domowe - 
    musimy jasno wytłumaczyć co model ma zrobić.
    
    PRZYKŁAD PROMPTU:
    "Obejrzyj to wideo i oceń na skali 1-5 czy fizyka jest realistyczna.
     1 = całkowicie nierealistyczna, 5 = bardzo realistyczna"
    
    DLACZEGO UŻYWAMY YAML:
    - Łatwy do edycji (nie trzeba zmieniać kodu!)
    - Czytelny format
    - Można przechowywać różne prompty dla różnych zadań
    
    Args:
        prompt_path: Ścieżka do pliku YAML z promptem
    
    Returns:
        tuple: (system_prompt, user_prompt)
            - system_prompt: Ogólne instrukcje dla modelu (jego "rola")
            - user_prompt: Konkretne pytanie/zadanie
    
    STRUKTURA PLIKU YAML:
    system_prompt: "Jesteś ekspertem od fizyki..."
    user_prompt: "Oceń to wideo..."
    """
    # 🎓 Jeśli ścieżka nie jest absolutna, dodaj ROOT na początku
    # Dzięki temu możemy używać relatywnych ścieżek typu "prompts/video_reward.yaml"
    if not os.path.isabs(prompt_path):
        prompt_path = os.path.join(ROOT, prompt_path)

    # 🎓 Otwórz i załaduj plik YAML
    # yaml.safe_load() parsuje YAML do słownika Pythona
    with open(prompt_path, "r") as f:
        config = yaml.safe_load(f)

    # 🎓 Pobierz prompty z konfiguracji, użyj domyślnych jeśli nie ma
    system_prompt = config.get("system_prompt", SYSTEM_PROMPT)
    user_prompt = config.get("user_prompt", "")

    # 🎓 Sprawdź czy user_prompt istnieje - jest wymagany!
    if not user_prompt:
        raise ValueError(f"No user_prompt found in {prompt_path}")

    return system_prompt, user_prompt


def run_inference_for_video(
    llm: vllm.LLM,
    processor: transformers.Qwen3VLProcessor,
    video_url: str,
    system_prompt: str,
    user_prompt: str,
    vision_kwargs: dict | None,
    sampling_params: vllm.SamplingParams,
) -> str:
    """Uruchom inferencję (przewidywanie) dla pojedynczego wideo.

    🎓 WYJAŚNIENIE - CO TO JEST INFERENCJA:
    Inferencja to proces używania wytrenowanego modelu AI do robienia przewidywań.
    W naszym przypadku: model "ogląda" wideo i ocenia jego fizyczność.
    
    To jest jak egzamin - model już się nauczył, teraz sprawdzamy co potrafi.
    
    ETAPY INFERENCJI:
    1. Przygotowanie konwersacji (prompt + wideo)
    2. Przetworzenie wideo do formatu zrozumiałego dla modelu
    3. Uruchomienie modelu (generowanie odpowiedzi)
    4. Zwrócenie tekstu z odpowiedzią
    
    Args:
        llm: Załadowany model językowy (Large Language Model)
        processor: Procesor do przygotowania danych wejściowych
        video_url: Link do wideo do analizy
        system_prompt: Instrukcje systemowe dla modelu
        user_prompt: Konkretne pytanie użytkownika
        vision_kwargs: Parametry przetwarzania wideo (fps, rozdzielczość)
        sampling_params: Parametry generowania tekstu (temperatura, max_tokens)
    
    Returns:
        str: Tekstowa odpowiedź modelu
    
    DLACZEGO NIE POBIERAMY WIDEO:
    vLLM potrafi ładować wideo bezpośrednio z URL, więc nie musimy go pobierać.
    To oszczędza dysk i przyspiesza proces.
    """
    # 🎓 KROK 1: Utwórz konwersację (format czatu)
    # Model "widzi" konwersację jak rozmowę:
    # System: "Jesteś ekspertem..."
    # User: "Oceń to wideo..." [wideo]
    # Assistant: [tu model generuje odpowiedź]
    conversation = create_conversation(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        videos=[video_url],
        vision_kwargs=vision_kwargs,
    )

    # 🎓 KROK 2: Przetwórz dane wejściowe do formatu modelu
    # add_vision_ids określa czy dodawać identyfikatory dla wielu mediów
    # Mamy tylko 1 wideo, więc False
    add_vision_ids = False
    prompt = processor.apply_chat_template(
        conversation,
        tokenize=False,  # Nie tokenizuj jeszcze (zostanie zrobione później)
        add_generation_prompt=True,  # Dodaj znacznik rozpoczęcia generowania
        add_vision_ids=add_vision_ids,
    )

    # 🎓 KROK 3: Przetwórz wideo
    # process_vision_info() konwertuje wideo do tensorów (wielowymiarowych tablic liczb)
    # które model potrafi przetworzyć
    image_inputs, video_inputs, video_kwargs = qwen_vl_utils.process_vision_info(
        conversation,
        image_patch_size=processor.image_processor.patch_size,
        return_video_kwargs=True,
        return_video_metadata=True,
    )

    # 🎓 KROK 4: Przygotuj dane multimedialne dla modelu
    # Model może przyjąć zarówno obrazy jak i wideo, więc sprawdzamy co mamy
    mm_data = {}
    if image_inputs is not None:
        mm_data["image"] = image_inputs
    if video_inputs is not None:
        mm_data["video"] = video_inputs

    # 🎓 KROK 5: Połącz wszystko w jedną strukturę wejściową
    llm_inputs = {
        "prompt": prompt,                    # Tekst promptu
        "multi_modal_data": mm_data,        # Dane wideo
        "mm_processor_kwargs": video_kwargs, # Parametry przetwarzania
    }

    # 🎓 KROK 6: URUCHOM MODEL!
    # To jest moment, w którym model "myśli" i generuje odpowiedź
    # [llm_inputs] jest listą bo vLLM może przetwarzać wiele próbek naraz (batch)
    outputs = llm.generate([llm_inputs], sampling_params=sampling_params)

    # 🎓 KROK 7: Wyodrębnij tekst z odpowiedzi
    # outputs[0] - pierwsza (jedyna) odpowiedź
    # .outputs[0] - pierwszy (jedyny) wygenerowany tekst
    # .text - czysty tekst
    # .strip() - usuń białe znaki z początku i końca
    output_text = outputs[0].outputs[0].text.strip()
    return output_text


def run_inference_for_dataset(args):
    """Run inference on videos for a dataset."""
    # Load video data
    print(f"Loading videos from HuggingFace dataset: {args.dataset}")
    video_data = get_video_data(args.dataset, args.split)

    print(f"\nFound {len(video_data)} videos to process")

    if not video_data:
        print("❌ No videos to process!")
        return

    # Use provided output directory
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nUsing output directory: {output_dir}")

    # Load prompt configuration
    prompt_path = args.input_file
    system_prompt, user_prompt = load_prompt_config(prompt_path)

    # Create Offline args with defaults (will be used for vision_kwargs and sampling_params)
    offline_args = Offline(
        model=args.model,
        revision=args.revision,
        input_file=args.input_file,
        videos=[],  # Will be set per video
        images=[],
    )

    # Set vision kwargs for video processing
    vision_kwargs = {
        "fps": 16.0,
        "total_pixels": 8192 * 28 * 28,  # 6,422,528
        "max_pixels": None,
        "max_frames": None,
    }
    # Remove None values
    vision_kwargs = {k: v for k, v in vision_kwargs.items() if v is not None}
    VisionConfig.model_validate(vision_kwargs)

    # Initialize model and processor once (reused across all videos)
    print(f"\nInitializing vLLM model: {offline_args.model}")
    llm = vllm.LLM(
        model=offline_args.model,
        revision=offline_args.revision,
        max_model_len=offline_args.max_model_len,
        limit_mm_per_prompt={"video": 1},
        enforce_eager=True,
    )
    print("✓ Model loaded successfully")

    print("Loading processor...")
    processor: transformers.Qwen3VLProcessor = (
        transformers.AutoProcessor.from_pretrained(offline_args.model)
    )
    print("✓ Processor loaded successfully")

    # Create sampling params for inference
    sampling_kwargs = dict(offline_args.sampling_kwargs)
    sampling_kwargs.update(
        {
            "seed": 1,
            "temperature": 0,  # Greedy decoding
            "max_tokens": 2048,
        }
    )
    # Remove None values (top_p, top_k, repetition_penalty not set)
    sampling_kwargs = {k: v for k, v in sampling_kwargs.items() if v is not None}
    sampling_params = vllm.SamplingParams(**sampling_kwargs)

    # Process each video
    for i, video_item in enumerate(video_data, 1):
        video_url = video_item["video_url"]
        ground_truth = video_item["ground_truth"]

        json_path = os.path.join(output_dir, f"{i}.json")

        if os.path.exists(json_path):
            print(
                f"\n[{i}/{len(video_data)}] 📋 Results already exist: {os.path.basename(json_path)}. Skipping..."
            )
            continue

        print(f"\n[{i}/{len(video_data)}] Processing: {video_url}")

        try:
            # Run inference (reusing the same model)
            output_text = run_inference_for_video(
                llm=llm,
                processor=processor,
                video_url=video_url,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                vision_kwargs=vision_kwargs,
                sampling_params=sampling_params,
            )

            # Parse answer
            score = parse_answer_from_text(output_text)

            # Save results to JSON
            result_entry = {
                "video_url": video_url,
                "ground_truth": ground_truth,
                "output_text": output_text,
                "pred_score": score,
            }

            with open(json_path, "w") as f:
                json.dump(result_entry, f, indent=2)

            if score is not None:
                print(
                    f"✅ Saved results (score: {score}) to {os.path.basename(json_path)}"
                )
            else:
                print(f"✅ Saved results to {os.path.basename(json_path)}")
                print(f"   Output: {output_text[:200]}...")

        except Exception as e:
            print(f"❌ Error processing video: {str(e)}")
            traceback.print_exc()

    print(f"\n✅ Batch processing completed. Results saved to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    # Dataset arguments
    parser.add_argument(
        "--dataset",
        type=str,
        default="videophysics/videophy2_test",
        help='Dataset name (default: "videophysics/videophy2_test")',
    )
    parser.add_argument(
        "--split", type=str, default="test", help="Dataset split (default: test)"
    )

    # Model arguments
    parser.add_argument(
        "--model",
        type=str,
        default="nvidia/Cosmos-Reason2-2B",
        help="Model name or path (default: nvidia/Cosmos-Reason2-2B)",
    )
    parser.add_argument("--revision", type=str, default=None, help="Model revision")

    # Prompt arguments
    parser.add_argument(
        "--input-file",
        type=str,
        default="prompts/video_reward.yaml",
        help="Path to input yaml file",
    )

    # Output arguments
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/videophy2_test",
        help="Output directory for JSON results",
    )

    args = parser.parse_args()
    run_inference_for_dataset(args)


if __name__ == "__main__":
    main()
