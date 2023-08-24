from Chatbot import Chatbot


class Vera(Chatbot):
    def __init__(self):
        super().__init__(name="Vera")
        self.load_personality("Vera")
        self.introduce()


if __name__ == "__main__":
    chatbot = Vera()

    while True:
        user_input = input("User: ")

        response = chatbot.generate_response(user_input)

        print(f"{chatbot.name}: {response}")

