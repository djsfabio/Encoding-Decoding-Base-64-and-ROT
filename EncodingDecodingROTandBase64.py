import string
import base64
import operator

ALPHABET = string.ascii_uppercase
SPECIAL_CHARS = " ,.-;:_?!='\""


def encrypt(plain_text, key):
    cipher_text = ""
    for letter in plain_text:
        if letter in SPECIAL_CHARS:
            cipher_text += letter
            continue
        index = ALPHABET.find(letter.upper())
        new_index = flatten(index + key)
        cipher_text += ALPHABET[new_index]
    return cipher_text


def decrypt(cipher_text, key=None):
    if key is None:
        key = find_key_from_cipher(cipher_text)

    plain_text = []
    for i in range(0, len(key)):
        plain_text.append("")

    for i in range(0, len(key)):
        for letter in cipher_text:
            if letter in SPECIAL_CHARS:
                plain_text[i] += letter
                continue
            index = ALPHABET.find(letter.upper())
            new_index = flatten(index - key[i])
            plain_text[i] += ALPHABET[new_index]

    return plain_text


def flatten(number):
    return number - (26*(number//26))


def que_des_majuscules(texte, taille_bloc=5):
    # remplace les caracteres accentues, supprime les espaces et la ponctuation
    # renvoie une chaine de lettres majuscules
    chaine = ""
    i = 0  # tient le compte des lettres du message transforme
    texte = texte.lower()
    for c in texte:
        if 97 <= ord(c) <= 122:
            chaine += chr(ord(c)-32)
        elif c in ("Ã¤", "Ã ", "Ã¢"):
            chaine += "A"
        elif c in ("Ã©", "Ã¨", "Ã«", "Ãª"):
            chaine += "E"
        elif c in ("Ã®", "Ã¯"):
            chaine += "I"
        elif c in ("Ã´", "Ã¶"):
            chaine += "O"
        elif c in ("Ã¼", "Ã»", "Ã¹"):
            chaine += "U"
        elif c == "Ã§":
            chaine += "C"
        else:   # on ne tient pas compte du caractere lu
            i -= 1
        i += 1
        if taille_bloc > 0 and i % taille_bloc == 0 and i > 0 and chaine[-1] != " ":
            chaine += " "  # ajoute une espace tous les "taille_bloc" caracteres
    return chaine


def ic(texte):
    chaine = que_des_majuscules(texte, 0)
    frequences = [0]*26
    n = len(chaine)
    for c in chaine:
        frequences[ord(c)-65] += 1
    indice = 0.0
    for ni in frequences:
        indice += ni*(ni-1)
    return indice/(n*(n-1))


def find_key_from_cipher(cipher_text):
    key = []
    # L'index de E, que ce soit pour l'anglais ou le français
    index_of_most_common_letter = 4

    # Calculate distribution
    distribution_dict = analyse_letter_distribution(cipher_text)
    distribution_dict = dict(
        sorted(distribution_dict.items(), key=operator.itemgetter(1), reverse=True))
    # Get common letters
    for letter, apparition in distribution_dict.items():
        if(apparition >= len(cipher_text)*(1/22)):
            key.append(ALPHABET.find(letter.upper()) -
                       index_of_most_common_letter)

    return key


def analyse_letter_distribution(cipher_text):
    distribution_dict = {}
    for letter in cipher_text:
        if letter in SPECIAL_CHARS:
            continue
        if letter not in distribution_dict:
            distribution_dict[letter] = 1
        else:
            distribution_dict[letter] += 1
    if len(distribution_dict.values()) != len(distribution_dict.values()):
        print("Multiple letters appear the same amount of times! Uh oh.")
    return distribution_dict


def isBase64(s):
    try:
        phrase_base64 = base64.b64decode(s)
        phrase = phrase_base64.decode('utf-8')
        return True
    except Exception:
        return False


if __name__ == "__main__":
    phrase = input(
        "Veuillez entrer votre phrase à chiffrer ou déchiffrer sans accents : \n")
    if(isBase64(phrase)):
        phrase_base64 = base64.b64decode(phrase)
        phrase = phrase_base64.decode('utf-8')
        print("\nVoici la phrase décodé de la base 64 : \n")
        print("\n" + phrase.upper() + "\n")
    icPhrase = ic(phrase)
    print("\nVoici l'IC pour cette phrase " + str(icPhrase) + "\n")
    choix = str(input(
        "Souhaitez-vous coder (y) ou décoder (f) votre texte ? Répondre par \"y\" ou \"f\" : \n"))

    if(choix == "y"):
        decalage = int(
            input("Veuillez entrer le décalage de césar entre 0 et 25 : \n"))
        if(decalage <= 25 and decalage >= 0):
            print(encrypt(phrase, decalage))
        else:
            print("Veuillez sélectionner une valeur correct comprise entre 0 et 25.")
    elif(choix == "f"):
        incrementation = 1
        print("Voici toutes les phrases viables : ")
        toutesLesPhrasesViables = decrypt(phrase)
        if(icPhrase <= 0.079 and icPhrase >= 0.071):
            print("La phrase suivante est décodée : \n")
            print(toutesLesPhrasesViables[0])
        else:
            for i in toutesLesPhrasesViables:
                print("\nLa phrase suivante est en " + str(incrementation) +
                      "e position sur " + str(len(toutesLesPhrasesViables)) + " : ")
                print(i)
                incrementation += 1
    else:
        print("Veuillez sélectionner une valeur correct, soit y ou f.")

