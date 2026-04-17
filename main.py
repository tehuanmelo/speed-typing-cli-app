from textual.app import App
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Label, Header, Footer, Input, ListView, Static
from textual.binding import Binding
from textual import events
from data.data import sentences
import random
from time import time

class SpeedTyping(App):
    def __init__(self):
        super().__init__()
        self.current_sentence = None
        self.printed_sentence = None
        self.start = None
        self.typed = None
        self.typing_completed = False
    
    BINDINGS = [
        Binding("escape", "quit", "Quit")
    ]
    
    CSS_PATH = "main.tcss"
    
    def on_mount(self):
        self.sentence_label = self.query_one("#sentence-label")
        self.user_input = self.query_one("#user-input")
        self.wpm_label = self.query_one("#wpm-label")
        
        self.refresh_app()
    
    def compose(self):
        with Vertical(classes="main"):
            yield Label(id="sentence-label")
            with Vertical(id="container"):
                yield Input(id="user-input")
                yield Label(id="wpm-label")
                yield Static("[orange]esc[/orange] exit   [orange]enter[/orange] new sentence", id="footer")
        
    def get_duration(self):
        if self.start is None:
            return 0
        return (time() - self.start) / 60
    
    def check_input_length(self):
        if self.start is None:
            return 0
        return len(self.current_sentence) == len(self.typed)
    
    def get_words_per_minute(self):
        if self.start is None or not self.typed:
            return 0

        minutes = self.get_duration()
        if minutes == 0:
            return 0

        chars_typed = len(self.typed)
        words_typed = chars_typed / 5
        wpm = words_typed / minutes
        return wpm
        
    def refresh_app(self):
        self.current_sentence = random.choice(sentences)
        self.sentence_label.update(self.current_sentence)
        self.start = None
        self.typed = None
        self.typing_completed = False
        self.user_input.value = ""
        self.wpm_label.update(self.get_result())
        
    def refresh_sentence_label(self):
        label_sentence = ""
        for char_typed, char_curr in zip(self.typed, self.current_sentence):
            if char_typed == char_curr:
                label_sentence += f"[white on green]{char_typed}[/white on green]"
            else:
                label_sentence += f"[white on red]{char_typed}[/white on red]"
                
        label_sentence += self.current_sentence[len(self.typed):]
        return label_sentence
    
    def get_accuracy(self):
        if  self.start is None or not len(self.typed) or not (self.current_sentence):
            return 0
        count = 0
        for char_typed, char_curr in zip(self.typed, self.current_sentence):
                if char_typed == char_curr: 
                    count+=1
        return count / len(self.current_sentence)
    
    def get_result(self) -> str:
        return f"WPM: {self.get_words_per_minute():.2f} Accuracy: {self.get_accuracy():.2%} Time: {self.get_duration():.2f}"
        
 
    def on_input_changed(self, event: Input.Changed):
        if self.typing_completed:
            return
        if self.start is None and event.value:
            self.start = time()
        self.typed = self.user_input.value
        self.sentence_label.update(self.refresh_sentence_label())
        if self.check_input_length():
            self.wpm_label.update(self.get_result())
            self.typing_completed = True
            self.user_input.value = ""
        

    def on_key(self, event: events.Key):
        if event.key == "enter":
            self.refresh_app()
        
        
def main():
    app = SpeedTyping()
    app.run(inline=True)
    
if __name__ == "__main__":
    main()