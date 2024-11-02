# Описание

FINAL_train_qwen.ipynb - обучение модели

qwen_test.ipynb - файл для теста модели

## Запуск 

1) git clone https://github.com/Elisey-e/VK_hakaton.git

2) cd VK_hakaton

3) Скачать веса https://disk.yandex.ru/d/XQvAVgxdzT6vlw - папка qwen: исходная модель фиксированной версии(внимание: веса слишком большие, поэтому не были загружены, в метаданных есть версия нужного коммита); папка russia_chad: дообученная модель, поместить её в директорию проекта 

4) ""exec qwen_test.ipynb : Run All""

## Train

Загрузка датасета расположена в разделе Data

Требуемый формат выходного датасета(или фолда KFold):

DatasetDict({

    train: Dataset({
    
        features: ['text'],
        
        num_rows: 5341 })
        
    test: Dataset({
    
        features: ['text'],
        
        num_rows: 594})})


1) Ресурсы подгружаются как локально, так и из базы HF. Требуемые пути указаны в верхней части блокнота.
