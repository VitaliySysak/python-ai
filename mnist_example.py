import os
import numpy as np
import matplotlib.pyplot as plt

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

from PIL import Image



def save_image(image_data, image_path):
    """
    Зберігає зображення у відтінках сірого за вказаним шляхом.
    Використовується для збереження прикладів зображень із набору MNIST.
    """
    plt.imshow(image_data, cmap='gray')
    plt.savefig(image_path)


def display_img_data(X, y):
    """
    Виводить 10 перших зображень з підписами відповідних міток.
    Застосовується для візуального перегляду даних навчального набору.
    """
    plt.figure(figsize=(10, 5))
    for i in range(10):
        image_data = X[i]
        plt.subplot(2, 5, i + 1)
        plt.imshow(image_data, cmap='gray')
        plt.title(f"Label: {y[i]}")
        plt.axis('off')
    plt.show()


def save_img_data_to_file(X, y, folder_name):
    """
    Зберігає перші 10 зображень з набору у вказану директорію.
    Кожне зображення записується як окремий PNG-файл.
    """
    plt.figure()
    plt.axis('off')
    for i in range(10):
        image_data = X[i]
        image_path = os.path.join(folder_name, f"image_{i}.png")
        save_image(image_data, image_path)
    plt.close()


def prepare_mnist_data():
    """
    Завантажує набір даних MNIST, змінює форму даних та нормалізує пікселі (0-1).
    Повертає навчальний та тестовий набори.
    """
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0
    return x_train, y_train, x_test, y_test


def train_and_save_model(model_path, x_train, y_train, x_test, y_test):
    """
    Створює, компілює та навчає згорткову нейронну мережу.
    Зберігає модель у файл .h5 після навчання.
    """
    # Побудова моделі
    model = keras.Sequential([
        layers.Conv2D(32, 3, activation="relu", input_shape=(28, 28, 1)),
        layers.MaxPooling2D(2),
        layers.Dropout(0.25),
        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(2),
        layers.Dropout(0.25),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(10, activation="softmax"),
    ])
    # Компіляція моделі
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )
    # Навчання моделі
    model.fit(x_train, y_train, batch_size=64, epochs=5, verbose=2)
    # Оцінка моделі
    loss, accuracy = model.evaluate(x_test, y_test, verbose=2)
    print(f"Значення втрат на тестовому наборі: {loss:.4f}")
    print(f"Точність на тестовому наборі: {accuracy:.4f}")
    # Збереження моделі
    model.save(model_path)


def predict_using_raw_data(model_path, X_data, y_data):
    """
    Завантажує збережену модель і виконує передбачення на масиві зображень (numpy).
    Виводить реальні та передбачені мітки.
    """
    ...

    loaded_model = keras.models.load_model(model_path)
    predictions = loaded_model.predict(X_data)
    print(f"Вихідні дані:      {y_data}")
    print(f"Прогнозовані дані: {predictions.argmax(axis=1)}")


def predict_using_img_data(model_path, image_path):
    """
    Завантажує модель і виконує передбачення на одному зображенні з диска.
    Повертає передбачену цифру.
    """
    loaded_model = keras.models.load_model(model_path)
    # Завантаження та обробка зображення
    img = Image.open(image_path).convert("L")                               # Відкриття та перетворення в чорно-біле
    img = img.resize((28, 28))                                              # Зміна розміру до 28x28
    img_array = np.array(img)                                               # Перетворення в numpy масив
    img_array = img_array.reshape(1, 28, 28, 1).astype("float32") / 255.0   # Форматування та нормалізація
    # Прогнозування
    prediction = loaded_model.predict(img_array)
    predicted_digit = np.argmax(prediction)
    return predicted_digit

def analyze_prediction_accuracy_per_class(model_path, X_data, y_data, result_file_path):
    """
    Аналізує точність розпізнавання по кожній цифрі (0-9).
    Зберігає статистику у текстовий файл.
    """
    model = keras.models.load_model(model_path)
    predictions = model.predict(X_data)
    predicted_labels = predictions.argmax(axis=1)

    class_counts = {i: 0 for i in range(10)}
    correct_counts = {i: 0 for i in range(10)}

    for true, pred in zip(y_data, predicted_labels):
        class_counts[true] += 1
        if true == pred:
            correct_counts[true] += 1

    with open(result_file_path, "w", encoding="utf-8") as f:
        f.write("=== Аналіз точності по класах ===\n")
        for digit in range(10):
            total = class_counts[digit]
            correct = correct_counts[digit]
            accuracy = (correct / total * 100) if total > 0 else 0
            f.write(f"Цифра {digit}: точність {accuracy:.2f}% ({correct}/{total} правильних)\n")

        total_correct = sum(correct_counts.values())
        total_samples = len(y_data)
        overall_accuracy = total_correct / total_samples * 100
        f.write(f"\nЗагальна точність: {overall_accuracy:.2f}% ({total_correct}/{total_samples})\n")



def main():
    x_train, y_train, x_test, y_test = prepare_mnist_data()

    folder_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(folder_path, "models/mnist_model_after_modify.h5")
    if not os.path.exists(model_path):
        train_and_save_model(model_path, x_train, y_train, x_test, y_test)

    digits_num = 20
    predict_using_raw_data(model_path, x_test[:digits_num], y_test[:digits_num])

    display_img_data(x_train, y_train)
    save_img_data_to_file(x_train, y_train, folder_path)

    images = ["image_1.png", "image_2.png", "my_images/test_five.png", "my_images/test_zero.png", "my_images/test_three.png"]
    for image in images:
        image_path = os.path.join(folder_path, image)
        image = Image.open(image_path)
        plt.figure()
        plt.imshow(image)
        plt.axis('off')
        plt.show()
        predicted_digit = predict_using_img_data(model_path, image_path)
        print(f"Predicted digit: {predicted_digit}")

    # модель розпізнала 2/3 намальованих мною зображень
    # найгірше розпізнає 8
    result_file = os.path.join(folder_path, "results.txt")
    analyze_prediction_accuracy_per_class(model_path, x_test[:digits_num], y_test[:digits_num], result_file)



if __name__ == "__main__":
    main()
