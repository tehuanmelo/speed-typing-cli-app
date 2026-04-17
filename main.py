from textual.app import App
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Label, Header, Footer, Input, ListView, Static
from textual.binding import Binding
from data.data import sentences
import random
from time import time

class SpeedTyping(App):
    def __init__(self):
        super().__init__()
        self.current_sentence = None
        self.printed_sentence = None
        self.accuracy = None
        self.start = None
        self.typed = None
    
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
        
    def get_duration(self):
        return (time() - self.start) / 60
    
    def check_input_length(self):
        return len(self.current_sentence) == len(self.typed)
    
    def get_words_per_minute(self):
        words_typed = sum([len(word) for word in self.typed]) / len(self.typed.split())
        return words_typed / self.get_duration()
        
    def refresh_app(self):
        self.current_sentence = random.choice(sentences)
        self.sentence_label.update(self.current_sentence)
        self.accuracy = None
        self.start = None
        self.typed = None
        self.user_input.value = ""
        
    def refresh_sentence_label(self):
        label_sentence = ""
        for i, char in enumerate(self.typed):
            if char == self.current_sentence[i]:
                label_sentence += f"[white on green]{self.typed[i]}[/white on green]"
            elif char != self.current_sentence[i]:
                label_sentence += f"[white on red]{self.typed[i]}[/white on red]"
                
        label_sentence += self.current_sentence[len(self.typed):]
        return label_sentence
    
    def get_accuracy(self):
        if not len(self.typed) or not (self.current_sentence):
            return 0
        count = 0
        for char_typed, char_curr in zip(self.typed, self.current_sentence):
                if char_typed == char_curr: 
                    count+=1
        return count / len(self.current_sentence)
        
 
    def on_input_changed(self, event: Input.Changed):
        if self.start is None and event.value:
            self.start = time()
        self.typed = self.user_input.value
        self.sentence_label.update(self.refresh_sentence_label())
        if self.check_input_length():
            self.wpm_label.update(f"WPM: {self.get_words_per_minute():.2f} Accuracy: {self.get_accuracy():.2%} Time: {self.get_duration():.2f}")
            self.refresh_app()
        
        
def main():
    app = SpeedTyping()
    app.run(inline=True)
    
if __name__ == "__main__":
    main()