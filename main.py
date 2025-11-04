import sys
import csv
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QLabel,
)
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class SimpleAudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простой аудиоплеер")
        self.setGeometry(0, 0, 400, 800)
        # Создаём .csv файл
        with open("status_log.csv", "w", encoding="utf-8", newline="") as state_file:
            writer = csv.writer(state_file)
            writer.writerow(["Номер действия", "Действие"])
            self.action_counter = 0
        with open("status_log.csv", "r", encoding="utf-8", newline="") as state_file:
            reader = csv.reader(state_file)
            self.rows = list(reader)

        self.file_name = ""
        self.vol = 100.0

        # Создаем медиаплеер
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(self.vol)

        # Создаём кнопку для выбора файла
        self.open_button = QPushButton("Открыть файл", self)
        self.open_button.setGeometry(50, 30, 100, 40)
        self.open_button.clicked.connect(self.open_music_file)
        self.open_button.move(200, 400)

        # Создаем кнопку для проигрывания фалйа
        self.play_pause_button = QPushButton("Воспроизвести", self)
        self.play_pause_button.setGeometry(50, 30, 100, 40)
        self.play_pause_button.clicked.connect(self.play_audio)
        self.play_pause_button.move(100, 100)

        # Создаём поле с состоянием проигрывания и подписываем его
        self.song_status = QLineEdit(self)
        self.song_status.move(100, 200)
        self.song_status.setText("Выберите файл")
        self.song_status_label = QLabel(self)
        self.song_status_label.setText("Состояние:")
        self.song_status_label.move(20, 200)

        # Создаём поле для ввода значения звука и кнопку для подтверждения ввода
        self.loudness = QLineEdit(self)
        self.loudness.move(100, 300)
        self.loudness_label = QLabel(self)
        self.loudness_label.setText("Громкость, %:")
        self.loudness_label.move(15, 300)
        self.loudness_button = QPushButton(self)
        self.loudness_button.move(200, 300)
        self.loudness_button.clicked.connect(self.change_loudness)
        self.loudness_button.setText("Подтвердить")

    def play_audio(self):
        """Воспроизведение или пауза при нажатии на кнопку"""

        # Добавляем данные в .csv файл
        self.rows.append([self.action_counter, "Начато воспроизведение"])
        with open("status_log.csv", "w", encoding="utf-8", newline="") as state_file:
            writer = csv.writer(state_file)
            writer.writerows(self.rows)
            self.action_counter += 1
        self.player.play()

        # Вписываем состояние файла в поле
        if QMediaPlayer.isPlaying(self.player):
            self.song_status.setText("Проигрывается")
        else:
            self.song_status.setText("Выберите файл")

        # Устанавливаем начальное значение звука
        if self.vol < 100:
            self.loudness.setText(f"{str(self.vol)}%")
        else:
            self.loudness.setText("100.0%")

    def open_music_file(self):
        """Открытие файла через диалоговое окно"""

        # Добавляем данные в .csv файл
        self.rows.append([self.action_counter, "Открыт файл"])
        with open("status_log.csv", "w", encoding="utf-8", newline="") as state_file:
            writer = csv.writer(state_file)
            writer.writerows(self.rows)
            self.action_counter += 1
        # Получаем путь к файлу и сохраняем его в переменную
        self.file_name = QFileDialog.getOpenFileName(self, "OpenFile")[0]

        # Загружаем файл по сохранённому пути
        self.player.setSource(QUrl.fromLocalFile(self.file_name))

        if QMediaPlayer.isPlaying(self.player):
            self.song_status.setText("Проигрывается")
        else:
            self.song_status.setText("На паузе")

    def change_loudness(self):
        """Установка громкости на введённое значение"""

        # Получаем новое значение звука в процентах и изменяем громкость
        try:
            # Добавляем данные в .csv файл
            self.rows.append([self.action_counter, "Изменена громкость"])
            with open(
                "status_log.csv", "w", encoding="utf-8", newline=""
            ) as state_file:
                writer = csv.writer(state_file)
                writer.writerows(self.rows)
                self.action_counter += 1
            self.vol = float(self.loudness.text())
        except ValueError:
            # Добавляем данные в .csv файл
            self.rows.append(
                [self.action_counter, "Введено неверное значение громкости"]
            )
            with open(
                "status_log.csv", "w", encoding="utf-8", newline=""
            ) as state_file:
                writer = csv.writer(state_file)
                writer.writerows(self.rows)
                self.action_counter += 1
        self.audio_output.setVolume(self.vol / 100)

        # Изменяем текст в поле для ввода звука
        if self.vol < 100:
            self.loudness.setText(f"{str(self.vol)}%")
        else:
            self.loudness.setText("100.0%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleAudioPlayer()
    window.show()
    sys.exit(app.exec())
