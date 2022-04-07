def encrypt(text, direction):
    result = ''
    key = 5
    if direction:
        for letter in text:
            result += chr(ord(letter)+key)
    else:
        for letter in text:
            result += chr(ord(letter)-key)

    return result






if __name__ == "__main__":
    source_text = input("Введите текст:")
    code_text = encrypt(source_text, True)
    back_text = encrypt(code_text, False)

    print("      Исходный текст:", source_text)
    print("В зашифрованном виде:", code_text)
    print("Расшифрованный текст:", back_text)

    g = input("")