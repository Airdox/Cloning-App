"""
Voice Cloning App - A secure Kivy application for voice model training and synthesis.

This module provides a GUI application for training voice models and performing
text-to-speech synthesis with security best practices implemented.
"""

import re
import secrets
import logging
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock

# Configure logging for security and debugging
logging.basicConfig(level=logging.INFO)


class SecurityValidator:
    """Utility class for input validation and security checks."""

    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """
        Validate file path to prevent path traversal attacks.

        Args:
            file_path: Path to validate

        Returns:
            True if path is safe, False otherwise
        """
        try:
            # Resolve path and check if it's within allowed directories
            resolved_path = Path(file_path).resolve()
            home_path = Path.home().resolve()

            # Allow files only within user's home directory or common safe directories
            allowed_paths = [home_path, Path("/tmp").resolve()]

            return any(
                str(resolved_path).startswith(str(allowed_path))
                for allowed_path in allowed_paths
            )
        except (OSError, ValueError):
            return False

    @staticmethod
    def sanitize_text_input(text: str, max_length: int = 1000) -> str:
        """
        Sanitize text input to prevent injection attacks.

        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""

        # Remove potentially dangerous characters and limit length
        sanitized = text.strip()[:max_length]
        # Remove null bytes and other control characters
        sanitized = ''.join(char for char in sanitized if ord(char) >= 32)

        return sanitized

    @staticmethod
    def validate_model_name(name: str) -> bool:
        """
        Validate model name for safe file system usage.

        Args:
            name: Model name to validate

        Returns:
            True if name is safe, False otherwise
        """
        if not name or len(name) > 50:
            return False

        # Only allow alphanumeric characters, underscores, and hyphens
        return re.match(r'^[a-zA-Z0-9_-]+$', name) is not None


class VoiceCloningApp(App):
    """
    Main application class for voice cloning functionality.

    Provides a GUI interface for training voice models and performing
    text-to-speech synthesis with security features.
    """

    def __init__(self, **kwargs):
        """Initialize the application with secure defaults."""
        super().__init__(**kwargs)
        self.validator = SecurityValidator()
        self.logger = logging.getLogger(__name__)

        # Initialize UI components to None - will be created in build()
        self.main_layout = None
        self.tabs = None
        self.train_tab = None
        self.train_layout = None
        self.file_chooser = None
        self.select_button = None
        self.selected_files_label = None
        self.model_name_input = None
        self.train_button = None
        self.progress_layout = None
        self.progress_label = None
        self.progress_bar = None
        self.log_label = None
        self.log_output = None
        self.tts_tab = None
        self.tts_layout = None
        self.model_selection = None
        self.selected_model_label = None
        self.text_input = None
        self.synthesize_button = None
        self.play_button = None
        self.tts_status = None
        self.train_event = None

    def build(self):
        """Build the main application interface."""
        self.main_layout = BoxLayout(orientation='vertical')
        self.tabs = TabbedPanel(do_default_tab=False)

        # Create tabs
        self._create_training_tab()
        self._create_tts_tab()

        # Add tabs to main layout
        self.main_layout.add_widget(self.tabs)
        return self.main_layout

    def _create_training_tab(self):
        """Create the voice model training tab."""
        self.train_tab = TabbedPanelItem(text='Stimmenmodell trainieren')
        self.train_layout = BoxLayout(
            orientation='vertical', padding=10, spacing=10
        )

        # File selection section
        self.train_layout.add_widget(
            Label(text='Audiodateien für Training auswählen:')
        )

        # Use secure file chooser with restricted path
        safe_path = str(Path.home())
        self.file_chooser = FileChooserListView(path=safe_path)
        self.train_layout.add_widget(self.file_chooser)

        # File selection button
        self.select_button = Button(
            text='Dateien auswählen', size_hint=(1, 0.1)
        )
        self.select_button.bind(on_press=self.select_files)
        self.train_layout.add_widget(self.select_button)

        # Selected files display
        self.selected_files_label = Label(
            text='Keine Dateien ausgewählt', size_hint=(1, 0.1)
        )
        self.train_layout.add_widget(self.selected_files_label)

        # Model name input with validation
        self.model_name_input = TextInput(
            hint_text='Modellname eingeben (nur Buchstaben, Zahlen, _, -)',
            size_hint=(1, 0.1)
        )
        self.train_layout.add_widget(self.model_name_input)

        # Training start button
        self.train_button = Button(
            text='Training starten', size_hint=(1, 0.1)
        )
        self.train_button.bind(on_press=self.start_training)
        self.train_layout.add_widget(self.train_button)

        # Progress section
        self._create_progress_section()

        # Log section
        self._create_log_section()

        self.train_tab.add_widget(self.train_layout)
        self.tabs.add_widget(self.train_tab)

    def _create_progress_section(self):
        """Create the progress tracking section."""
        self.progress_layout = BoxLayout(
            orientation='vertical', size_hint=(1, 0.2)
        )
        self.progress_label = Label(text='Fortschritt: 0%')
        self.progress_bar = ProgressBar(max=100, value=0)
        self.progress_layout.add_widget(self.progress_label)
        self.progress_layout.add_widget(self.progress_bar)
        self.train_layout.add_widget(self.progress_layout)

    def _create_log_section(self):
        """Create the logging output section."""
        self.log_label = Label(
            text='Log-Ausgabe:', size_hint=(1, 0.1), halign='left'
        )
        self.log_label.bind(size=self.log_label.setter('text_size'))
        self.train_layout.add_widget(self.log_label)

        self.log_output = Label(
            text='', size_hint=(1, 0.3), halign='left', valign='top'
        )
        self.log_output.bind(size=self.log_output.setter('text_size'))
        self.train_layout.add_widget(self.log_output)

    def _create_tts_tab(self):
        """Create the text-to-speech tab."""
        self.tts_tab = TabbedPanelItem(text='Text-to-Speech')
        self.tts_layout = BoxLayout(
            orientation='vertical', padding=10, spacing=10
        )

        # Model selection
        self.tts_layout.add_widget(Label(text='Stimmenmodell auswählen:'))
        self.model_selection = Button(
            text='Modell auswählen', size_hint=(1, 0.1)
        )
        self.model_selection.bind(on_press=self.select_model)
        self.tts_layout.add_widget(self.model_selection)

        # Selected model display
        self.selected_model_label = Label(
            text='Kein Modell ausgewählt', size_hint=(1, 0.1)
        )
        self.tts_layout.add_widget(self.selected_model_label)

        # Text input
        self.tts_layout.add_widget(Label(text='Text eingeben:'))
        self.text_input = TextInput(
            hint_text='Text für Sprachsynthese eingeben (max 1000 Zeichen)',
            size_hint=(1, 0.3)
        )
        self.tts_layout.add_widget(self.text_input)

        # Synthesis button
        self.synthesize_button = Button(
            text='Sprachsynthese starten', size_hint=(1, 0.1)
        )
        self.synthesize_button.bind(on_press=self.start_synthesis)
        self.tts_layout.add_widget(self.synthesize_button)

        # Play button
        self.play_button = Button(
            text='Audio abspielen', size_hint=(1, 0.1), disabled=True
        )
        self.play_button.bind(on_press=self.play_audio)
        self.tts_layout.add_widget(self.play_button)

        # Status display
        self.tts_status = Label(text='Bereit', size_hint=(1, 0.1))
        self.tts_layout.add_widget(self.tts_status)

        self.tts_tab.add_widget(self.tts_layout)
        self.tabs.add_widget(self.tts_tab)

    def select_files(self, _instance):
        """
        Handle file selection with security validation.

        Args:
            _instance: Button instance (unused but required by Kivy)
        """
        selected = self.file_chooser.selection
        if selected:
            # Validate all selected file paths
            valid_files = []
            for file_path in selected:
                if self.validator.validate_file_path(file_path):
                    valid_files.append(file_path)
                else:
                    self.logger.warning("Invalid file path rejected: %s", file_path)

            if valid_files:
                self.selected_files_label.text = f'{len(valid_files)} Dateien ausgewählt'
                file_names = [Path(f).name for f in valid_files]
                self.log_output.text += (
                    f'Validierte Dateien ausgewählt: {", ".join(file_names)}\n'
                )
            else:
                self.selected_files_label.text = 'Keine gültigen Dateien'
                self.log_output.text += 'Fehler: Keine gültigen Dateien gefunden\n'
        else:
            self.selected_files_label.text = 'Keine Dateien ausgewählt'

    def start_training(self, _instance):
        """
        Start the training process with security validation.

        Args:
            _instance: Button instance (unused but required by Kivy)
        """
        try:
            # Validate file selection
            if not self.file_chooser.selection:
                self.log_output.text += 'Fehler: Keine Audiodateien ausgewählt\n'
                return

            # Validate and sanitize model name
            raw_model_name = self.model_name_input.text.strip()
            if not self.validator.validate_model_name(raw_model_name):
                self.log_output.text += (
                    'Fehler: Ungültiger Modellname. '
                    'Nur Buchstaben, Zahlen, _ und - erlaubt (max 50 Zeichen)\n'
                )
                return

            # Sanitize model name
            model_name = self.validator.sanitize_text_input(raw_model_name, 50)

            self.log_output.text += f'Training gestartet für Modell: {model_name}\n'
            self.progress_bar.value = 0
            self.progress_label.text = 'Fortschritt: 0%'

            # Start simulated training progress
            self.train_event = Clock.schedule_interval(self.update_progress, 0.5)

        except Exception as e:
            self.logger.error("Error in start_training: %s", e)
            self.log_output.text += f'Fehler beim Trainingsstart: {str(e)}\n'

    def update_progress(self, _dt):
        """
        Update training progress with secure random generation.

        Args:
            _dt: Time delta (unused but required by Kivy Clock)
        """
        try:
            if self.progress_bar.value >= 100:
                if self.train_event:
                    self.train_event.cancel()
                self.log_output.text += 'Training abgeschlossen!\n'
                self.progress_label.text = 'Fortschritt: 100%'
                return

            # Use secure random for simulation (replaced insecure random.randint)
            progress_increment = secrets.randbelow(5) + 1  # 1-5 range
            new_value = min(self.progress_bar.value + progress_increment, 100)
            self.progress_bar.value = new_value
            self.progress_label.text = f'Fortschritt: {int(new_value)}%'

            # Log updates at intervals
            current_progress = int(new_value)
            previous_progress = int(self.progress_bar.value - progress_increment)
            if current_progress % 10 == 0 and current_progress != previous_progress:
                self.log_output.text += f'Training bei {current_progress}% abgeschlossen...\n'

        except Exception as e:
            self.logger.error("Error in update_progress: %s", e)
            if self.train_event:
                self.train_event.cancel()

    def select_model(self, _instance):
        """
        Simulate model selection with secure randomization.

        Args:
            _instance: Button instance (unused but required by Kivy)
        """
        try:
            # In a real app, this would show a file dialog
            models = ['Modell_1', 'Modell_2', 'Modell_3']
            # Use secure random instead of random.choice
            selected_index = secrets.randbelow(len(models))
            selected_model = models[selected_index]
            self.selected_model_label.text = f'Ausgewähltes Modell: {selected_model}'
            self.logger.info("Model selected: %s", selected_model)

        except Exception as e:
            self.logger.error("Error in select_model: %s", e)
            self.selected_model_label.text = 'Fehler bei Modellauswahl'

    def start_synthesis(self, _instance):
        """
        Start text synthesis with input validation.

        Args:
            _instance: Button instance (unused but required by Kivy)
        """
        try:
            # Validate model selection
            if self.selected_model_label.text == 'Kein Modell ausgewählt':
                self.tts_status.text = 'Fehler: Kein Modell ausgewählt'
                return

            # Validate and sanitize text input
            raw_text = self.text_input.text
            if not raw_text or not raw_text.strip():
                self.tts_status.text = 'Fehler: Kein Text eingegeben'
                return

            # Sanitize text input to prevent injection attacks
            sanitized_text = self.validator.sanitize_text_input(raw_text, 1000)

            if len(sanitized_text) != len(raw_text):
                self.tts_status.text = 'Text wurde bereinigt - bitte überprüfen'
                self.text_input.text = sanitized_text
                return

            self.tts_status.text = 'Sprachsynthese läuft...'
            self.logger.info("Starting synthesis for %d characters", len(sanitized_text))

            # Simulate processing time
            Clock.schedule_once(self.finish_synthesis, 2)

        except Exception as e:
            self.logger.error("Error in start_synthesis: %s", e)
            self.tts_status.text = f'Fehler: {str(e)}'

    def finish_synthesis(self, _dt):
        """
        Complete the synthesis process.

        Args:
            _dt: Time delta (unused but required by Kivy Clock)
        """
        try:
            self.tts_status.text = 'Sprachsynthese abgeschlossen'
            self.play_button.disabled = False
            self.logger.info("Synthesis completed successfully")

        except Exception as e:
            self.logger.error("Error in finish_synthesis: %s", e)
            self.tts_status.text = 'Fehler beim Abschluss der Synthese'

    def play_audio(self, _instance):
        """
        Simulate audio playback.

        Args:
            _instance: Button instance (unused but required by Kivy)
        """
        try:
            self.tts_status.text = 'Audio wird abgespielt...'
            self.logger.info("Audio playback started")

            def _finish_playback(_dt):
                self.tts_status.text = 'Audio abgespielt'
                self.logger.info("Audio playback completed")

            Clock.schedule_once(_finish_playback, 2)

        except Exception as e:
            self.logger.error("Error in play_audio: %s", e)
            self.tts_status.text = 'Fehler beim Abspielen'

if __name__ == '__main__':
    app = VoiceCloningApp()
    app.run()
